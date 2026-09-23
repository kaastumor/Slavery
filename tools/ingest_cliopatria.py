#!/usr/bin/env python3
"""Load the exact pinned Cliopatria corpus into disposable raw/staging PostGIS.

M2 #119 deliberately stops before atlas entity resolution or publication.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import os
from pathlib import Path
import sys
import urllib.request
import uuid

from psycopg.types.json import Jsonb

from profile_cliopatria import (
    UPSTREAM_COMMIT,
    UPSTREAM_GIT_BLOB_SHA1,
    UPSTREAM_PATH,
    UPSTREAM_RELEASE,
    UPSTREAM_REPO,
    UPSTREAM_URL,
    git_blob_sha1,
    load_features,
    profile,
)

UPSTREAM_SHA256 = "d01ae3a20d358cc5d54f69d9d725d390767d9c8759ac89ad6f90c58d106f3370"
UPSTREAM_SIZE_BYTES = 44_231_317
DATASET_KEY = f"cliopatria:{UPSTREAM_RELEASE}:{UPSTREAM_COMMIT}"
SOURCE_CRS = "EPSG:4326"

SOURCE_ID = uuid.uuid5(uuid.NAMESPACE_URL, "hsa:source:cliopatria")
SOURCE_VERSION_ID = uuid.uuid5(
    uuid.NAMESPACE_URL, f"hsa:source-version:cliopatria:{UPSTREAM_COMMIT}:{UPSTREAM_SHA256}"
)
SOURCE_ASSET_ID = uuid.uuid5(
    uuid.NAMESPACE_URL, f"hsa:source-asset:cliopatria:{UPSTREAM_COMMIT}:{UPSTREAM_SHA256}"
)
INGEST_RUN_ID = uuid.uuid5(
    uuid.NAMESPACE_URL, f"hsa:ingest:cliopatria:{UPSTREAM_COMMIT}:{UPSTREAM_SHA256}"
)


def canonical_json(value: object) -> str:
    return json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(",", ":"))


def feature_checksum(feature: dict) -> str:
    return hashlib.sha256(canonical_json(feature).encode("utf-8")).hexdigest()


def raw_record_id(ordinal: int) -> uuid.UUID:
    return uuid.uuid5(
        uuid.NAMESPACE_URL,
        f"hsa:raw:cliopatria:{UPSTREAM_COMMIT}:{UPSTREAM_SHA256}:{ordinal}",
    )


def text_projection(value: object) -> str | None:
    if value is None:
        return None
    if isinstance(value, str):
        return value
    return canonical_json(value)


def feature_projection(feature: dict, ordinal: int) -> tuple:
    properties = feature.get("properties") or {}
    geometry = feature.get("geometry")
    feature_id = feature.get("id")
    return (
        ordinal,
        raw_record_id(ordinal),
        text_projection(feature_id),
        Jsonb(feature),
        feature_checksum(feature),
        text_projection(properties.get("Name")),
        text_projection(properties.get("Type")),
        properties.get("FromYear"),
        properties.get("ToYear"),
        text_projection(properties.get("MemberOf")),
        text_projection(properties.get("Components")),
        text_projection(properties.get("SeshatID")),
        text_projection(properties.get("Wikidata")),
        text_projection(properties.get("Wikipedia")),
        Jsonb(geometry) if geometry is not None else None,
    )


def load_asset(input_path: Path | None, cache_path: Path | None) -> bytes:
    if input_path is not None:
        return input_path.read_bytes()
    if cache_path is not None and cache_path.exists():
        return cache_path.read_bytes()

    request = urllib.request.Request(
        UPSTREAM_URL,
        headers={"User-Agent": "historical-slavery-atlas-cliopatria-ingest/1"},
    )
    with urllib.request.urlopen(request, timeout=120) as response:
        data = response.read()

    if cache_path is not None:
        cache_path.parent.mkdir(parents=True, exist_ok=True)
        cache_path.write_bytes(data)
    return data


def verify_asset(data: bytes) -> None:
    if len(data) != UPSTREAM_SIZE_BYTES:
        raise ValueError(
            f"Cliopatria asset size mismatch: {len(data)} != {UPSTREAM_SIZE_BYTES}"
        )
    blob = git_blob_sha1(data)
    if blob != UPSTREAM_GIT_BLOB_SHA1:
        raise ValueError(
            f"Cliopatria Git blob mismatch: {blob} != {UPSTREAM_GIT_BLOB_SHA1}"
        )
    sha256 = hashlib.sha256(data).hexdigest()
    if sha256 != UPSTREAM_SHA256:
        raise ValueError(
            f"Cliopatria SHA-256 mismatch: {sha256} != {UPSTREAM_SHA256}"
        )


def verify_expected_profile(features: list[dict], expected_profile_path: Path) -> None:
    expected = json.loads(expected_profile_path.read_text(encoding="utf-8"))
    source = expected.get("source") or {}
    if source.get("commit") != UPSTREAM_COMMIT:
        raise ValueError("expected profile commit does not match pinned Cliopatria commit")
    if source.get("git_blob_sha1") != UPSTREAM_GIT_BLOB_SHA1:
        raise ValueError("expected profile Git blob does not match pinned Cliopatria asset")
    if source.get("sha256") != UPSTREAM_SHA256:
        raise ValueError("expected profile SHA-256 does not match pinned Cliopatria asset")

    actual = profile(features)
    if actual != expected.get("profile"):
        raise ValueError(
            "full-corpus profile differs from checked validation/cliopatria_v0.2.0_profile.json"
        )


def prepare_schema(conn, schema_sql: Path) -> None:
    with conn.cursor() as cur:
        cur.execute(schema_sql.read_text(encoding="utf-8"))
    conn.commit()


def _existing_dataset(conn) -> dict | None:
    with conn.cursor() as cur:
        cur.execute(
            """
            SELECT dataset_key, source_version_id, source_asset_id, ingest_run_id,
                   upstream_repository, upstream_release, upstream_commit, upstream_path,
                   git_blob_sha1, asset_sha256, feature_count, source_crs, status
            FROM staging.cliopatria_dataset
            WHERE dataset_key=%s
            """,
            (DATASET_KEY,),
        )
        row = cur.fetchone()
        if row is None:
            return None
        columns = [d.name for d in cur.description]
        return dict(zip(columns, row))


def verify_existing_dataset(conn, metadata: dict, expected_count: int) -> None:
    expected = {
        "dataset_key": DATASET_KEY,
        "source_version_id": SOURCE_VERSION_ID,
        "source_asset_id": SOURCE_ASSET_ID,
        "ingest_run_id": INGEST_RUN_ID,
        "upstream_repository": UPSTREAM_REPO,
        "upstream_release": UPSTREAM_RELEASE,
        "upstream_commit": UPSTREAM_COMMIT,
        "upstream_path": UPSTREAM_PATH,
        "git_blob_sha1": UPSTREAM_GIT_BLOB_SHA1,
        "asset_sha256": UPSTREAM_SHA256,
        "feature_count": expected_count,
        "source_crs": SOURCE_CRS,
        "status": "completed",
    }
    for key, expected_value in expected.items():
        if metadata.get(key) != expected_value:
            raise RuntimeError(
                f"existing Cliopatria dataset metadata drift for {key}: "
                f"{metadata.get(key)!r} != {expected_value!r}"
            )

    with conn.cursor() as cur:
        cur.execute(
            "SELECT count(*) FROM staging.cliopatria_feature WHERE dataset_key=%s",
            (DATASET_KEY,),
        )
        staging_count = cur.fetchone()[0]
        cur.execute(
            """
            SELECT count(*) FROM raw.raw_record
            WHERE ingest_run_id=%s AND record_type='cliopatria_feature'
            """,
            (INGEST_RUN_ID,),
        )
        raw_count = cur.fetchone()[0]
    if staging_count != expected_count or raw_count != expected_count:
        raise RuntimeError(
            "existing Cliopatria load is incomplete: "
            f"staging={staging_count}, raw={raw_count}, expected={expected_count}"
        )


def register_source_metadata(conn, code_version: str) -> None:
    with conn.cursor() as cur:
        cur.execute(
            """
            INSERT INTO atlas.source(
                source_id, title, author_or_institution, source_type,
                source_classification, geographic_scope, temporal_scope,
                reliability_limitations, notes
            ) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s)
            ON CONFLICT (source_id) DO NOTHING
            """,
            (
                SOURCE_ID,
                "Cliopatria",
                "Seshat Global History Databank",
                "geospatial dataset",
                "dataset",
                "global",
                "3400 BCE to 2024 CE (source convention)",
                "One reconstruction of historical polity extent; border, naming and duration uncertainty remain. Raw availability is not atlas geometry approval.",
                "Pinned for M2 raw geography integration under D-059.",
            ),
        )
        cur.execute(
            """
            INSERT INTO atlas.source_version(
                source_version_id, source_id, version_label,
                url_or_identifier, license_status, redistribution_status, notes
            ) VALUES (%s,%s,%s,%s,%s,%s,%s)
            ON CONFLICT (source_version_id) DO NOTHING
            """,
            (
                SOURCE_VERSION_ID,
                SOURCE_ID,
                f"{UPSTREAM_RELEASE} @ {UPSTREAM_COMMIT}",
                UPSTREAM_URL,
                "CC BY 4.0",
                "permitted with attribution",
                "Exact pinned Git commit and asset checksum; source-native years/hierarchy preserved.",
            ),
        )
        cur.execute(
            """
            INSERT INTO atlas.source_asset(
                source_asset_id, source_version_id, filename_or_object_key,
                media_type, checksum_sha256, storage_location,
                redistribution_status, notes
            ) VALUES (%s,%s,%s,%s,%s,%s,%s,%s)
            ON CONFLICT (source_asset_id) DO NOTHING
            """,
            (
                SOURCE_ASSET_ID,
                SOURCE_VERSION_ID,
                UPSTREAM_PATH,
                "application/zip",
                UPSTREAM_SHA256,
                UPSTREAM_URL,
                "CC BY 4.0; upstream asset not vendored in repository",
                f"Git blob SHA-1 {UPSTREAM_GIT_BLOB_SHA1}",
            ),
        )

        cur.execute(
            """
            SELECT source_id, version_label, url_or_identifier, license_status
            FROM atlas.source_version WHERE source_version_id=%s
            """,
            (SOURCE_VERSION_ID,),
        )
        version = cur.fetchone()
        if version != (
            SOURCE_ID,
            f"{UPSTREAM_RELEASE} @ {UPSTREAM_COMMIT}",
            UPSTREAM_URL,
            "CC BY 4.0",
        ):
            raise RuntimeError("existing Cliopatria SOURCE_VERSION conflicts with pinned metadata")

        cur.execute(
            """
            SELECT source_version_id, checksum_sha256
            FROM atlas.source_asset WHERE source_asset_id=%s
            """,
            (SOURCE_ASSET_ID,),
        )
        asset = cur.fetchone()
        if asset != (SOURCE_VERSION_ID, UPSTREAM_SHA256):
            raise RuntimeError("existing Cliopatria SOURCE_ASSET conflicts with pinned metadata")

        cur.execute(
            """
            INSERT INTO audit.ingest_run(
                ingest_run_id, source_version_id, source_asset_id,
                code_version, status, notes
            ) VALUES (%s,%s,%s,%s,'started',%s)
            """,
            (
                INGEST_RUN_ID,
                SOURCE_VERSION_ID,
                SOURCE_ASSET_ID,
                code_version,
                "M2 #119 disposable full-corpus raw/staging ingestion; not publication.",
            ),
        )


def ingest_features(conn, features: list[dict], code_version: str) -> None:
    register_source_metadata(conn, code_version)
    expected_count = len(features)

    with conn.cursor() as cur:
        cur.execute(
            """
            INSERT INTO staging.cliopatria_dataset(
                dataset_key, source_version_id, source_asset_id, ingest_run_id,
                upstream_repository, upstream_release, upstream_commit, upstream_path,
                git_blob_sha1, asset_sha256, feature_count, source_crs, status, notes
            ) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,'loading',%s)
            """,
            (
                DATASET_KEY,
                SOURCE_VERSION_ID,
                SOURCE_ASSET_ID,
                INGEST_RUN_ID,
                UPSTREAM_REPO,
                UPSTREAM_RELEASE,
                UPSTREAM_COMMIT,
                UPSTREAM_PATH,
                UPSTREAM_GIT_BLOB_SHA1,
                UPSTREAM_SHA256,
                expected_count,
                SOURCE_CRS,
                "Raw source rows only; no POLITY/RELATION flattening or atlas identity resolution.",
            ),
        )

        cur.execute(
            """
            CREATE TEMP TABLE cliopatria_load_buffer (
                source_row_ordinal integer NOT NULL,
                raw_record_id uuid NOT NULL,
                source_feature_id text,
                raw_payload jsonb NOT NULL,
                feature_sha256 text NOT NULL,
                name_raw text,
                type_raw text,
                from_year_raw integer,
                to_year_raw integer,
                member_of_raw text,
                components_raw text,
                seshat_id_raw text,
                wikidata_raw text,
                wikipedia_raw text,
                geometry_json jsonb
            ) ON COMMIT DROP
            """
        )

        with cur.copy(
            """
            COPY cliopatria_load_buffer(
                source_row_ordinal, raw_record_id, source_feature_id,
                raw_payload, feature_sha256, name_raw, type_raw,
                from_year_raw, to_year_raw, member_of_raw, components_raw,
                seshat_id_raw, wikidata_raw, wikipedia_raw, geometry_json
            ) FROM STDIN
            """
        ) as copy:
            for ordinal, feature in enumerate(features, start=1):
                copy.write_row(feature_projection(feature, ordinal))

        cur.execute(
            """
            INSERT INTO raw.raw_record(
                raw_record_id, ingest_run_id, record_type, source_native_id,
                raw_payload, checksum_sha256
            )
            SELECT raw_record_id, %s, 'cliopatria_feature', source_feature_id,
                   raw_payload, feature_sha256
            FROM cliopatria_load_buffer
            ORDER BY source_row_ordinal
            """,
            (INGEST_RUN_ID,),
        )

        cur.execute(
            """
            INSERT INTO staging.cliopatria_feature(
                dataset_key, source_row_ordinal, raw_record_id, source_feature_id,
                name_raw, type_raw, from_year_raw, to_year_raw,
                member_of_raw, components_raw, seshat_id_raw,
                wikidata_raw, wikipedia_raw, geom
            )
            SELECT %s, source_row_ordinal, raw_record_id, source_feature_id,
                   name_raw, type_raw, from_year_raw, to_year_raw,
                   member_of_raw, components_raw, seshat_id_raw,
                   wikidata_raw, wikipedia_raw,
                   CASE
                       WHEN geometry_json IS NULL THEN NULL
                       ELSE ST_SetSRID(ST_GeomFromGeoJSON(geometry_json::text), 4326)
                   END
            FROM cliopatria_load_buffer
            ORDER BY source_row_ordinal
            """,
            (DATASET_KEY,),
        )

        cur.execute(
            """
            UPDATE staging.cliopatria_dataset
            SET status='completed', loaded_at=now()
            WHERE dataset_key=%s
            """,
            (DATASET_KEY,),
        )
        cur.execute(
            """
            UPDATE audit.ingest_run
            SET status='completed', completed_at=now()
            WHERE ingest_run_id=%s
            """,
            (INGEST_RUN_ID,),
        )


def database_counts(conn) -> dict:
    with conn.cursor() as cur:
        cur.execute(
            """
            SELECT
                count(*) AS feature_count,
                count(*) FILTER (WHERE type_raw='POLITY') AS polity_rows,
                count(*) FILTER (WHERE type_raw='RELATION') AS relation_rows,
                count(DISTINCT name_raw) AS distinct_names,
                min(from_year_raw) AS source_min_year,
                max(to_year_raw) AS source_max_year
            FROM staging.cliopatria_feature
            WHERE dataset_key=%s
            """,
            (DATASET_KEY,),
        )
        row = cur.fetchone()
    return {
        "feature_count": row[0],
        "polity_rows": row[1],
        "relation_rows": row[2],
        "distinct_names": row[3],
        "source_min_year": row[4],
        "source_max_year": row[5],
    }


def run_reconciliation(conn, path: Path) -> None:
    with conn.cursor() as cur:
        cur.execute(path.read_text(encoding="utf-8"))
    conn.commit()


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--dsn", default=os.environ.get("DATABASE_URL"))
    parser.add_argument("--input", type=Path)
    parser.add_argument("--cache-path", type=Path)
    parser.add_argument("--schema-sql", type=Path, required=True)
    parser.add_argument("--expected-profile", type=Path, required=True)
    parser.add_argument("--reconcile-sql", type=Path)
    parser.add_argument("--report", type=Path)
    parser.add_argument("--code-version", default=os.environ.get("GITHUB_SHA", "working-tree"))
    args = parser.parse_args()

    if not args.dsn:
        parser.error("--dsn or DATABASE_URL is required")

    data = load_asset(args.input, args.cache_path)
    verify_asset(data)
    features = load_features(data)
    verify_expected_profile(features, args.expected_profile)

    import psycopg

    action = "inserted"
    with psycopg.connect(args.dsn, autocommit=False) as conn:
        prepare_schema(conn, args.schema_sql)
        existing = _existing_dataset(conn)
        if existing is not None:
            verify_existing_dataset(conn, existing, len(features))
            action = "noop"
        else:
            try:
                with conn.transaction():
                    ingest_features(conn, features, args.code_version)
            except Exception:
                conn.rollback()
                raise

        if args.reconcile_sql:
            run_reconciliation(conn, args.reconcile_sql)
        counts = database_counts(conn)

    report = {
        "action": action,
        "dataset_key": DATASET_KEY,
        "source": {
            "repository": UPSTREAM_REPO,
            "release": UPSTREAM_RELEASE,
            "commit": UPSTREAM_COMMIT,
            "path": UPSTREAM_PATH,
            "git_blob_sha1": UPSTREAM_GIT_BLOB_SHA1,
            "sha256": UPSTREAM_SHA256,
            "size_bytes": len(data),
        },
        "database": counts,
        "promotion": "none; disposable raw/staging integration only",
    }
    rendered = json.dumps(report, indent=2, sort_keys=True) + "\n"
    if args.report:
        args.report.parent.mkdir(parents=True, exist_ok=True)
        args.report.write_text(rendered, encoding="utf-8")
    print(rendered, end="")
    return 0


if __name__ == "__main__":
    sys.exit(main())
