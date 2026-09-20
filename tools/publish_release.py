#!/usr/bin/env python3
"""Promote one pre-built, reviewed non-canonical release artifact.

The artifact is the release membership contract. Promotion verifies the exact
membership against current reviewed rows, but never discovers or expands
membership at apply time. Dry-run is the default.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import os
from pathlib import Path
import sys
from typing import Any


class PublishError(ValueError):
    pass


def canonical_json(data: Any) -> str:
    return json.dumps(data, ensure_ascii=False, sort_keys=True, separators=(",", ":"))


def artifact_sha256(data: dict[str, Any]) -> str:
    material = {k: v for k, v in data.items() if k != "artifact_sha256"}
    return hashlib.sha256(canonical_json(material).encode("utf-8")).hexdigest()


def load_manifest(path: Path) -> dict[str, Any]:
    data = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(data, dict):
        raise PublishError("top-level manifest must be an object")
    required = (
        "release_version", "schema_version", "claim_ids", "spatial_entity_ids",
        "geometry_ids", "source_version_ids", "changelog", "qc_summary",
        "unresolved_issues", "artifact_sha256",
    )
    for key in required:
        if key not in data:
            raise PublishError(f"{key} is required")
    for key in ("claim_ids", "spatial_entity_ids", "geometry_ids", "source_version_ids"):
        if not isinstance(data[key], list):
            raise PublishError(f"{key} must be an array")
        if key == "claim_ids" and not data[key]:
            raise PublishError("claim_ids must be a non-empty array")
        if data[key] != sorted(data[key]) or len(data[key]) != len(set(data[key])):
            raise PublishError(f"{key} must be sorted and unique")
    if data.get("canonical", False):
        raise PublishError("this tool is for non-canonical preview/public releases only")
    expected = artifact_sha256(data)
    if data["artifact_sha256"] != expected:
        raise PublishError(
            f"artifact_sha256 mismatch: expected {expected}, got {data['artifact_sha256']}"
        )
    return data


def inspect_release(cur, manifest: dict[str, Any]) -> dict[str, Any]:
    claim_ids = manifest["claim_ids"]
    cur.execute(
        """
        select c.claim_id::text, c.review_status::text, c.publication_status::text,
               c.claim_kind_code,
               exists(select 1 from atlas.claim_source cs where cs.claim_id=c.claim_id) as has_source,
               case when t.claim_id is null then true else exists(
                   select 1 from atlas.geometry g
                   where g.spatial_entity_id=t.spatial_entity_id
                     and g.review_status='reviewed'
                     and (g.valid_years is null or c.valid_years is null or g.valid_years && c.valid_years)
               ) end as has_geometry_resolution
        from atlas.claim c
        left join atlas.territorial_practice_claim t on t.claim_id=c.claim_id
        where c.claim_id = any(%s::uuid[])
        order by c.claim_id
        """,
        (claim_ids,),
    )
    rows = cur.fetchall()
    found = {row[0] for row in rows}
    problems: list[str] = []
    missing = sorted(set(claim_ids) - found)
    if missing:
        problems.append("unknown claim ids: " + ", ".join(missing))
    for claim_id, review, publication, kind, has_source, has_geometry in rows:
        if review != "reviewed":
            problems.append(f"{claim_id}: review_status={review}, expected reviewed")
        if publication not in ("unpublished", "published"):
            problems.append(f"{claim_id}: publication_status={publication} cannot be published")
        if not has_source:
            problems.append(f"{claim_id}: no CLAIM_SOURCE evidence")
        if kind == "territorial_practice" and not has_geometry:
            problems.append(f"{claim_id}: no overlapping reviewed geometry or unresolved geometry record")

    cur.execute(
        """select array_agg(distinct t.spatial_entity_id::text order by t.spatial_entity_id::text)
             from atlas.territorial_practice_claim t where t.claim_id=any(%s::uuid[])""",
        (claim_ids,),
    )
    actual_spatial = cur.fetchone()[0] or []
    cur.execute(
        """select array_agg(distinct g.geometry_id::text order by g.geometry_id::text)
             from atlas.geometry g where g.geometry_id=any(%s::uuid[]) and g.review_status='reviewed'""",
        (manifest["geometry_ids"],),
    )
    actual_geometry = cur.fetchone()[0] or []
    cur.execute(
        """select array_agg(distinct cs.source_version_id::text order by cs.source_version_id::text)
             from atlas.claim_source cs where cs.claim_id=any(%s::uuid[])""",
        (claim_ids,),
    )
    actual_sources = cur.fetchone()[0] or []

    if actual_spatial != manifest["spatial_entity_ids"]:
        problems.append("spatial_entity_ids differ from tested artifact membership")
    if actual_geometry != manifest["geometry_ids"]:
        problems.append("geometry_ids contain missing or unreviewed artifact members")
    if actual_sources != manifest["source_version_ids"]:
        problems.append("source_version_ids differ from tested artifact membership")
    return {"rows": rows, "problems": problems}


def publish(conn, manifest: dict[str, Any]) -> dict[str, Any]:
    with conn.cursor() as cur:
        check = inspect_release(cur, manifest)
        if check["problems"]:
            raise PublishError("; ".join(check["problems"]))
        cur.execute("select exists(select 1 from audit.release_manifest where release_version=%s)", (manifest["release_version"],))
        if cur.fetchone()[0]:
            raise PublishError(f"release {manifest['release_version']} already exists")

        release_payload = {
            "canonical": False,
            "purpose": manifest.get("purpose", "public_mvp_preview"),
            "artifact_sha256": manifest["artifact_sha256"],
            "claim_ids": manifest["claim_ids"],
            "spatial_entity_ids": manifest["spatial_entity_ids"],
            "geometry_ids": manifest["geometry_ids"],
            "source_version_ids": manifest["source_version_ids"],
        }
        cur.execute("update atlas.claim set publication_status='published'::atlas.publication_status where claim_id=any(%s::uuid[])", (manifest["claim_ids"],))
        cur.execute(
            """insert into audit.release_manifest(
                   release_version, schema_version, status, changelog, qc_summary,
                   unresolved_issues, manifest
               ) values (%s,%s,'published',%s,%s,%s,%s::jsonb)""",
            (manifest["release_version"], manifest["schema_version"], manifest["changelog"],
             manifest["qc_summary"], manifest["unresolved_issues"], json.dumps(release_payload)),
        )
        for source_version_id in manifest["source_version_ids"]:
            cur.execute(
                "insert into audit.release_source_version(release_version,source_version_id) values (%s,%s)",
                (manifest["release_version"], source_version_id),
            )
    return release_payload


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("manifest_file", type=Path)
    parser.add_argument("--dsn", default=os.environ.get("DATABASE_URL"))
    parser.add_argument("--apply", action="store_true")
    args = parser.parse_args()
    try:
        manifest = load_manifest(args.manifest_file)
    except (OSError, json.JSONDecodeError, PublishError) as exc:
        raise SystemExit(f"invalid publication artifact: {exc}") from exc
    if not args.dsn:
        if args.apply:
            parser.error("--dsn or DATABASE_URL is required with --apply")
        print(json.dumps({"release_version": manifest["release_version"], "claim_count": len(manifest["claim_ids"]), "artifact_sha256": manifest["artifact_sha256"], "canonical": False, "mode": "artifact-integrity dry run; supply DATABASE_URL for database gate checks"}, indent=2))
        return 0
    try:
        import psycopg
    except ImportError as exc:
        raise SystemExit("psycopg is required; install requirements.txt") from exc
    with psycopg.connect(args.dsn, autocommit=False) as conn:
        with conn.cursor() as cur:
            check = inspect_release(cur, manifest)
        if check["problems"]:
            for problem in check["problems"]:
                print(f"BLOCK: {problem}", file=sys.stderr)
            return 2
        print(f"READY: exact artifact {manifest['artifact_sha256']} passes the publication gate")
        if not args.apply:
            conn.rollback()
            print("DRY RUN: no database changes made")
            return 0
        try:
            with conn.transaction():
                payload = publish(conn, manifest)
        except Exception:
            conn.rollback()
            raise
    print(json.dumps(payload, indent=2))
    return 0


if __name__ == "__main__":
    sys.exit(main())
