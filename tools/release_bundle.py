#!/usr/bin/env python3
"""Build, verify and publish D-054 preservation-grade release bundles.

The bundle freezes exact membership plus the database object state that affects
the current public_mvp_preview API. Publication verifies that frozen state and
writes it to the typed release-membership tables. It never discovers membership
during apply and it never moves the D-053 public release channel.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import os
from pathlib import Path
import sys
from typing import Any

BUNDLE_SCHEMA = "historical-slavery-atlas-full-state-bundle-v1"
PURPOSE = "public_mvp_preview"


class BundleError(ValueError):
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
        raise BundleError("candidate must be a JSON object")
    for key in (
        "release_version",
        "schema_version",
        "claim_ids",
        "changelog",
        "qc_summary",
        "unresolved_issues",
    ):
        if key not in data:
            raise BundleError(f"candidate.{key} is required")
    if data.get("canonical", False):
        raise BundleError("bundle v1 is for non-canonical public preview releases")
    if data.get("purpose", PURPOSE) != PURPOSE:
        raise BundleError(f"candidate purpose must be {PURPOSE}")
    claim_ids = data["claim_ids"]
    if not isinstance(claim_ids, list) or not claim_ids:
        raise BundleError("candidate.claim_ids must be a non-empty array")
    claim_ids = [str(value) for value in claim_ids]
    if len(claim_ids) != len(set(claim_ids)):
        raise BundleError("candidate.claim_ids must be unique")
    data["claim_ids"] = sorted(claim_ids)
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
               t.spatial_entity_id::text,
               exists(
                   select 1 from atlas.geometry g
                   where g.spatial_entity_id=t.spatial_entity_id
                     and g.review_status='reviewed'
                     and (
                       g.valid_years is null
                       or c.valid_years is null
                       or g.valid_years && c.valid_years
                     )
               ) as has_geometry
        from atlas.claim c
        left join atlas.territorial_practice_claim t on t.claim_id=c.claim_id
        where c.claim_id = any(%s::uuid[])
        order by c.claim_id
        """,
        (claim_ids,),
    )
    rows = cur.fetchall()
    found = {str(row[0]) for row in rows}
    problems: list[str] = []
    missing = sorted(set(claim_ids) - found)
    if missing:
        problems.append("unknown claim ids: " + ", ".join(missing))

    for claim_id, kind, review, publication, has_source, spatial_id, has_geometry in rows:
        claim_id = str(claim_id)
        if kind != "territorial_practice":
            problems.append(
                f"{claim_id}: bundle v1 supports territorial_practice only; found {kind}"
            )
        if review != "reviewed":
            problems.append(f"{claim_id}: review_status={review}, expected reviewed")
        if publication not in ("unpublished", "published"):
            problems.append(
                f"{claim_id}: publication_status={publication} cannot be published"
            )
        if not has_source:
            problems.append(f"{claim_id}: no claim-source evidence")
        if spatial_id is None:
            problems.append(f"{claim_id}: missing territorial-practice spatial entity")
        if not has_geometry:
            problems.append(f"{claim_id}: no overlapping reviewed geometry")

    if problems:
        raise BundleError("; ".join(problems))

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
        "actor_ids": [],
        "spatial_entity_ids": spatial_ids,
        "geometry_ids": geometry_ids,
        "voyage_ids": [],
        "coverage_assessment_ids": [],
        "claim_source_ids": claim_source_ids,
        "source_version_ids": source_version_ids,
        "source_ids": source_ids,
    }


def _payload_map(cur, query: str, ids: list[str]) -> dict[str, Any]:
    if not ids:
        return {}
    cur.execute(query, (ids,))
    result = {str(object_id): payload for object_id, payload in cur.fetchall()}
    if set(result) != set(ids):
        missing = sorted(set(ids) - set(result))
        extra = sorted(set(result) - set(ids))
        raise BundleError(
            f"bundle object membership mismatch; missing={missing} extra={extra}"
        )
    return dict(sorted(result.items()))


def snapshot_objects(
    cur,
    membership: dict[str, list[str]],
) -> tuple[dict[str, dict[str, Any]], dict[str, Any]]:
    objects: dict[str, dict[str, Any]] = {}

    # publication_status is normalized to the state the row will have after
    # release publication, so the bundle remains verifiable after apply.
    objects["claims"] = _payload_map(
        cur,
        """
        select c.claim_id::text,
               jsonb_build_object(
                 'claim',
                   to_jsonb(c)
                   || jsonb_build_object('publication_status','published'),
                 'territorial_practice', to_jsonb(t)
               )
        from atlas.claim c
        join atlas.territorial_practice_claim t using (claim_id)
        where c.claim_id=any(%s::uuid[])
        order by c.claim_id
        """,
        membership["claim_ids"],
    )
    objects["claim_sources"] = _payload_map(
        cur,
        """
        select cs.claim_source_id::text, to_jsonb(cs)
        from atlas.claim_source cs
        where cs.claim_source_id=any(%s::uuid[])
        order by cs.claim_source_id
        """,
        membership["claim_source_ids"],
    )
    objects["spatial_entities"] = _payload_map(
        cur,
        """
        select se.spatial_entity_id::text,
               jsonb_build_object(
                 'spatial_entity', to_jsonb(se),
                 'polity',
                   case when p.spatial_entity_id is null then null else to_jsonb(p) end
               )
        from atlas.spatial_entity se
        left join atlas.polity p using (spatial_entity_id)
        where se.spatial_entity_id=any(%s::uuid[])
        order by se.spatial_entity_id
        """,
        membership["spatial_entity_ids"],
    )
    objects["geometries"] = _payload_map(
        cur,
        """
        select g.geometry_id::text,
               (to_jsonb(g) - 'geom')
               || jsonb_build_object(
                    'geom_srid', case when g.geom is null then null else st_srid(g.geom) end,
                    'geom_ewkb_hex',
                      case when g.geom is null then null
                           else encode(st_asewkb(g.geom),'hex') end
                  )
        from atlas.geometry g
        where g.geometry_id=any(%s::uuid[])
        order by g.geometry_id
        """,
        membership["geometry_ids"],
    )
    objects["render_geometries"] = _payload_map(
        cur,
        """
        select g.geometry_id::text,
               (to_jsonb(g) - 'geom')
               || jsonb_build_object(
                    'geom_srid', case when g.geom is null then null else st_srid(g.geom) end,
                    'geom_ewkb_hex',
                      case when g.geom is null then null
                           else encode(st_asewkb(g.geom),'hex') end
                  )
        from publish.map_geometry g
        where g.geometry_id=any(%s::uuid[])
        order by g.geometry_id
        """,
        membership["geometry_ids"],
    )
    objects["source_versions"] = _payload_map(
        cur,
        """
        select sv.source_version_id::text, to_jsonb(sv)
        from atlas.source_version sv
        where sv.source_version_id=any(%s::uuid[])
        order by sv.source_version_id
        """,
        membership["source_version_ids"],
    )
    objects["sources"] = _payload_map(
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
    row = cur.fetchone()
    if not row:
        raise BundleError("no active cartographic land fabric")
    cartography = {
        "fabric_id": str(row[0]),
        "content_sha256": str(row[1]),
    }
    return objects, cartography


def object_digests(objects: dict[str, dict[str, Any]]) -> dict[str, dict[str, str]]:
    return {
        group: {
            object_id: sha256_value(payload)
            for object_id, payload in sorted(group_objects.items())
        }
        for group, group_objects in sorted(objects.items())
    }


def build_bundle(
    conn,
    candidate: dict[str, Any],
    *,
    candidate_sha256: str,
    source_git_sha: str | None,
) -> dict[str, Any]:
    with conn.cursor() as cur:
        membership = discover_membership(cur, candidate["claim_ids"])
        objects, cartography = snapshot_objects(cur, membership)

    digests = object_digests(objects)
    state = {
        "membership": membership,
        "object_digests": digests,
        "cartography": cartography,
    }
    return {
        "bundle_schema": BUNDLE_SCHEMA,
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
        "membership": membership,
        "cartography": cartography,
        "objects": objects,
        "object_digests": digests,
        "database_state_sha256": sha256_value(state),
    }


def validate_bundle(bundle: dict[str, Any]) -> None:
    if bundle.get("bundle_schema") != BUNDLE_SCHEMA:
        raise BundleError("unsupported release bundle schema")
    release = bundle.get("release")
    membership = bundle.get("membership")
    objects = bundle.get("objects")
    digests = bundle.get("object_digests")
    cartography = bundle.get("cartography")
    if not isinstance(release, dict) or release.get("purpose") != PURPOSE:
        raise BundleError("bundle release metadata/purpose is invalid")
    if release.get("canonical") is not False:
        raise BundleError("bundle v1 must be non-canonical")
    if not isinstance(membership, dict) or not isinstance(objects, dict):
        raise BundleError("bundle membership/objects are required")
    if not isinstance(digests, dict):
        raise BundleError("bundle object_digests are required")

    group_membership = {
        "claims": "claim_ids",
        "claim_sources": "claim_source_ids",
        "spatial_entities": "spatial_entity_ids",
        "geometries": "geometry_ids",
        "render_geometries": "geometry_ids",
        "source_versions": "source_version_ids",
        "sources": "source_ids",
    }
    for group, member_key in group_membership.items():
        ids = membership.get(member_key)
        group_objects = objects.get(group)
        group_digests = digests.get(group)
        if not isinstance(ids, list) or ids != sorted(set(ids)):
            raise BundleError(f"membership.{member_key} must be sorted unique")
        if not isinstance(group_objects, dict) or set(group_objects) != set(ids):
            raise BundleError(f"objects.{group} keys must match membership.{member_key}")
        if not isinstance(group_digests, dict) or set(group_digests) != set(ids):
            raise BundleError(
                f"object_digests.{group} keys must match membership.{member_key}"
            )
        recalculated = {
            object_id: sha256_value(payload)
            for object_id, payload in sorted(group_objects.items())
        }
        if recalculated != group_digests:
            raise BundleError(f"object_digests.{group} does not match bundle objects")

    for key in ("actor_ids", "voyage_ids", "coverage_assessment_ids"):
        value = membership.get(key)
        if value != []:
            raise BundleError(f"bundle v1 requires empty membership.{key}")

    if not isinstance(cartography, dict):
        raise BundleError("bundle cartography metadata is required")
    if not cartography.get("fabric_id") or not cartography.get("content_sha256"):
        raise BundleError("bundle cartography fabric/checksum is required")

    state = {
        "membership": membership,
        "object_digests": digests,
        "cartography": cartography,
    }
    if bundle.get("database_state_sha256") != sha256_value(state):
        raise BundleError("bundle database_state_sha256 mismatch")


def verify_database_state(conn, bundle: dict[str, Any]) -> None:
    validate_bundle(bundle)
    membership = bundle["membership"]
    with conn.cursor() as cur:
        # claim_source is not a typed release table, so verify the complete set
        # for released claims; an added/removed evidence link must block apply.
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
            raise BundleError(
                "claim-source membership drift: "
                f"bundle={membership['claim_source_ids']} current={current_links}"
            )
        objects, cartography = snapshot_objects(cur, membership)

    if cartography != bundle["cartography"]:
        raise BundleError(
            f"cartography drift: bundle={bundle['cartography']} current={cartography}"
        )

    current_digests = object_digests(objects)
    if current_digests != bundle["object_digests"]:
        changed: list[str] = []
        for group, expected in bundle["object_digests"].items():
            current = current_digests.get(group, {})
            for object_id in sorted(set(expected) | set(current)):
                if expected.get(object_id) != current.get(object_id):
                    changed.append(f"{group}:{object_id}")
        raise BundleError("database object drift: " + ", ".join(changed))


def apply_bundle(
    conn,
    bundle: dict[str, Any],
    *,
    bundle_path: Path,
    storage_status: str,
    storage_locator: str | None,
) -> None:
    verify_database_state(conn, bundle)
    release = bundle["release"]
    membership = bundle["membership"]
    digests = bundle["object_digests"]
    bundle_sha256 = sha256_file(bundle_path)

    with conn.cursor() as cur:
        cur.execute(
            "select exists(select 1 from audit.release_manifest where release_version=%s)",
            (release["release_version"],),
        )
        if cur.fetchone()[0]:
            raise BundleError(f"release {release['release_version']} already exists")

        manifest = {
            "canonical": False,
            "purpose": PURPOSE,
            "claim_ids": membership["claim_ids"],
            "actor_ids": membership["actor_ids"],
            "spatial_entity_ids": membership["spatial_entity_ids"],
            "geometry_ids": membership["geometry_ids"],
            "voyage_ids": membership["voyage_ids"],
            "coverage_assessment_ids": membership["coverage_assessment_ids"],
            "source_version_ids": membership["source_version_ids"],
            "release_bundle": {
                "bundle_schema": BUNDLE_SCHEMA,
                "bundle_sha256": bundle_sha256,
                "database_state_sha256": bundle["database_state_sha256"],
                "candidate_sha256": bundle["candidate_sha256"],
                "source_git_sha": bundle.get("source_git_sha"),
                "cartography": bundle["cartography"],
            },
        }

        # Membership is inserted while the release is validated. Updating the
        # release to published then activates the D-054 immutability guards.
        cur.execute(
            """
            insert into audit.release_manifest(
                release_version, schema_version, status, changelog,
                qc_summary, unresolved_issues, manifest
            ) values (%s,%s,'validated',%s,%s,%s,%s::jsonb)
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

        for claim_id in membership["claim_ids"]:
            cur.execute(
                """
                insert into audit.release_claim(
                    release_version, claim_id, object_sha256, capture_status
                ) values (%s,%s::uuid,%s,'captured_at_release')
                """,
                (release["release_version"], claim_id, digests["claims"][claim_id]),
            )

        for spatial_id in membership["spatial_entity_ids"]:
            cur.execute(
                """
                insert into audit.release_spatial_entity(
                    release_version, spatial_entity_id, object_sha256, capture_status
                ) values (%s,%s::uuid,%s,'captured_at_release')
                """,
                (
                    release["release_version"],
                    spatial_id,
                    digests["spatial_entities"][spatial_id],
                ),
            )

        for geometry_id in membership["geometry_ids"]:
            cur.execute(
                """
                insert into audit.release_geometry(
                    release_version, geometry_id, object_sha256, capture_status
                ) values (%s,%s::uuid,%s,'captured_at_release')
                """,
                (
                    release["release_version"],
                    geometry_id,
                    digests["geometries"][geometry_id],
                ),
            )

        for source_version_id in membership["source_version_ids"]:
            cur.execute(
                """
                insert into audit.release_source_version(
                    release_version, source_version_id, object_sha256, capture_status
                ) values (%s,%s::uuid,%s,'captured_at_release')
                """,
                (
                    release["release_version"],
                    source_version_id,
                    digests["source_versions"][source_version_id],
                ),
            )

        cur.execute(
            """
            insert into audit.release_artifact(
                release_version, artifact_role, filename, sha256, size_bytes,
                media_type, storage_status, storage_locator, capture_status
            ) values (%s,'full_state_bundle',%s,%s,%s,'application/json',%s,%s,'captured_at_release')
            """,
            (
                release["release_version"],
                bundle_path.name,
                bundle_sha256,
                bundle_path.stat().st_size,
                storage_status,
                storage_locator,
            ),
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
            raise BundleError(
                f"claim publication rowcount={cur.rowcount}, "
                f"expected={len(membership['claim_ids'])}"
            )

        cur.execute(
            """
            update audit.release_manifest
            set status='published'
            where release_version=%s and status='validated'
            """,
            (release["release_version"],),
        )
        if cur.rowcount != 1:
            raise BundleError("failed to transition release validated -> published")


def connect(dsn: str):
    try:
        import psycopg
    except ImportError as exc:
        raise SystemExit("psycopg is required; run through the tooling container") from exc
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
    lint.add_argument("bundle", type=Path)

    verify = sub.add_parser("verify")
    verify.add_argument("bundle", type=Path)
    verify.add_argument("--dsn", default=os.environ.get("DATABASE_URL"))

    apply = sub.add_parser("apply")
    apply.add_argument("bundle", type=Path)
    apply.add_argument("--dsn", default=os.environ.get("DATABASE_URL"))
    apply.add_argument(
        "--storage-status",
        choices=("workflow_artifact", "object_store", "repository", "external"),
        required=True,
    )
    apply.add_argument("--storage-locator")

    args = parser.parse_args()

    try:
        if args.command == "build":
            if not args.dsn:
                parser.error("--dsn or DATABASE_URL is required for build")
            candidate = load_candidate(args.candidate)
            with connect(args.dsn) as conn:
                bundle = build_bundle(
                    conn,
                    candidate,
                    candidate_sha256=sha256_file(args.candidate),
                    source_git_sha=args.source_git_sha,
                )
                conn.rollback()
            args.output.parent.mkdir(parents=True, exist_ok=True)
            args.output.write_bytes(canonical_bytes(bundle))
            print(
                json.dumps(
                    {
                        "release_version": bundle["release"]["release_version"],
                        "bundle": str(args.output),
                        "bundle_sha256": sha256_file(args.output),
                        "database_state_sha256": bundle["database_state_sha256"],
                        "claim_count": len(bundle["membership"]["claim_ids"]),
                        "geometry_count": len(bundle["membership"]["geometry_ids"]),
                    },
                    indent=2,
                )
            )
            return 0

        bundle = json.loads(args.bundle.read_text(encoding="utf-8"))
        validate_bundle(bundle)
        if args.command == "lint":
            print(
                json.dumps(
                    {
                        "release_version": bundle["release"]["release_version"],
                        "bundle_schema": bundle["bundle_schema"],
                        "bundle_sha256": sha256_file(args.bundle),
                        "database_state_sha256": bundle["database_state_sha256"],
                        "mode": "lint-only",
                    },
                    indent=2,
                )
            )
            return 0

        if not args.dsn:
            parser.error("--dsn or DATABASE_URL is required")

        with connect(args.dsn) as conn:
            verify_database_state(conn, bundle)
            if args.command == "verify":
                conn.rollback()
                print(
                    json.dumps(
                        {
                            "release_version": bundle["release"]["release_version"],
                            "bundle_sha256": sha256_file(args.bundle),
                            "database_state_sha256": bundle["database_state_sha256"],
                            "mode": "verified-no-write",
                        },
                        indent=2,
                    )
                )
                return 0

            try:
                with conn.transaction():
                    apply_bundle(
                        conn,
                        bundle,
                        bundle_path=args.bundle,
                        storage_status=args.storage_status,
                        storage_locator=args.storage_locator,
                    )
            except Exception:
                conn.rollback()
                raise

        print(
            json.dumps(
                {
                    "release_version": bundle["release"]["release_version"],
                    "bundle_sha256": sha256_file(args.bundle),
                    "database_state_sha256": bundle["database_state_sha256"],
                    "mode": "published-exact-bundle",
                    "channel_moved": False,
                },
                indent=2,
            )
        )
        return 0
    except (OSError, json.JSONDecodeError, BundleError) as exc:
        print(f"BLOCK: {exc}", file=sys.stderr)
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
