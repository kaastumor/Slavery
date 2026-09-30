#!/usr/bin/env python3
"""Rehearse #379 released ISIL/Yazidi Sinjar evidence-locus recovery.

This is a disposable-only exact-identity fixture and augmentation test. It recreates
only the released ISIL/Yazidi case objects needed for the test, including v0.8.1
release membership and the shared UNITAD source-version relationship. It then adds
one Sinjar-town evidence locus, replays the augmentation as an exact no-op, and
rolls the entire transaction back.

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

REVIEW = ROOT / "data/research/geometry_reviews/population_100_100_released_geo_tranche_03_isil_sinjar.json"

TARGET_SPATIAL_ID = "c6edcdcd-0583-5d19-a54b-a1f3e1e32ffc"
ENSLAVEMENT_CLAIM = "88e48d2e-5b06-5b37-80bb-82e07db36a3f"
SEXUAL_SLAVERY_CLAIM = "b862e0a9-a857-57e0-8aa3-e37daf0844cf"
CLAIMS = (ENSLAVEMENT_CLAIM, SEXUAL_SLAVERY_CLAIM)
UNITAD_SOURCE_ID = "062f2f6c-fd64-5cfb-8825-d04c88503f7c"
UNITAD_SOURCE_VERSION_ID = "dc410234-3f13-5e41-9ce9-4391a850cc23"
RELEASE_VERSION = "v0.8.1"

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
    "atlas.claim_evidence_locus": 2,
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
        raise ClosureError("unexpected #379 review schema")
    if value.get("issue") != 379:
        raise ClosureError("review issue drift")
    if value.get("status") != "INTERNAL_REVIEW_COMPLETE_READY_FOR_DISPOSABLE_REHEARSAL":
        raise ClosureError("review is not at disposable-rehearsal gate")
    facets = value.get("released_case", {}).get("claim_facets") or []
    if {row.get("claim_id") for row in facets} != set(CLAIMS):
        raise ClosureError("released claim membership drift")
    if value.get("candidate", {}).get("disposition") != "ACCEPT_FOR_DISPOSABLE_REHEARSAL":
        raise ClosureError("Sinjar candidate is not accepted for rehearsal")
    if value.get("qc", {}).get("historical_practice_polygons_added") != 0:
        raise ClosureError("review unexpectedly permits a practice polygon")
    return value


def insert_release_fixture(conn) -> None:
    """Insert the minimum exact-identity v0.8.1 case fixture.

    The fixture preserves the production UUIDs, source-version relationship and
    release-membership object hashes. It is not a substitute release bundle and is
    always rolled back.
    """
    with conn.cursor() as cur:
        occupied = cur.execute(
            """select
               (select count(*) from atlas.spatial_entity where spatial_entity_id=%s),
               (select count(*) from atlas.claim where claim_id=any(%s::uuid[])),
               (select count(*) from atlas.source_version where source_version_id=%s),
               (select count(*) from audit.release_manifest where release_version=%s)""",
            (TARGET_SPATIAL_ID, list(CLAIMS), UNITAD_SOURCE_VERSION_ID, RELEASE_VERSION),
        ).fetchone()
        if any(occupied):
            raise ClosureError("released-case fixture requires clean exact identities")

        cur.execute(
            """insert into atlas.source(
                 source_id,title,source_type,geographic_scope,temporal_scope,notes)
               values (%s,%s,%s,%s,%s,%s)""",
            (
                UNITAD_SOURCE_ID,
                "v0.6.1 global evidence source — Iraq/Syria under ISIL, especially Yazidi population from 2014",
                "Workbook-linked historical source",
                "Mesopotamia & Near East",
                "1900–present",
                "Disposable exact-identity fixture mirroring the production workbook-linked UNITAD source.",
            ),
        )
        cur.execute(
            """insert into atlas.source_version(
                 source_version_id,source_id,version_label,url_or_identifier,notes)
               values (%s,%s,%s,%s,%s)""",
            (
                UNITAD_SOURCE_VERSION_ID,
                UNITAD_SOURCE_ID,
                "exact URL cited by canonical v0.6.1 (v0.4.8 Evidence)",
                "https://www.unitad.un.org/sites/www.unitad.un.org/files/sinjar_brief_public_updated_0_2.pdf",
                "Exact production source-version identity; disposable fixture only.",
            ),
        )
        cur.execute(
            """insert into atlas.spatial_entity(
                 spatial_entity_id,entity_type_code,canonical_name,display_name,
                 from_year,notes,review_status)
               values (%s,'region',%s,%s,1900,%s,'reviewed')""",
            (
                TARGET_SPATIAL_ID,
                "Iraq/Syria under ISIL, especially Yazidi population from 2014",
                "Iraq/Syria under ISIL, especially Yazidi population from 2014",
                "Disposable exact-identity fixture of the released analytical target.",
            ),
        )

        claim_rows = (
            (
                ENSLAVEMENT_CLAIM,
                "slavery_enslavement",
                "fdbcae720fcfc2030bf168d09c6458fa4bd6e9b47249fe6021bdcef9e381deed",
                "90d68d06-479c-5b3b-b09d-a950369617c1",
            ),
            (
                SEXUAL_SLAVERY_CLAIM,
                "sexual_slavery",
                "f6a7143cf1cfd17688b23716ab67708f6e20d9e71e0c33fed3d0fe44e46ce69f",
                "ab02d03c-1744-5c9a-85e5-b8e692e31157",
            ),
        )
        for claim_id, practice_type, object_sha, claim_source_id in claim_rows:
            cur.execute(
                """insert into atlas.claim(
                     claim_id,claim_kind_code,from_year,date_text_original,
                     temporal_precision,spatial_precision,summary,confidence,
                     review_status,publication_status,notes)
                   values (
                     %s,'territorial_practice',2014,'from 2014',
                     'open_ended_from_year','workbook area/region label',
                     %s,'S','reviewed','unpublished',%s)""",
                (
                    claim_id,
                    "UNITAD found reasonable grounds for crimes including enslavement, sexual slavery and the slave trade against Yazidis, with women and girls treated as property and sold or transferred.",
                    "Disposable exact-identity fixture of the released claim; no P-level.",
                ),
            )
            cur.execute(
                """insert into atlas.territorial_practice_claim(
                     claim_id,spatial_entity_id,practice_type_code,practice_level,
                     coverage_state_code,classification_status,notes)
                   values (%s,%s,%s,null,'classified','strong workbook classification',%s)""",
                (
                    claim_id,
                    TARGET_SPATIAL_ID,
                    practice_type,
                    "P-level intentionally unassigned; disposable exact-identity fixture.",
                ),
            )
            cur.execute(
                """insert into atlas.claim_source(
                     claim_source_id,claim_id,source_version_id,evidence_role,
                     independence_group,directness,direction,locator,notes)
                   values (%s,%s,%s,'global workbook evidence row',null,
                           'exact source URL cited by workbook','supports',
                           'v0.4.8 Evidence!6',%s)""",
                (
                    claim_source_id,
                    claim_id,
                    UNITAD_SOURCE_VERSION_ID,
                    "Disposable exact-identity fixture preserving the production UNITAD linkage.",
                ),
            )

        cur.execute(
            """insert into audit.release_manifest(
                 release_version,schema_version,status,changelog,qc_summary,
                 unresolved_issues,manifest)
               values (%s,'0034','published',%s,%s,%s,%s::jsonb)""",
            (
                RELEASE_VERSION,
                "Disposable v0.8.1 membership fixture for #379 only.",
                "Exact two-claim membership identity used to test a geometry-only augmentation.",
                "Not a full release bundle; transaction always rolls back.",
                json.dumps({"fixture": "issue-379-disposable-release-membership"}),
            ),
        )
        for claim_id, _practice_type, object_sha, _claim_source_id in claim_rows:
            cur.execute(
                """insert into audit.release_claim(
                     release_version,claim_id,object_sha256,capture_status)
                   values (%s,%s,%s,'captured_at_release')""",
                (RELEASE_VERSION, claim_id, object_sha),
            )


def apply_once(conn, review: dict[str, Any]) -> dict[str, Any]:
    candidate = review["candidate"]
    with conn.cursor() as cur:
        locus_id, locus_created = ensure_locus_entity(cur, candidate["new_locus_entity"])

        source, version = source_parts(candidate["geometry_source"])
        geometry_sv = ensure_source_version(cur, source, version)
        geometry_id, geometry_inserted = ensure_geometry(
            cur, locus_id, candidate["geometry"], geometry_sv
        )

        link_results = {}
        for link in candidate["locus_links"]:
            inserted = ensure_locus_link(cur, link["claim_id"], locus_id, link)
            link_results[link["claim_id"]] = inserted

    return {
        "locus_spatial_entity_id": locus_id,
        "locus_created": locus_created,
        "geometry_id": geometry_id,
        "geometry_inserted": geometry_inserted,
        "geometry_source_version_id": geometry_sv,
        "locus_links_inserted": link_results,
    }


def replay_is_noop(result: dict[str, Any]) -> bool:
    return (
        not result.get("locus_created")
        and not result.get("geometry_inserted")
        and all(not inserted for inserted in result.get("locus_links_inserted", {}).values())
    )


def assert_delta(before: dict[str, int], after: dict[str, int]) -> dict[str, int]:
    delta = {table: after[table] - before[table] for table in TRACKED}
    for table, expected in STRICT_DELTA.items():
        if delta[table] != expected:
            raise ClosureError(f"unexpected #379 closure delta for {table}: {delta[table]} != {expected}")
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
            raise ClosureError("Sinjar locus entity semantic drift")

        geom = cur.execute(
            """select accuracy_status::text,GeometryType(geom),geometry_source_native_id,
                      from_year,to_year,review_status::text
                 from atlas.geometry where geometry_id=%s""",
            (geometry_id,),
        ).fetchone()
        if geom != (
            "modern_proxy",
            "POINT",
            "GeoNames 448149",
            2014,
            2014,
            "reviewed",
        ):
            raise ClosureError("Sinjar geometry semantic drift")

        links = cur.execute(
            """select claim_id::text,role_text,notes
                 from atlas.claim_evidence_locus
                where spatial_entity_id=%s
                order by claim_id::text""",
            (locus_id,),
        ).fetchall()
        expected_links = sorted(
            (
                link["claim_id"],
                link["role_text"],
                link.get("notes"),
            )
            for link in candidate["locus_links"]
        )
        if links != expected_links:
            raise ClosureError("Sinjar claim-evidence-locus linkage drift")

        historical_sources = cur.execute(
            """select claim_id::text,source_version_id::text,count(*)
                 from atlas.claim_source
                where claim_id=any(%s::uuid[])
                group by claim_id,source_version_id
                order by claim_id::text""",
            (list(CLAIMS),),
        ).fetchall()
        if historical_sources != [
            (ENSLAVEMENT_CLAIM, UNITAD_SOURCE_VERSION_ID, 1),
            (SEXUAL_SLAVERY_CLAIM, UNITAD_SOURCE_VERSION_ID, 1),
        ]:
            raise ClosureError("historical source linkage changed")

        membership = cur.execute(
            """select claim_id::text,object_sha256,capture_status
                 from audit.release_claim
                where release_version=%s and claim_id=any(%s::uuid[])
                order by claim_id::text""",
            (RELEASE_VERSION, list(CLAIMS)),
        ).fetchall()
        if membership != [
            (
                ENSLAVEMENT_CLAIM,
                "fdbcae720fcfc2030bf168d09c6458fa4bd6e9b47249fe6021bdcef9e381deed",
                "captured_at_release",
            ),
            (
                SEXUAL_SLAVERY_CLAIM,
                "f6a7143cf1cfd17688b23716ab67708f6e20d9e71e0c33fed3d0fe44e46ce69f",
                "captured_at_release",
            ),
        ]:
            raise ClosureError("v0.8.1 release membership changed")

        release_geom = cur.execute(
            "select count(*) from audit.release_geometry where geometry_id=%s",
            (geometry_id,),
        ).fetchone()[0]
        if release_geom != 0:
            raise ClosureError("new Sinjar geometry unexpectedly entered release membership")

        p_levels = cur.execute(
            """select count(*) from atlas.territorial_practice_claim
                where claim_id=any(%s::uuid[]) and practice_level is not null""",
            (list(CLAIMS),),
        ).fetchone()[0]
        if p_levels:
            raise ClosureError("rehearsal introduced a P-level")

        published = cur.execute(
            """select count(*) from atlas.claim
                where claim_id=any(%s::uuid[])
                  and publication_status::text <> 'unpublished'""",
            (list(CLAIMS),),
        ).fetchone()[0]
        if published:
            raise ClosureError("rehearsal changed claim publication status")

        target_geom = cur.execute(
            "select count(*) from atlas.geometry where spatial_entity_id=%s",
            (TARGET_SPATIAL_ID,),
        ).fetchone()[0]
        if target_geom:
            raise ClosureError("rehearsal attached geometry to the broad ISIL/Iraq-Syria target")


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
            raise ClosureError("unchanged #379 replay altered tracked counts")
        if not replay_is_noop(second):
            raise ClosureError("unchanged #379 replay was not an exact no-op")
    finally:
        conn.rollback()

    restored = counts(conn)
    conn.rollback()
    if restored != original:
        raise ClosureError("#379 rollback failed to restore original counts")

    return {
        "record_kind": "released_geo_recovery_tranche_03_rehearsal_receipt",
        "version": 1,
        "issue": 379,
        "mode": "DISPOSABLE_ROLLBACK",
        "fixture": {
            "release_version": RELEASE_VERSION,
            "released_claim_ids": list(CLAIMS),
            "shared_unitad_source_version_id": UNITAD_SOURCE_VERSION_ID,
        },
        "first_pass": first,
        "second_pass": second,
        "tracked_closure_delta": delta,
        "released_case_linked_mapped_representations_added": 1,
        "claim_evidence_locus_links_added": 2,
        "historical_practice_polygons_added": 0,
        "historical_claim_source_delta": 0,
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
        "issue": 379,
        "mode": "plan_only",
        "released_claim_ids": list(CLAIMS),
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

    print("RELEASED_GEO_RECOVERY_TRANCHE_03_REHEARSAL_RECEIPT_BEGIN")
    print(json.dumps(receipt, ensure_ascii=False, indent=2, sort_keys=True))
    print("RELEASED_GEO_RECOVERY_TRANCHE_03_REHEARSAL_RECEIPT_END")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
