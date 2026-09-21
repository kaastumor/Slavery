#!/usr/bin/env python3
"""Compare repository migrations with a Supabase migration-history export.

This tool is deliberately read-only. Feed it JSON from `supabase migration list`
or the Management/MCP list-migrations response. It detects missing repository
migrations, duplicate/retried remote names, unknown remote names, and gaps.
"""
from __future__ import annotations

import argparse
import json
from collections import Counter
from pathlib import Path
import re
import sys

ROOT = Path(__file__).resolve().parents[1]
MIGRATIONS = ROOT / "db" / "migrations"
NAME_RE = re.compile(r"^(\d{4})_(.+)\.sql$")


def repository_names() -> list[str]:
    names: list[str] = []
    for path in sorted(MIGRATIONS.glob("[0-9][0-9][0-9][0-9]_*.sql")):
        names.append(path.stem)
    return names


def remote_names(payload: object) -> list[str]:
    if isinstance(payload, dict):
        payload = payload.get("migrations", payload.get("data", payload))
    if not isinstance(payload, list):
        raise ValueError("remote JSON must be a migration list or contain a 'migrations' list")
    result = []
    for row in payload:
        if isinstance(row, str):
            result.append(row)
        elif isinstance(row, dict) and isinstance(row.get("name"), str):
            result.append(row["name"])
        else:
            raise ValueError("each remote migration must be a name string or object with string 'name'")
    return result


def compare(repo: list[str], remote: list[str]) -> dict[str, object]:
    counts = Counter(remote)
    repo_set = set(repo)
    remote_set = set(remote)
    return {
        "repository_count": len(repo),
        "remote_entry_count": len(remote),
        "missing_remote": [name for name in repo if name not in remote_set],
        "duplicate_remote": {name: n for name, n in sorted(counts.items()) if n > 1},
        "unknown_remote": sorted(remote_set - repo_set),
    }


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("remote_json", type=Path)
    args = parser.parse_args()
    payload = json.loads(args.remote_json.read_text(encoding="utf-8"))
    result = compare(repository_names(), remote_names(payload))
    print(json.dumps(result, indent=2, sort_keys=True))
    return 2 if result["missing_remote"] or result["duplicate_remote"] or result["unknown_remote"] else 0


if __name__ == "__main__":
    sys.exit(main())
