#!/usr/bin/env python3
"""Load one canonical land fabric into cartography.land_fabric.

The atlas basemap and published historical polygon clipping should use the same
immutable source URL. This loader preserves source commit/blob IDs and content
checksums, and activates exactly one fabric at a time.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import os
import urllib.request

import psycopg

DEFAULT_URL = (
    "https://raw.githubusercontent.com/nvkelso/natural-earth-vector/"
    "ca96624a56bd078437bca8184e78163e5039ad19/"
    "geojson/ne_10m_land.geojson"
)
DEFAULT_FABRIC_ID = "natural-earth-ne_10m_land-v5.1.1-ca96624"
DEFAULT_SOURCE_NAME = "Natural Earth land"
DEFAULT_SOURCE_VERSION = "5.1.1"
DEFAULT_COMMIT_SHA = "ca96624a56bd078437bca8184e78163e5039ad19"
DEFAULT_BLOB_SHA = "2d76878175b8054acd9c5a52917ee9ea59a36fc5"


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument("--database-url", default=os.environ.get("DATABASE_URL"))
    parser.add_argument("--source-url", default=DEFAULT_URL)
    parser.add_argument("--fabric-id", default=DEFAULT_FABRIC_ID)
    parser.add_argument("--source-name", default=DEFAULT_SOURCE_NAME)
    parser.add_argument("--source-version", default=DEFAULT_SOURCE_VERSION)
    parser.add_argument("--source-commit-sha", default=DEFAULT_COMMIT_SHA)
    parser.add_argument("--source-blob-sha", default=DEFAULT_BLOB_SHA)
    parser.add_argument("--file", help="Read GeoJSON from a local file instead of source-url")
    return parser.parse_args()


def load_bytes(args: argparse.Namespace) -> bytes:
    if args.file:
        with open(args.file, "rb") as handle:
            return handle.read()

    with urllib.request.urlopen(args.source_url, timeout=120) as response:
        if response.status != 200:
            raise RuntimeError(f"source returned HTTP {response.status}")
        return response.read()


def main() -> None:
    args = parse_args()
    if not args.database_url:
        raise SystemExit("DATABASE_URL or --database-url is required")

    raw = load_bytes(args)
    document = json.loads(raw.decode("utf-8"))
    if document.get("type") != "FeatureCollection":
        raise SystemExit("expected GeoJSON FeatureCollection")

    content_md5 = hashlib.md5(raw).hexdigest()
    content_sha256 = hashlib.sha256(raw).hexdigest()

    sql = """
    with source_geojson as (
        select %s::jsonb as doc
    ),
    features as (
        select jsonb_array_elements(doc->'features') as feature
        from source_geojson
    ),
    land as (
        select st_multi(
                 st_collectionextract(
                   st_unaryunion(
                     st_collect(
                       st_setsrid(
                         st_geomfromgeojson((feature->'geometry')::text),
                         4326
                       )
                     )
                   ),
                   3
                 )
               ) as geom
        from features
    ),
    deactivate as (
        update cartography.land_fabric
        set active=false
        where active
        returning fabric_id
    )
    insert into cartography.land_fabric(
        fabric_id,
        source_name,
        source_version,
        source_url,
        source_commit_sha,
        source_blob_sha,
        content_md5,
        content_sha256,
        active,
        geom,
        created_at
    )
    select %s,%s,%s,%s,%s,%s,%s,%s,true,geom,now()
    from land
    on conflict (fabric_id) do update set
        source_name=excluded.source_name,
        source_version=excluded.source_version,
        source_url=excluded.source_url,
        source_commit_sha=excluded.source_commit_sha,
        source_blob_sha=excluded.source_blob_sha,
        content_md5=excluded.content_md5,
        content_sha256=excluded.content_sha256,
        active=true,
        geom=excluded.geom,
        created_at=now();
    """

    with psycopg.connect(args.database_url) as conn:
        with conn.cursor() as cur:
            cur.execute(
                sql,
                (
                    json.dumps(document, separators=(",", ":")),
                    args.fabric_id,
                    args.source_name,
                    args.source_version,
                    args.source_url,
                    args.source_commit_sha,
                    args.source_blob_sha,
                    content_md5,
                    content_sha256,
                ),
            )
        conn.commit()

    print(
        json.dumps(
            {
                "fabric_id": args.fabric_id,
                "source_version": args.source_version,
                "source_url": args.source_url,
                "source_commit_sha": args.source_commit_sha,
                "source_blob_sha": args.source_blob_sha,
                "content_md5": content_md5,
                "content_sha256": content_sha256,
                "bytes": len(raw),
            },
            indent=2,
        )
    )


if __name__ == "__main__":
    main()
