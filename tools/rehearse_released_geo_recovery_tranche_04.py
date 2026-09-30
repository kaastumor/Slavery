#!/usr/bin/env python3
"""Rehearse #383 Sogdiana / Afrosiab released-case geo recovery.

Disposable-only test. It recreates the minimum exact v0.8.1 claim/target/source/
release identities needed for the test, including the existing reviewed unresolved
Sogdiana target-geometry row. It then adds one Afrosiab specialist evidence locus,
requires unchanged replay to be an exact no-op, and rolls the whole transaction back.

There is deliberately no production commit path.
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

from tools.add_research_case import ensure_source_version
from tools.rehearse_geometry_closure_tranche_01 import (
    ClosureError,
    ensure_geometry,
    ensure_locus_link,
    source_parts,
)
from tools.rehearse_geometry_closure_tranche_02 import ensure_locus_entity

REVIEW = ROOT / "data/research/geometry_reviews/population_100_100_released_geo_tranche_04_sogdiana_samarkand.json"

TARGET_SPATIAL_ID = "a6718e1f-5683-48f4-90fb-cc35ad263ba5"
CLAIM_ID = "63dda32b-6c3e-4b3e-9c5a-36596e6cdc1b"
HISTORICAL_SOURCE_ID = "9147c278-4c58-437a-b365-6c561d2cfc83"
HISTORICAL_SOURCE_VERSION_ID = "cc49573e-8621-43d2-b054-a496c66cdcc8"
HISTORICAL_CLAIM_SOURCE_ID = "9ca80f84-ce24-407b-9ed5-579cb0f5e23f"
UNRESOLVED_GEOMETRY_ID = "ef33b27a-2b8f-4fc0-a523-885137706193"
RELEASE_VERSION = "v0.8.1"
RELEASE_OBJECT_SHA = "e1c7a4977a11a9e1ba50f1287776adf7b0d4def3bf449d318d19b9d11dca6b55"

TRACKED = (
    "atlas.spatial_entity",
    "atlas.source",
    "atlas.source_version",
    "atlas.claim",
    "atlas.territorial_practice_claim",
    "atlas.claim_source",
    "atlas.geometry",
    "atlas.claim_evidence_locus",
    "audit.release_manifest",
    "audit.release_claim",
    "audit.release_geometry",
    "audit.release_channel",
)

STRICT_DELTA = {
    "atlas.spatial_entity": 1,
    "atlas.source": 1,
    "atlas.source_version": 1,
    "atlas.claim": 0,
    "atlas.territorial_practice_claim": 0,
    "atlas.claim_source": 0,
    "atlas.geometry": 1,
    "atlas.claim_evidence_locus": 1,
    "audit.release_manifest": 0,
    "audit.release_claim": 0,
    "audit.release_geometry": 0,
    "audit.release_channel": 0,
}


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


def load_review(path: Path = REVIEW) -> dict[str, Any]:
    value = json.loads(path.read_text(encoding="utf-8"))
    if value.get("schema") != "historical-slavery-atlas-100-100-released-geo-recovery-review-v1":
        raise ClosureError("unexpected #383 review schema")
    if value.get("issue") != 383:
        raise ClosureError("review issue drift")
    if value.get("status") != "INTERNAL_REVIEW_COMPLETE_READY_FOR_DISPOSABLE_REHEARSAL":
        raise ClosureError("review is not at disposable-rehearsal gate")
    facets = value.get("released_case", {}).get("claim_facets") or []
    if len(facets) != 1 or facets[0].get("claim_id") != CLAIM_ID:
        raise ClosureError("released claim identity drift")
    if facets[0].get("release_object_sha256") != RELEASE_OBJECT_SHA:
        raise ClosureError("released object hash drift")
    if value.get("candidate", {}).get("disposition") != "ACCEPT_FOR_DISPOSABLE_REHEARSAL":
        raise ClosureError("Sogdiana candidate is not accepted for rehearsal")
    if value.get("candidate", {}).get("semantic_role") != "claim_evidence_locus_probable_contract_setting":
        raise ClosureError("Sogdiana locus role drift")
    if value.get("qc", {}).get("historical_practice_polygons_added") != 0:
        raise ClosureError("review unexpectedly permits a practice polygon")
    return value


def insert_release_fixture(conn) -> None:
    """Insert the minimum exact-identity released Sogdiana fixture."""
    with conn.cursor() as cur:
        occupied = cur.execute(
            """select
               (select count(*) from atlas.spatial_entity where spatial_entity_id=%s),
               (select count(*) from atlas.claim where claim_id=%s),
               (select count(*) from atlas.source_version where source_version_id=%s),
               (select count(*) from atlas.geometry where geometry_id=%s),
               (select count(*) from audit.release_manifest where release_version=%s)""",
            (
                TARGET_SPATIAL_ID,
                CLAIM_ID,
                HISTORICAL_SOURCE_VERSION_ID,
                UNRESOLVED_GEOMETRY_ID,
                RELEASE_VERSION,
            ),
        ).fetchone()
        if any(occupied):
            raise ClosureError("released-case fixture requires clean exact identities")

        cur.execute(
            """insert into atlas.source(
                 source_id,title,author_or_institution,source_type,
                 source_classification,geographic_scope,temporal_scope,
                 independence_notes,reliability_limitations)
               values (%s,%s,%s,%s,%s,%s,%s,%s,%s)""",
            (
                HISTORICAL_SOURCE_ID,
                "Marriage i. The Marriage Contract in the Pre-Islamic Period ii. Sogdian Marriage Contract",
                "Ilya Yakubovich; Encyclopaedia Iranica",
                "specialist_reference",
                "secondary",
                "Sogdiana / Samarkand documentary milieu",
                "early eighth century CE",
                "Disposable fixture of the already accepted historical source family.",
                "Place of conclusion is a specialist inference; Mount Mugh is the document findspot.",
            ),
        )
        cur.execute(
            """insert into atlas.source_version(
                 source_version_id,source_id,version_label,url_or_identifier,notes)
               values (%s,%s,%s,%s,%s)""",
            (
                HISTORICAL_SOURCE_VERSION_ID,
                HISTORICAL_SOURCE_ID,
                "Encyclopaedia Iranica, Sogdian marriage contract",
                "https://www.iranicaonline.org/articles/marriage-contract-in-the-pre-islamic-period/marriage-i-the-marriage-contract-in-the-pre-islamic-period-ii-sogdian-marriage-contract/",
                "Exact production source-version identity; disposable fixture only.",
            ),
        )
        cur.execute(
            """insert into atlas.spatial_entity(
                 spatial_entity_id,entity_type_code,canonical_name,display_name,
                 notes,review_status)
               values (%s,'region',%s,%s,%s,'reviewed')""",
            (
                TARGET_SPATIAL_ID,
                "Early eighth-century Sogdiana",
                "Sogdiana",
                "Disposable exact-identity fixture of the released analytical target.",
            ),
        )
        cur.execute(
            """insert into atlas.claim(
                 claim_id,claim_kind_code,from_year,to_year,date_text_original,
                 temporal_precision,spatial_precision,summary,confidence,
                 review_status,publication_status,notes)
               values (
                 %s,'territorial_practice',709,710,
                 'tenth regnal year of Tarkhun, king of Samarkand (ca. 709-710 CE)',
                 'bounded_year_range','historical region/documentary milieu',
                 %s,'S','reviewed','published',%s)""",
            (
                CLAIM_ID,
                "The accepted Sogdian marriage-contract package recognizes slave status within an early eighth-century Sogdian legal/documentary context.",
                "Disposable exact-identity fixture; existing released P2 is preserved, not recalculated.",
            ),
        )
        cur.execute(
            """insert into atlas.territorial_practice_claim(
                 claim_id,spatial_entity_id,practice_type_code,practice_level,
                 coverage_state_code,classification_status,notes)
               values (%s,%s,'slavery_enslavement','P2','classified',
                       'released legacy classification',%s)""",
            (
                CLAIM_ID,
                TARGET_SPATIAL_ID,
                "Existing released P2 reproduced only as a prerequisite fixture; geometry work must not strengthen or recalculate it.",
            ),
        )
        cur.execute(
            """insert into atlas.claim_source(
                 claim_source_id,claim_id,source_version_id,evidence_role,
                 directness,direction,locator,notes)
               values (%s,%s,%s,%s,%s,'supports',%s,%s)""",
            (
                HISTORICAL_CLAIM_SOURCE_ID,
                CLAIM_ID,
                HISTORICAL_SOURCE_VERSION_ID,
                "source-native legal recognition of slave status in the Samarkand documentary milieu",
                "specialist edition and translation",
                "Nov. 3 lines 11-17; Nov. 4 lines 7-15; discussion dating the contract to ca. 709-710 CE and probably Samarkand",
                "Disposable fixture preserving the accepted historical source linkage.",
            ),
        )
        cur.execute(
            """insert into atlas.geometry(
                 geometry_id,spatial_entity_id,from_year,to_year,
                 geometry_source_version_id,geometry_source_native_id,
                 resolution_method,accuracy_status,geom,notes,review_status)
               values (%s,%s,709,710,null,null,%s,'unresolved',null,%s,'reviewed')""",
            (
                UNRESOLVED_GEOMETRY_ID,
                TARGET_SPATIAL_ID,
                "Resolve the Samarkand/Panjikent documentary context and contemporaneous Sogdian political geography separately. Do not use modern Uzbekistan/Tajikistan, a Silk Road diaspora footprint, or a maximum-extent imperial polygon as a territorial proxy.",
                "Exact production unresolved target-geometry identity; disposable fixture only.",
            ),
        )
        cur.execute(
            """insert into audit.release_manifest(
                 release_version,schema_version,status,changelog,qc_summary,
                 unresolved_issues,manifest)
               values (%s,'0034','draft',%s,%s,%s,%s::jsonb)""",
            (
                RELEASE_VERSION,
                "Disposable v0.8.1 membership fixture for #383 only.",
                "Exact released claim/object identity used to test geometry-only augmentation.",
                "Not a full release bundle; transaction always rolls back.",
                json.dumps({"fixture": "issue-383-disposable-release-membership"}),
            ),
        )
        cur.execute(
            """insert into audit.release_claim(
                 release_version,claim_id,object_sha256,capture_status)
               values (%s,%s,%s,'captured_at_release')""",
            (RELEASE_VERSION, CLAIM_ID, RELEASE_OBJECT_SHA),
        )
        cur.execute(
            "update audit.release_manifest set status='published' where release_version=%s",
            (RELEASE_VERSION,),
        )


def normalized_geometry(candidate: dict[str, Any]) -> dict[str, Any]:
    geom = dict(candidate["geometry"])
    native = geom.pop("geometry_source_native_id", None)
    if native is not None:
        geom["source_native_id"] = native
    if geom.get("source_native_id") != "UNESCO-WHC-603rev-001":
        raise ClosureError("UNESCO component identity drift")
    return geom


def apply_once(conn, review: dict[str, Any]) -> dict[str, Any]:
    candidate = review["candidate"]
    with conn.cursor() as cur:
        locus_id, locus_created = ensure_locus_entity(cur, candidate["new_locus_entity"])
        source, version = source_parts(candidate["geometry_source"])
        geometry_sv = ensure_source_version(cur, source, version)
        geometry_id, geometry_inserted = ensure_geometry(
            cur, locus_id, normalized_geometry(candidate), geometry_sv
        )
        links = candidate.get("locus_links") or []
        if len(links) != 1:
            raise ClosureError("expected exactly one Sogdiana locus link")
        link_inserted = ensure_locus_link(cur, CLAIM_ID, locus_id, links[0])
    return {
        "locus_spatial_entity_id": locus_id,
        "locus_created": locus_created,
        "geometry_source_version_id": geometry_sv,
        "geometry_id": geometry_id,
        "geometry_inserted": geometry_inserted,
        "locus_link_inserted": link_inserted,
    }


def replay_is_noop(result: dict[str, Any]) -> bool:
    return (
        not result.get("locus_created")
        and not result.get("geometry_inserted")
        and not result.get("locus_link_inserted")
    )


def assert_delta(before: dict[str, int], after: dict[str, int]) -> dict[str, int]:
    delta = {table: after[table] - before[table] for table in TRACKED}
    for table, expected in STRICT_DELTA.items():
        if delta[table] != expected:
            raise ClosureError(
                f"unexpected #383 closure delta for {table}: {delta[table]} != {expected}"
            )
    return delta


def verify_semantics(conn, review: dict[str, Any], first: dict[str, Any]) -> None:
    candidate = review["candidate"]
    locus_id = first["locus_spatial_entity_id"]
    geometry_id = first["geometry_id"]
    with conn.cursor() as cur:
        entity = cur.execute(
            """select canonical_name,entity_type_code,from_year,to_year,review_status::text
                 from atlas.spatial_entity where spatial_entity_id=%s""",
            (locus_id,),
        ).fetchone()
        expected_entity = candidate["new_locus_entity"]
        if entity != (
            expected_entity["canonical_name"],
            expected_entity["entity_type_code"],
            expected_entity["from_year"],
            expected_entity["to_year"],
            expected_entity["review_status"],
        ):
            raise ClosureError("Afrosiab locus entity semantic drift")

        geom = cur.execute(
            """select accuracy_status::text,GeometryType(geom),geometry_source_native_id,
                      from_year,to_year,review_status::text
                 from atlas.geometry where geometry_id=%s""",
            (geometry_id,),
        ).fetchone()
        if geom != (
            "specialist",
            "POINT",
            "UNESCO-WHC-603rev-001",
            709,
            710,
            "reviewed",
        ):
            raise ClosureError("Afrosiab geometry semantic drift")

        expected_link = candidate["locus_links"][0]
        link = cur.execute(
            """select role_text,notes
                 from atlas.claim_evidence_locus
                where claim_id=%s and spatial_entity_id=%s""",
            (CLAIM_ID, locus_id),
        ).fetchone()
        if link != (expected_link["role_text"], expected_link.get("notes")):
            raise ClosureError("Sogdiana claim-evidence-locus linkage drift")

        historical = cur.execute(
            """select source_version_id::text,evidence_role,locator
                 from atlas.claim_source where claim_id=%s""",
            (CLAIM_ID,),
        ).fetchall()
        if historical != [(
            HISTORICAL_SOURCE_VERSION_ID,
            "source-native legal recognition of slave status in the Samarkand documentary milieu",
            "Nov. 3 lines 11-17; Nov. 4 lines 7-15; discussion dating the contract to ca. 709-710 CE and probably Samarkand",
        )]:
            raise ClosureError("historical claim-source linkage changed")

        claim_state = cur.execute(
            """select c.review_status::text,c.publication_status::text,
                      t.practice_level::text,t.practice_type_code
                 from atlas.claim c
                 join atlas.territorial_practice_claim t using(claim_id)
                where c.claim_id=%s""",
            (CLAIM_ID,),
        ).fetchone()
        if claim_state != ("reviewed", "published", "P2", "slavery_enslavement"):
            raise ClosureError("released Sogdiana claim state changed")

        target_geom = cur.execute(
            """select geometry_id::text,accuracy_status::text,
                      from_year,to_year,(geom is null),review_status::text
                 from atlas.geometry where spatial_entity_id=%s
                order by geometry_id::text""",
            (TARGET_SPATIAL_ID,),
        ).fetchall()
        if target_geom != [(
            UNRESOLVED_GEOMETRY_ID,
            "unresolved",
            709,
            710,
            True,
            "reviewed",
        )]:
            raise ClosureError("existing unresolved Sogdiana target geometry changed")

        membership = cur.execute(
            """select object_sha256,capture_status
                 from audit.release_claim
                where release_version=%s and claim_id=%s""",
            (RELEASE_VERSION, CLAIM_ID),
        ).fetchone()
        if membership != (RELEASE_OBJECT_SHA, "captured_at_release"):
            raise ClosureError("v0.8.1 Sogdiana release membership changed")

        release_geom = cur.execute(
            "select count(*) from audit.release_geometry where geometry_id=%s",
            (geometry_id,),
        ).fetchone()[0]
        if release_geom != 0:
            raise ClosureError("new Afrosiab geometry unexpectedly entered release membership")

        source_links = cur.execute(
            "select count(*) from atlas.claim_source where claim_id=%s",
            (CLAIM_ID,),
        ).fetchone()[0]
        if source_links != 1:
            raise ClosureError("geometry rehearsal added historical claim-source evidence")


def run(conn, review: dict[str, Any]) -> dict[str, Any]:
    original = counts(conn)
    first = second = delta = None
    try:
        insert_release_fixture(conn)
        closure_before = counts(conn)
        first = apply_once(conn, review)
        closure_after = counts(conn)
        delta = assert_delta(closure_before, closure_after)
        verify_semantics(conn, review, first)

        second = apply_once(conn, review)
        if counts(conn) != closure_after:
            raise ClosureError("unchanged #383 replay altered tracked counts")
        if not replay_is_noop(second):
            raise ClosureError("unchanged #383 replay was not an exact no-op")
    finally:
        conn.rollback()

    restored = counts(conn)
    conn.rollback()
    if restored != original:
        raise ClosureError("#383 rollback failed to restore original counts")

    return {
        "record_kind": "released_geo_recovery_tranche_04_rehearsal_receipt",
        "version": 1,
        "issue": 383,
        "mode": "DISPOSABLE_ROLLBACK",
        "fixture": {
            "release_version": RELEASE_VERSION,
            "released_claim_id": CLAIM_ID,
            "historical_source_version_id": HISTORICAL_SOURCE_VERSION_ID,
            "unresolved_target_geometry_id": UNRESOLVED_GEOMETRY_ID,
        },
        "first_pass": first,
        "second_pass": second,
        "tracked_closure_delta": delta,
        "released_case_linked_mapped_representations_added": 1,
        "claim_evidence_locus_links_added": 1,
        "historical_claim_source_delta": 0,
        "historical_practice_polygons_added": 0,
        "target_geometry_rows_replaced": 0,
        "claim_delta": 0,
        "release_membership_delta": 0,
        "release_geometry_delta": 0,
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
    print(json.dumps({
        "issue": 383,
        "mode": "plan_only",
        "released_claim_id": CLAIM_ID,
        "expected_closure_delta": STRICT_DELTA,
        "production_write_path": False,
    }, indent=2, sort_keys=True))

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

    print("RELEASED_GEO_RECOVERY_TRANCHE_04_REHEARSAL_RECEIPT_BEGIN")
    print(json.dumps(receipt, ensure_ascii=False, indent=2, sort_keys=True))
    print("RELEASED_GEO_RECOVERY_TRANCHE_04_REHEARSAL_RECEIPT_END")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
