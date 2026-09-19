#!/usr/bin/env python3
"""Insert one reviewed research case into the canonical atlas schema.

The input is intentionally claim-centric. It never publishes a claim: publication
is a separate gate. Run without --apply to validate and print a plan.
"""
from __future__ import annotations

import argparse
import json
import os
from pathlib import Path
import sys
from typing import Any


PRACTICE_LEVELS = {None, "P0", "P1", "P2", "P3", "P4"}
REVIEW_STATUSES = {"draft", "reviewed"}
COVERAGE_STATES = {
    "not_researched",
    "source_identified",
    "reviewed",
    "classified",
    "disputed",
    "researched_inconclusive",
}
GEOMETRY_ACCURACY = {
    "exact",
    "specialist",
    "approximate_historical",
    "modern_proxy",
    "unresolved",
}
EVIDENCE_DIRECTIONS = {"supports", "challenges", "qualifies", "context"}


class SpecError(ValueError):
    pass


def _required(obj: dict[str, Any], key: str, where: str) -> Any:
    value = obj.get(key)
    if value is None or value == "":
        raise SpecError(f"{where}.{key} is required")
    return value


def _check_years(obj: dict[str, Any], where: str) -> None:
    start, end = obj.get("from_year"), obj.get("to_year")
    if start is not None and not isinstance(start, int):
        raise SpecError(f"{where}.from_year must be an integer or null")
    if end is not None and not isinstance(end, int):
        raise SpecError(f"{where}.to_year must be an integer or null")
    if start is not None and end is not None and start > end:
        raise SpecError(f"{where}.from_year must be <= to_year")


def validate_case_spec(spec: dict[str, Any]) -> None:
    spatial = _required(spec, "spatial_entity", "case")
    if not isinstance(spatial, dict):
        raise SpecError("case.spatial_entity must be an object")
    _required(spatial, "canonical_name", "case.spatial_entity")
    _required(spatial, "entity_type_code", "case.spatial_entity")
    _check_years(spatial, "case.spatial_entity")

    claim = _required(spec, "claim", "case")
    if not isinstance(claim, dict):
        raise SpecError("case.claim must be an object")
    _required(claim, "summary", "case.claim")
    _check_years(claim, "case.claim")
    review_status = claim.get("review_status", "draft")
    if review_status not in REVIEW_STATUSES:
        raise SpecError("case.claim.review_status must be draft or reviewed")
    if claim.get("publication_status") not in (None, "unpublished"):
        raise SpecError("research ingestion may only create unpublished claims")

    practice = _required(claim, "territorial_practice", "case.claim")
    if not isinstance(practice, dict):
        raise SpecError("case.claim.territorial_practice must be an object")
    _required(practice, "practice_type_code", "case.claim.territorial_practice")
    coverage = _required(practice, "coverage_state_code", "case.claim.territorial_practice")
    if coverage not in COVERAGE_STATES:
        raise SpecError(f"unsupported coverage state: {coverage}")
    if practice.get("practice_level") not in PRACTICE_LEVELS:
        raise SpecError("practice_level must be null or P0-P4")

    evidence = _required(spec, "evidence", "case")
    if not isinstance(evidence, list) or not evidence:
        raise SpecError("case.evidence must be a non-empty array")
    for index, item in enumerate(evidence):
        where = f"case.evidence[{index}]"
        if not isinstance(item, dict):
            raise SpecError(f"{where} must be an object")
        source = _required(item, "source", where)
        version = _required(item, "version", where)
        if not isinstance(source, dict) or not isinstance(version, dict):
            raise SpecError(f"{where}.source and .version must be objects")
        _required(source, "title", f"{where}.source")
        _required(version, "url_or_identifier", f"{where}.version")
        direction = item.get("direction", "supports")
        if direction not in EVIDENCE_DIRECTIONS:
            raise SpecError(f"unsupported evidence direction: {direction}")

    geometry = spec.get("geometry")
    if geometry is not None:
        if not isinstance(geometry, dict):
            raise SpecError("case.geometry must be an object or null")
        _check_years(geometry, "case.geometry")
        accuracy = _required(geometry, "accuracy_status", "case.geometry")
        if accuracy not in GEOMETRY_ACCURACY:
            raise SpecError(f"unsupported geometry accuracy: {accuracy}")
        _required(geometry, "resolution_method", "case.geometry")
        geojson = geometry.get("geojson")
        if accuracy == "unresolved" and geojson is not None:
            raise SpecError("unresolved geometry must have geojson=null")
        if accuracy != "unresolved":
            if not isinstance(geojson, dict):
                raise SpecError("resolved geometry requires a GeoJSON geometry object")
            source = _required(geometry, "source", "case.geometry")
            version = _required(geometry, "version", "case.geometry")
            if not isinstance(source, dict) or not isinstance(version, dict):
                raise SpecError("case.geometry.source and .version must be objects")
            _required(source, "title", "case.geometry.source")
            _required(version, "url_or_identifier", "case.geometry.version")


def load_spec(path: Path) -> dict[str, Any]:
    spec = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(spec, dict):
        raise SpecError("top-level JSON value must be an object")
    validate_case_spec(spec)
    return spec


def plan(spec: dict[str, Any]) -> dict[str, Any]:
    claim = spec["claim"]
    practice = claim["territorial_practice"]
    return {
        "spatial_entity": spec["spatial_entity"]["canonical_name"],
        "entity_type": spec["spatial_entity"]["entity_type_code"],
        "claim_interval": [claim.get("from_year"), claim.get("to_year")],
        "practice_type": practice["practice_type_code"],
        "practice_level": practice.get("practice_level"),
        "coverage_state": practice["coverage_state_code"],
        "review_status": claim.get("review_status", "draft"),
        "publication_status": "unpublished",
        "evidence_sources": len(spec["evidence"]),
        "geometry_accuracy": (spec.get("geometry") or {}).get("accuracy_status"),
    }


def _one_or_none(cur, query: str, params: tuple[Any, ...]):
    cur.execute(query, params)
    rows = cur.fetchall()
    if len(rows) > 1:
        raise RuntimeError("expected at most one matching row, found multiple")
    return rows[0] if rows else None


def ensure_source_version(cur, source: dict[str, Any], version: dict[str, Any]) -> str:
    url = version["url_or_identifier"]
    existing = _one_or_none(
        cur,
        """
        select sv.source_version_id
        from atlas.source_version sv
        where sv.url_or_identifier = %s
        """,
        (url,),
    )
    if existing:
        return str(existing[0])

    cur.execute(
        """
        insert into atlas.source(
            title, author_or_institution, source_type, source_classification,
            language_code, geographic_scope, temporal_scope,
            independence_notes, reliability_limitations, notes
        ) values (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)
        returning source_id
        """,
        (
            source["title"],
            source.get("author_or_institution"),
            source.get("source_type"),
            source.get("source_classification"),
            source.get("language_code"),
            source.get("geographic_scope"),
            source.get("temporal_scope"),
            source.get("independence_notes"),
            source.get("reliability_limitations"),
            source.get("notes"),
        ),
    )
    source_id = cur.fetchone()[0]
    cur.execute(
        """
        insert into atlas.source_version(
            source_id, version_label, publication_or_creation_date_text,
            publication_year, accessed_at, url_or_identifier,
            license_status, redistribution_status, notes
        ) values (%s,%s,%s,%s,coalesce(%s::timestamptz, now()),%s,%s,%s,%s)
        returning source_version_id
        """,
        (
            source_id,
            version.get("version_label"),
            version.get("publication_or_creation_date_text"),
            version.get("publication_year"),
            version.get("accessed_at"),
            url,
            version.get("license_status"),
            version.get("redistribution_status"),
            version.get("notes"),
        ),
    )
    return str(cur.fetchone()[0])


def ensure_spatial_entity(cur, spatial: dict[str, Any]) -> str:
    existing = _one_or_none(
        cur,
        """
        select spatial_entity_id, entity_type_code
        from atlas.spatial_entity
        where canonical_name = %s
        """,
        (spatial["canonical_name"],),
    )
    if existing:
        if existing[1] != spatial["entity_type_code"]:
            raise RuntimeError(
                f"existing spatial entity type is {existing[1]!r}, "
                f"spec requested {spatial['entity_type_code']!r}"
            )
        return str(existing[0])

    cur.execute(
        """
        insert into atlas.spatial_entity(
            entity_type_code, canonical_name, display_name, from_year, to_year,
            notes, review_status
        ) values (%s,%s,%s,%s,%s,%s,%s::atlas.review_status)
        returning spatial_entity_id
        """,
        (
            spatial["entity_type_code"],
            spatial["canonical_name"],
            spatial.get("display_name"),
            spatial.get("from_year"),
            spatial.get("to_year"),
            spatial.get("notes"),
            spatial.get("review_status", "draft"),
        ),
    )
    return str(cur.fetchone()[0])


def insert_case(conn, spec: dict[str, Any]) -> str:
    with conn.cursor() as cur:
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
                'territorial_practice',%s,%s,%s,%s,%s,%s,%s,%s,
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

        practice = claim["territorial_practice"]
        cur.execute(
            """
            insert into atlas.territorial_practice_claim(
                claim_id, spatial_entity_id, practice_type_code, practice_level,
                coverage_state_code, classification_status, notes
            ) values (%s,%s,%s,%s::atlas.practice_level,%s,%s,%s)
            """,
            (
                claim_id,
                spatial_id,
                practice["practice_type_code"],
                practice.get("practice_level"),
                practice["coverage_state_code"],
                practice.get("classification_status"),
                practice.get("notes"),
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
                geometry_source_version_id = ensure_source_version(
                    cur, geometry["source"], geometry["version"]
                )
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
                    json.dumps(geometry.get("geojson")) if geometry.get("geojson") is not None else None,
                    json.dumps(geometry.get("geojson")) if geometry.get("geojson") is not None else None,
                    geometry.get("notes"),
                    geometry.get("review_status", "draft"),
                ),
            )

    return claim_id


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("case_file", type=Path)
    parser.add_argument("--dsn", default=os.environ.get("DATABASE_URL"))
    parser.add_argument("--apply", action="store_true", help="commit the case to PostgreSQL")
    args = parser.parse_args()

    try:
        spec = load_spec(args.case_file)
    except (OSError, json.JSONDecodeError, SpecError) as exc:
        raise SystemExit(f"invalid research case: {exc}") from exc

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
                claim_id = insert_case(conn, spec)
        except Exception:
            conn.rollback()
            raise
    print(f"inserted unpublished claim {claim_id}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
