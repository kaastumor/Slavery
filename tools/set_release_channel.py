#!/usr/bin/env python3
"""Inspect or atomically repoint an atlas release serving channel."""
from __future__ import annotations

import argparse
import os
import sys
from dataclasses import dataclass


class ChannelError(ValueError):
    pass


@dataclass(frozen=True)
class ReleaseTarget:
    release_version: str
    status: str
    purpose: str | None


def inspect(cur, channel: str, target: str) -> tuple[str | None, ReleaseTarget]:
    cur.execute(
        """
        select release_version
        from audit.release_channel
        where channel_code=%s
        """,
        (channel,),
    )
    row = cur.fetchone()
    current = row[0] if row else None

    cur.execute(
        """
        select release_version, status, manifest->>'purpose'
        from audit.release_manifest
        where release_version=%s
        """,
        (target,),
    )
    row = cur.fetchone()
    if not row:
        raise ChannelError(f"target release {target!r} does not exist")

    release = ReleaseTarget(row[0], row[1], row[2])
    if release.status != "published":
        raise ChannelError(
            f"target release {target!r} has status {release.status!r}, expected 'published'"
        )
    if release.purpose != channel:
        raise ChannelError(
            f"target release {target!r} has purpose {release.purpose!r}, expected {channel!r}"
        )
    return current, release


def repoint(
    conn,
    *,
    channel: str,
    target: str,
    expected_current: str | None,
    allow_initialize: bool,
    updated_by: str | None,
    note: str | None,
) -> tuple[str | None, str]:
    with conn.cursor() as cur:
        cur.execute(
            """
            select release_version
            from audit.release_channel
            where channel_code=%s
            for update
            """,
            (channel,),
        )
        locked = cur.fetchone()
        current = locked[0] if locked else None

        _, release = inspect(cur, channel, target)

        if current is None:
            if not allow_initialize:
                raise ChannelError(
                    f"channel {channel!r} is uninitialized; pass --allow-initialize explicitly"
                )
            cur.execute(
                """
                insert into audit.release_channel(
                    channel_code, release_version, updated_by, note
                ) values (%s,%s,%s,%s)
                """,
                (channel, target, updated_by, note),
            )
        else:
            if expected_current is None:
                raise ChannelError(
                    "an existing channel move requires --expected-current for compare-and-set safety"
                )
            if current != expected_current:
                raise ChannelError(
                    f"channel {channel!r} currently points to {current!r}, "
                    f"not expected {expected_current!r}"
                )
            cur.execute(
                """
                update audit.release_channel
                set release_version=%s, updated_by=%s, note=%s
                where channel_code=%s and release_version=%s
                """,
                (target, updated_by, note, channel, expected_current),
            )
            if cur.rowcount != 1:
                raise ChannelError("release channel compare-and-set update affected no row")

        cur.execute(
            "select release_version from audit.release_channel where channel_code=%s",
            (channel,),
        )
        moved = cur.fetchone()
        if not moved or moved[0] != release.release_version:
            raise ChannelError("release channel verification failed after update")

    return current, release.release_version


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("target_release")
    parser.add_argument("--channel", default="public_mvp_preview")
    parser.add_argument("--expected-current")
    parser.add_argument("--allow-initialize", action="store_true")
    parser.add_argument("--updated-by", default=os.environ.get("GITHUB_ACTOR"))
    parser.add_argument("--note")
    parser.add_argument("--dsn", default=os.environ.get("DATABASE_URL"))
    parser.add_argument("--apply", action="store_true")
    args = parser.parse_args()

    if not args.dsn:
        parser.error("--dsn or DATABASE_URL is required")

    try:
        import psycopg
    except ImportError as exc:
        raise SystemExit("psycopg is required; run through the tooling container") from exc

    try:
        with psycopg.connect(args.dsn, autocommit=False) as conn:
            with conn.cursor() as cur:
                current, target = inspect(cur, args.channel, args.target_release)

            print(
                f"READY: channel={args.channel} current={current or '<uninitialized>'} "
                f"target={target.release_version}"
            )

            if not args.apply:
                conn.rollback()
                print("DRY RUN: no database changes made")
                return 0

            try:
                with conn.transaction():
                    before, after = repoint(
                        conn,
                        channel=args.channel,
                        target=args.target_release,
                        expected_current=args.expected_current,
                        allow_initialize=args.allow_initialize,
                        updated_by=args.updated_by,
                        note=args.note,
                    )
            except Exception:
                conn.rollback()
                raise

        print(
            f"APPLIED: channel={args.channel} "
            f"{before or '<uninitialized>'} -> {after}"
        )
        return 0
    except ChannelError as exc:
        print(f"BLOCK: {exc}", file=sys.stderr)
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
