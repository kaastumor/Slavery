#!/usr/bin/env python3
"""Small checksum-enforced SQL migration runner for the atlas foundation."""
from __future__ import annotations

import argparse
import hashlib
import os
from pathlib import Path
import sys
import re


ROOT = Path(__file__).resolve().parents[1]
MIGRATIONS_DIR = ROOT / "db" / "migrations"
META_SCHEMA = "atlas_meta"
META_TABLE = "schema_migration"


def sha256(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as f:
        for chunk in iter(lambda: f.read(1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest()


def discover() -> list[Path]:
    files = sorted(MIGRATIONS_DIR.glob("[0-9][0-9][0-9][0-9]_*.sql"))
    names = [p.name for p in files]
    if len(names) != len(set(names)):
        raise RuntimeError("Duplicate migration filenames detected")
    return files


def migration_body(path: Path) -> str:
    """Return migration SQL without the legacy outer BEGIN/COMMIT wrapper.

    Foundation migrations 0001-0011 were authored for psql and contain their
    own top-level BEGIN/COMMIT. The checksum ledger runner owns the transaction
    so it strips exactly one leading BEGIN and one trailing COMMIT when present.
    Internal/nested transaction control is rejected.
    """
    sql = path.read_text(encoding="utf-8")
    body = re.sub(r"(?im)^\s*BEGIN\s*;\s*", "", sql, count=1)
    body = re.sub(r"(?im)\s*COMMIT\s*;\s*$", "", body, count=1)
    if re.search(r"(?im)^\s*(BEGIN|COMMIT|ROLLBACK)\s*;", body):
        raise RuntimeError(f"Nested transaction control is not supported in {path.name}")
    return body.strip() + "\n"

def ensure_ledger(conn) -> None:
    with conn.cursor() as cur:
        cur.execute(f"CREATE SCHEMA IF NOT EXISTS {META_SCHEMA}")
        cur.execute(
            f"""
            CREATE TABLE IF NOT EXISTS {META_SCHEMA}.{META_TABLE} (
                migration_name text PRIMARY KEY,
                checksum_sha256 text NOT NULL,
                applied_at timestamptz NOT NULL DEFAULT now()
            )
            """
        )
    conn.commit()


def applied(conn) -> dict[str, str]:
    with conn.cursor() as cur:
        cur.execute(
            f"SELECT migration_name, checksum_sha256 FROM {META_SCHEMA}.{META_TABLE} ORDER BY migration_name"
        )
        return dict(cur.fetchall())


def status(conn) -> int:
    ensure_ledger(conn)
    existing = applied(conn)
    rc = 0
    for path in discover():
        checksum = sha256(path)
        if path.name not in existing:
            state = "PENDING"
        elif existing[path.name] == checksum:
            state = "APPLIED"
        else:
            state = "CHECKSUM_MISMATCH"
            rc = 2
        print(f"{state:17} {path.name} {checksum[:12]}")
    for name in sorted(set(existing) - {p.name for p in discover()}):
        print(f"ORPHANED_APPLIED   {name} {existing[name][:12]}")
        rc = 2
    return rc


def up(conn) -> int:
    ensure_ledger(conn)
    existing = applied(conn)
    for path in discover():
        checksum = sha256(path)
        old = existing.get(path.name)
        if old:
            if old != checksum:
                raise RuntimeError(
                    f"Applied migration {path.name} changed: database={old}, file={checksum}. "
                    "Never edit an applied migration; add a new numbered migration."
                )
            print(f"==> already applied {path.name}")
            continue
        sql = migration_body(path)
        print(f"==> applying {path.name}")
        try:
            with conn.transaction():
                with conn.cursor() as cur:
                    cur.execute(sql)
                    cur.execute(
                        f"INSERT INTO {META_SCHEMA}.{META_TABLE} (migration_name, checksum_sha256) VALUES (%s, %s)",
                        (path.name, checksum),
                    )
        except Exception:
            conn.rollback()
            raise
    return status(conn)


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("command", choices=["up", "status"])
    parser.add_argument("--dsn", default=os.environ.get("DATABASE_URL"))
    args = parser.parse_args()
    if not args.dsn:
        parser.error("--dsn or DATABASE_URL is required")
    try:
        import psycopg
    except ImportError as exc:  # pragma: no cover
        raise SystemExit("psycopg is required; run this through the tooling container") from exc
    try:
        import psycopg
    except ImportError as exc:
        raise SystemExit("psycopg is required; run this through the tooling container") from exc
    with psycopg.connect(args.dsn, autocommit=False) as conn:
        return up(conn) if args.command == "up" else status(conn)


if __name__ == "__main__":
    sys.exit(main())
