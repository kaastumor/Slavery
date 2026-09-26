#!/usr/bin/env python3
"""Publish an exact Gate-4 canonical release package into audit metadata.

This tool never discovers release membership from mutable database state.  It consumes
an already-verified canonical release package rooted in the frozen D-109 authority
closure, re-verifies that the live governed objects still match that closure, then
registers exact typed membership and exact package-file checksums.

Publication is deliberately channel-neutral: claim publication_status values are not
changed and audit.release_channel is not moved.  Gate 5 owns public serving cutover.
"""
from __future__ import annotations

import argparse
import json
import os
from pathlib import Path
import sys
from typing import Any

import psycopg

from build_canonical_release import (
    expected_files,
    load_json,
    sha256_file,
    verify_package,
)
from full_state_release_bundle import (
    object_digests,
    sha256_value,
    snapshot_objects,
)


class PublicationError(ValueError):
    pass


MEMBERSHIP_TABLES = {
    "claim_ids": ("audit.release_claim", "claim_id", "claims"),
    "actor_ids": ("audit.release_actor", "actor_id", "actors"),
    "spatial_entity_ids": (
        "audit.release_spatial_entity",
        "spatial_entity_id",
        "spatial_entities",
    ),
    "geometry_ids": ("audit.release_geometry", "geometry_id", "geometries"),
    "voyage_ids": ("audit.release_voyage", "voyage_id", "voyages"),
    "coverage_assessment_ids": (
        "audit.release_coverage_assessment",
        "coverage_assessment_id",
        "coverage_assessments",
    ),
    "source_version_ids": (
        "audit.release_source_version",
        "source_version_id",
        "source_versions",
    ),
    "research_target_result_ids": (
        "audit.release_research_target_result",
        "research_target_result_id",
        "research_target_results",
    ),
}


def media_type(filename: str) -> str:
    if filename.endswith(".json"):
        return "application/json"
    if filename.endswith(".md"):
        return "text/markdown"
    return "text/plain"


def package_artifacts(
    release_dir: Path,
    *,
    source_git_sha: str,
    release_version: str,
) -> list[dict[str, Any]]:
    files = sorted(expected_files())
    actual = {path.name for path in release_dir.iterdir() if path.is_file()}
    if actual != set(files):
        raise PublicationError(
            f"release file set differs from package contract: {actual} != {set(files)}"
        )
    return [
        {
            "filename": filename,
            "sha256": sha256_file(release_dir / filename),
            "size_bytes": (release_dir / filename).stat().st_size,
            "media_type": media_type(filename),
            "storage_status": "repository",
            "storage_locator": (
                f"git:{source_git_sha}:data/releases/{release_version}/{filename}"
            ),
        }
        for filename in files
    ]


def load_publication_inputs(
    spec_path: Path,
    authority_path: Path,
    cartography_path: Path,
    release_dir: Path,
    *,
    source_git_sha: str,
) -> dict[str, Any]:
    verify_package(spec_path, authority_path, cartography_path, release_dir)
    spec = load_json(spec_path)
    authority = load_json(authority_path)
    manifest = load_json(release_dir / "manifest.json")

    if manifest.get("canonical") is not True:
        raise PublicationError("canonical release manifest must declare canonical=true")
    if manifest.get("release_version") != spec["release_version"]:
        raise PublicationError("release version differs between spec and manifest")
    if manifest.get("authority", {}).get("membership") != authority["membership"]:
        raise PublicationError("manifest membership differs from D-109 authority")
    if manifest.get("public_channel", {}).get("moved_by_release") is not False:
        raise PublicationError("Gate-4 publication must remain channel-neutral")

    return {
        "spec": spec,
        "authority": authority,
        "manifest": manifest,
        "artifacts": package_artifacts(
            release_dir,
            source_git_sha=source_git_sha,
            release_version=spec["release_version"],
        ),
        "changelog": (release_dir / "CHANGELOG.md").read_text(encoding="utf-8"),
        "qc_summary": (release_dir / "QC_SUMMARY.md").read_text(encoding="utf-8"),
        "unresolved_issues": (
            release_dir / "UNRESOLVED_ISSUES.md"
        ).read_text(encoding="utf-8"),
    }


def fetch_channel(cur, channel_code: str) -> tuple[str, str, str] | None:
    cur.execute(
        """
        select release_version, updated_by, note
        from audit.release_channel
        where channel_code=%s
        """,
        (channel_code,),
    )
    row = cur.fetchone()
    if not row:
        return None
    return (str(row[0]), str(row[1]), str(row[2]))


def fetch_claim_publication(cur, claim_ids: list[str]) -> dict[str, str]:
    cur.execute(
        """
        select claim_id::text, publication_status::text
        from atlas.claim
        where claim_id=any(%s::uuid[])
        order by claim_id
        """,
        (claim_ids,),
    )
    return {str(claim_id): str(status) for claim_id, status in cur.fetchall()}


def verify_live_authority(
    cur,
    data: dict[str, Any],
) -> dict[str, Any]:
    spec = data["spec"]
    authority = data["authority"]
    release_version = spec["release_version"]

    cur.execute(
        "select status from audit.release_manifest where release_version=%s",
        (release_version,),
    )
    row = cur.fetchone()
    if row:
        raise PublicationError(
            f"release {release_version} already exists with status={row[0]}"
        )

    cur.execute(
        """
        select migration_name
        from atlas_meta.schema_migration
        order by migration_name desc
        limit 1
        """
    )
    migration_row = cur.fetchone()
    if not migration_row:
        raise PublicationError("schema migration ledger is empty")
    migration_name = str(migration_row[0])
    if not migration_name.startswith(spec["schema_version"] + "_"):
        raise PublicationError(
            f"live schema head {migration_name} does not match "
            f"{spec['schema_version']}"
        )

    channel = fetch_channel(cur, "public_mvp_preview")
    expected_channel = spec["public_channel"]["current_release"]
    if channel is None or channel[0] != expected_channel:
        raise PublicationError(
            f"public_mvp_preview={channel!r}, expected {expected_channel!r}"
        )

    membership = authority["membership"]
    objects, cartography = snapshot_objects(cur, membership)
    current_digests = object_digests(objects)
    if current_digests != authority["object_digests"]:
        changed: list[str] = []
        for group, expected in authority["object_digests"].items():
            current = current_digests.get(group, {})
            for object_id in sorted(set(expected) | set(current)):
                if expected.get(object_id) != current.get(object_id):
                    changed.append(f"{group}:{object_id}")
        raise PublicationError(
            "live D-109 object state drifted: " + ", ".join(changed)
        )
    if sha256_value(cartography) != authority["cartography_sha256"]:
        raise PublicationError("live production cartography drifted from D-109 proof")

    claim_publication = fetch_claim_publication(cur, membership["claim_ids"])
    if set(claim_publication) != set(membership["claim_ids"]):
        raise PublicationError("authority claim membership missing from live database")

    return {
        "schema_head": migration_name,
        "public_channel": channel,
        "claim_publication": claim_publication,
    }


def insert_membership(cur, data: dict[str, Any]) -> None:
    release_version = data["spec"]["release_version"]
    authority = data["authority"]
    for member_key, (table, id_column, object_group) in MEMBERSHIP_TABLES.items():
        ids = authority["membership"][member_key]
        digests = authority["object_digests"][object_group]
        for object_id in ids:
            digest = digests[object_id]
            cur.execute(
                f"""
                insert into {table}(
                    release_version, {id_column}, object_sha256, capture_status
                ) values (%s,%s::uuid,%s,'captured_at_release')
                """,
                (release_version, object_id, digest),
            )


def insert_artifacts(cur, data: dict[str, Any]) -> None:
    release_version = data["spec"]["release_version"]
    for artifact in data["artifacts"]:
        cur.execute(
            """
            insert into audit.release_artifact(
                release_version, artifact_role, filename, sha256, size_bytes,
                media_type, storage_status, storage_locator, capture_status
            ) values (
                %s,'canonical_release_file',%s,%s,%s,%s,%s,%s,
                'captured_at_release'
            )
            """,
            (
                release_version,
                artifact["filename"],
                artifact["sha256"],
                artifact["size_bytes"],
                artifact["media_type"],
                artifact["storage_status"],
                artifact["storage_locator"],
            ),
        )


def publish(conn, data: dict[str, Any]) -> dict[str, Any]:
    spec = data["spec"]
    authority = data["authority"]
    release_version = spec["release_version"]

    with conn.cursor() as cur:
        before = verify_live_authority(cur, data)

        cur.execute(
            """
            insert into audit.release_manifest(
                release_version, schema_version, status, changelog,
                qc_summary, unresolved_issues, manifest
            ) values (%s,%s,'validated',%s,%s,%s,%s::jsonb)
            """,
            (
                release_version,
                spec["schema_version"],
                data["changelog"],
                data["qc_summary"],
                data["unresolved_issues"],
                json.dumps(data["manifest"], ensure_ascii=False, separators=(",", ":")),
            ),
        )
        insert_membership(cur, data)
        insert_artifacts(cur, data)

        cur.execute(
            """
            update audit.release_manifest
            set status='published'
            where release_version=%s and status='validated'
            """,
            (release_version,),
        )
        if cur.rowcount != 1:
            raise PublicationError("failed validated -> published transition")

        after_channel = fetch_channel(cur, "public_mvp_preview")
        if after_channel != before["public_channel"]:
            raise PublicationError("Gate-4 publication moved the public release channel")

        after_claim_publication = fetch_claim_publication(
            cur, authority["membership"]["claim_ids"]
        )
        if after_claim_publication != before["claim_publication"]:
            raise PublicationError("Gate-4 publication changed claim publication_status")

        verify_published(cur, data)

    conn.commit()
    return {
        "release_version": release_version,
        "status": "published",
        "schema_head": before["schema_head"],
        "membership_sha256": authority["membership_sha256"],
        "database_state_sha256": authority["database_state_sha256"],
        "artifact_count": len(data["artifacts"]),
        "public_channel": before["public_channel"][0],
        "public_channel_moved": False,
        "claim_publication_status_changed": False,
    }


def verify_published(cur, data: dict[str, Any]) -> None:
    release_version = data["spec"]["release_version"]
    authority = data["authority"]

    cur.execute(
        """
        select schema_version,status,manifest
        from audit.release_manifest
        where release_version=%s
        """,
        (release_version,),
    )
    row = cur.fetchone()
    if not row:
        raise PublicationError("published release manifest missing")
    if str(row[0]) != data["spec"]["schema_version"] or str(row[1]) != "published":
        raise PublicationError("published release manifest status/schema mismatch")
    if row[2] != data["manifest"]:
        raise PublicationError("database release manifest differs from exact package manifest")

    for member_key, (table, id_column, object_group) in MEMBERSHIP_TABLES.items():
        cur.execute(
            f"""
            select {id_column}::text, object_sha256, capture_status
            from {table}
            where release_version=%s
            order by {id_column}
            """,
            (release_version,),
        )
        rows = cur.fetchall()
        actual = {
            str(object_id): (str(digest), str(capture_status))
            for object_id, digest, capture_status in rows
        }
        expected = {
            object_id: (
                authority["object_digests"][object_group][object_id],
                "captured_at_release",
            )
            for object_id in authority["membership"][member_key]
        }
        if actual != expected:
            raise PublicationError(f"published {member_key} membership/digests differ")

    cur.execute(
        """
        select filename,sha256,size_bytes,media_type,storage_status,storage_locator,
               capture_status
        from audit.release_artifact
        where release_version=%s and artifact_role='canonical_release_file'
        order by filename
        """,
        (release_version,),
    )
    rows = cur.fetchall()
    actual_artifacts = {
        str(filename): {
            "sha256": str(digest),
            "size_bytes": int(size_bytes),
            "media_type": str(media),
            "storage_status": str(storage_status),
            "storage_locator": str(storage_locator),
            "capture_status": str(capture_status),
        }
        for (
            filename,
            digest,
            size_bytes,
            media,
            storage_status,
            storage_locator,
            capture_status,
        ) in rows
    }
    expected_artifacts = {
        artifact["filename"]: {
            "sha256": artifact["sha256"],
            "size_bytes": artifact["size_bytes"],
            "media_type": artifact["media_type"],
            "storage_status": artifact["storage_status"],
            "storage_locator": artifact["storage_locator"],
            "capture_status": "captured_at_release",
        }
        for artifact in data["artifacts"]
    }
    if actual_artifacts != expected_artifacts:
        raise PublicationError("published package artifact registry differs from package")


def assert_immutability_guards(
    conn,
    *,
    release_version: str,
    sample_claim_id: str,
) -> None:
    attempts = (
        (
            "artifact",
            """
            update audit.release_artifact
            set storage_locator=storage_locator
            where release_version=%s
            """,
            (release_version,),
        ),
        (
            "membership",
            """
            update audit.release_claim
            set object_sha256=object_sha256
            where release_version=%s and claim_id=%s::uuid
            """,
            (release_version, sample_claim_id),
        ),
    )
    for label, statement, params in attempts:
        blocked = False
        try:
            with conn.transaction():
                with conn.cursor() as cur:
                    cur.execute(statement, params)
        except psycopg.Error:
            blocked = True
        if not blocked:
            conn.rollback()
            raise PublicationError(
                f"published release {label} remained mutable"
            )


def verify_after_commit(conn, data: dict[str, Any]) -> dict[str, Any]:
    with conn.cursor() as cur:
        verify_published(cur, data)
        channel = fetch_channel(cur, "public_mvp_preview")
        if channel is None:
            raise PublicationError("public_mvp_preview channel disappeared")
        if channel[0] != data["spec"]["public_channel"]["current_release"]:
            raise PublicationError("public channel moved after Gate-4 commit")
    conn.rollback()

    sample_claim_id = data["authority"]["membership"]["claim_ids"][0]
    assert_immutability_guards(
        conn,
        release_version=data["spec"]["release_version"],
        sample_claim_id=sample_claim_id,
    )
    conn.rollback()
    return {
        "verification": "PUBLISHED_EXACT_PACKAGE_IMMUTABILITY_PASS",
        "public_channel_moved": False,
    }


def connect(dsn: str):
    return psycopg.connect(dsn, autocommit=False)


def main() -> int:
    parser = argparse.ArgumentParser()
    sub = parser.add_subparsers(dest="command", required=True)

    for name in ("plan", "publish", "verify"):
        cmd = sub.add_parser(name)
        cmd.add_argument("spec", type=Path)
        cmd.add_argument("authority_bundle", type=Path)
        cmd.add_argument("cartography_fingerprint", type=Path)
        cmd.add_argument("release_dir", type=Path)
        cmd.add_argument("--source-git-sha", required=True)
        if name != "plan":
            cmd.add_argument("--dsn", default=os.environ.get("DATABASE_URL"))

    args = parser.parse_args()
    try:
        data = load_publication_inputs(
            args.spec,
            args.authority_bundle,
            args.cartography_fingerprint,
            args.release_dir,
            source_git_sha=args.source_git_sha,
        )

        if args.command == "plan":
            print(
                json.dumps(
                    {
                        "release_version": data["spec"]["release_version"],
                        "membership_counts": {
                            key: len(values)
                            for key, values in data["authority"]["membership"].items()
                        },
                        "artifact_count": len(data["artifacts"]),
                        "public_channel_moved": False,
                        "claim_publication_status_changed": False,
                        "mode": "plan-no-write",
                    },
                    indent=2,
                )
            )
            return 0

        if not args.dsn:
            parser.error("--dsn or DATABASE_URL is required")

        with connect(args.dsn) as conn:
            if args.command == "publish":
                result = publish(conn, data)
                result.update(verify_after_commit(conn, data))
            else:
                with conn.cursor() as cur:
                    verify_published(cur, data)
                    channel = fetch_channel(cur, "public_mvp_preview")
                    if channel is None or channel[0] != data["spec"]["public_channel"]["current_release"]:
                        raise PublicationError("public channel differs from Gate-4 contract")
                conn.rollback()
                result = verify_after_commit(conn, data)
                result["release_version"] = data["spec"]["release_version"]

        print(json.dumps(result, indent=2, sort_keys=True))
        return 0
    except (OSError, json.JSONDecodeError, PublicationError, psycopg.Error) as exc:
        print(f"BLOCK: {exc}", file=sys.stderr)
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
