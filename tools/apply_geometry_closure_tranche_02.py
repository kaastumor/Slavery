#!/usr/bin/env python3
"""Apply #374 geometry closure tranche 2 after explicit production authorization.

Default mode is read-only. This production path is fail-closed and adds only
four reviewed case-linked mapped representations. Brazil remains HOLD.

No claim, P-level, release membership, publication status, or serving channel
may change.
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

from tools.rehearse_geometry_closure_tranche_01 import ClosureError, counts
from tools.rehearse_geometry_closure_tranche_02 import (
    ACCEPTED,
    BRAZIL_HOLD,
    REVIEW,
    STRICT_DELTA,
    apply_once,
    load_review,
    replay_is_noop,
    verify_semantics,
)

PLAN = ROOT / "data/research/geometry_reviews/population_100_100_closure_tranche_02_production_plan.json"
RECEIPT = ROOT / "data/research/geometry_reviews/population_100_100_closure_tranche_02_rehearsal_receipt.json"

EXPECTED_PRODUCTION = {
    "overnight-2026-09-27/india/bonded-labour-v2": {
        "claim_id": "1d707382-b0b8-479d-81e3-efcea01c4ab0",
        "spatial_entity_id": "4c0cf106-f55e-4e98-901a-63cd5cce5bc7",
        "canonical_name": "India",
    },
    "overnight-2026-09-27/myanmar/state-forced-labour-v2": {
        "claim_id": "365e6258-f03f-4677-b775-cd5a9f18414a",
        "spatial_entity_id": "91c7f969-f47a-465c-a304-57328b59d052",
        "canonical_name": "Myanmar",
    },
    "overnight-2026-09-27/pakistan/bonded-labour-v2": {
        "claim_id": "47175a77-76bb-4a92-ac3c-cb22b7a8131f",
        "spatial_entity_id": "da4f5a3d-316b-4afb-90e3-53db83af3f10",
        "canonical_name": "Pakistan",
    },
    "post-overnight-2026-09-27/nazi-germany/state-forced-labour-1942-1944-v2": {
        "claim_id": "51063cdb-f485-47c9-9056-e374476632dd",
        "spatial_entity_id": "aba9b942-063a-4b8b-a21b-4232056f81cf",
        "canonical_name": "Nazi Germany",
    },
}

NEW_SOURCE_URLS = (
    "https://www.geonames.org/1258744/closepet.html",
    "https://www.geonames.org/11154185/shadaw.html",
    "https://files.ilo.org/public/english/standards/relm/gb/docs/gb273/myanma8c.htm",
    "https://www.geonames.org/advanced-search.html?q=Lahore&startRow=0",
    "https://www.hrw.org/reports/1995/Pakistan.htm",
    "https://denkmaldatenbank.berlin.de/daobj.php?obj_dok_nr=09045213",
)

NEW_IDENTITIES = (
    "Ramanagaram",
    "Shadaw Township — Daw Taku testimony context",
    "Lahore outskirts brick-kiln evidence context",
    "GBI camp 75/76 Schöneweide",
)


def load_plan(path: Path = PLAN) -> dict[str, Any]:
    value = json.loads(path.read_text(encoding="utf-8"))
    if value.get("record_kind") != "geometry_closure_tranche_02_production_plan":
        raise ClosureError("unexpected production plan")
    if value.get("issue") != 374:
        raise ClosureError("production plan issue drift")
    if value.get("expected_live_delta") != STRICT_DELTA:
        raise ClosureError("production plan delta drift")
    return value


def load_receipt(path: Path = RECEIPT) -> dict[str, Any]:
    value = json.loads(path.read_text(encoding="utf-8"))
    if value.get("record_kind") != "geometry_closure_tranche_02_rehearsal_receipt":
        raise ClosureError("unexpected rehearsal receipt")
    if value.get("workflow_result") != "PASS":
        raise ClosureError("rehearsal CI is not green")
    if value.get("status") != "PASS_DISPOSABLE_ROLLBACK_READY_FOR_EXPLICIT_PRODUCTION_GATE":
        raise ClosureError("rehearsal has not reached production gate")
    if value.get("tracked_closure_delta") != STRICT_DELTA:
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
    if args.production_write_authorized != "ISSUE-374-EXPLICIT":
        raise ClosureError(
            "production apply requires --production-write-authorized ISSUE-374-EXPLICIT"
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


def resolve_production_ids(conn) -> dict[str, dict[str, str]]:
    resolved: dict[str, dict[str, str]] = {}
    with conn.cursor() as cur:
        for case_key, expected in EXPECTED_PRODUCTION.items():
            row = cur.execute(
                """select r.claim_id::text,
                          t.spatial_entity_id::text,
                          se.canonical_name,
                          c.review_status::text,
                          c.publication_status::text,
                          t.practice_level::text
                     from audit.research_case_ingest r
                     join atlas.claim c using(claim_id)
                     join atlas.territorial_practice_claim t using(claim_id)
                     join atlas.spatial_entity se using(spatial_entity_id)
                    where r.case_key=%s""",
                (case_key,),
            ).fetchone()
            if row is None:
                raise ClosureError(f"missing live production case {case_key}")
            actual = {
                "claim_id": row[0],
                "spatial_entity_id": row[1],
                "canonical_name": row[2],
            }
            for key in ("claim_id", "spatial_entity_id", "canonical_name"):
                if actual[key] != expected[key]:
                    raise ClosureError(f"live identity drift for {case_key}: {key}")
            if (row[3], row[4], row[5]) != ("reviewed", "unpublished", None):
                raise ClosureError(f"live claim state drift for {case_key}")
            resolved[case_key] = {
                "claim_id": row[0],
                "target_spatial_entity_id": row[1],
                "target_canonical_name": row[2],
            }
    return resolved


def live_preflight(
    conn,
    prerequisite_ids: dict[str, dict[str, str]],
) -> dict[str, Any]:
    claim_ids = [item["claim_id"] for item in prerequisite_ids.values()]
    with conn.cursor() as cur:
        identity_hits = cur.execute(
            "select count(*) from atlas.spatial_entity where canonical_name=any(%s)",
            (list(NEW_IDENTITIES),),
        ).fetchone()[0]
        source_hits = cur.execute(
            "select count(*) from atlas.source_version where url_or_identifier=any(%s)",
            (list(NEW_SOURCE_URLS),),
        ).fetchone()[0]
        locus_links = cur.execute(
            "select count(*) from atlas.claim_evidence_locus where claim_id=any(%s::uuid[])",
            (claim_ids,),
        ).fetchone()[0]
        release_hits = cur.execute(
            "select count(*) from audit.release_claim where claim_id=any(%s::uuid[])",
            (claim_ids,),
        ).fetchone()[0]
        brazil_row = cur.execute(
            """select c.review_status::text,c.publication_status::text,t.practice_level::text,
                      (select count(*) from atlas.claim_evidence_locus cel
                        where cel.claim_id=c.claim_id)
                 from audit.research_case_ingest r
                 join atlas.claim c using(claim_id)
                 join atlas.territorial_practice_claim t using(claim_id)
                where r.case_key=%s""",
            (BRAZIL_HOLD,),
        ).fetchone()
        india_hrw = cur.execute(
            """select source_version_id::text from atlas.source_version
                where url_or_identifier=%s""",
            (
                "https://www.hrw.org/report/2003/01/22/small-change/bonded-child-labor-indias-silk-industry",
            ),
        ).fetchall()
        channel = cur.execute(
            """select channel_code,release_version from audit.release_channel
                where channel_code='public_mvp_preview'"""
        ).fetchone()

    if identity_hits != 0:
        raise ClosureError("one or more tranche-2 locus identities already exist")
    if source_hits != 0:
        raise ClosureError("one or more tranche-2 new source URLs already exist")
    if locus_links != 0:
        raise ClosureError("one or more accepted production claims already have locus links")
    if release_hits != 0:
        raise ClosureError("accepted current-method claims unexpectedly entered release membership")
    if brazil_row is None or brazil_row != ("reviewed", "unpublished", None, 0):
        raise ClosureError("Brazil HOLD state drift")
    if len(india_hrw) != 1 or india_hrw[0][0] != "43eaef18-4b5e-489c-84a5-5c035d433cfc":
        raise ClosureError("India HRW source-version reuse drift")

    return {
        "candidate_identity_hits": identity_hits,
        "new_source_url_hits": source_hits,
        "existing_locus_links": locus_links,
        "release_membership_hits": release_hits,
        "brazil_hold_intact": True,
        "india_hrw_reused_source_version_id": india_hrw[0][0],
        "release_channel": list(channel) if channel else None,
    }


def assert_live_delta(before: dict[str, int], after: dict[str, int]) -> dict[str, int]:
    delta = {table: after[table] - before[table] for table in before}
    for table, expected in STRICT_DELTA.items():
        if delta[table] != expected:
            raise ClosureError(
                f"unexpected production delta for {table}: {delta[table]} != {expected}"
            )
    return delta


def run_production(
    conn,
    review: dict[str, Any],
    *,
    git_revision: str,
) -> dict[str, Any]:
    prerequisite_ids = resolve_production_ids(conn)
    preflight = live_preflight(conn, prerequisite_ids)
    before = counts(conn)

    first = apply_once(conn, review, prerequisite_ids)
    after = counts(conn)
    delta = assert_live_delta(before, after)
    verify_semantics(conn, review, prerequisite_ids)

    second = apply_once(conn, review, prerequisite_ids)
    if counts(conn) != after:
        raise ClosureError("unchanged production replay altered tracked counts")
    if not replay_is_noop(second):
        raise ClosureError("unchanged production replay was not an exact no-op")

    return {
        "record_kind": "geometry_closure_tranche_02_production_receipt",
        "version": 1,
        "issue": 374,
        "mode": "PRODUCTION_COMMIT",
        "git_revision": git_revision,
        "preflight": preflight,
        "first_pass": first,
        "second_pass": second,
        "before_counts": before,
        "after_counts": after,
        "tracked_closure_delta": delta,
        "mapped_representations_added": 4,
        "held_cases_unchanged": [BRAZIL_HOLD],
        "historical_practice_polygons_added": 0,
        "national_proxy_polygons_promoted": 0,
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
    rehearsal = load_receipt()

    print(json.dumps({
        "issue": 374,
        "mode": "plan_only",
        "rehearsal_run_id": rehearsal["workflow_run_id"],
        "accepted_case_keys": list(ACCEPTED),
        "held_case_keys": [BRAZIL_HOLD],
        "expected_live_delta": STRICT_DELTA,
        "production_write_authorized": False,
        "release_or_public_cutover_authorized": False,
    }, indent=2, sort_keys=True))

    if not args.apply:
        print("DRY RUN: no database changes made")
        return 0
    if not args.dsn:
        parser.error("--dsn or DATABASE_URL is required with --apply")

    current = require_authority(args)

    import psycopg
    with psycopg.connect(args.dsn, autocommit=False) as conn:
        try:
            receipt = run_production(conn, review, git_revision=current)
            conn.commit()
        except Exception:
            conn.rollback()
            raise

    print("GEOMETRY_CLOSURE_TRANCHE_02_PRODUCTION_RECEIPT_BEGIN")
    print(json.dumps(receipt, ensure_ascii=False, indent=2, sort_keys=True))
    print("GEOMETRY_CLOSURE_TRANCHE_02_PRODUCTION_RECEIPT_END")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
