#!/usr/bin/env python3
"""Apply #370 geometry closure tranche 1 after explicit production authorization.

Default mode is read-only. The production path is fail-closed behind:
- the successful disposable-rehearsal receipt;
- ATLAS_GEOMETRY_WRITE_AUTHORIZED=1;
- --production-write-authorized ISSUE-370-EXPLICIT;
- an exact checked-out git revision matching --expected-main-sha;
- clean live collision/precondition checks.

This tool adds mapped representations only. It does not add claims, P-levels,
release membership, publication changes, or serving-channel changes.
"""
from __future__ import annotations

import argparse
import json
import os
from pathlib import Path
import subprocess
import sys
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from tools.rehearse_geometry_closure_tranche_01 import (
    ClosureError,
    REVIEW,
    STRICT_DELTA,
    apply_once,
    assert_delta,
    counts,
    load_review,
    verify_claims,
    verify_semantics,
)

PLAN = ROOT / "data/research/geometry_reviews/population_100_100_closure_tranche_01_production_plan.json"
RECEIPT = ROOT / "data/research/geometry_reviews/population_100_100_closure_tranche_01_rehearsal_receipt.json"

CLOSURE_SOURCE_URLS = (
    "https://whc.unesco.org/en/list/1278/maps/",
    "https://www.persee.fr/doc/cea_0008-0055_1989_num_29_114_1643",
    "https://www.geonames.org/2394092/godome.html",
    "https://geographic.org/geographic_names/name.php?c=mali&fid=3915&uni=-1595671",
)

EXPECTED_RELEASE_MEMBERSHIPS = [
    ("v0.8.2", "1567b140-eeba-4b32-b37d-f31dcb35e1dd", "ae657d3350163b988ef9a502bf1202112ec807f2ccce410053c7b7f1b10df164", "captured_at_release"),
    ("v0.8.2", "9d1ccd8e-ba6d-4dbe-aea8-6d3f2b98942c", "8d6c0fd554a4d5b74f2681086a2c0900b5f5d407c19499d81b4dbc85ccfffd3b", "captured_at_release"),
    ("v0.8.2", "9f5397c7-8b7b-4218-ad10-b85abf56eae8", "7a5d4fe4af98b4635d69836b26db9c5a7dd43c58eeb951b0025af10542c2b7f9", "captured_at_release"),
    ("v0.8.2-public-mvp-v1", "1567b140-eeba-4b32-b37d-f31dcb35e1dd", "ae657d3350163b988ef9a502bf1202112ec807f2ccce410053c7b7f1b10df164", "captured_at_release"),
    ("v0.8.2-public-mvp-v1", "9d1ccd8e-ba6d-4dbe-aea8-6d3f2b98942c", "8d6c0fd554a4d5b74f2681086a2c0900b5f5d407c19499d81b4dbc85ccfffd3b", "captured_at_release"),
    ("v0.8.2-public-mvp-v1", "9f5397c7-8b7b-4218-ad10-b85abf56eae8", "7a5d4fe4af98b4635d69836b26db9c5a7dd43c58eeb951b0025af10542c2b7f9", "captured_at_release"),
]


def load_plan(path: Path = PLAN) -> dict[str, Any]:
    value = json.loads(path.read_text(encoding="utf-8"))
    if value.get("record_kind") != "geometry_closure_tranche_01_production_plan":
        raise ClosureError("unexpected production plan")
    if value.get("issue") != 370:
        raise ClosureError("production plan issue drift")
    expected = value.get("expected_live_delta") or {}
    if expected != STRICT_DELTA:
        raise ClosureError("production plan delta drift")
    return value


def load_rehearsal_receipt(path: Path = RECEIPT) -> dict[str, Any]:
    value = json.loads(path.read_text(encoding="utf-8"))
    if value.get("record_kind") != "geometry_closure_tranche_01_rehearsal_receipt":
        raise ClosureError("unexpected rehearsal receipt")
    if value.get("workflow_result") != "PASS":
        raise ClosureError("rehearsal CI is not green")
    if value.get("status") != "PASS_DISPOSABLE_ROLLBACK_READY_FOR_EXPLICIT_PRODUCTION_GATE":
        raise ClosureError("rehearsal has not reached the production gate")
    if value.get("tracked_table_delta") != STRICT_DELTA:
        raise ClosureError("rehearsal delta differs from production contract")
    if not value.get("rollback_restored_counts"):
        raise ClosureError("rehearsal rollback did not restore counts")
    return value


def git_head() -> str:
    try:
        return subprocess.check_output(
            ["git", "rev-parse", "HEAD"],
            cwd=ROOT,
            text=True,
            stderr=subprocess.DEVNULL,
        ).strip()
    except (OSError, subprocess.CalledProcessError) as exc:
        raise ClosureError("cannot verify checked-out git revision") from exc


def require_authority(args: argparse.Namespace) -> str:
    if args.production_write_authorized != "ISSUE-370-EXPLICIT":
        raise ClosureError(
            "production apply requires --production-write-authorized ISSUE-370-EXPLICIT"
        )
    if os.environ.get("ATLAS_GEOMETRY_WRITE_AUTHORIZED") != "1":
        raise ClosureError("production apply requires ATLAS_GEOMETRY_WRITE_AUTHORIZED=1")
    if not args.expected_main_sha:
        raise ClosureError("production apply requires --expected-main-sha")
    current = git_head()
    if current != args.expected_main_sha:
        raise ClosureError(
            f"checked-out revision {current} does not match expected main {args.expected_main_sha}"
        )
    return current


def verify_exact_production_ids(
    prerequisite_ids: dict[str, dict[str, str]],
    plan: dict[str, Any],
) -> None:
    expected = {
        row["case_key"]: (
            row["production_claim_id"],
            row["production_spatial_entity_id"],
        )
        for row in plan["production_cases"]
    }
    for case_key, resolved in prerequisite_ids.items():
        wanted = expected.get(case_key)
        if wanted is None:
            raise ClosureError(f"unexpected production case {case_key}")
        actual = (resolved["claim_id"], resolved["spatial_entity_id"])
        if actual != wanted:
            raise ClosureError(
                f"live production identity drift for {case_key}: {actual} != {wanted}"
            )


def live_preflight(conn, prerequisite_ids: dict[str, dict[str, str]]) -> dict[str, Any]:
    dahomey = prerequisite_ids[
        "production-batch-2026-09-29/dahomey/royal-captive-allocation-sale-1727-v1"
    ]
    goryeo = prerequisite_ids[
        "production-batch-2026-09-29/goryeo/nobi-status-review-0956-v1"
    ]
    taghaza = prerequisite_ids[
        "production-batch-2026-09-29/taghaza/slave-salt-mining-1352-v1"
    ]

    with conn.cursor() as cur:
        jakin = cur.execute(
            "select count(*) from atlas.spatial_entity where canonical_name='Jakin (Godomey)'"
        ).fetchone()[0]
        source_hits = cur.execute(
            "select count(*) from atlas.source_version where url_or_identifier=any(%s)",
            (list(CLOSURE_SOURCE_URLS),),
        ).fetchone()[0]
        goryeo_geom = cur.execute(
            """select count(*) from atlas.geometry
                where spatial_entity_id=%s
                  and geometry_source_native_id='UNESCO WHC 1278rev-001'""",
            (goryeo["spatial_entity_id"],),
        ).fetchone()[0]
        taghaza_geom = cur.execute(
            """select count(*) from atlas.geometry
                where spatial_entity_id=%s
                  and geometry_source_native_id like 'NGA UFI -1075410%%'""",
            (taghaza["spatial_entity_id"],),
        ).fetchone()[0]
        dahomey_loci = cur.execute(
            "select count(*) from atlas.claim_evidence_locus where claim_id=%s",
            (dahomey["claim_id"],),
        ).fetchone()[0]
        dahomey_unresolved = cur.execute(
            """select count(*) from atlas.geometry
                where spatial_entity_id=%s
                  and accuracy_status='unresolved'
                  and geom is null""",
            (dahomey["spatial_entity_id"],),
        ).fetchone()[0]
        channel = cur.execute(
            """select channel_code,release_version
                 from audit.release_channel
                where channel_code='public_mvp_preview'"""
        ).fetchone()
        release_memberships = cur.execute(
            """select release_version,claim_id::text,object_sha256,capture_status
                 from audit.release_claim
                where claim_id=any(%s::uuid[])
                order by release_version,claim_id::text""",
            ([item["claim_id"] for item in prerequisite_ids.values()],),
        ).fetchall()

    observed = {
        "jakin_entity_hits": jakin,
        "closure_source_url_hits": source_hits,
        "goryeo_geometry_hits": goryeo_geom,
        "taghaza_geometry_hits": taghaza_geom,
        "dahomey_locus_links": dahomey_loci,
        "dahomey_unresolved_geometry_rows": dahomey_unresolved,
        "release_channel": list(channel) if channel else None,
        "release_memberships": release_memberships,
    }
    expected = {
        "jakin_entity_hits": 0,
        "closure_source_url_hits": 0,
        "goryeo_geometry_hits": 0,
        "taghaza_geometry_hits": 0,
        "dahomey_locus_links": 0,
        "dahomey_unresolved_geometry_rows": 1,
    }
    for key, wanted in expected.items():
        if observed[key] != wanted:
            raise ClosureError(
                f"live preflight drift for {key}: {observed[key]} != {wanted}"
            )
    if channel != ("public_mvp_preview", "v0.8.2-public-mvp-v1"):
        raise ClosureError(f"public serving channel drift: {channel}")
    if release_memberships != EXPECTED_RELEASE_MEMBERSHIPS:
        raise ClosureError(
            "v0.8.2 and serving membership/object identities drifted"
        )
    return observed


def no_op_replay_ok(result: dict[str, Any]) -> bool:
    for item in result.values():
        if (
            item.get("geometry_inserted")
            or item.get("claim_source_inserted")
            or item.get("locus_link_inserted")
        ):
            return False
    return True


def run_production(
    conn,
    review: dict[str, Any],
    plan: dict[str, Any],
    *,
    git_revision: str,
) -> dict[str, Any]:
    prerequisite_ids = verify_claims(conn)
    verify_exact_production_ids(prerequisite_ids, plan)
    preflight = live_preflight(conn, prerequisite_ids)
    before = counts(conn)

    first = apply_once(conn, review, prerequisite_ids)
    after_first = counts(conn)
    delta = assert_delta(before, after_first)
    verify_semantics(
        conn,
        prerequisite_ids,
        expected_release_memberships=EXPECTED_RELEASE_MEMBERSHIPS,
    )

    second = apply_once(conn, review, prerequisite_ids)
    if counts(conn) != after_first:
        raise ClosureError("unchanged production replay altered tracked counts")
    if not no_op_replay_ok(second):
        raise ClosureError("unchanged production replay was not an exact no-op")

    claim_ids = [item["claim_id"] for item in prerequisite_ids.values()]
    with conn.cursor() as cur:
        bad_publication = cur.execute(
            """select count(*) from atlas.claim
                where claim_id=any(%s::uuid[])
                  and publication_status::text <> 'unpublished'""",
            (claim_ids,),
        ).fetchone()[0]
        bad_p = cur.execute(
            """select count(*) from atlas.territorial_practice_claim
                where claim_id=any(%s::uuid[]) and practice_level is not null""",
            (claim_ids,),
        ).fetchone()[0]
    if bad_publication:
        raise ClosureError("geometry closure changed claim publication state")
    if bad_p:
        raise ClosureError("geometry closure introduced a P-level")

    return {
        "record_kind": "geometry_closure_tranche_01_production_receipt",
        "version": 1,
        "issue": 370,
        "mode": "PRODUCTION_COMMIT",
        "git_revision": git_revision,
        "preflight": preflight,
        "first_pass": first,
        "second_pass": second,
        "before_counts": before,
        "after_counts": after_first,
        "tracked_table_delta": delta,
        "mapped_representations_added": 3,
        "historical_practice_polygons_added": 0,
        "claim_delta": 0,
        "release_membership_delta": 0,
        "serving_channel_delta": 0,
        "publication_changes": 0,
        "p_level_changes": 0,
    }


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--dsn", default=os.environ.get("DATABASE_URL", ""))
    parser.add_argument("--apply", action="store_true")
    parser.add_argument("--production-write-authorized")
    parser.add_argument("--expected-main-sha")
    args = parser.parse_args()

    review = load_review(REVIEW)
    plan = load_plan()
    rehearsal = load_rehearsal_receipt()

    dry = {
        "issue": 370,
        "mode": "plan_only",
        "rehearsal_run_id": rehearsal["workflow_run_id"],
        "candidates": [row["case_key"] for row in review["candidates"]],
        "expected_live_delta": STRICT_DELTA,
        "production_write_authorized": False,
        "release_or_public_cutover_authorized": False,
    }
    print(json.dumps(dry, ensure_ascii=False, indent=2, sort_keys=True))
    if not args.apply:
        print("DRY RUN: no database changes made")
        return 0
    if not args.dsn:
        parser.error("--dsn or DATABASE_URL is required with --apply")

    current = require_authority(args)

    import psycopg
    with psycopg.connect(args.dsn, autocommit=False) as conn:
        try:
            receipt = run_production(
                conn,
                review,
                plan,
                git_revision=current,
            )
            conn.commit()
        except Exception:
            conn.rollback()
            raise

    print("GEOMETRY_CLOSURE_PRODUCTION_RECEIPT_BEGIN")
    print(json.dumps(receipt, ensure_ascii=False, indent=2, sort_keys=True))
    print("GEOMETRY_CLOSURE_PRODUCTION_RECEIPT_END")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
