#!/usr/bin/env python3
"""Insert one reviewed external/network participation research case.

The input remains claim-centric and unpublished. This loader exists because the
canonical schema already models external/network participation separately from
territorial practice. Run without --apply to validate and print a plan.
"""
from __future__ import annotations

import argparse
import json
import os
from pathlib import Path
import sys
from typing import Any

try:
    from .add_research_case import (
        case_content_sha256,
        ensure_source_version,
        ensure_spatial_entity,
        existing_case_ingest,
    )
    from .validate_external_case import SpecError, load as load_spec
except ImportError:
    from add_research_case import (
        case_content_sha256,
        ensure_source_version,
        ensure_spatial_entity,
        existing_case_ingest,
    )
    from validate_external_case import SpecError, load as load_spec


def plan(spec: dict[str, Any]) -> dict[str, Any]:
    claim = spec["claim"]
    external = claim["external_participation"]
    return {
        "case_key": spec["case_key"],
        "content_sha256": case_content_sha256(spec),
        "spatial_entity": spec["spatial_entity"]["canonical_name"],
        "entity_type": spec["spatial_entity"]["entity_type_code"],
        "claim_kind": "external_participation",
        "claim_interval": [claim.get("from_year"), claim.get("to_year")],
        "participation_type": external["participation_type_code"],
        "review_status": claim.get("review_status", "draft"),
        "publication_status": "unpublished",
        "evidence_sources": len(spec["evidence"]),
        "geometry_accuracy": (spec.get("geometry") or {}).get("accuracy_status"),
        "practice_level": None,
    }


def insert_case(
    conn,
    spec: dict[str, Any],
    *,
    source_path: str | None = None,
    git_revision: str | None = None,
) -> tuple[str, bool]:
    case_key = spec.get("case_key")
    if not case_key:
        raise SpecError("case.case_key is required for database ingestion")

    content_hash = case_content_sha256(spec)

    with conn.cursor() as cur:
        existing = existing_case_ingest(cur, case_key)
        if existing:
            existing_hash, claim_id = existing
            if existing_hash == content_hash:
                return str(claim_id), False
            raise RuntimeError(
                f"research case {case_key!r} was already applied with different content; "
                "create a new case_key and use the normal review/supersession path"
            )

        spatial_id = ensure_spatial_entity(cur, spec["spatial_entity"])

        source_version_ids: list[tuple[str, dict[str, Any]]] = []
        for evidence in spec["evidence"]:
            sv_id = ensure_source_version(cur, evidence["source"], evidence["version"])
            source_version_ids.append((sv_id, evidence))

        claim = spec["claim"]
        cur.execute(
            """
            insert into atlas.claim(
                claim_kind_code, from_year, to_year, date_text_original,
                temporal_precision, temporal_certainty, spatial_precision,
                summary, confidence, review_status, publication_status, notes
            ) values (
                'external_participation',%s,%s,%s,%s,%s,%s,%s,%s,
                %s::atlas.review_status,'unpublished'::atlas.publication_status,%s
            )
            returning claim_id
            """,
            (
                claim.get("from_year"),
                claim.get("to_year"),
                claim.get("date_text_original"),
                claim.get("temporal_precision"),
                claim.get("temporal_certainty"),
                claim.get("spatial_precision"),
                claim["summary"],
                claim.get("confidence"),
                claim.get("review_status", "draft"),
                claim.get("notes"),
            ),
        )
        claim_id = str(cur.fetchone()[0])

        external = claim["external_participation"]
        cur.execute(
            """
            insert into atlas.external_participation_claim(
                claim_id, spatial_entity_id, participation_type_code, role_text, notes
            ) values (%s,%s,%s,%s,%s)
            """,
            (
                claim_id,
                spatial_id,
                external["participation_type_code"],
                external.get("role_text"),
                external.get("notes"),
            ),
        )

        for source_version_id, evidence in source_version_ids:
            cur.execute(
                """
                insert into atlas.claim_source(
                    claim_id, source_version_id, evidence_role, independence_group,
                    directness, direction, locator, notes
                ) values (%s,%s,%s,%s,%s,%s::atlas.evidence_direction,%s,%s)
                """,
                (
                    claim_id,
                    source_version_id,
                    evidence.get("evidence_role"),
                    evidence.get("independence_group"),
                    evidence.get("directness"),
                    evidence.get("direction", "supports"),
                    evidence.get("locator"),
                    evidence.get("notes"),
                ),
            )

        geometry = spec.get("geometry")
        if geometry is not None:
            geometry_source_version_id = None
            if geometry["accuracy_status"] != "unresolved":
                source = geometry.get("source")
                version = geometry.get("version")
                if not isinstance(source, dict) or not isinstance(version, dict):
                    raise SpecError(
                        "resolved external geometry requires case.geometry.source "
                        "and case.geometry.version objects"
                    )
                geometry_source_version_id = ensure_source_version(cur, source, version)

            raw_geojson = geometry.get("geojson")
            cur.execute(
                """
                insert into atlas.geometry(
                    spatial_entity_id, from_year, to_year, geometry_source_version_id,
                    geometry_source_native_id, resolution_method, accuracy_status,
                    geom, notes, review_status
                ) values (
                    %s,%s,%s,%s,%s,%s,%s::atlas.geometry_accuracy,
                    case when %s::jsonb is null then null
                         else st_setsrid(st_geomfromgeojson(%s::text),4326) end,
                    %s,%s::atlas.review_status
                )
                """,
                (
                    spatial_id,
                    geometry.get("from_year"),
                    geometry.get("to_year"),
                    geometry_source_version_id,
                    geometry.get("source_native_id"),
                    geometry["resolution_method"],
                    geometry["accuracy_status"],
                    json.dumps(raw_geojson) if raw_geojson is not None else None,
                    json.dumps(raw_geojson) if raw_geojson is not None else None,
                    geometry.get("notes"),
                    geometry.get("review_status", "draft"),
                ),
            )

        cur.execute(
            """
            insert into audit.research_case_ingest(
                case_key, content_sha256, claim_id, source_path, git_revision
            ) values (%s,%s,%s,%s,%s)
            """,
            (case_key, content_hash, claim_id, source_path, git_revision),
        )

    return claim_id, True


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("case_file", type=Path)
    parser.add_argument("--dsn", default=os.environ.get("DATABASE_URL"))
    parser.add_argument("--apply", action="store_true", help="commit the case to PostgreSQL")
    parser.add_argument(
        "--git-revision",
        default=os.environ.get("GITHUB_SHA"),
        help="optional repository revision recorded in the ingestion ledger",
    )
    args = parser.parse_args()

    try:
        spec = load_spec(args.case_file)
    except (OSError, json.JSONDecodeError, SpecError) as exc:
        raise SystemExit(f"invalid external participation case: {exc}") from exc

    print(json.dumps(plan(spec), indent=2, ensure_ascii=False))
    if not args.apply:
        print("DRY RUN: no database changes made")
        return 0
    if not args.dsn:
        parser.error("--dsn or DATABASE_URL is required with --apply")

    try:
        import psycopg
    except ImportError as exc:
        raise SystemExit("psycopg is required; install requirements.txt") from exc

    with psycopg.connect(args.dsn, autocommit=False) as conn:
        try:
            with conn.transaction():
                claim_id, inserted = insert_case(
                    conn,
                    spec,
                    source_path=str(args.case_file),
                    git_revision=args.git_revision,
                )
        except Exception:
            conn.rollback()
            raise

    if inserted:
        print(f"inserted unpublished external-participation claim {claim_id}")
    else:
        print(f"NO-OP: external participation case already applied unchanged as claim {claim_id}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
