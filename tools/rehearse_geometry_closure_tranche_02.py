#!/usr/bin/env python3
"""Rehearse #374 geometry closure tranche 2 in disposable PostGIS only.

The rehearsal first reconstructs the four accepted current-method claims from their
reviewed packets. It then measures only the case-linked geometry/locus amendments,
replays them unchanged as exact no-ops, and rolls the entire transaction back.

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

from tools.add_research_case import (
    ensure_source_version,
    ensure_spatial_entity,
    insert_case,
    load_spec,
)
from tools.rehearse_geometry_closure_tranche_01 import (
    ClosureError,
    counts,
    ensure_geometry,
    ensure_locus_link,
    source_parts,
)

REVIEW = ROOT / "data/research/geometry_reviews/population_100_100_closure_tranche_02.json"

PACKETS = {
    "overnight-2026-09-27/india/bonded-labour-v2":
        ROOT / "data/research/recovery/overnight_2026_09_27/03_india_bonded_labour_v2.json",
    "overnight-2026-09-27/myanmar/state-forced-labour-v2":
        ROOT / "data/research/recovery/overnight_2026_09_27/05_myanmar_forced_labour_v2.json",
    "overnight-2026-09-27/pakistan/bonded-labour-v2":
        ROOT / "data/research/recovery/overnight_2026_09_27/07_pakistan_bonded_labour_v2.json",
    "post-overnight-2026-09-27/nazi-germany/state-forced-labour-1942-1944-v2":
        ROOT / "data/research/recovery/post_overnight_2026_09_27/nazi_germany_state_forced_labour_v2.json",
}

ACCEPTED = tuple(PACKETS)
BRAZIL_HOLD = "overnight-2026-09-27/brazil/rural-debt-bondage-2003-2005-v2"

STRICT_DELTA = {
    "atlas.spatial_entity": 4,
    "atlas.source": 6,
    "atlas.source_version": 6,
    "atlas.geometry": 4,
    "atlas.claim_source": 2,
    "atlas.claim_evidence_locus": 4,
    "atlas.claim": 0,
    "audit.release_claim": 0,
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


def load_review(path: Path = REVIEW) -> dict[str, Any]:
    value = json.loads(path.read_text(encoding="utf-8"))
    if value.get("schema") != "historical-slavery-atlas-100-100-geometry-closure-review-v1":
        raise ClosureError("unexpected review schema")
    if value.get("issue") != 374:
        raise ClosureError("review issue drift")
    rows = value.get("candidates") or []
    accepted = {
        row["case_key"]
        for row in rows
        if row.get("disposition") == "ACCEPT_FOR_DISPOSABLE_REHEARSAL"
    }
    held = {
        row["case_key"]
        for row in rows
        if row.get("disposition") == "HOLD_PLACE_IDENTITY_BEFORE_GEOMETRY"
    }
    if accepted != set(ACCEPTED):
        raise ClosureError("accepted tranche membership drift")
    if held != {BRAZIL_HOLD}:
        raise ClosureError("Brazil HOLD membership drift")
    if value.get("qc", {}).get("historical_practice_polygons_added") != 0:
        raise ClosureError("review unexpectedly permits historical-practice polygons")
    return value


def insert_prerequisites(conn) -> dict[str, dict[str, str]]:
    resolved: dict[str, dict[str, str]] = {}
    with conn.cursor() as cur:
        prior = cur.execute(
            "select count(*) from audit.research_case_ingest where case_key=any(%s)",
            (list(ACCEPTED),),
        ).fetchone()[0]
        if prior:
            raise ClosureError("tranche-2 rehearsal requires clean prerequisite case keys")

    for case_key, path in PACKETS.items():
        spec = load_spec(path, require_case_key=True)
        if spec["case_key"] != case_key:
            raise ClosureError(f"packet case-key drift for {case_key}")
        claim_id, inserted = insert_case(
            conn,
            spec,
            source_path=str(path.relative_to(ROOT)),
            git_revision="TRANCHE_02_DISPOSABLE_PREREQUISITE",
        )
        if not inserted:
            raise ClosureError(f"unexpected prerequisite no-op for {case_key}")
        with conn.cursor() as cur:
            row = cur.execute(
                """select c.review_status::text,c.publication_status::text,
                          t.practice_level::text,t.spatial_entity_id::text,
                          se.canonical_name
                     from atlas.claim c
                     join atlas.territorial_practice_claim t using(claim_id)
                     join atlas.spatial_entity se using(spatial_entity_id)
                    where c.claim_id=%s""",
                (claim_id,),
            ).fetchone()
        if row is None or row[0:3] != ("reviewed", "unpublished", None):
            raise ClosureError(f"prerequisite review/publication/P-level drift for {case_key}")
        resolved[case_key] = {
            "claim_id": str(claim_id),
            "target_spatial_entity_id": row[3],
            "target_canonical_name": row[4],
        }
    return resolved


def ensure_locus_entity(cur, entity: dict[str, Any]) -> tuple[str, bool]:
    row = cur.execute(
        "select spatial_entity_id::text,entity_type_code from atlas.spatial_entity where canonical_name=%s",
        (entity["canonical_name"],),
    ).fetchone()
    if row:
        if row[1] != entity["entity_type_code"]:
            raise ClosureError("existing locus entity has wrong type")
        return row[0], False
    spatial_id = ensure_spatial_entity(cur, entity)
    return spatial_id, True


def ensure_context_claim_source(
    cur,
    claim_id: str,
    source_version_id: str,
    block: dict[str, Any],
) -> bool:
    rows = cur.execute(
        """select evidence_role,independence_group,directness,direction::text,
                  locator,claim_fitness
             from atlas.claim_source
            where claim_id=%s and source_version_id=%s
              and evidence_role=%s""",
        (claim_id, source_version_id, block["evidence_role"]),
    ).fetchall()
    if len(rows) > 1:
        raise ClosureError("duplicate context claim-source relation")
    expected = (
        block["evidence_role"],
        block.get("independence_group"),
        block.get("directness"),
        block.get("direction", "context"),
        block.get("locator"),
        block.get("claim_fitness"),
    )
    if rows:
        if tuple(rows[0]) != expected:
            raise ClosureError("existing context claim-source differs")
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
            block.get("independence_group"),
            block.get("directness"),
            block.get("direction", "context"),
            block.get("locator"),
            block.get("notes"),
            block.get("claim_fitness"),
        ),
    )
    return True


def apply_once(
    conn,
    review: dict[str, Any],
    prerequisite_ids: dict[str, dict[str, str]],
) -> dict[str, Any]:
    out: dict[str, Any] = {}
    accepted_rows = [
        row for row in review["candidates"]
        if row.get("disposition") == "ACCEPT_FOR_DISPOSABLE_REHEARSAL"
    ]
    with conn.cursor() as cur:
        for row in accepted_rows:
            key = row["case_key"]
            claim_id = prerequisite_ids[key]["claim_id"]

            context_inserted = False
            context_sv = None
            if row.get("new_context_source"):
                source, version = source_parts(row["new_context_source"])
                context_sv = ensure_source_version(cur, source, version)
                context_inserted = ensure_context_claim_source(
                    cur, claim_id, context_sv, row["new_context_source"]
                )

            locus_id, locus_created = ensure_locus_entity(cur, row["new_locus_entity"])

            source, version = source_parts(row["geometry_source"])
            geometry_sv = ensure_source_version(cur, source, version)
            geometry_id, geometry_inserted = ensure_geometry(
                cur, locus_id, row["geometry"], geometry_sv
            )
            locus_link_inserted = ensure_locus_link(
                cur, claim_id, locus_id, row["locus_link"]
            )

            out[key] = {
                "claim_id": claim_id,
                "locus_spatial_entity_id": locus_id,
                "locus_created": locus_created,
                "geometry_id": geometry_id,
                "geometry_inserted": geometry_inserted,
                "geometry_source_version_id": geometry_sv,
                "context_source_version_id": context_sv,
                "context_claim_source_inserted": context_inserted,
                "locus_link_inserted": locus_link_inserted,
            }
    return out


def assert_delta(before: dict[str, int], after: dict[str, int]) -> dict[str, int]:
    delta = {table: after[table] - before[table] for table in before}
    for table, expected in STRICT_DELTA.items():
        if delta[table] != expected:
            raise ClosureError(f"unexpected tranche-2 delta for {table}: {delta[table]} != {expected}")
    return delta


def verify_semantics(
    conn,
    review: dict[str, Any],
    prerequisite_ids: dict[str, dict[str, str]],
) -> None:
    accepted_rows = [
        row for row in review["candidates"]
        if row.get("disposition") == "ACCEPT_FOR_DISPOSABLE_REHEARSAL"
    ]
    with conn.cursor() as cur:
        for row in accepted_rows:
            claim_id = prerequisite_ids[row["case_key"]]["claim_id"]
            locus = cur.execute(
                """select cel.role_text,se.canonical_name,se.entity_type_code,
                          g.accuracy_status::text,GeometryType(g.geom)
                     from atlas.claim_evidence_locus cel
                     join atlas.spatial_entity se using(spatial_entity_id)
                     join atlas.geometry g using(spatial_entity_id)
                    where cel.claim_id=%s
                      and se.canonical_name=%s
                      and g.geometry_source_native_id=%s""",
                (
                    claim_id,
                    row["new_locus_entity"]["canonical_name"],
                    row["geometry"]["source_native_id"],
                ),
            ).fetchone()
            if locus is None:
                raise ClosureError(f"missing case-linked locus for {row['case_key']}")
            if locus[0] != row["locus_link"]["role_text"]:
                raise ClosureError("locus role drift")
            if locus[1] != row["new_locus_entity"]["canonical_name"]:
                raise ClosureError("locus identity drift")
            if locus[3] != row["geometry"]["accuracy_status"] or locus[4] != "POINT":
                raise ClosureError("locus geometry role/type drift")

        brazil_claim = cur.execute(
            "select claim_id::text from audit.research_case_ingest where case_key=%s",
            (BRAZIL_HOLD,),
        ).fetchone()
        if brazil_claim is not None:
            brazil_links = cur.execute(
                "select count(*) from atlas.claim_evidence_locus where claim_id=%s",
                (brazil_claim[0],),
            ).fetchone()[0]
            if brazil_links:
                raise ClosureError("Brazil HOLD unexpectedly gained a locus")

        claim_ids = [item["claim_id"] for item in prerequisite_ids.values()]
        release_hits = cur.execute(
            "select count(*) from audit.release_claim where claim_id=any(%s::uuid[])",
            (claim_ids,),
        ).fetchone()[0]
        non_null_p = cur.execute(
            """select count(*) from atlas.territorial_practice_claim
                where claim_id=any(%s::uuid[]) and practice_level is not null""",
            (claim_ids,),
        ).fetchone()[0]
        published = cur.execute(
            """select count(*) from atlas.claim
                where claim_id=any(%s::uuid[])
                  and publication_status::text <> 'unpublished'""",
            (claim_ids,),
        ).fetchone()[0]
    if release_hits or non_null_p or published:
        raise ClosureError("tranche-2 rehearsal crossed claim/release/publication boundary")


def replay_is_noop(result: dict[str, Any]) -> bool:
    return all(
        not item.get("locus_created")
        and not item.get("geometry_inserted")
        and not item.get("context_claim_source_inserted")
        and not item.get("locus_link_inserted")
        for item in result.values()
    )


def run(conn, review: dict[str, Any]) -> dict[str, Any]:
    original = counts(conn)
    first = second = delta = prerequisite_ids = None
    try:
        prerequisite_ids = insert_prerequisites(conn)
        closure_before = counts(conn)

        first = apply_once(conn, review, prerequisite_ids)
        closure_after = counts(conn)
        delta = assert_delta(closure_before, closure_after)
        verify_semantics(conn, review, prerequisite_ids)

        second = apply_once(conn, review, prerequisite_ids)
        if counts(conn) != closure_after:
            raise ClosureError("unchanged tranche-2 replay altered tracked counts")
        if not replay_is_noop(second):
            raise ClosureError("unchanged tranche-2 replay was not an exact no-op")
    finally:
        conn.rollback()

    restored = counts(conn)
    conn.rollback()
    if restored != original:
        raise ClosureError("tranche-2 rollback failed to restore original counts")

    return {
        "record_kind": "geometry_closure_tranche_02_rehearsal_receipt",
        "version": 1,
        "issue": 374,
        "mode": "DISPOSABLE_ROLLBACK",
        "prerequisite_case_count": len(ACCEPTED),
        "accepted_geometry_cases": len(ACCEPTED),
        "held_cases": [BRAZIL_HOLD],
        "prerequisite_ids": prerequisite_ids,
        "first_pass": first,
        "second_pass": second,
        "tracked_closure_delta": delta,
        "case_linked_mapped_representations_after_apply": 4,
        "historical_practice_polygons_added": 0,
        "national_proxy_polygons_promoted": 0,
        "claim_delta": 0,
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
    print(json.dumps({
        "issue": 374,
        "mode": "plan_only",
        "accepted_case_keys": list(ACCEPTED),
        "held_case_keys": [BRAZIL_HOLD],
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

    print("GEOMETRY_CLOSURE_TRANCHE_02_REHEARSAL_RECEIPT_BEGIN")
    print(json.dumps(receipt, ensure_ascii=False, indent=2, sort_keys=True))
    print("GEOMETRY_CLOSURE_TRANCHE_02_REHEARSAL_RECEIPT_END")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
