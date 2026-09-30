#!/usr/bin/env python3
"""Apply #379 released ISIL/Yazidi Sinjar evidence-locus recovery.

Default mode is read-only. The production path is fail-closed behind:
- a successful disposable rehearsal receipt bound to the exact review blob;
- ATLAS_GEOMETRY_WRITE_AUTHORIZED=1;
- --production-write-authorized ISSUE-379-EXPLICIT;
- an exact checked-out git revision matching --expected-main-sha;
- fresh live identity/source/locus/release-membership preconditions.

This tool adds one evidence-locus point and two claim-locus links only.
It must not add or alter historical claims, claim-source evidence, P-levels,
release membership, release geometry membership, publication status, or the
public serving channel.
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

from tools.rehearse_geometry_closure_tranche_01 import ClosureError
from tools.rehearse_released_geo_recovery_tranche_03 import (
    REVIEW,
    STRICT_DELTA,
    TARGET_SPATIAL_ID,
    ENSLAVEMENT_CLAIM,
    SEXUAL_SLAVERY_CLAIM,
    CLAIMS,
    UNITAD_SOURCE_VERSION_ID,
    RELEASE_VERSION,
    apply_once,
    counts,
    load_review,
    replay_is_noop,
    verify_semantics,
)

PLAN = ROOT / "data/research/geometry_reviews/population_100_100_released_geo_tranche_03_production_plan.json"
RECEIPT = ROOT / "data/research/geometry_reviews/population_100_100_released_geo_tranche_03_rehearsal_receipt.json"

EXPECTED_REVIEW_BLOB = "248067822dcbc1d5e18c06c90bb056209d3c6a18"
EXPECTED_UNITAD_SOURCE_ID = "062f2f6c-fd64-5cfb-8825-d04c88503f7c"
EXPECTED_TARGET_NAME = "Iraq/Syria under ISIL, especially Yazidi population from 2014"
SINJAR_ENTITY_NAME = "Sinjar town — Yazidi capture/holding locus"
SINJAR_GEOMETRY_URL = "https://www.geonames.org/448149/sinjar.html"

EXPECTED_RELEASE_OBJECTS = {
    ENSLAVEMENT_CLAIM: "fdbcae720fcfc2030bf168d09c6458fa4bd6e9b47249fe6021bdcef9e381deed",
    SEXUAL_SLAVERY_CLAIM: "f6a7143cf1cfd17688b23716ab67708f6e20d9e71e0c33fed3d0fe44e46ce69f",
}

EXPECTED_PRACTICE_TYPES = {
    ENSLAVEMENT_CLAIM: "slavery_enslavement",
    SEXUAL_SLAVERY_CLAIM: "sexual_slavery",
}


def git_blob_sha(path: Path) -> str:
    try:
        rel = path.relative_to(ROOT)
        return subprocess.check_output(
            ["git", "hash-object", str(rel)],
            cwd=ROOT,
            text=True,
            stderr=subprocess.DEVNULL,
        ).strip()
    except (OSError, subprocess.CalledProcessError, ValueError) as exc:
        raise ClosureError(f"cannot verify git blob identity for {path}") from exc


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


def load_plan(path: Path = PLAN) -> dict[str, Any]:
    value = json.loads(path.read_text(encoding="utf-8"))
    if value.get("record_kind") != "released_geo_recovery_tranche_03_production_plan":
        raise ClosureError("unexpected #379 production plan")
    if value.get("issue") != 379:
        raise ClosureError("production plan issue drift")
    if value.get("status") != "READY_FOR_EXPLICIT_PRODUCTION_WRITE_GATE_AFTER_PLAN_CI":
        raise ClosureError("production plan is not at explicit write gate")
    if value.get("review_git_blob_sha") != EXPECTED_REVIEW_BLOB:
        raise ClosureError("production plan review-blob constant drift")
    if value.get("review_git_blob_sha") != git_blob_sha(REVIEW):
        raise ClosureError("production plan is not bound to the current review blob")
    if value.get("expected_live_delta") != STRICT_DELTA:
        raise ClosureError("production plan delta drift")
    return value


def load_rehearsal_receipt(path: Path = RECEIPT) -> dict[str, Any]:
    value = json.loads(path.read_text(encoding="utf-8"))
    if value.get("record_kind") != "released_geo_recovery_tranche_03_rehearsal_receipt":
        raise ClosureError("unexpected #379 rehearsal receipt")
    if value.get("issue") != 379:
        raise ClosureError("rehearsal receipt issue drift")
    if value.get("workflow_result") != "PASS":
        raise ClosureError("rehearsal CI is not green")
    if value.get("status") != "PASS_DISPOSABLE_ROLLBACK_READY_FOR_EXPLICIT_PRODUCTION_GATE":
        raise ClosureError("rehearsal has not reached the explicit production gate")
    if value.get("review_git_blob_sha") != EXPECTED_REVIEW_BLOB:
        raise ClosureError("rehearsal receipt review-blob constant drift")
    if value.get("review_git_blob_sha") != git_blob_sha(REVIEW):
        raise ClosureError("rehearsal receipt is not bound to the current review blob")
    if value.get("tracked_closure_delta") != STRICT_DELTA:
        raise ClosureError("rehearsal delta differs from production contract")
    if not value.get("rollback_restored_counts"):
        raise ClosureError("rehearsal rollback did not restore counts")
    return value


def require_authority(args: argparse.Namespace) -> str:
    if args.production_write_authorized != "ISSUE-379-EXPLICIT":
        raise ClosureError(
            "production apply requires --production-write-authorized ISSUE-379-EXPLICIT"
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


def live_preflight(conn) -> dict[str, Any]:
    with conn.cursor() as cur:
        target = cur.execute(
            """select canonical_name,display_name,review_status::text
                 from atlas.spatial_entity
                where spatial_entity_id=%s""",
            (TARGET_SPATIAL_ID,),
        ).fetchone()
        if target is None:
            raise ClosureError("released ISIL/Yazidi target spatial entity is missing")
        if target[0] != EXPECTED_TARGET_NAME or target[2] != "reviewed":
            raise ClosureError("released target spatial identity/review state drift")

        claim_rows = cur.execute(
            """select c.claim_id::text,t.practice_type_code,c.review_status::text,
                      c.publication_status::text,t.practice_level::text,
                      t.spatial_entity_id::text
                 from atlas.claim c
                 join atlas.territorial_practice_claim t on t.claim_id=c.claim_id
                where c.claim_id=any(%s::uuid[])
                order by c.claim_id::text""",
            (list(CLAIMS),),
        ).fetchall()
        if len(claim_rows) != 2:
            raise ClosureError("expected exactly two released ISIL/Yazidi claim facets")
        for claim_id, practice_type, review_status, publication_status, p_level, spatial_id in claim_rows:
            if practice_type != EXPECTED_PRACTICE_TYPES[claim_id]:
                raise ClosureError(f"practice-type drift for {claim_id}")
            if (review_status, publication_status, p_level) != ("reviewed", "unpublished", None):
                raise ClosureError(f"claim-state drift for {claim_id}")
            if spatial_id != TARGET_SPATIAL_ID:
                raise ClosureError(f"target spatial identity drift for {claim_id}")

        unitad = cur.execute(
            """select source_version_id::text,source_id::text,url_or_identifier
                 from atlas.source_version
                where source_version_id=%s""",
            (UNITAD_SOURCE_VERSION_ID,),
        ).fetchone()
        if unitad != (
            UNITAD_SOURCE_VERSION_ID,
            EXPECTED_UNITAD_SOURCE_ID,
            "https://www.unitad.un.org/sites/www.unitad.un.org/files/sinjar_brief_public_updated_0_2.pdf",
        ):
            raise ClosureError("UNITAD source-version identity drift")

        historical_links = cur.execute(
            """select claim_id::text,source_version_id::text,count(*)
                 from atlas.claim_source
                where claim_id=any(%s::uuid[])
                group by claim_id,source_version_id
                order by claim_id::text""",
            (list(CLAIMS),),
        ).fetchall()
        if historical_links != [
            (ENSLAVEMENT_CLAIM, UNITAD_SOURCE_VERSION_ID, 1),
            (SEXUAL_SLAVERY_CLAIM, UNITAD_SOURCE_VERSION_ID, 1),
        ]:
            raise ClosureError("historical claim-source linkage drift")

        sinjar_entity_hits = cur.execute(
            "select count(*) from atlas.spatial_entity where canonical_name=%s",
            (SINJAR_ENTITY_NAME,),
        ).fetchone()[0]
        sinjar_source_hits = cur.execute(
            "select count(*) from atlas.source_version where url_or_identifier=%s",
            (SINJAR_GEOMETRY_URL,),
        ).fetchone()[0]
        locus_links = cur.execute(
            "select count(*) from atlas.claim_evidence_locus where claim_id=any(%s::uuid[])",
            (list(CLAIMS),),
        ).fetchone()[0]
        target_geometry_rows = cur.execute(
            "select count(*) from atlas.geometry where spatial_entity_id=%s",
            (TARGET_SPATIAL_ID,),
        ).fetchone()[0]

        membership = cur.execute(
            """select claim_id::text,object_sha256,capture_status
                 from audit.release_claim
                where release_version=%s
                  and claim_id=any(%s::uuid[])
                order by claim_id::text""",
            (RELEASE_VERSION, list(CLAIMS)),
        ).fetchall()
        expected_membership = [
            (
                ENSLAVEMENT_CLAIM,
                EXPECTED_RELEASE_OBJECTS[ENSLAVEMENT_CLAIM],
                "captured_at_release",
            ),
            (
                SEXUAL_SLAVERY_CLAIM,
                EXPECTED_RELEASE_OBJECTS[SEXUAL_SLAVERY_CLAIM],
                "captured_at_release",
            ),
        ]
        if membership != expected_membership:
            raise ClosureError("immutable v0.8.1 membership/object identity drift")

        manifest_status = cur.execute(
            "select status from audit.release_manifest where release_version=%s",
            (RELEASE_VERSION,),
        ).fetchone()
        if manifest_status != ("published",):
            raise ClosureError("v0.8.1 release manifest is not published")

        release_target_geometry = cur.execute(
            """select count(*)
                 from audit.release_geometry rg
                 join atlas.geometry g on g.geometry_id=rg.geometry_id
                where rg.release_version=%s
                  and g.spatial_entity_id=%s""",
            (RELEASE_VERSION, TARGET_SPATIAL_ID),
        ).fetchone()[0]

        channel = cur.execute(
            """select channel_code,release_version
                 from audit.release_channel
                where channel_code='public_mvp_preview'"""
        ).fetchone()
        if channel != ("public_mvp_preview", "v0.8.1-public-mvp-v2"):
            raise ClosureError("public serving channel drift")

    if sinjar_entity_hits != 0:
        raise ClosureError("Sinjar locus identity collision")
    if sinjar_source_hits != 0:
        raise ClosureError("Sinjar GeoNames source-version collision")
    if locus_links != 0:
        raise ClosureError("released ISIL/Yazidi facets already have locus links")
    if target_geometry_rows != 0:
        raise ClosureError("broad ISIL/Iraq-Syria target already has geometry")
    if release_target_geometry != 0:
        raise ClosureError("broad ISIL/Iraq-Syria target unexpectedly has release geometry")

    return {
        "target_identity": TARGET_SPATIAL_ID,
        "claim_ids": list(CLAIMS),
        "unitad_source_version_id": UNITAD_SOURCE_VERSION_ID,
        "sinjar_entity_hits": sinjar_entity_hits,
        "sinjar_geometry_source_hits": sinjar_source_hits,
        "existing_locus_links": locus_links,
        "broad_target_geometry_rows": target_geometry_rows,
        "release_membership_hits": len(membership),
        "release_target_geometry_rows": release_target_geometry,
        "release_manifest_status": manifest_status[0],
        "serving_channel": list(channel),
    }


def assert_live_delta(before: dict[str, int], after: dict[str, int]) -> dict[str, int]:
    delta = {table: after[table] - before[table] for table in before}
    for table, expected in STRICT_DELTA.items():
        if delta[table] != expected:
            raise ClosureError(
                f"unexpected #379 production delta for {table}: {delta[table]} != {expected}"
            )
    return delta


def run_production(
    conn,
    review: dict[str, Any],
    *,
    git_revision: str,
) -> dict[str, Any]:
    preflight = live_preflight(conn)
    before = counts(conn)

    first = apply_once(conn, review)
    after = counts(conn)
    delta = assert_live_delta(before, after)
    verify_semantics(conn, review, first)

    second = apply_once(conn, review)
    if counts(conn) != after:
        raise ClosureError("unchanged #379 production replay altered tracked counts")
    if not replay_is_noop(second):
        raise ClosureError("unchanged #379 production replay was not an exact no-op")

    # Re-run the immutable/source/channel preconditions that should remain true
    # except for the three intentionally added collision-sensitive objects.
    with conn.cursor() as cur:
        historical_links = cur.execute(
            """select claim_id::text,source_version_id::text,count(*)
                 from atlas.claim_source
                where claim_id=any(%s::uuid[])
                group by claim_id,source_version_id
                order by claim_id::text""",
            (list(CLAIMS),),
        ).fetchall()
        if historical_links != [
            (ENSLAVEMENT_CLAIM, UNITAD_SOURCE_VERSION_ID, 1),
            (SEXUAL_SLAVERY_CLAIM, UNITAD_SOURCE_VERSION_ID, 1),
        ]:
            raise ClosureError("production augmentation altered historical claim-source evidence")

        membership = cur.execute(
            """select claim_id::text,object_sha256,capture_status
                 from audit.release_claim
                where release_version=%s
                  and claim_id=any(%s::uuid[])
                order by claim_id::text""",
            (RELEASE_VERSION, list(CLAIMS)),
        ).fetchall()
        if membership != [
            (
                ENSLAVEMENT_CLAIM,
                EXPECTED_RELEASE_OBJECTS[ENSLAVEMENT_CLAIM],
                "captured_at_release",
            ),
            (
                SEXUAL_SLAVERY_CLAIM,
                EXPECTED_RELEASE_OBJECTS[SEXUAL_SLAVERY_CLAIM],
                "captured_at_release",
            ),
        ]:
            raise ClosureError("production augmentation altered immutable release membership")

        channel = cur.execute(
            """select channel_code,release_version
                 from audit.release_channel
                where channel_code='public_mvp_preview'"""
        ).fetchone()
        if channel != ("public_mvp_preview", "v0.8.1-public-mvp-v2"):
            raise ClosureError("production augmentation altered public serving channel")

    return {
        "record_kind": "released_geo_recovery_tranche_03_production_receipt",
        "version": 1,
        "issue": 379,
        "mode": "PRODUCTION_COMMIT",
        "git_revision": git_revision,
        "preflight": preflight,
        "first_pass": first,
        "second_pass": second,
        "before_counts": before,
        "after_counts": after,
        "tracked_closure_delta": delta,
        "released_case_linked_mapped_representations_added": 1,
        "claim_evidence_locus_links_added": 2,
        "historical_claim_source_delta": 0,
        "historical_practice_polygons_added": 0,
        "broad_target_geometry_delta": 0,
        "claim_delta": 0,
        "release_membership_delta": 0,
        "release_geometry_delta": 0,
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

    print(json.dumps({
        "issue": 379,
        "mode": "plan_only",
        "review_blob_sha": plan["review_git_blob_sha"],
        "rehearsal_run_id": rehearsal["workflow_run_id"],
        "released_claim_ids": list(CLAIMS),
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

    print("RELEASED_GEO_RECOVERY_TRANCHE_03_PRODUCTION_RECEIPT_BEGIN")
    print(json.dumps(receipt, ensure_ascii=False, indent=2, sort_keys=True))
    print("RELEASED_GEO_RECOVERY_TRANCHE_03_PRODUCTION_RECEIPT_END")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
