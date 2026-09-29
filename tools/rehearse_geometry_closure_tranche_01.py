#!/usr/bin/env python3
"""Rehearse #370 geometry closure tranche 1 in disposable PostGIS only.

This tool has no production commit path. --apply is accepted only with
--disposable-test-db, CI=true, and the local Compose database. The complete
transaction is rolled back after exact delta and idempotency checks.
"""
from __future__ import annotations

import argparse
import json
import os
from pathlib import Path
import sys
from typing import Any
from urllib.parse import urlparse

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from tools.add_research_case import ensure_source_version, ensure_spatial_entity

REVIEW = ROOT / "data/research/geometry_reviews/population_100_100_closure_tranche_01.json"

EXPECTED = {
    "production-batch-2026-09-29/goryeo/nobi-status-review-0956-v1": {
        "claim_kind": "legal_event",
        "canonical_name": "Goryeo",
    },
    "production-batch-2026-09-29/dahomey/royal-captive-allocation-sale-1727-v1": {
        "claim_kind": "territorial_practice",
        "canonical_name": "Dahomey",
    },
    "production-batch-2026-09-29/taghaza/slave-salt-mining-1352-v1": {
        "claim_kind": "territorial_practice",
        "canonical_name": "Taghaza",
    },
}

TRACKED = (
    "atlas.spatial_entity",
    "atlas.source",
    "atlas.source_version",
    "atlas.geometry",
    "atlas.claim_source",
    "atlas.claim_evidence_locus",
    "atlas.claim",
    "audit.release_claim",
    "audit.release_channel",
)

STRICT_DELTA = {
    "atlas.spatial_entity": 1,
    "atlas.source": 4,
    "atlas.source_version": 4,
    "atlas.geometry": 3,
    "atlas.claim_source": 1,
    "atlas.claim_evidence_locus": 1,
    "atlas.claim": 0,
    "audit.release_claim": 0,
    "audit.release_channel": 0,
}


class ClosureError(RuntimeError):
    pass


def load_review(path: Path = REVIEW) -> dict[str, Any]:
    review = json.loads(path.read_text(encoding="utf-8"))
    if review.get("schema") != "historical-slavery-atlas-100-100-geometry-closure-review-v1":
        raise ClosureError("unexpected review schema")
    if review.get("status") != "INTERNAL_REVIEW_COMPLETE_READY_FOR_DISPOSABLE_REHEARSAL":
        raise ClosureError("review is not at disposable-rehearsal gate")
    rows = review.get("candidates") or []
    if len(rows) != 3:
        raise ClosureError("expected exactly three closure candidates")
    keys = {row.get("case_key") for row in rows}
    if keys != set(EXPECTED):
        raise ClosureError("closure candidate membership drift")
    if review.get("qc", {}).get("historical_practice_polygons_added") != 0:
        raise ClosureError("review unexpectedly permits a practice polygon")
    return review


def require_disposable_dsn(dsn: str) -> None:
    parsed = urlparse(dsn)
    if parsed.scheme not in ("postgres", "postgresql"):
        raise ClosureError("unexpected DSN scheme")
    if parsed.hostname != "db" or parsed.username != "atlas" or parsed.path != "/slavery_atlas":
        raise ClosureError("rehearsal only permits the local Compose database")
    if parsed.query or parsed.fragment:
        raise ClosureError("DSN overrides are forbidden")


def counts(conn) -> dict[str, int]:
    with conn.cursor() as cur:
        return {
            table: cur.execute(f"select count(*) from {table}").fetchone()[0]
            for table in TRACKED
        }


def source_parts(block: dict[str, Any]) -> tuple[dict[str, Any], dict[str, Any]]:
    source = {
        "title": block["title"],
        "author_or_institution": block.get("author_or_institution"),
        "source_type": block.get("source_type"),
        "source_classification": block.get("source_classification"),
        "language_code": block.get("language_code"),
        "geographic_scope": block.get("geographic_scope"),
        "temporal_scope": block.get("temporal_scope"),
        "independence_notes": block.get("independence_notes"),
        "reliability_limitations": block.get("reliability_limitations"),
        "notes": block.get("notes"),
    }
    version = {
        "version_label": block.get("version_label"),
        "publication_or_creation_date_text": block.get("publication_or_creation_date_text"),
        "publication_year": block.get("publication_year"),
        "accessed_at": block.get("accessed_at"),
        "url_or_identifier": block["url_or_identifier"],
        "license_status": block.get("license_status"),
        "redistribution_status": block.get("redistribution_status"),
        "notes": block.get("version_notes"),
    }
    return source, version


def verify_claims(conn) -> dict[str, dict[str, str]]:
    """Resolve disposable IDs from immutable case keys and verify semantic identity.

    Production UUIDs are intentionally not replay-stable. The case key plus claim kind,
    canonical spatial identity and reviewed/unpublished state are the durable contract.
    """
    resolved: dict[str, dict[str, str]] = {}
    with conn.cursor() as cur:
        for case_key, expected in EXPECTED.items():
            row = cur.execute(
                """select r.claim_id::text,
                          c.claim_kind_code,
                          c.review_status::text,
                          c.publication_status::text,
                          coalesce(t.spatial_entity_id, le.jurisdiction_spatial_entity_id)::text,
                          se.canonical_name
                     from audit.research_case_ingest r
                     join atlas.claim c using(claim_id)
                     left join atlas.territorial_practice_claim t using(claim_id)
                     left join atlas.legal_event le using(claim_id)
                     join atlas.spatial_entity se
                       on se.spatial_entity_id =
                          coalesce(t.spatial_entity_id, le.jurisdiction_spatial_entity_id)
                    where r.case_key=%s""",
                (case_key,),
            ).fetchone()
            if row is None:
                raise ClosureError(f"missing prerequisite case {case_key}")
            claim_id, claim_kind, review_status, publication_status, spatial_id, canonical_name = row
            if claim_kind != expected["claim_kind"]:
                raise ClosureError(f"claim-kind drift for {case_key}")
            if canonical_name != expected["canonical_name"]:
                raise ClosureError(f"spatial identity drift for {case_key}")
            if (review_status, publication_status) != ("reviewed", "unpublished"):
                raise ClosureError(f"prerequisite claim state drift for {case_key}")
            resolved[case_key] = {
                "claim_id": claim_id,
                "spatial_entity_id": spatial_id,
            }
    return resolved


def ensure_geometry(cur, spatial_id: str, geom: dict[str, Any], source_version_id: str) -> tuple[str, bool]:
    rows = cur.execute(
        """select geometry_id::text, from_year, to_year, accuracy_status::text,
                  geometry_source_version_id::text, resolution_method,
                  ST_Equals(
                    geom,
                    ST_SetSRID(ST_GeomFromGeoJSON(%s::text),4326)
                  )
             from atlas.geometry
            where spatial_entity_id=%s
              and geometry_source_native_id=%s""",
        (
            json.dumps(geom["geojson"]),
            spatial_id,
            geom["source_native_id"],
        ),
    ).fetchall()
    if len(rows) > 1:
        raise ClosureError("duplicate geometry identity")
    if rows:
        row = rows[0]
        expected = (
            geom.get("from_year"),
            geom.get("to_year"),
            geom["accuracy_status"],
            source_version_id,
            geom["resolution_method"],
            True,
        )
        if tuple(row[1:]) != expected:
            raise ClosureError(f"existing geometry differs for {geom['source_native_id']}")
        return row[0], False

    cur.execute(
        """insert into atlas.geometry(
             spatial_entity_id,from_year,to_year,geometry_source_version_id,
             geometry_source_native_id,resolution_method,accuracy_status,
             geom,notes,review_status)
           values (
             %s,%s,%s,%s,%s,%s,%s::atlas.geometry_accuracy,
             ST_SetSRID(ST_GeomFromGeoJSON(%s::text),4326),
             %s,%s::atlas.review_status)
           returning geometry_id::text""",
        (
            spatial_id,
            geom.get("from_year"),
            geom.get("to_year"),
            source_version_id,
            geom["source_native_id"],
            geom["resolution_method"],
            geom["accuracy_status"],
            json.dumps(geom["geojson"]),
            geom.get("notes"),
            geom.get("review_status", "reviewed"),
        ),
    )
    return cur.fetchone()[0], True


def ensure_context_claim_source(cur, claim_id: str, source_version_id: str, block: dict[str, Any]) -> bool:
    rows = cur.execute(
        """select evidence_role, direction::text, locator, claim_fitness
             from atlas.claim_source
            where claim_id=%s and source_version_id=%s and evidence_role=%s""",
        (claim_id, source_version_id, block["evidence_role"]),
    ).fetchall()
    if len(rows) > 1:
        raise ClosureError("duplicate Dahomey place-identity claim source")
    expected = (
        block["evidence_role"],
        block.get("direction", "context"),
        block.get("locator"),
        block.get("claim_fitness"),
    )
    if rows:
        if tuple(rows[0]) != expected:
            raise ClosureError("existing Dahomey place-identity claim source differs")
        return False
    cur.execute(
        """insert into atlas.claim_source(
             claim_id,source_version_id,evidence_role,independence_group,directness,
             direction,locator,notes,claim_fitness)
           values (%s,%s,%s,%s,%s,%s::atlas.evidence_direction,%s,%s,%s)""",
        (
            claim_id,
            source_version_id,
            block["evidence_role"],
            "law-jakin-godomey-1989",
            "specialist historical-geography synthesis",
            block.get("direction", "context"),
            block.get("locator"),
            "Place-identity context only; not an independent slavery/practice attestation.",
            block.get("claim_fitness"),
        ),
    )
    return True


def ensure_locus_link(cur, claim_id: str, spatial_id: str, block: dict[str, Any]) -> bool:
    row = cur.execute(
        """select role_text, notes
             from atlas.claim_evidence_locus
            where claim_id=%s and spatial_entity_id=%s""",
        (claim_id, spatial_id),
    ).fetchone()
    expected = (block["role_text"], block.get("notes"))
    if row:
        if tuple(row) != expected:
            raise ClosureError("existing claim-evidence-locus differs")
        return False
    cur.execute(
        """insert into atlas.claim_evidence_locus(claim_id,spatial_entity_id,role_text,notes)
           values (%s,%s,%s,%s)""",
        (claim_id, spatial_id, block["role_text"], block.get("notes")),
    )
    return True


def apply_once(
    conn,
    review: dict[str, Any],
    prerequisite_ids: dict[str, dict[str, str]],
) -> dict[str, Any]:
    result: dict[str, Any] = {}
    with conn.cursor() as cur:
        for row in review["candidates"]:
            prerequisite = prerequisite_ids[row["case_key"]]
            claim_id = prerequisite["claim_id"]
            target_spatial_id = prerequisite["spatial_entity_id"]

            if row["target"].startswith("Goryeo"):
                source, version = source_parts(row["geometry_source"])
                sv = ensure_source_version(cur, source, version)
                geom_id, inserted = ensure_geometry(
                    cur, target_spatial_id, row["geometry"], sv
                )
                result[row["case_key"]] = {
                    "geometry_id": geom_id,
                    "geometry_inserted": inserted,
                }

            elif row["target"].startswith("Dahomey"):
                identity_source, identity_version = source_parts(row["historical_identity_source"])
                identity_sv = ensure_source_version(cur, identity_source, identity_version)
                claim_source_inserted = ensure_context_claim_source(
                    cur, claim_id, identity_sv, row["historical_identity_source"]
                )

                locus = row["new_locus_entity"]
                locus_id = ensure_spatial_entity(cur, locus)

                source, version = source_parts(row["geometry_source"])
                geometry_sv = ensure_source_version(cur, source, version)
                geom_id, geom_inserted = ensure_geometry(
                    cur, locus_id, row["geometry"], geometry_sv
                )
                link_inserted = ensure_locus_link(cur, claim_id, locus_id, row["locus_link"])
                result[row["case_key"]] = {
                    "locus_spatial_entity_id": locus_id,
                    "geometry_id": geom_id,
                    "geometry_inserted": geom_inserted,
                    "claim_source_inserted": claim_source_inserted,
                    "locus_link_inserted": link_inserted,
                }

            elif row["target"].startswith("Taghaza"):
                source, version = source_parts(row["geometry_source"])
                sv = ensure_source_version(cur, source, version)
                geom_id, inserted = ensure_geometry(
                    cur, target_spatial_id, row["geometry"], sv
                )
                result[row["case_key"]] = {
                    "geometry_id": geom_id,
                    "geometry_inserted": inserted,
                }
            else:
                raise ClosureError("unexpected closure candidate")
    return result


def assert_delta(before: dict[str, int], after: dict[str, int]) -> dict[str, int]:
    delta = {table: after[table] - before[table] for table in TRACKED}
    for table, expected in STRICT_DELTA.items():
        if delta[table] != expected:
            raise ClosureError(f"unexpected delta for {table}: {delta[table]} != {expected}")
    return delta


def verify_semantics(
    conn,
    prerequisite_ids: dict[str, dict[str, str]],
) -> None:
    goryeo_ids = prerequisite_ids[
        "production-batch-2026-09-29/goryeo/nobi-status-review-0956-v1"
    ]
    dahomey_ids = prerequisite_ids[
        "production-batch-2026-09-29/dahomey/royal-captive-allocation-sale-1727-v1"
    ]
    taghaza_ids = prerequisite_ids[
        "production-batch-2026-09-29/taghaza/slave-salt-mining-1352-v1"
    ]
    claim_ids = [item["claim_id"] for item in prerequisite_ids.values()]

    with conn.cursor() as cur:
        goryeo = cur.execute(
            """select count(*)
                 from atlas.geometry
                where spatial_entity_id=%s
                  and geometry_source_native_id='UNESCO WHC 1278rev-001'
                  and accuracy_status='modern_proxy'
                  and GeometryType(geom)='POINT'""",
            (goryeo_ids["spatial_entity_id"],),
        ).fetchone()[0]
        dahomey = cur.execute(
            """select count(*)
                 from atlas.claim_evidence_locus cel
                 join atlas.spatial_entity se using(spatial_entity_id)
                 join atlas.geometry g using(spatial_entity_id)
                where cel.claim_id=%s
                  and se.canonical_name='Jakin (Godomey)'
                  and g.accuracy_status='modern_proxy'
                  and GeometryType(g.geom)='POINT'""",
            (dahomey_ids["claim_id"],),
        ).fetchone()[0]
        taghaza = cur.execute(
            """select count(*)
                 from atlas.geometry
                where spatial_entity_id=%s
                  and geometry_source_native_id like 'NGA UFI -1075410%%'
                  and accuracy_status='modern_proxy'
                  and GeometryType(geom)='POINT'""",
            (taghaza_ids["spatial_entity_id"],),
        ).fetchone()[0]
        unresolved_dahomey = cur.execute(
            """select count(*)
                 from atlas.geometry
                where spatial_entity_id=%s
                  and accuracy_status='unresolved' and geom is null""",
            (dahomey_ids["spatial_entity_id"],),
        ).fetchone()[0]
        release_hits = cur.execute(
            """select count(*)
                 from audit.release_claim
                where claim_id=any(%s::uuid[])""",
            (claim_ids,),
        ).fetchone()[0]
        non_null_p = cur.execute(
            """select count(*)
                 from atlas.territorial_practice_claim
                where claim_id=any(%s::uuid[]) and practice_level is not null""",
            (claim_ids,),
        ).fetchone()[0]
    if (goryeo, dahomey, taghaza) != (1, 1, 1):
        raise ClosureError("expected exactly three reviewed mapped representations")
    if unresolved_dahomey != 1:
        raise ClosureError("Dahomey unresolved target geometry was altered")
    if release_hits != 0:
        raise ClosureError("closure candidates unexpectedly entered release membership")
    if non_null_p != 0:
        raise ClosureError("closure rehearsal introduced a P-level")


def run(conn, review: dict[str, Any]) -> dict[str, Any]:
    prerequisite_ids = verify_claims(conn)
    before = counts(conn)
    try:
        first = apply_once(conn, review, prerequisite_ids)
        after_first = counts(conn)
        delta = assert_delta(before, after_first)
        verify_semantics(conn, prerequisite_ids)

        second = apply_once(conn, review, prerequisite_ids)
        after_second = counts(conn)
        if after_second != after_first:
            raise ClosureError("unchanged replay altered tracked counts")
        if any(
            item.get("geometry_inserted")
            or item.get("claim_source_inserted")
            or item.get("locus_link_inserted")
            for item in second.values()
        ):
            raise ClosureError("unchanged replay was not an exact no-op")
    finally:
        conn.rollback()

    restored = counts(conn)
    conn.rollback()
    if restored != before:
        raise ClosureError("rollback failed to restore tracked counts")

    return {
        "record_kind": "geometry_closure_tranche_01_rehearsal_receipt",
        "issue": 370,
        "mode": "DISPOSABLE_ROLLBACK",
        "first_pass": first,
        "second_pass": second,
        "tracked_table_delta": delta,
        "mapped_representations_after_apply": 3,
        "historical_practice_polygons_added": 0,
        "release_membership_delta": 0,
        "publication_changes": 0,
        "p_level_changes": 0,
        "rollback_restored_counts": True,
    }


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--review", type=Path, default=REVIEW)
    parser.add_argument("--dsn", default=os.environ.get("DATABASE_URL", ""))
    parser.add_argument("--apply", action="store_true")
    parser.add_argument("--disposable-test-db", action="store_true")
    args = parser.parse_args()

    review = load_review(args.review)
    plan = {
        "issue": 370,
        "mode": "plan_only",
        "candidates": [row["case_key"] for row in review["candidates"]],
        "expected_delta": STRICT_DELTA,
        "production_write_path": False,
    }
    print(json.dumps(plan, ensure_ascii=False, indent=2, sort_keys=True))
    if not args.apply:
        print("DRY RUN: no database changes made")
        return 0

    if not args.disposable_test_db:
        raise SystemExit("ERROR: this tool has no production apply path")
    if os.environ.get("CI") != "true":
        raise SystemExit("ERROR: disposable apply requires CI=true")
    if not args.dsn:
        parser.error("--dsn or DATABASE_URL is required with --apply")
    require_disposable_dsn(args.dsn)

    import psycopg
    with psycopg.connect(args.dsn, autocommit=False) as conn:
        receipt = run(conn, review)

    print("GEOMETRY_CLOSURE_REHEARSAL_RECEIPT_BEGIN")
    print(json.dumps(receipt, ensure_ascii=False, indent=2, sort_keys=True))
    print("GEOMETRY_CLOSURE_REHEARSAL_RECEIPT_END")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
