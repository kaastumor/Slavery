#!/usr/bin/env python3
"""Create a small immutable provenance manifest for derived atlas artifacts."""
from __future__ import annotations

import argparse
from datetime import datetime, timezone
import hashlib
import json
import os
from pathlib import Path
from typing import Iterable


SCHEMA_VERSION = "atlas-artifact-manifest-v1"


def sha256(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest()


def records(paths: Iterable[Path]) -> list[dict[str, object]]:
    result = []
    for path in paths:
        if not path.is_file():
            raise SystemExit(f"artifact input does not exist: {path}")
        result.append(
            {
                "path": str(path),
                "size_bytes": path.stat().st_size,
                "sha256": sha256(path),
            }
        )
    return result


def key_values(values: list[str], label: str) -> dict[str, str]:
    parsed: dict[str, str] = {}
    for value in values:
        if "=" not in value:
            raise SystemExit(f"{label} must use KEY=VALUE: {value}")
        key, item = value.split("=", 1)
        key = key.strip()
        if not key:
            raise SystemExit(f"{label} key may not be empty")
        parsed[key] = item
    return parsed


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--kind", required=True)
    parser.add_argument("--artifact", action="append", type=Path, default=[])
    parser.add_argument("--input", action="append", type=Path, default=[])
    parser.add_argument("--qc", action="append", type=Path, default=[])
    parser.add_argument("--tool", action="append", default=[])
    parser.add_argument("--param", action="append", default=[])
    parser.add_argument("--metadata", action="append", default=[])
    parser.add_argument("--git-sha", default=os.environ.get("GITHUB_SHA"))
    parser.add_argument("--output", required=True, type=Path)
    args = parser.parse_args()

    if not args.artifact:
        parser.error("at least one --artifact is required")

    manifest = {
        "schema_version": SCHEMA_VERSION,
        "artifact_kind": args.kind,
        "created_at": datetime.now(timezone.utc).isoformat(),
        "git_sha": args.git_sha,
        "tools": args.tool,
        "parameters": key_values(args.param, "--param"),
        "metadata": key_values(args.metadata, "--metadata"),
        "inputs": records(args.input),
        "artifacts": records(args.artifact),
        "qc": records(args.qc),
    }

    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(
        json.dumps(manifest, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )
    print(json.dumps(manifest, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
