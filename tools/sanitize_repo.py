#!/usr/bin/env python3
"""Fast repository-integrity checks for CI and local development."""

from __future__ import annotations

import re
import subprocess
import sys
from pathlib import Path

REQUIRED = {
    "BACKLOG.md",
    "docs/23_PROJECT_CHARTER.md",
    "docs/24_WAY_OF_WORKING.md",
    "docs/25_PROJECT_HEALTH.md",
    "docs/automation/hourly-worker.md",
    "docs/08_DECISIONS_LOG.md",
    "SECURITY.md",
}

FORBIDDEN_PATH_PATTERNS = (
    re.compile(r"(^|/)\.env$"),
    re.compile(r"^data/releases/.*\.xlsx$", re.I),
    re.compile(r"^backups/(?!\.gitkeep$).+"),
    re.compile(r"(^|/)(?:node_modules|__pycache__|\.pytest_cache)(/|$)"),
    re.compile(r"\.(?:dump|sql\.gz|pem|key|pfx|p12)$", re.I),
)

LOCAL_PATH_PATTERNS = (
    re.compile(r"\b[A-Za-z]:\\\\Users\\\\[^\\\\\s]+\\\\"),
    re.compile(r"/Users/[^/\s]+/"),
    re.compile(r"/home/[^/\s]+/"),
)

SECRET_PATTERNS = (
    ("private key", re.compile(r"-----BEGIN [A-Z ]*PRIVATE KEY-----")),
    ("GitHub token", re.compile(r"\bghp_[A-Za-z0-9]{20,}\b")),
    ("GitHub fine-grained token", re.compile(r"\bgithub_pat_[A-Za-z0-9_]{20,}\b")),
    ("OpenAI-style secret", re.compile(r"\bsk-(?:proj-)?[A-Za-z0-9_-]{20,}\b")),
    ("AWS access key", re.compile(r"\bAKIA[0-9A-Z]{16}\b")),
)

TEXT_SUFFIXES = {
    ".md", ".txt", ".py", ".sql", ".sh", ".ps1", ".yml", ".yaml", ".json",
    ".toml", ".ts", ".js", ".mjs", ".css", ".html", ".xml", ".csv", ".geojson",
}
TEXT_NAMES = {".gitignore", ".gitattributes", ".editorconfig", ".python-version"}


def tracked_files(root: Path) -> list[str]:
    proc = subprocess.run(
        ["git", "ls-files", "-z"],
        cwd=root,
        check=True,
        capture_output=True,
    )
    return [p.decode("utf-8") for p in proc.stdout.split(b"\0") if p]


def is_text_candidate(path: str) -> bool:
    p = Path(path)
    return p.name in TEXT_NAMES or p.suffix.lower() in TEXT_SUFFIXES


def scan(root: Path, paths: list[str]) -> list[str]:
    failures: list[str] = []
    tracked = set(paths)

    for required in sorted(REQUIRED):
        if required not in tracked:
            failures.append(f"missing required project structure: {required}")

    for rel in paths:
        normalized = rel.replace("\\", "/")
        for pattern in FORBIDDEN_PATH_PATTERNS:
            if pattern.search(normalized):
                failures.append(f"forbidden tracked path: {rel}")
                break

        file_path = root / rel
        try:
            size = file_path.stat().st_size
        except OSError:
            continue

        if size > 5_000_000:
            failures.append(f"unexpected tracked file larger than 5 MB: {rel} ({size} bytes)")
            continue

        if not is_text_candidate(rel):
            continue

        try:
            text = file_path.read_text(encoding="utf-8")
        except (OSError, UnicodeDecodeError):
            continue

        for line_no, line in enumerate(text.splitlines(), start=1):
            if line.startswith(("<<<<<<< ", ">>>>>>> ")):
                failures.append(f"merge marker: {rel}:{line_no}")

        for label, pattern in SECRET_PATTERNS:
            if pattern.search(text):
                failures.append(f"possible {label}: {rel}")

        for pattern in LOCAL_PATH_PATTERNS:
            if pattern.search(text):
                failures.append(f"machine-local user path: {rel}")
                break

    return failures


def main() -> int:
    root = Path(__file__).resolve().parents[1]
    failures = scan(root, tracked_files(root))
    if failures:
        print("Repository sanitation FAILED:")
        for failure in failures:
            print(f"- {failure}")
        return 1
    print("Repository sanitation passed.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
