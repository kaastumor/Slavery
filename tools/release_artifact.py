#!/usr/bin/env python3
"""Build, verify and publish immutable public-preview release artifacts (D-054).

Build lane:
  release_artifact.py build candidate.json artifact.json --dsn ...

Promotion lane:
  release_artifact.py verify artifact.json --dsn ...
  release_artifact.py apply artifact.json --dsn ...

The apply path never discovers release membership. It verifies the exact frozen
IDs/digests and writes those membership arrays unchanged.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import os
from pathlib import Path
import sys
from typing import Any

ARTIFACT_SCHEMA = "historical-slavery-atlas-release-artifact-v1"
PURPOSE = "public_mvp_preview"


class ReleaseArtifactError(ValueError):
    pass


def canonical_bytes(value: Any) -> bytes:
    return (
        json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(",", ":"))
        + "\n"
    ).encode("utf-8")


def sha256_value(value: Any) -> str:
    return hashlib.sha256(canonical_bytes(value)).hexdigest()


def sha256_file(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def load_candidate(path: Path) -> dict[str, Any]:
    data = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(data, dict):
        raise ReleaseArtifactError("candidate must be a JSON object")
    for key in (
        "release_version",
        "schema_version",
        "claim_ids",
        "changelog",
        "qc_summary",
        "unresolved_issues",
    ):
        if key not in data:
            raise ReleaseArtifactError(f"candidate.{key} is required")
    if data.get("canonical", False):
        raise ReleaseArtifactError("D-054 artifact v1 is for non-canonical public previews only")
    if data.get("purpose", PURPOSE) != PURPOSE:
        raise ReleaseArtifactError(f"candidate purpose must be {PURPOSE}")
    ids = data["claim_ids"]
    if not isinstance(ids, list) or not ids:
        raise ReleaseArtifactError("candidate.claim_ids must be a non-empty array")
    if len(ids) != len(set(ids)):
        raise ReleaseArtifactError("candidate.claim_ids must be unique")
    data["claim_ids"] = sorted(str(item) for item in ids)
    data["canonical"] = False
    data["purpose"] = PURPOSE
    return data


def _fetch_ids(cur, query: str, params: tuple[Any, ...]) -> list[str]:
    cur.execute(query, params)
    return sorted(str(row[0]) for row in cur.fetchall())


def discover_membership(cur, claim_ids: list[str]) -> dict[str, list[str]]:
    cur.execute(
        """
        select c.claim_id::text, c.claim_kind_code, c.review_status::text,
               c.publication_status::text,
               exists(select 1 from atlas.claim_source cs where cs.claim_id=c.claim_id) as has_source,
               exists(
                   select 1 from atlas.territorial_practice_claim t
                   where t.claim_id=c.claim_id
               ) as has_practice,
               exists(
                   select 1
                   from atlas.territorial_practice_claim t
                   join atlas.geometry g on g.spatial_entity_id=t.spatial_entity_id
                   where t.claim_id=c.claim_id
                     and g.review_status='reviewed'
                     and (
                       g.valid_years is null
                       or c.valid_years is null
                       or g.valid_years && c.valid_years
                     )
               ) as has_geometry
        from atlas.claim c
        where c.claim_id = any(%s::uuid[])
        order by c.claim_id
        """,
        (claim_ids,),
    )
    rows = cur.fetchall()
    found = {str(row[0]) for row in rows}
    missing = sorted(set(claim_ids) - found)
    problems: list[str] = []
    if missing:
        problems.append("unknown claim ids: " + ", ".join(missing))
    for claim_id, kind, review, publication, has_source, has_practice, has_geometry in rows:
        claim_id = str(claim_id)
        if kind != "territorial_practice":
            problems.append(
                f"{claim_id}: artifact v1 supports territorial_practice only; found {kind}"
            )
        if review != "reviewed":
            problems.append(f"{claim_id}: review_status={review}, expected reviewed")
        if publication not in ("unpublished", "published"):
            problems.append(f"{claim_id}: publication_status={publication} cannot be published")
        if not has_source:
            problems.append(f"{claim_id}: no claim-source evidence")
        if not has_practice:
            problems.append(f"{claim_id}: missing territorial_practice subtype")
        if not has_geometry:
            problems.append(f"{claim_id}: no overlapping reviewed geometry")
    if problems:
        raise ReleaseArtifactError("; ".join(problems))

    spatial_ids = _fetch_ids(
        cur,
        """
        select distinct t.spatial_entity_id::text
        from atlas.territorial_practice_claim t
        where t.claim_id=any(%s::uuid[])
        """,
        (claim_ids,),
    )
    geometry_ids = _fetch_ids(
        cur,
        """
        select distinct g.geometry_id::text
        from atlas.geometry g
        where g.spatial_entity_id=any(%s::uuid[])
          and g.review_status='reviewed'
        """,
        (spatial_ids,),
    )
    claim_source_ids = _fetch_ids(
        cur,
        """
        select cs.claim_source_id::text
        from atlas.claim_source cs
        where cs.claim_id=any(%s::uuid[])
        """,
        (claim_ids,),
    )
    source_version_ids = _fetch_ids(
        cur,
        """
        select distinct cs.source_version_id::text
        from atlas.claim_source cs
        where cs.claim_id=any(%s::uuid[])
        """,
        (claim_ids,),
    )
    source_ids = _fetch_ids(
        cur,
        """
        select distinct sv.source_id::text
        from atlas.source_version sv
        where sv.source_version_id=any(%s::uuid[])
        """,
        (source_version_ids,),
    )
    return {
        "claim_ids": sorted(claim_ids),
        "spatial_entity_ids": spatial_ids,
        "geometry_ids": geometry_ids,
        "claim_source_ids": claim_source_ids,
        "source_version_ids": source_version_ids,
        "source_ids": source_ids,
    }


def _snapshot_map(cur, query: str, ids: list[str]) -> dict[str, str]:
    if not ids:
        return {}
    cur.execute(query, (ids,))
    rows = cur.fetchall()
    result = {str(object_id): sha256_value(payload) for object_id, payload in rows}
    if set(result) != set(ids):
        missing = sorted(set(ids) - set(result))
        extra = sorted(set(result) - set(ids))
        raise ReleaseArtifactError(
            f"snapshot membership mismatch; missing={missing} extra={extra}"
        )
    return dict(sorted(result.items()))


def snapshot_frozen_state(cur, membership: dict[str, list[str]]) -> tuple[dict[str, dict[str, str]], dict[str, Any]]:
    digests: dict[str, dict[str, str]] = {}

    digests["claims"] = _snapshot_map(
        cur,
        """
        select c.claim_id::text,
               jsonb_build_object(
                 'claim', to_jsonb(c) - 'publication_status',
                 'territorial_practice', to_jsonb(t)
               )
        from atlas.claim c
        join atlas.territorial_practice_claim t using (claim_id)
        where c.claim_id=any(%s::uuid[])
        order by c.claim_id
        """,
        membership["claim_ids"],
    )
    digests["claim_sources"] = _snapshot_map(
        cur,
        """
        select cs.claim_source_id::text, to_jsonb(cs)
        from atlas.claim_source cs
        where cs.claim_source_id=any(%s::uuid[])
        order by cs.claim_source_id
        """,
        membership["claim_source_ids"],
    )
    digests["spatial_entities"] = _snapshot_map(
        cur,
        """
        select se.spatial_entity_id::text,
               jsonb_build_object(
                 'spatial_entity', to_jsonb(se),
                 'polity', case when p.spatial_entity_id is null then null else to_jsonb(p) end
               )
        from atlas.spatial_entity se
        left join atlas.polity p using (spatial_entity_id)
        where se.spatial_entity_id=any(%s::uuid[])
        order by se.spatial_entity_id
        """,
        membership["spatial_entity_ids"],
    )
    digests["geometries"] = _snapshot_map(
        cur,
        """
        select g.geometry_id::text,
               (to_jsonb(g) - 'geom')
               || jsonb_build_object(
                    'geom_ewkb_hex',
                    case when g.geom is null then null else encode(st_asewkb(g.geom),'hex') end
                  )
        from atlas.geometry g
        where g.geometry_id=any(%s::uuid[])
        order by g.geometry_id
        """,
        membership["geometry_ids"],
    )
    digests["render_geometries"] = _snapshot_map(
        cur,
        """
        select g.geometry_id::text,
               (to_jsonb(g) - 'geom')
               || jsonb_build_object(
                    'geom_ewkb_hex',
                    case when g.geom is null then null else encode(st_asewkb(g.geom),'hex') end
                  )
        from publish.map_geometry g
        where g.geometry_id=any(%s::uuid[])
        order by g.geometry_id
        """,
        membership["geometry_ids"],
    )
    digests["source_versions"] = _snapshot_map(
        cur,
        """
        select sv.source_version_id::text, to_jsonb(sv)
        from atlas.source_version sv
        where sv.source_version_id=any(%s::uuid[])
        order by sv.source_version_id
        """,
        membership["source_version_ids"],
    )
    digests["sources"] = _snapshot_map(
        cur,
        """
        select s.source_id::text, to_jsonb(s)
        from atlas.source s
        where s.source_id=any(%s::uuid[])
        order by s.source_id
        """,
        membership["source_ids"],
    )

    cur.execute(
        """
        select fabric_id, content_sha256
        from cartography.land_fabric
        where active
        order by created_at desc
        limit 1
        """
    )
    fabric = cur.fetchone()
    if not fabric:
        raise ReleaseArtifactError("no active cartographic land fabric")
    cartography = {
        "fabric_id": str(fabric[0]),
        "content_sha256": str(fabric[1]),
    }
    return digests, cartography


def build_artifact(conn, candidate: dict[str, Any], *, candidate_sha256: str, source_git_sha: str | None) -> dict[str, Any]:
    with conn.cursor() as cur:
        membership = discover_membership(cur, candidate["claim_ids"])
        digests, cartography = snapshot_frozen_state(cur, membership)

    state = {
        "membership": membership,
        "digests": digests,
        "cartography": cartography,
    }
    return {
        "artifact_schema": ARTIFACT_SCHEMA,
        "release": {
            "release_version": candidate["release_version"],
            "schema_version": candidate["schema_version"],
            "purpose": PURPOSE,
            "canonical": False,
            "changelog": candidate["changelog"],
            "qc_summary": candidate["qc_summary"],
            "unresolved_issues": candidate["unresolved_issues"],
        },
        "candidate_sha256": candidate_sha256,
        "source_git_sha": source_git_sha,
        **state,
        "database_state_sha256": sha256_value(state),
    }


def validate_artifact(artifact: dict[str, Any]) -> None:
    if artifact.get("artifact_schema") != ARTIFACT_SCHEMA:
        raise ReleaseArtifactError("unsupported release artifact schema")
    release = artifact.get("release")
    membership = artifact.get("membership")
    digests = artifact.get("digests")
    cartography = artifact.get("cartography")
    if not isinstance(release, dict) or release.get("purpose") != PURPOSE:
        raise ReleaseArtifactError("artifact release metadata/purpose is invalid")
    if release.get("canonical") is not False:
        raise ReleaseArtifactError("artifact v1 must be non-canonical")
    if not isinstance(membership, dict) or not isinstance(digests, dict):
        raise ReleaseArtifactError("artifact membership/digests are required")
    expected_maps = {
        "claims": "claim_ids",
        "claim_sources": "claim_source_ids",
        "spatial_entities": "spatial_entity_ids",
        "geometries": "geometry_ids",
        "render_geometries": "geometry_ids",
        "source_versions": "source_version_ids",
        "sources": "source_ids",
    }
    for digest_key, member_key in expected_maps.items():
        ids = membership.get(member_key)
        mapping = digests.get(digest_key)
        if not isinstance(ids, list) or ids != sorted(set(ids)):
            raise ReleaseArtifactError(f"membership.{member_key} must be sorted unique")
        if not isinstance(mapping, dict) or set(mapping) != set(ids):
            raise ReleaseArtifactError(
                f"digests.{digest_key} keys must exactly match membership.{member_key}"
            )
        for value in mapping.values():
            if not isinstance(value, str) or len(value) != 64:
                raise ReleaseArtifactError(f"digests.{digest_key} contains invalid SHA-256")
    if not isinstance(cartography, dict) or not cartography.get("fabric_id") or not cartography.get("content_sha256"):
        raise ReleaseArtifactError("artifact cartography identity is required")

    state = {
        "membership": membership,
        "digests": digests,
        "cartography": cartography,
    }
    if artifact.get("database_state_sha256") != sha256_value(state):
        raise ReleaseArtifactError("artifact database_state_sha256 mismatch")


def verify_database_state(conn, artifact: dict[str, Any]) -> None:
    validate_artifact(artifact)
    membership = artifact["membership"]
    with conn.cursor() as cur:
        current_links = _fetch_ids(
            cur,
            """
            select cs.claim_source_id::text
            from atlas.claim_source cs
            where cs.claim_id=any(%s::uuid[])
            """,
            (membership["claim_ids"],),
        )
        if current_links != membership["claim_source_ids"]:
            raise ReleaseArtifactError(
                "claim-source membership drift: "
                f"artifact={membership['claim_source_ids']} current={current_links}"
            )
        current_digests, current_cartography = snapshot_frozen_state(cur, membership)

    if current_cartography != artifact["cartography"]:
        raise ReleaseArtifactError(
            f"cartography drift: artifact={artifact['cartography']} current={current_cartography}"
        )
    if current_digests != artifact["digests"]:
        changed: list[str] = []
        for group, expected in artifact["digests"].items():
            current = current_digests.get(group, {})
            for object_id in sorted(set(expected) | set(current)):
                if expected.get(object_id) != current.get(object_id):
                    changed.append(f"{group}:{object_id}")
        raise ReleaseArtifactError("database object drift: " + ", ".join(changed))


def apply_artifact(conn, artifact: dict[str, Any], artifact_sha256: str) -> None:
    verify_database_state(conn, artifact)
    release = artifact["release"]
    membership = artifact["membership"]

    with conn.cursor() as cur:
        cur.execute(
            "select exists(select 1 from audit.release_manifest where release_version=%s)",
            (release["release_version"],),
        )
        if cur.fetchone()[0]:
            raise ReleaseArtifactError(
                f"release {release['release_version']} already exists"
            )

        cur.execute(
            """
            update atlas.claim
            set publication_status='published'::atlas.publication_status
            where claim_id=any(%s::uuid[])
            """,
            (membership["claim_ids"],),
        )
        if cur.rowcount != len(membership["claim_ids"]):
            raise ReleaseArtifactError(
                f"claim publication rowcount={cur.rowcount}, expected={len(membership['claim_ids'])}"
            )

        manifest = {
            "canonical": False,
            "purpose": PURPOSE,
            "claim_ids": membership["claim_ids"],
            "spatial_entity_ids": membership["spatial_entity_ids"],
            "geometry_ids": membership["geometry_ids"],
            "source_version_ids": membership["source_version_ids"],
            "release_artifact": {
                "artifact_schema": ARTIFACT_SCHEMA,
                "artifact_sha256": artifact_sha256,
                "candidate_sha256": artifact["candidate_sha256"],
                "database_state_sha256": artifact["database_state_sha256"],
                "source_git_sha": artifact.get("source_git_sha"),
                "claim_source_ids": membership["claim_source_ids"],
                "source_ids": membership["source_ids"],
                "cartography": artifact["cartography"],
                "object_digests": artifact["digests"],
            },
        }
        cur.execute(
            """
            insert into audit.release_manifest(
                release_version, schema_version, status, changelog,
                qc_summary, unresolved_issues, manifest
            ) values (%s,%s,'published',%s,%s,%s,%s::jsonb)
            """,
            (
                release["release_version"],
                release["schema_version"],
                release["changelog"],
                release["qc_summary"],
                release["unresolved_issues"],
                json.dumps(manifest, separators=(",", ":")),
            ),
        )
        for source_version_id in membership["source_version_ids"]:
            cur.execute(
                """
                insert into audit.release_source_version(release_version,source_version_id)
                values (%s,%s::uuid)
                """,
                (release["release_version"], source_version_id),
            )


def connect(dsn: str):
    try:
        import psycopg
    except ImportError as exc:
        raise SystemExit("psycopg is required; install requirements.txt") from exc
    return psycopg.connect(dsn, autocommit=False)


def main() -> int:
    parser = argparse.ArgumentParser()
    sub = parser.add_subparsers(dest="command", required=True)

    build = sub.add_parser("build")
    build.add_argument("candidate", type=Path)
    build.add_argument("output", type=Path)
    build.add_argument("--dsn", default=os.environ.get("DATABASE_URL"))
    build.add_argument("--source-git-sha", default=os.environ.get("GITHUB_SHA"))

    lint = sub.add_parser("lint")
    lint.add_argument("artifact", type=Path)

    verify = sub.add_parser("verify")
    verify.add_argument("artifact", type=Path)
    verify.add_argument("--dsn", default=os.environ.get("DATABASE_URL"))

    apply = sub.add_parser("apply")
    apply.add_argument("artifact", type=Path)
    apply.add_argument("--dsn", default=os.environ.get("DATABASE_URL"))

    args = parser.parse_args()

    try:
        if args.command == "build":
            if not args.dsn:
                parser.error("--dsn or DATABASE_URL is required for build")
            candidate = load_candidate(args.candidate)
            with connect(args.dsn) as conn:
                artifact = build_artifact(
                    conn,
                    candidate,
                    candidate_sha256=sha256_file(args.candidate),
                    source_git_sha=args.source_git_sha,
                )
                conn.rollback()
            args.output.parent.mkdir(parents=True, exist_ok=True)
            args.output.write_bytes(canonical_bytes(artifact))
            print(json.dumps({
                "release_version": artifact["release"]["release_version"],
                "artifact": str(args.output),
                "database_state_sha256": artifact["database_state_sha256"],
                "claim_count": len(artifact["membership"]["claim_ids"]),
                "geometry_count": len(artifact["membership"]["geometry_ids"]),
            }, indent=2))
            return 0

        artifact = json.loads(args.artifact.read_text(encoding="utf-8"))
        validate_artifact(artifact)
        if args.command == "lint":
            print(json.dumps({
                "release_version": artifact["release"]["release_version"],
                "artifact_schema": artifact["artifact_schema"],
                "database_state_sha256": artifact["database_state_sha256"],
                "mode": "lint-only",
            }, indent=2))
            return 0

        if not args.dsn:
            parser.error("--dsn or DATABASE_URL is required")
        with connect(args.dsn) as conn:
            verify_database_state(conn, artifact)
            if args.command == "verify":
                conn.rollback()
                print(json.dumps({
                    "release_version": artifact["release"]["release_version"],
                    "database_state_sha256": artifact["database_state_sha256"],
                    "mode": "verified-no-write",
                }, indent=2))
                return 0
            with conn.transaction():
                apply_artifact(conn, artifact, sha256_file(args.artifact))
        print(json.dumps({
            "release_version": artifact["release"]["release_version"],
            "artifact_sha256": sha256_file(args.artifact),
            "database_state_sha256": artifact["database_state_sha256"],
            "mode": "published-artifact",
            "channel_moved": False,
        }, indent=2))
        return 0
    except (OSError, json.JSONDecodeError, ReleaseArtifactError) as exc:
        print(f"BLOCK: {exc}", file=sys.stderr)
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
