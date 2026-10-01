#!/usr/bin/env python3
"""Disposable rehearsal for the first D-124 five-case #369 pilot batch.

This tool has deliberately NO production commit path. It binds the five reviewed
repository packets by Git blob SHA-1, applies them atomically only to the local
Compose PostGIS database, requires unchanged replay to be an exact no-op, verifies
core deltas and release/public invariants, then rolls the entire transaction back.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import os
from pathlib import Path
import sys
from typing import Any
from urllib.parse import urlparse

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from tools.add_research_case import (  # noqa: E402
    case_content_sha256,
    insert_case as insert_territorial_case,
    load_spec as load_territorial_spec,
)
from tools.add_external_participation_case import (  # noqa: E402
    insert_case as insert_external_case,
    load_spec as load_external_spec,
)

MANIFEST = (
    ROOT
    / "data/research/recovery/population_100_100_intake_2026_10_01"
    / "pilot_batch_manifest.json"
)
EXPECTED_MEMBERS = 5

TRACKED_TABLES = (
    "atlas.spatial_entity",
    "atlas.source",
    "atlas.source_version",
    "atlas.geometry",
    "atlas.claim",
    "atlas.territorial_practice_claim",
    "atlas.external_participation_claim",
    "atlas.claim_source",
    "audit.research_case_ingest",
    "audit.release_claim",
    "audit.release_geometry",
    "audit.release_channel",
)

STRICT_DELTAS = {
    "atlas.spatial_entity": 5,
    "atlas.geometry": 5,
    "atlas.claim": 5,
    "atlas.territorial_practice_claim": 2,
    "atlas.external_participation_claim": 3,
    "atlas.claim_source": 21,
    "audit.research_case_ingest": 5,
    "audit.release_claim": 0,
    "audit.release_geometry": 0,
    "audit.release_channel": 0,
}


class RehearsalError(RuntimeError):
    pass


def git_blob_sha1(path: Path) -> str:
    raw = path.read_bytes()
    header = f"blob {len(raw)}\0".encode("ascii")
    return hashlib.sha1(header + raw).hexdigest()


def load_manifest(path: Path = MANIFEST) -> dict[str, Any]:
    value = json.loads(path.read_text(encoding="utf-8"))
    if value.get("record_kind") != "atlas_100_100_pilot_batch_manifest":
        raise RehearsalError("unexpected pilot manifest kind")
    if value.get("issue") != 369 or value.get("decision") != "D-124":
        raise RehearsalError("pilot manifest is not bound to #369 / D-124")
    if value.get("status") != "READY_FOR_DISPOSABLE_REHEARSAL_ONLY_NOT_PRODUCTION_AUTHORIZED":
        raise RehearsalError("pilot manifest is not at the disposable rehearsal gate")
    if value.get("authority", {}).get("production_write_authorized") is not False:
        raise RehearsalError("pilot manifest must explicitly deny production authority")

    members = value.get("members") or []
    if len(members) != EXPECTED_MEMBERS:
        raise RehearsalError(f"expected {EXPECTED_MEMBERS} pilot members")

    keys = [row.get("case_key") for row in members]
    paths = [row.get("path") for row in members]
    if len(keys) != len(set(keys)) or len(paths) != len(set(paths)):
        raise RehearsalError("pilot manifest contains duplicate case keys or paths")

    if sum(row.get("claim_kind") == "territorial_practice" for row in members) != 2:
        raise RehearsalError("pilot manifest must contain exactly two territorial cases")
    if sum(row.get("claim_kind") == "external_participation" for row in members) != 3:
        raise RehearsalError("pilot manifest must contain exactly three external cases")
    return value


def load_candidates(
    manifest: dict[str, Any],
) -> list[tuple[dict[str, Any], dict[str, Any], str]]:
    loaded: list[tuple[dict[str, Any], dict[str, Any], str]] = []
    for row in manifest["members"]:
        path = ROOT / row["path"]
        observed_blob = git_blob_sha1(path)
        if observed_blob != row["git_blob_sha1"]:
            raise RehearsalError(
                f"packet blob drift for {row['case_key']}: "
                f"{observed_blob} != {row['git_blob_sha1']}"
            )

        importer = row["importer"]
        if importer == "tools/add_research_case.py":
            spec = load_territorial_spec(path, require_case_key=True)
            kind = "territorial_practice"
        elif importer == "tools/add_external_participation_case.py":
            spec = load_external_spec(path)
            kind = "external_participation"
        else:
            raise RehearsalError(f"unsupported pilot importer: {importer}")

        if spec.get("case_key") != row["case_key"]:
            raise RehearsalError(f"case-key mismatch for {row['target']}")
        if kind != row["claim_kind"]:
            raise RehearsalError(f"claim-kind mismatch for {row['case_key']}")
        if spec["claim"].get("review_status") != "reviewed":
            raise RehearsalError("pilot members must remain reviewed")
        if spec["claim"].get("publication_status") != "unpublished":
            raise RehearsalError("pilot members must remain unpublished")
        if kind == "territorial_practice":
            if spec["claim"]["territorial_practice"].get("practice_level") is not None:
                raise RehearsalError("pilot territorial member has a P-level")
        else:
            if "territorial_practice" in spec["claim"] or "practice_level" in spec["claim"]:
                raise RehearsalError("external member leaked into territorial/P-level semantics")
        loaded.append((row, spec, kind))
    return loaded


def plan(manifest: dict[str, Any]) -> dict[str, Any]:
    loaded = load_candidates(manifest)
    return {
        "issue": 369,
        "decision": "D-124",
        "mode": "disposable_rehearsal_only",
        "member_count": len(loaded),
        "case_keys": [row["case_key"] for row, _, _ in loaded],
        "claim_kinds": {
            "territorial_practice": sum(k == "territorial_practice" for _, _, k in loaded),
            "external_participation": sum(k == "external_participation" for _, _, k in loaded),
        },
        "packet_blobs": {
            row["case_key"]: row["git_blob_sha1"] for row, _, _ in loaded
        },
        "production_write_authorized": False,
        "release_selection_authorized": False,
        "public_cutover_authorized": False,
    }


def require_disposable_dsn(dsn: str) -> None:
    parsed = urlparse(dsn)
    if parsed.scheme not in ("postgres", "postgresql"):
        raise RehearsalError("unexpected DSN scheme")
    if parsed.hostname != "db" or parsed.username != "atlas" or parsed.path != "/slavery_atlas":
        raise RehearsalError("pilot rehearsal only permits the local Compose database")
    if parsed.query or parsed.fragment:
        raise RehearsalError("DSN overrides are forbidden in disposable rehearsal")


def counts(conn) -> dict[str, int]:
    with conn.cursor() as cur:
        result: dict[str, int] = {}
        for table in TRACKED_TABLES:
            cur.execute(f"select count(*) from {table}")
            result[table] = int(cur.fetchone()[0])
        return result


def preflight_absence(
    conn,
    candidates: list[tuple[dict[str, Any], dict[str, Any], str]],
) -> None:
    keys = [row["case_key"] for row, _, _ in candidates]
    names = [spec["spatial_entity"]["canonical_name"] for _, spec, _ in candidates]
    with conn.cursor() as cur:
        cur.execute(
            "select count(*) from audit.research_case_ingest where case_key = any(%s)",
            (keys,),
        )
        if cur.fetchone()[0]:
            raise RehearsalError("one or more pilot case keys already exist")
        cur.execute(
            "select count(*) from atlas.spatial_entity where canonical_name = any(%s)",
            (names,),
        )
        if cur.fetchone()[0]:
            raise RehearsalError("one or more pilot canonical spatial identities already exist")


def assert_delta(before: dict[str, int], after: dict[str, int]) -> dict[str, int]:
    delta = {table: after[table] - before[table] for table in TRACKED_TABLES}
    for table, expected in STRICT_DELTAS.items():
        if delta[table] != expected:
            raise RehearsalError(
                f"unexpected pilot delta for {table}: {delta[table]} != {expected}"
            )

    source_delta = delta["atlas.source"]
    version_delta = delta["atlas.source_version"]
    if source_delta != version_delta:
        raise RehearsalError("new source/source-version deltas diverged")
    if source_delta < 0 or source_delta > 23:
        raise RehearsalError("source reuse delta outside reviewed 0..23 envelope")
    return delta


def semantic_checks(conn, case_keys: list[str]) -> dict[str, int]:
    with conn.cursor() as cur:
        cur.execute(
            """
            select
              count(*) filter (where c.claim_kind_code='territorial_practice'),
              count(*) filter (where c.claim_kind_code='external_participation'),
              count(*) filter (where c.publication_status='unpublished'),
              count(*) filter (
                where c.claim_kind_code='territorial_practice'
                  and t.practice_level is null
              ),
              count(*) filter (
                where c.claim_kind_code='external_participation'
                  and t.claim_id is null
                  and e.claim_id is not null
              )
            from audit.research_case_ingest r
            join atlas.claim c using(claim_id)
            left join atlas.territorial_practice_claim t using(claim_id)
            left join atlas.external_participation_claim e using(claim_id)
            where r.case_key = any(%s)
            """,
            (case_keys,),
        )
        territorial, external, unpublished, null_p, external_clean = map(int, cur.fetchone())

        cur.execute(
            """
            with subjects as (
              select r.case_key,
                     coalesce(t.spatial_entity_id,e.spatial_entity_id) as spatial_entity_id
              from audit.research_case_ingest r
              join atlas.claim c using(claim_id)
              left join atlas.territorial_practice_claim t using(claim_id)
              left join atlas.external_participation_claim e using(claim_id)
              where r.case_key = any(%s)
            )
            select
              count(*) filter (where g.geom is not null and g.accuracy_status='modern_proxy'),
              count(*) filter (where g.geom is null and g.accuracy_status='unresolved'),
              count(*) filter (
                where g.geom is not null
                  and geometrytype(g.geom) in ('POLYGON','MULTIPOLYGON')
              )
            from subjects s
            join atlas.geometry g using(spatial_entity_id)
            """,
            (case_keys,),
        )
        resolved_proxy, unresolved, polygons = map(int, cur.fetchone())

    observed = {
        "territorial_claims": territorial,
        "external_claims": external,
        "unpublished_claims": unpublished,
        "territorial_null_p_levels": null_p,
        "external_without_territorial_subtype": external_clean,
        "resolved_modern_proxy_points": resolved_proxy,
        "unresolved_null_geometry_rows": unresolved,
        "resolved_polygon_rows": polygons,
    }
    expected = {
        "territorial_claims": 2,
        "external_claims": 3,
        "unpublished_claims": 5,
        "territorial_null_p_levels": 2,
        "external_without_territorial_subtype": 3,
        "resolved_modern_proxy_points": 2,
        "unresolved_null_geometry_rows": 3,
        "resolved_polygon_rows": 0,
    }
    if observed != expected:
        raise RehearsalError(f"pilot semantic composition drift: {observed} != {expected}")
    return observed


def run(
    conn,
    manifest: dict[str, Any],
    *,
    git_revision: str,
) -> dict[str, Any]:
    candidates = load_candidates(manifest)
    case_keys = [row["case_key"] for row, _, _ in candidates]
    before = counts(conn)
    generated: list[dict[str, Any]] = []

    try:
        preflight_absence(conn, candidates)

        for row, spec, kind in candidates:
            if kind == "territorial_practice":
                claim_id, inserted = insert_territorial_case(
                    conn,
                    spec,
                    source_path=row["path"],
                    git_revision=git_revision,
                )
            else:
                claim_id, inserted = insert_external_case(
                    conn,
                    spec,
                    source_path=row["path"],
                    git_revision=git_revision,
                )
            if not inserted:
                raise RehearsalError(f"unexpected first-pass no-op for {row['case_key']}")
            generated.append(
                {
                    "case_key": row["case_key"],
                    "claim_kind": kind,
                    "claim_id": claim_id,
                    "content_sha256": case_content_sha256(spec),
                }
            )

        after_first = counts(conn)
        delta = assert_delta(before, after_first)
        composition = semantic_checks(conn, case_keys)

        for row, spec, kind in candidates:
            if kind == "territorial_practice":
                _, inserted = insert_territorial_case(
                    conn,
                    spec,
                    source_path=row["path"],
                    git_revision=git_revision,
                )
            else:
                _, inserted = insert_external_case(
                    conn,
                    spec,
                    source_path=row["path"],
                    git_revision=git_revision,
                )
            if inserted:
                raise RehearsalError(f"unchanged replay was not a no-op for {row['case_key']}")

        after_replay = counts(conn)
        if after_replay != after_first:
            raise RehearsalError("unchanged replay changed tracked table counts")

        conn.rollback()
        after_rollback = counts(conn)
        if after_rollback != before:
            raise RehearsalError("rollback did not restore tracked table counts")

        return {
            "status": "DISPOSABLE_REHEARSAL_PASS",
            "member_count": len(candidates),
            "generated_first_pass": generated,
            "first_pass_delta": delta,
            "semantic_composition": composition,
            "unchanged_replay": "EXACT_NO_OP",
            "rollback": "RESTORED_TRACKED_COUNTS",
            "production_write_authorized": False,
            "release_effect": "none",
        }
    except Exception:
        conn.rollback()
        raise


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--dsn", default=os.environ.get("DATABASE_URL"))
    parser.add_argument("--apply", action="store_true")
    parser.add_argument("--disposable-test-db", action="store_true")
    parser.add_argument("--git-revision", default=os.environ.get("GITHUB_SHA") or "unknown")
    args = parser.parse_args()

    manifest = load_manifest()
    print(json.dumps(plan(manifest), indent=2, ensure_ascii=False))

    if not args.apply:
        print("DRY RUN: exact pilot manifest validated; no database changes made")
        return 0

    if not args.disposable_test_db:
        raise SystemExit(
            "pilot batch driver has NO production apply path; "
            "--apply requires --disposable-test-db"
        )
    if os.environ.get("CI") != "true":
        raise SystemExit("disposable pilot rehearsal requires CI=true")
    if not args.dsn:
        parser.error("--dsn or DATABASE_URL is required with --apply")
    require_disposable_dsn(args.dsn)

    try:
        import psycopg
    except ImportError as exc:
        raise SystemExit("psycopg is required; install requirements.txt") from exc

    with psycopg.connect(args.dsn, autocommit=False) as conn:
        receipt = run(conn, manifest, git_revision=args.git_revision)

    print(json.dumps(receipt, indent=2, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    sys.exit(main())
