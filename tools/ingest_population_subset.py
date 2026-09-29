#!/usr/bin/env python3
"""Validate and atomically ingest the #360 accepted population subset.

Default mode is read-only planning. --apply requires either:
- --disposable-test-db with CI=true, in which case the transaction is always rolled back; or
- explicit production authorization flags plus ATLAS_PRODUCTION_WRITE_AUTHORIZED=1.

The production path inserts reviewed/unpublished candidates only. It never adds
release membership, publishes claims, or moves a serving channel.
"""
from __future__ import annotations

import argparse
import json
import os
from pathlib import Path
import sys
from urllib.parse import urlparse
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from tools.add_research_case import (
    case_content_sha256,
    insert_case as insert_territorial_case,
    load_spec as load_territorial_spec,
)
from tools.add_legal_event_case import (
    content_sha256 as legal_content_sha256,
    insert_case as insert_legal_case,
    load_spec as load_legal_spec,
)

MANIFEST = ROOT / "data/research/recovery/production_batch_2026_09_29/accepted_subset_manifest.json"
EXPECTED_ACCEPTED = 12
EXPECTED_HELD = 11

TRACKED_TABLES = (
    "atlas.spatial_entity",
    "atlas.claim",
    "atlas.legal_event",
    "atlas.territorial_practice_claim",
    "atlas.source",
    "atlas.source_version",
    "atlas.claim_source",
    "atlas.geometry",
    "audit.research_target",
    "audit.research_target_result",
    "audit.research_target_source",
    "audit.research_target_claim",
    "audit.research_target_review",
    "audit.research_case_ingest",
    "audit.release_claim",
    "audit.release_channel",
)

STRICT_DELTAS = {
    "atlas.spatial_entity": 12,
    "atlas.claim": 12,
    "atlas.legal_event": 1,
    "atlas.territorial_practice_claim": 11,
    "atlas.claim_source": 20,
    "atlas.geometry": 10,
    "audit.research_target": 1,
    "audit.research_target_result": 1,
    "audit.research_target_source": 2,
    "audit.research_target_claim": 1,
    "audit.research_target_review": 1,
    "audit.research_case_ingest": 12,
    "audit.release_claim": 0,
    "audit.release_channel": 0,
}


class IngestError(RuntimeError):
    pass


def load_manifest(path: Path = MANIFEST) -> dict[str, Any]:
    value = json.loads(path.read_text(encoding="utf-8"))
    if value.get("record_kind") != "production_population_accepted_subset_manifest":
        raise IngestError("unexpected accepted-subset manifest")
    accepted = value.get("accepted") or []
    held = value.get("held_exclusions") or []
    if len(accepted) != EXPECTED_ACCEPTED or len(held) != EXPECTED_HELD:
        raise IngestError("accepted/held accounting drift")
    if value.get("register_accounting", {}).get("unaccounted_targets") != 0:
        raise IngestError("manifest still has unaccounted targets")
    if value.get("status") != "READY_FOR_EXPLICIT_PRODUCTION_INGEST_APPROVAL_NOT_RELEASE_APPROVAL":
        raise IngestError("manifest is not at the production-ingest approval gate")
    keys = [row["case_key"] for row in accepted]
    if len(keys) != len(set(keys)):
        raise IngestError("duplicate accepted case key")
    return value


def load_candidates(manifest: dict[str, Any]) -> list[tuple[dict[str, Any], dict[str, Any], str]]:
    result = []
    for row in manifest["accepted"]:
        path = ROOT / row["path"]
        if row["importer"] == "tools/add_legal_event_case.py":
            spec = load_legal_spec(path, require_case_key=True)
            digest = legal_content_sha256(spec)
            kind = "legal_event"
        elif row["importer"] == "tools/add_research_case.py":
            spec = load_territorial_spec(path, require_case_key=True)
            digest = case_content_sha256(spec)
            kind = "territorial_practice"
        else:
            raise IngestError(f"unsupported importer for {row['case_key']}")
        if spec["case_key"] != row["case_key"]:
            raise IngestError(f"case-key mismatch for {row['target']}")
        if digest != row["content_sha256"]:
            raise IngestError(f"content hash mismatch for {row['case_key']}")
        if spec["claim"].get("publication_status") != "unpublished":
            raise IngestError("accepted subset must remain unpublished at ingest")
        if kind == "territorial_practice":
            practice = spec["claim"]["territorial_practice"]
            if practice.get("practice_level") is not None:
                raise IngestError("accepted territorial candidate has a new P-level")
        result.append((row, spec, kind))
    return result


def plan(manifest: dict[str, Any]) -> dict[str, Any]:
    loaded = load_candidates(manifest)
    return {
        "issue": 360,
        "mode": "plan_only",
        "accepted_cases": len(loaded),
        "held_exclusions": len(manifest["held_exclusions"]),
        "case_keys": [row["case_key"] for row, _, _ in loaded],
        "claim_kinds": {
            "legal_event": sum(kind == "legal_event" for _, _, kind in loaded),
            "territorial_practice": sum(kind == "territorial_practice" for _, _, kind in loaded),
        },
        "expected_database_delta_live_preflight": manifest["expected_database_delta_if_explicitly_ingested"],
        "release_membership_change": 0,
        "publication_change": 0,
        "serving_channel_change": 0,
        "production_write_authorized": False,
    }


def require_disposable_dsn(dsn: str) -> None:
    parsed = urlparse(dsn)
    if parsed.scheme not in ("postgres", "postgresql"):
        raise IngestError("unexpected DSN scheme")
    if parsed.hostname != "db" or parsed.username != "atlas" or parsed.path != "/slavery_atlas":
        raise IngestError("disposable rehearsal only permits the local Compose database")
    if parsed.query or parsed.fragment:
        raise IngestError("DSN overrides are forbidden in disposable rehearsal")


def check_apply_authority(args: argparse.Namespace) -> str:
    if args.disposable_test_db:
        if os.environ.get("CI") != "true":
            raise IngestError("disposable apply requires CI=true")
        require_disposable_dsn(args.dsn)
        return "disposable_rollback"
    if args.production_write_authorized != "ISSUE-360-EXPLICIT":
        raise IngestError("production apply requires --production-write-authorized ISSUE-360-EXPLICIT")
    if os.environ.get("ATLAS_PRODUCTION_WRITE_AUTHORIZED") != "1":
        raise IngestError("production apply requires ATLAS_PRODUCTION_WRITE_AUTHORIZED=1")
    if not args.expected_main_sha or not args.expected_pr_head_sha:
        raise IngestError("production apply requires refreshed expected main and PR head SHAs")
    return "production_commit"


def counts(conn) -> dict[str, int]:
    with conn.cursor() as cur:
        return {table: cur.execute(f"select count(*) from {table}").fetchone()[0]
                for table in TRACKED_TABLES}


def resolved_geometry_count(conn, case_keys: list[str]) -> int:
    with conn.cursor() as cur:
        return cur.execute(
            """select count(*)
                 from atlas.geometry g
                 join atlas.territorial_practice_claim t using(spatial_entity_id)
                 join audit.research_case_ingest r on r.claim_id=t.claim_id
                where r.case_key = any(%s)
                  and g.geom is not null""",
            (case_keys,),
        ).fetchone()[0]


def preflight_absence(conn, candidates: list[tuple[dict[str, Any], dict[str, Any], str]]) -> None:
    keys = [row["case_key"] for row, _, _ in candidates]
    names = [spec["spatial_entity"]["canonical_name"] for _, spec, _ in candidates]
    with conn.cursor() as cur:
        if cur.execute(
            "select count(*) from audit.research_case_ingest where case_key=any(%s)", (keys,)
        ).fetchone()[0]:
            raise IngestError("one or more accepted case keys already exist")
        if cur.execute(
            "select count(*) from atlas.spatial_entity where canonical_name=any(%s)", (names,)
        ).fetchone()[0]:
            raise IngestError("one or more accepted canonical spatial identities already exist")


def assert_delta(before: dict[str, int], after: dict[str, int]) -> dict[str, int]:
    delta = {table: after[table] - before[table] for table in TRACKED_TABLES}
    for table, expected in STRICT_DELTAS.items():
        if delta[table] != expected:
            raise IngestError(f"unexpected delta for {table}: {delta[table]} != {expected}")
    if delta["atlas.source_version"] < 28 or delta["atlas.source_version"] > 29:
        raise IngestError("source-version delta outside reviewed 28-29 range")
    if delta["atlas.source"] != delta["atlas.source_version"]:
        raise IngestError("source/source-version delta mismatch in candidate ingest")
    return delta


def run(conn, manifest: dict[str, Any], *, git_revision: str, rollback: bool) -> dict[str, Any]:
    candidates = load_candidates(manifest)
    case_keys = [row["case_key"] for row, _, _ in candidates]
    before = counts(conn)
    generated: list[dict[str, str]] = []
    first_counts = None
    delta = None
    try:
        preflight_absence(conn, candidates)
        for row, spec, kind in candidates:
            if kind == "legal_event":
                claim_id, inserted = insert_legal_case(
                    conn, spec, source_path=row["path"], git_revision=git_revision
                )
            else:
                claim_id, inserted = insert_territorial_case(
                    conn, spec, source_path=row["path"], git_revision=git_revision
                )
            if not inserted:
                raise IngestError(f"unexpected first-pass no-op for {row['case_key']}")
            generated.append({"case_key": row["case_key"], "claim_id": claim_id})
        first_counts = counts(conn)
        delta = assert_delta(before, first_counts)
        if resolved_geometry_count(conn, case_keys) != 9:
            raise IngestError("expected exactly nine resolved geometry rows")

        for index, (row, spec, kind) in enumerate(candidates):
            if kind == "legal_event":
                claim_id, inserted = insert_legal_case(
                    conn, spec, source_path=row["path"], git_revision=git_revision
                )
            else:
                claim_id, inserted = insert_territorial_case(
                    conn, spec, source_path=row["path"], git_revision=git_revision
                )
            if inserted or claim_id != generated[index]["claim_id"]:
                raise IngestError("unchanged replay was not an exact no-op")
        if counts(conn) != first_counts:
            raise IngestError("unchanged replay altered tracked table counts")

        with conn.cursor() as cur:
            if cur.execute(
                """select count(*) from atlas.claim c
                   join audit.research_case_ingest r using(claim_id)
                   where r.case_key=any(%s)
                     and c.publication_status::text <> 'unpublished'""",
                (case_keys,),
            ).fetchone()[0]:
                raise IngestError("candidate ingest changed publication status")
            if cur.execute(
                """select count(*) from atlas.territorial_practice_claim t
                   join audit.research_case_ingest r using(claim_id)
                   where r.case_key=any(%s) and t.practice_level is not null""",
                (case_keys,),
            ).fetchone()[0]:
                raise IngestError("candidate ingest created a P-level")
    finally:
        if rollback:
            conn.rollback()

    if rollback:
        restored = counts(conn)
        conn.rollback()
        if restored != before:
            raise IngestError("rollback failed to restore tracked table counts")

    return {
        "record_kind": "population_subset_ingest_receipt",
        "version": 1,
        "issue": 360,
        "mode": "DISPOSABLE_ROLLBACK" if rollback else "PRODUCTION_COMMIT",
        "input_manifest": str(MANIFEST.relative_to(ROOT)),
        "git_revision_recorded": git_revision,
        "accepted_cases": len(candidates),
        "first_pass_inserted": len(generated),
        "second_pass_noops": len(generated),
        "generated_claim_ids": generated,
        "tracked_table_delta": delta,
        "resolved_geometry_rows": 9,
        "release_claim_delta": 0,
        "publication_changes": 0,
        "serving_channel_changes": 0,
        "rollback_restored_counts": rollback,
    }


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--manifest", type=Path, default=MANIFEST)
    parser.add_argument("--dsn", default=os.environ.get("DATABASE_URL", ""))
    parser.add_argument("--apply", action="store_true")
    parser.add_argument("--disposable-test-db", action="store_true")
    parser.add_argument("--production-write-authorized")
    parser.add_argument("--expected-main-sha")
    parser.add_argument("--expected-pr-head-sha")
    parser.add_argument("--git-revision", default=os.environ.get("GITHUB_SHA", "UNSET"))
    args = parser.parse_args()

    manifest = load_manifest(args.manifest)
    dry = plan(manifest)
    print(json.dumps(dry, ensure_ascii=False, indent=2, sort_keys=True))
    if not args.apply:
        print("DRY RUN: no database changes made")
        return 0
    if not args.dsn:
        parser.error("--dsn or DATABASE_URL is required with --apply")

    mode = check_apply_authority(args)
    if mode == "production_commit":
        auth = manifest["authority"]
        if args.expected_main_sha != auth["github_main_sha"]:
            raise IngestError("expected main SHA does not match reviewed manifest authority")
        if args.expected_pr_head_sha != args.git_revision:
            raise IngestError("production git revision must equal the explicitly refreshed PR head")

    import psycopg
    with psycopg.connect(args.dsn, autocommit=False) as conn:
        try:
            if mode == "disposable_rollback":
                receipt = run(conn, manifest, git_revision=args.git_revision, rollback=True)
            else:
                receipt = run(conn, manifest, git_revision=args.git_revision, rollback=False)
                conn.commit()
        except Exception:
            conn.rollback()
            raise
    print("POPULATION_SUBSET_INGEST_RECEIPT_BEGIN")
    print(json.dumps(receipt, ensure_ascii=False, indent=2, sort_keys=True))
    print("POPULATION_SUBSET_INGEST_RECEIPT_END")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
