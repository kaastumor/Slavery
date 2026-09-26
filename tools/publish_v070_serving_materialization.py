#!/usr/bin/env python3
"""Register the immutable v0.7.0 public serving materialization.

This publishes a non-canonical serving release record suitable for the existing
public_mvp_preview channel.  It copies only membership actually represented by the
materialized map/list payload and never moves the channel itself.
"""
from __future__ import annotations

import argparse
import json
import os
from pathlib import Path
import sys
from typing import Any

import psycopg

from build_v070_public_materialization import (
    MANIFEST_FILENAME,
    MATERIALIZATION_ID,
    PAYLOAD_FILENAME,
    load_json,
    sha256_file,
    verify_materialization,
)


class ServingPublicationError(ValueError):
    pass


def materialized_membership(
    authority: dict[str, Any],
    payload: dict[str, Any],
) -> dict[str, list[str]]:
    claim_ids = sorted(
        {
            str(claim["claim_id"])
            for place in payload["places"]
            for claim in place["claims"]
        }
    )
    spatial_ids = sorted(
        {str(place["spatial_entity_id"]) for place in payload["places"]}
    )
    source_version_ids = sorted(
        {
            str(source["source_version_id"])
            for place in payload["places"]
            for claim in place["claims"]
            for source in claim["sources"]
        }
    )

    if not set(claim_ids) <= set(authority["membership"]["claim_ids"]):
        raise ServingPublicationError("materialized claims exceed canonical membership")
    if not set(spatial_ids) <= set(authority["membership"]["spatial_entity_ids"]):
        raise ServingPublicationError(
            "materialized spatial entities exceed canonical membership"
        )
    if not set(source_version_ids) <= set(
        authority["membership"]["source_version_ids"]
    ):
        raise ServingPublicationError(
            "materialized source versions exceed canonical membership"
        )
    return {
        "claim_ids": claim_ids,
        "actor_ids": [],
        "spatial_entity_ids": spatial_ids,
        "geometry_ids": [],
        "voyage_ids": [],
        "coverage_assessment_ids": [],
        "source_version_ids": source_version_ids,
        "research_target_result_ids": [],
    }


def prepare(
    release_dir: Path,
    cartography_fingerprint: Path,
    materialization_dir: Path,
    *,
    source_git_sha: str,
) -> dict[str, Any]:
    verify_materialization(
        release_dir,
        cartography_fingerprint,
        materialization_dir,
    )
    source_manifest = load_json(release_dir / "manifest.json")
    authority = load_json(release_dir / "authority-state.json")
    materialization_manifest = load_json(
        materialization_dir / MANIFEST_FILENAME
    )
    payload = load_json(materialization_dir / PAYLOAD_FILENAME)
    membership = materialized_membership(authority, payload)

    manifest_sha = sha256_file(materialization_dir / MANIFEST_FILENAME)
    db_manifest = {
        "purpose": "public_mvp_preview",
        "canonical": False,
        "canonical_source_release": "v0.7.0",
        "source_membership_sha256": authority["membership_sha256"],
        "display_scope": payload["display_scope"],
        "claim_ids": membership["claim_ids"],
        "actor_ids": [],
        "spatial_entity_ids": membership["spatial_entity_ids"],
        "geometry_ids": [],
        "voyage_ids": [],
        "coverage_assessment_ids": [],
        "source_version_ids": membership["source_version_ids"],
        "research_target_result_ids": [],
        "serving_materialization": {
            "materialization_id": MATERIALIZATION_ID,
            "canonical_source_release": "v0.7.0",
            "canonical_source_release_manifest_sha256": materialization_manifest[
                "canonical_source_release_manifest_sha256"
            ],
            "payload_sha256": materialization_manifest["payload_sha256"],
            "payload_bytes": materialization_manifest["payload_bytes"],
            "materialization_manifest_sha256": manifest_sha,
            "reviewed_historical_geometry_count": 0,
        },
        "release_dimensions": payload["release_dimensions"],
    }
    artifacts = [
        {
            "filename": filename,
            "sha256": sha256_file(materialization_dir / filename),
            "size_bytes": (materialization_dir / filename).stat().st_size,
            "media_type": "application/json",
            "storage_status": "repository",
            "storage_locator": (
                f"git:{source_git_sha}:data/serving/{MATERIALIZATION_ID}/{filename}"
            ),
        }
        for filename in (PAYLOAD_FILENAME, MANIFEST_FILENAME)
    ]
    return {
        "source_manifest": source_manifest,
        "authority": authority,
        "materialization_manifest": materialization_manifest,
        "payload": payload,
        "membership": membership,
        "db_manifest": db_manifest,
        "artifacts": artifacts,
    }


MEMBERSHIP_TABLES = {
    "claim_ids": ("audit.release_claim", "claim_id", "claims"),
    "spatial_entity_ids": (
        "audit.release_spatial_entity",
        "spatial_entity_id",
        "spatial_entities",
    ),
    "source_version_ids": (
        "audit.release_source_version",
        "source_version_id",
        "source_versions",
    ),
}


def verify_source_release(cur, data: dict[str, Any]) -> None:
    cur.execute(
        """
        select status,manifest
        from audit.release_manifest
        where release_version='v0.7.0'
        """
    )
    row = cur.fetchone()
    if not row or str(row[0]) != "published":
        raise ServingPublicationError("canonical source release v0.7.0 is not published")
    if row[1] != data["source_manifest"]:
        raise ServingPublicationError(
            "live v0.7.0 manifest differs from committed canonical package"
        )

    for member_key, (table, id_column, object_group) in MEMBERSHIP_TABLES.items():
        expected_ids = data["membership"][member_key]
        if not expected_ids:
            continue
        cur.execute(
            f"""
            select {id_column}::text, object_sha256
            from {table}
            where release_version='v0.7.0'
              and {id_column}=any(%s::uuid[])
            order by {id_column}
            """,
            (expected_ids,),
        )
        actual = {str(object_id): str(digest) for object_id, digest in cur.fetchall()}
        expected = {
            object_id: data["authority"]["object_digests"][object_group][object_id]
            for object_id in expected_ids
        }
        if actual != expected:
            raise ServingPublicationError(
                f"canonical source release {member_key} digests differ"
            )


def current_channel(cur) -> str:
    cur.execute(
        """
        select release_version
        from audit.release_channel
        where channel_code='public_mvp_preview'
        """
    )
    row = cur.fetchone()
    if not row:
        raise ServingPublicationError("public_mvp_preview channel is missing")
    return str(row[0])


def insert_membership(cur, data: dict[str, Any]) -> None:
    authority = data["authority"]
    for member_key, (table, id_column, object_group) in MEMBERSHIP_TABLES.items():
        for object_id in data["membership"][member_key]:
            cur.execute(
                f"""
                insert into {table}(
                    release_version,{id_column},object_sha256,capture_status
                ) values (%s,%s::uuid,%s,'captured_at_release')
                """,
                (
                    MATERIALIZATION_ID,
                    object_id,
                    authority["object_digests"][object_group][object_id],
                ),
            )


def verify_published(cur, data: dict[str, Any]) -> None:
    cur.execute(
        """
        select status,manifest
        from audit.release_manifest
        where release_version=%s
        """,
        (MATERIALIZATION_ID,),
    )
    row = cur.fetchone()
    if not row or str(row[0]) != "published":
        raise ServingPublicationError("serving materialization is not published")
    if row[1] != data["db_manifest"]:
        raise ServingPublicationError("serving DB manifest differs from frozen plan")

    for member_key, (table, id_column, object_group) in MEMBERSHIP_TABLES.items():
        cur.execute(
            f"""
            select {id_column}::text,object_sha256,capture_status
            from {table}
            where release_version=%s
            order by {id_column}
            """,
            (MATERIALIZATION_ID,),
        )
        actual = {
            str(object_id): (str(digest), str(capture))
            for object_id, digest, capture in cur.fetchall()
        }
        expected = {
            object_id: (
                data["authority"]["object_digests"][object_group][object_id],
                "captured_at_release",
            )
            for object_id in data["membership"][member_key]
        }
        if actual != expected:
            raise ServingPublicationError(
                f"serving materialization {member_key} differs"
            )

    cur.execute(
        """
        select filename,sha256,size_bytes,storage_status,storage_locator,capture_status
        from audit.release_artifact
        where release_version=%s
          and artifact_role='public_serving_materialization'
        order by filename
        """,
        (MATERIALIZATION_ID,),
    )
    actual_artifacts = {
        str(filename): {
            "sha256": str(digest),
            "size_bytes": int(size_bytes),
            "storage_status": str(storage_status),
            "storage_locator": str(storage_locator),
            "capture_status": str(capture_status),
        }
        for filename, digest, size_bytes, storage_status, storage_locator, capture_status
        in cur.fetchall()
    }
    expected_artifacts = {
        artifact["filename"]: {
            "sha256": artifact["sha256"],
            "size_bytes": artifact["size_bytes"],
            "storage_status": artifact["storage_status"],
            "storage_locator": artifact["storage_locator"],
            "capture_status": "captured_at_release",
        }
        for artifact in data["artifacts"]
    }
    if actual_artifacts != expected_artifacts:
        raise ServingPublicationError("serving materialization artifacts differ")


def publish(conn, data: dict[str, Any]) -> dict[str, Any]:
    with conn.cursor() as cur:
        verify_source_release(cur, data)
        before_channel = current_channel(cur)
        if before_channel != "mvp-preview-ancient-v2":
            raise ServingPublicationError(
                f"unexpected pre-Gate5 channel target {before_channel}"
            )
        cur.execute(
            "select 1 from audit.release_manifest where release_version=%s",
            (MATERIALIZATION_ID,),
        )
        if cur.fetchone():
            raise ServingPublicationError(
                f"serving materialization {MATERIALIZATION_ID} already exists"
            )

        cur.execute(
            """
            insert into audit.release_manifest(
                release_version,schema_version,status,changelog,
                qc_summary,unresolved_issues,manifest
            ) values (%s,'0033','validated',%s,%s,%s,%s::jsonb)
            """,
            (
                MATERIALIZATION_ID,
                "Gate 5 serving materialization derived exactly from canonical v0.7.0.",
                (
                    "Deterministic release-derived payload; zero reviewed historical "
                    "geometries; channel not moved by publication."
                ),
                (
                    "Independent historical review remains 0. Non-territorial release "
                    "dimensions are summarized but not rendered as territorial claims."
                ),
                json.dumps(data["db_manifest"], ensure_ascii=False, separators=(",", ":")),
            ),
        )
        insert_membership(cur, data)
        for artifact in data["artifacts"]:
            cur.execute(
                """
                insert into audit.release_artifact(
                    release_version,artifact_role,filename,sha256,size_bytes,
                    media_type,storage_status,storage_locator,capture_status
                ) values (
                    %s,'public_serving_materialization',%s,%s,%s,%s,%s,%s,
                    'captured_at_release'
                )
                """,
                (
                    MATERIALIZATION_ID,
                    artifact["filename"],
                    artifact["sha256"],
                    artifact["size_bytes"],
                    artifact["media_type"],
                    artifact["storage_status"],
                    artifact["storage_locator"],
                ),
            )

        cur.execute(
            """
            update audit.release_manifest
            set status='published'
            where release_version=%s and status='validated'
            """,
            (MATERIALIZATION_ID,),
        )
        if cur.rowcount != 1:
            raise ServingPublicationError("failed validated -> published transition")
        verify_published(cur, data)
        if current_channel(cur) != before_channel:
            raise ServingPublicationError(
                "publishing serving materialization unexpectedly moved channel"
            )
    conn.commit()
    return {
        "materialization_id": MATERIALIZATION_ID,
        "status": "published",
        "channel_before": before_channel,
        "channel_moved": False,
        "claim_count": len(data["membership"]["claim_ids"]),
        "spatial_entity_count": len(data["membership"]["spatial_entity_ids"]),
        "source_version_count": len(data["membership"]["source_version_ids"]),
        "geometry_count": 0,
        "artifact_count": len(data["artifacts"]),
    }


def main() -> int:
    parser = argparse.ArgumentParser()
    sub = parser.add_subparsers(dest="command", required=True)
    for name in ("plan", "publish", "verify"):
        cmd = sub.add_parser(name)
        cmd.add_argument("release_dir", type=Path)
        cmd.add_argument("cartography_fingerprint", type=Path)
        cmd.add_argument("materialization_dir", type=Path)
        cmd.add_argument("--source-git-sha", required=True)
        if name != "plan":
            cmd.add_argument("--dsn", default=os.environ.get("DATABASE_URL"))

    args = parser.parse_args()
    try:
        data = prepare(
            args.release_dir,
            args.cartography_fingerprint,
            args.materialization_dir,
            source_git_sha=args.source_git_sha,
        )
        if args.command == "plan":
            print(
                json.dumps(
                    {
                        "materialization_id": MATERIALIZATION_ID,
                        "membership_counts": {
                            key: len(value)
                            for key, value in data["membership"].items()
                        },
                        "artifact_count": len(data["artifacts"]),
                        "channel_moved": False,
                        "mode": "plan-no-write",
                    },
                    indent=2,
                    sort_keys=True,
                )
            )
            return 0

        if not args.dsn:
            parser.error("--dsn or DATABASE_URL is required")
        with psycopg.connect(args.dsn, autocommit=False) as conn:
            if args.command == "publish":
                result = publish(conn, data)
            else:
                with conn.cursor() as cur:
                    verify_source_release(cur, data)
                    verify_published(cur, data)
                    result = {
                        "materialization_id": MATERIALIZATION_ID,
                        "verification": "PUBLISHED_SERVING_MATERIALIZATION_PASS",
                        "channel": current_channel(cur),
                    }
                conn.rollback()
        print(json.dumps(result, indent=2, sort_keys=True))
        return 0
    except (
        OSError,
        json.JSONDecodeError,
        ServingPublicationError,
        psycopg.Error,
    ) as exc:
        print(f"BLOCK: {exc}", file=sys.stderr)
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
