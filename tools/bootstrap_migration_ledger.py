#!/usr/bin/env python3
"""Bootstrap the repository checksum migration ledger on an already-migrated live DB.

This is a one-time reconciliation tool for #26 / #300. It does NOT apply historical
schema migrations. Dry-run is the default.

Safety model:
- require repository/live operational migration head 0030 while the frozen v0.6.1 DB migration candidate remains a 0029 historical input;
- require exact canonical workbook checksum lineage and prior migration validation;
- require live sentinel objects for the historical 0012-0014 platform-history gap;
- require Supabase platform history to match the explicit legacy-exception policy;
- reject any existing checksum-ledger mismatch;
- --apply additionally requires --confirm-head 0030.

The resulting atlas_meta.schema_migration rows are a verified-baseline recording of
the repository migration files that define the accepted live schema, not original
migration timestamps.
"""
from __future__ import annotations

import argparse
from collections import Counter
import hashlib
import json
import os
from pathlib import Path
import sys
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
MIGRATIONS_DIR = ROOT / "db" / "migrations"
DEFAULT_POLICY = ROOT / "config" / "migration_ledger_exceptions.json"

EXPECTED_RELEASE = "0.6.1-db-migration-candidate"
EXPECTED_REPOSITORY_HEAD = "0030"\nEXPECTED_RELEASE_SCHEMA_HEAD = "0029"
EXPECTED_WORKBOOK_SHA256 = (
    "0a38e4eb6f63c3bb4ce9543be379605d24dd9ff1c1cea1e0a49c0c3db7ba17d4"
)


class BootstrapError(RuntimeError):
    pass


def file_sha256(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest()


def repository_inventory() -> list[dict[str, str]]:
    paths = sorted(MIGRATIONS_DIR.glob("[0-9][0-9][0-9][0-9]_*.sql"))
    if not paths:
        raise BootstrapError("no repository migrations found")
    return [
        {
            "filename": path.name,
            "name": path.stem,
            "checksum_sha256": file_sha256(path),
        }
        for path in paths
    ]


def load_policy(path: Path) -> dict[str, Any]:
    data = json.loads(path.read_text(encoding="utf-8"))
    if data.get("schema_version") != "migration-ledger-exceptions-v1":
        raise BootstrapError("unsupported migration ledger exception policy")
    return data


def platform_history(cur) -> list[dict[str, str]]:
    cur.execute(
        """
        select version, name
        from supabase_migrations.schema_migrations
        order by version
        """
    )
    return [{"version": row[0], "name": row[1]} for row in cur.fetchall()]


def evaluate_platform_history(
    inventory: list[dict[str, str]],
    history: list[dict[str, str]],
    policy: dict[str, Any],
) -> dict[str, Any]:
    repo = [row["name"] for row in inventory]
    remote = [row["name"] for row in history]
    counts = Counter(remote)
    remote_set = set(remote)
    repo_set = set(repo)

    missing = [name for name in repo if name not in remote_set]
    duplicates = {name: count for name, count in sorted(counts.items()) if count > 1}
    unknown = sorted(remote_set - repo_set)

    allowed_missing = set(policy.get("allowed_missing_remote", []))
    allowed_dupes = {
        str(k): int(v)
        for k, v in policy.get("allowed_duplicate_remote", {}).items()
    }

    unexpected_missing = [name for name in missing if name not in allowed_missing]
    unexpected_duplicates = {
        name: count
        for name, count in duplicates.items()
        if allowed_dupes.get(name) != count
    }
    missing_expected_but_absent = sorted(allowed_missing - set(missing))
    expected_duplicate_changed = {
        name: {"expected": expected, "observed": duplicates.get(name, 1)}
        for name, expected in sorted(allowed_dupes.items())
        if duplicates.get(name) != expected
    }

    passed = not (
        unexpected_missing
        or unexpected_duplicates
        or unknown
        or missing_expected_but_absent
        or expected_duplicate_changed
    )
    return {
        "missing_remote": missing,
        "duplicate_remote": duplicates,
        "unknown_remote": unknown,
        "unexpected_missing_remote": unexpected_missing,
        "unexpected_duplicate_remote": unexpected_duplicates,
        "expected_missing_no_longer_missing": missing_expected_but_absent,
        "expected_duplicate_count_changed": expected_duplicate_changed,
        "pass": passed,
    }


def live_sentinels(cur) -> dict[str, Any]:
    cur.execute(
        """
        select
          to_regclass('publish.neutral_land_mask') is not null,
          to_regclass('cartography.land_fabric') is not null,
          coalesce((
            select column_default is not null
            from information_schema.columns
            where table_schema='cartography'
              and table_name='land_fabric'
              and column_name='created_at'
          ), false),
          to_regclass('audit.release_claim') is not null,
          to_regclass('audit.release_artifact') is not null
        """
    )
    row = cur.fetchone()
    return {
        "publish.neutral_land_mask": bool(row[0]),
        "cartography.land_fabric": bool(row[1]),
        "cartography.land_fabric.created_at_default": bool(row[2]),
        "audit.release_claim": bool(row[3]),
        "audit.release_artifact": bool(row[4]),
    }


def release_candidate(cur) -> dict[str, Any]:
    cur.execute(
        """
        select schema_version, status, manifest
        from audit.release_manifest
        where release_version=%s
        """,
        (EXPECTED_RELEASE,),
    )
    row = cur.fetchone()
    if not row:
        raise BootstrapError(f"missing live release manifest {EXPECTED_RELEASE}")
    manifest = row[2] or {}
    return {
        "schema_version": row[0],
        "status": row[1],
        "workbook_sha256": manifest.get("workbook_sha256"),
        "migration_validation": manifest.get("migration_validation"),
        "production_schema_head": manifest.get("production_schema_head"),
        "canonical": manifest.get("canonical"),
    }


def checksum_ledger_rows(cur) -> list[tuple[str, str]]:
    cur.execute("select to_regclass('atlas_meta.schema_migration') is not null")
    if not cur.fetchone()[0]:
        return []
    cur.execute(
        """
        select migration_name, checksum_sha256
        from atlas_meta.schema_migration
        order by migration_name
        """
    )
    return [(row[0], row[1]) for row in cur.fetchall()]


def validate_existing_ledger(
    inventory: list[dict[str, str]],
    existing: list[tuple[str, str]],
) -> dict[str, Any]:
    expected = {row["filename"]: row["checksum_sha256"] for row in inventory}
    actual = dict(existing)
    unknown = sorted(set(actual) - set(expected))
    mismatched = {
        name: {"expected": expected[name], "actual": actual[name]}
        for name in sorted(set(actual) & set(expected))
        if expected[name] != actual[name]
    }
    missing = [row["filename"] for row in inventory if row["filename"] not in actual]
    return {
        "existing_count": len(existing),
        "missing": missing,
        "unknown": unknown,
        "checksum_mismatch": mismatched,
        "pass": not unknown and not mismatched,
    }


def preflight(cur, policy_path: Path) -> dict[str, Any]:
    inventory = repository_inventory()
    if len(inventory) != 29 or inventory[-1]["name"] != "0029_claim_kind_function_privileges":
        raise BootstrapError("repository migration inventory is not the expected 0001-0029 set")

    policy = load_policy(policy_path)
    history = platform_history(cur)
    history_result = evaluate_platform_history(inventory, history, policy)
    if not history_result["pass"]:
        raise BootstrapError("Supabase platform migration history has unexpected drift")

    sentinels = live_sentinels(cur)
    if not all(sentinels.values()):
        raise BootstrapError(f"live schema sentinel failed: {sentinels}")

    release = release_candidate(cur)
    if release["schema_version"] != EXPECTED_SCHEMA_HEAD:
        raise BootstrapError(f"live release candidate schema head is {release['schema_version']!r}")
    if release["production_schema_head"] != EXPECTED_SCHEMA_HEAD:
        raise BootstrapError("release manifest production_schema_head is not 0029")
    if release["migration_validation"] != "passed":
        raise BootstrapError("release manifest does not record migration_validation=passed")
    if release["workbook_sha256"] != EXPECTED_WORKBOOK_SHA256:
        raise BootstrapError("canonical v0.6.1 workbook checksum lineage mismatch")
    if release["canonical"] not in (False, None):
        raise BootstrapError("0.6.1 DB migration candidate unexpectedly claims canonical=true")

    existing = checksum_ledger_rows(cur)
    ledger = validate_existing_ledger(inventory, existing)
    if not ledger["pass"]:
        raise BootstrapError("existing checksum ledger conflicts with repository files")

    return {
        "repository_head": EXPECTED_REPOSITORY_HEAD,
        "repository_migration_count": len(inventory),
        "repository_inventory": inventory,
        "platform_history": history_result,
        "live_sentinels": sentinels,
        "release_candidate": release,
        "checksum_ledger_before": ledger,
        "planned_baseline_inserts": ledger["missing"],
    }


def apply_baseline(conn, report: dict[str, Any]) -> None:
    inventory = {
        row["filename"]: row["checksum_sha256"]
        for row in report["repository_inventory"]
    }
    with conn.cursor() as cur:
        cur.execute("create schema if not exists atlas_meta")
        cur.execute(
            """
            create table if not exists atlas_meta.schema_migration (
                migration_name text primary key,
                checksum_sha256 text not null,
                applied_at timestamptz not null default now(),
                recording_method text not null default 'runner_apply',
                notes text
            )
            """
        )
        cur.execute(
            """
            alter table atlas_meta.schema_migration
              add column if not exists recording_method text not null default 'runner_apply',
              add column if not exists notes text
            """
        )
        cur.execute("lock table atlas_meta.schema_migration in exclusive mode")
        for filename, checksum in inventory.items():
            cur.execute(
                """
                insert into atlas_meta.schema_migration(
                    migration_name, checksum_sha256, recording_method, notes
                )
                values (%s,%s,'verified_production_baseline',
                        'Gate 0 #26/#300 baseline: repository checksum recorded after live schema and release-candidate verification; applied_at is baseline recording time, not original schema-application time.')
                on conflict (migration_name) do nothing
                """,
                (filename, checksum),
            )

        existing = checksum_ledger_rows(cur)
        validation = validate_existing_ledger(report["repository_inventory"], existing)
        if not validation["pass"] or validation["missing"]:
            raise BootstrapError(f"post-insert checksum ledger verification failed: {validation}")


def write_receipt(path: Path | None, payload: dict[str, Any]) -> None:
    if path is not None:
        path.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n", encoding="utf-8")


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--dsn", default=os.environ.get("DATABASE_URL"))
    parser.add_argument("--policy", type=Path, default=DEFAULT_POLICY)
    parser.add_argument("--receipt", type=Path)
    parser.add_argument("--apply", action="store_true")
    parser.add_argument("--confirm-head")
    args = parser.parse_args()

    if not args.dsn:
        parser.error("--dsn or DATABASE_URL is required")
    if args.apply and args.confirm_head != EXPECTED_SCHEMA_HEAD:
        parser.error(f"--apply requires --confirm-head {EXPECTED_SCHEMA_HEAD}")

    try:
        import psycopg
    except ImportError as exc:
        raise SystemExit("psycopg is required; run through the tooling container") from exc

    try:
        with psycopg.connect(args.dsn, autocommit=False) as conn:
            with conn.cursor() as cur:
                report = preflight(cur, args.policy)

            report["mode"] = "apply" if args.apply else "dry_run"
            report["baseline_semantics"] = (
                "verified repository checksum baseline; applied_at records baseline time, "
                "not original migration execution time"
            )

            if not args.apply:
                conn.rollback()
                write_receipt(args.receipt, report)
                print(json.dumps(report, indent=2, sort_keys=True))
                print("DRY RUN: no database changes made")
                return 0

            try:
                with conn.transaction():
                    apply_baseline(conn, report)
            except Exception:
                conn.rollback()
                raise

            with conn.cursor() as cur:
                after = validate_existing_ledger(
                    report["repository_inventory"],
                    checksum_ledger_rows(cur),
                )
            report["checksum_ledger_after"] = after
            if not after["pass"] or after["missing"]:
                raise BootstrapError("checksum ledger incomplete after apply")
            write_receipt(args.receipt, report)
            print(json.dumps(report, indent=2, sort_keys=True))
            return 0
    except BootstrapError as exc:
        print(f"BLOCK: {exc}", file=sys.stderr)
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
