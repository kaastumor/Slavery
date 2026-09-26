#!/usr/bin/env python3
"""Compare repository migrations with a Supabase migration-history export.

Raw platform-history irregularities are always reported. An optional explicit policy
can mark known production gaps/retries as accepted legacy history while still failing
on any new drift.
"""
from __future__ import annotations

import argparse
from collections import Counter
import json
from pathlib import Path
import sys
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
MIGRATIONS = ROOT / "db" / "migrations"


def repository_names() -> list[str]:
    return [p.stem for p in sorted(MIGRATIONS.glob("[0-9][0-9][0-9][0-9]_*.sql"))]


def remote_names(payload: Any) -> list[str]:
    if isinstance(payload, dict):
        payload = payload.get("migrations", payload.get("data", payload))
    if not isinstance(payload, list):
        raise ValueError("remote JSON must contain a migration list")
    out: list[str] = []
    for row in payload:
        if isinstance(row, str):
            out.append(row)
        elif isinstance(row, dict) and isinstance(row.get("name"), str):
            out.append(row["name"])
        else:
            raise ValueError("each remote migration needs a name")
    return out


def compare(repo: list[str], remote: list[str]) -> dict[str, Any]:
    counts = Counter(remote)
    rs = set(repo)
    ms = set(remote)
    return {
        "repository_count": len(repo),
        "remote_entry_count": len(remote),
        "missing_remote": [n for n in repo if n not in ms],
        "duplicate_remote": {n: c for n, c in sorted(counts.items()) if c > 1},
        "unknown_remote": sorted(ms - rs),
    }


def load_policy(path: Path | None) -> dict[str, Any] | None:
    if path is None:
        return None
    data = json.loads(path.read_text(encoding="utf-8"))
    if data.get("schema_version") != "migration-ledger-exceptions-v1":
        raise ValueError("unsupported migration ledger exception policy")
    return data


def evaluate(result: dict[str, Any], policy: dict[str, Any] | None) -> dict[str, Any]:
    if policy is None:
        return {
            **result,
            "policy_applied": False,
            "unexpected_missing_remote": list(result["missing_remote"]),
            "unexpected_duplicate_remote": dict(result["duplicate_remote"]),
            "unexpected_unknown_remote": list(result["unknown_remote"]),
            "accepted_missing_remote": [],
            "accepted_duplicate_remote": {},
            "pass": not (
                result["missing_remote"]
                or result["duplicate_remote"]
                or result["unknown_remote"]
            ),
        }

    allowed_missing = set(policy.get("allowed_missing_remote", []))
    allowed_dupes = {
        str(k): int(v)
        for k, v in policy.get("allowed_duplicate_remote", {}).items()
    }

    accepted_missing = [n for n in result["missing_remote"] if n in allowed_missing]
    unexpected_missing = [n for n in result["missing_remote"] if n not in allowed_missing]

    accepted_dupes: dict[str, int] = {}
    unexpected_dupes: dict[str, int] = {}
    for name, count in result["duplicate_remote"].items():
        if allowed_dupes.get(name) == count:
            accepted_dupes[name] = count
        else:
            unexpected_dupes[name] = count

    # Policy entries are exact expectations, not wildcards. If a known legacy
    # irregularity disappears or changes count, require review instead of silently
    # accepting the new shape.
    missing_expected_but_absent = sorted(allowed_missing - set(result["missing_remote"]))
    dup_expected_but_changed = {
        name: {
            "expected": expected,
            "observed": result["duplicate_remote"].get(name, 1),
        }
        for name, expected in sorted(allowed_dupes.items())
        if result["duplicate_remote"].get(name) != expected
    }

    unexpected_unknown = list(result["unknown_remote"])
    passed = not (
        unexpected_missing
        or unexpected_dupes
        or unexpected_unknown
        or missing_expected_but_absent
        or dup_expected_but_changed
    )

    return {
        **result,
        "policy_applied": True,
        "policy_schema_version": policy["schema_version"],
        "accepted_missing_remote": accepted_missing,
        "accepted_duplicate_remote": accepted_dupes,
        "unexpected_missing_remote": unexpected_missing,
        "unexpected_duplicate_remote": unexpected_dupes,
        "unexpected_unknown_remote": unexpected_unknown,
        "expected_missing_no_longer_missing": missing_expected_but_absent,
        "expected_duplicate_count_changed": dup_expected_but_changed,
        "pass": passed,
    }


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("remote_json", type=Path)
    parser.add_argument("--policy", type=Path)
    args = parser.parse_args()

    raw = compare(
        repository_names(),
        remote_names(json.loads(args.remote_json.read_text(encoding="utf-8"))),
    )
    result = evaluate(raw, load_policy(args.policy))
    print(json.dumps(result, indent=2, sort_keys=True))
    return 0 if result["pass"] else 2


if __name__ == "__main__":
    sys.exit(main())
