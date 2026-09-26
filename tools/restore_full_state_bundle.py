#!/usr/bin/env python3
"""Restore a Gate-3 preservation bundle into an empty migrated database.

This is a disaster-recovery proof for the reviewed canonical-research closure.
It never drops objects, never targets production implicitly, and commits only after
the restored composite object snapshots exactly match the frozen bundle digests.

Cartography is reconstructed separately from its pinned source using
tools/load_land_fabric.py; this tool restores the frozen cartography metadata timestamp
and verifies the pinned geometry/source digest.
"""
from __future__ import annotations

import argparse
import json
import os
from pathlib import Path
from typing import Any

import psycopg
from psycopg import sql

from full_state_release_bundle import (
    BundleError,
    object_digests,
    sha256_value,
    snapshot_objects,
    validate_bundle,
)


TOP_LEVEL_EMPTY = (
    ("atlas", "source_version"),
    ("atlas", "actor"),
    ("atlas", "spatial_entity"),
    ("atlas", "geometry"),
    ("atlas", "claim"),
    ("atlas", "voyage"),
    ("audit", "research_coverage_assessment"),
    ("audit", "research_target_result"),
)


def writable_columns(cur, schema: str, table: str) -> list[str]:
    cur.execute(
        """
        select column_name
        from information_schema.columns
        where table_schema=%s
          and table_name=%s
          and is_generated='NEVER'
          and identity_generation is null
        order by ordinal_position
        """,
        (schema, table),
    )
    cols = [row[0] for row in cur.fetchall()]
    if not cols:
        raise BundleError(f"table not found or has no writable columns: {schema}.{table}")
    return cols


def insert_record(cur, table_name: str, payload: dict[str, Any]) -> None:
    schema, table = table_name.split(".", 1)
    cols = writable_columns(cur, schema, table)
    col_sql = sql.SQL(",").join(sql.Identifier(c) for c in cols)
    select_sql = sql.SQL(",").join(
        sql.SQL("r.{}").format(sql.Identifier(c)) for c in cols
    )
    statement = sql.SQL(
        "insert into {}.{} ({}) "
        "select {} from jsonb_populate_record(null::{}.{}, %s::jsonb) as r "
        "on conflict do nothing"
    ).format(
        sql.Identifier(schema),
        sql.Identifier(table),
        col_sql,
        select_sql,
        sql.Identifier(schema),
        sql.Identifier(table),
    )
    cur.execute(statement, (json.dumps(payload, ensure_ascii=False),))


def require_empty_target(cur) -> None:
    occupied: list[str] = []
    for schema, table in TOP_LEVEL_EMPTY:
        cur.execute(
            sql.SQL("select count(*) from {}.{}").format(
                sql.Identifier(schema), sql.Identifier(table)
            )
        )
        count = int(cur.fetchone()[0])
        if count:
            occupied.append(f"{schema}.{table}={count}")
    if occupied:
        raise BundleError(
            "recovery target is not empty; refusing to merge frozen state into "
            + ", ".join(occupied)
        )


def restore_sources(cur, bundle: dict[str, Any]) -> None:
    for obj in bundle["objects"]["source_versions"].values():
        insert_record(cur, "atlas.source", obj["source"])
    for obj in bundle["objects"]["source_versions"].values():
        insert_record(cur, "atlas.source_version", obj["source_version"])
    for obj in bundle["objects"]["source_versions"].values():
        for asset in obj.get("assets", []):
            insert_record(cur, "atlas.source_asset", asset)


def restore_spatial(cur, bundle: dict[str, Any]) -> None:
    for obj in bundle["objects"]["spatial_entities"].values():
        insert_record(cur, "atlas.spatial_entity", obj["spatial_entity"])
    for obj in bundle["objects"]["spatial_entities"].values():
        if obj.get("polity"):
            insert_record(cur, "atlas.polity", obj["polity"])
    for obj in bundle["objects"]["geometries"].values():
        payload = dict(obj)
        geom_hex = payload.pop("geom_ewkb_hex", None)
        payload.pop("geom_srid", None)
        if geom_hex is None:
            insert_record(cur, "atlas.geometry", payload)
        else:
            schema, table = "atlas", "geometry"
            cols = writable_columns(cur, schema, table)
            base_cols = [c for c in cols if c != "geom"]
            col_sql = sql.SQL(",").join(
                sql.Identifier(c) for c in base_cols + ["geom"]
            )
            select_sql = sql.SQL(",").join(
                [sql.SQL("r.{}").format(sql.Identifier(c)) for c in base_cols]
                + [sql.SQL("st_geomfromewkb(decode(%s,'hex'))")]
            )
            statement = sql.SQL(
                "insert into {}.{} ({}) select {} "
                "from jsonb_populate_record(null::{}.{}, %s::jsonb) as r "
                "on conflict do nothing"
            ).format(
                sql.Identifier(schema),
                sql.Identifier(table),
                col_sql,
                select_sql,
                sql.Identifier(schema),
                sql.Identifier(table),
            )
            cur.execute(
                statement,
                (geom_hex, json.dumps(payload, ensure_ascii=False)),
            )


def restore_actors(cur, bundle: dict[str, Any]) -> None:
    for obj in bundle["objects"]["actors"].values():
        insert_record(cur, "atlas.actor", obj["actor"])
    for obj in bundle["objects"]["actors"].values():
        for name in obj.get("names", []):
            insert_record(cur, "atlas.actor_name", name)


def restore_claims_and_voyages(cur, bundle: dict[str, Any]) -> None:
    claims = bundle["objects"]["claims"]
    voyages = bundle["objects"]["voyages"]

    for obj in claims.values():
        insert_record(cur, "atlas.claim", obj["claim"])
    for obj in voyages.values():
        insert_record(cur, "atlas.voyage", obj["voyage"])

    singleton_tables = (
        ("territorial_practice", "atlas.territorial_practice_claim"),
        ("external_participation", "atlas.external_participation_claim"),
        ("legal_event", "atlas.legal_event"),
        ("actor_attribute", "atlas.actor_attribute_claim"),
    )
    list_tables = (
        ("claim_sources", "atlas.claim_source"),
        ("asserted_intervals", "atlas.claim_asserted_interval"),
        ("evidence_loci", "atlas.claim_evidence_locus"),
        ("inference_extents", "atlas.claim_inference_extent"),
        ("practice_facets", "atlas.practice_facet_assertion"),
        ("spatial_relations", "atlas.spatial_relation"),
        ("voyage_owners", "atlas.voyage_owner"),
        ("voyage_finance", "atlas.voyage_finance"),
        ("voyage_stops", "atlas.voyage_stop"),
    )
    for obj in claims.values():
        for key, table in singleton_tables:
            if obj.get(key):
                insert_record(cur, table, obj[key])
        for key, table in list_tables:
            for row in obj.get(key, []):
                insert_record(cur, table, row)

    # Voyage snapshots repeat relation rows so the voyage is self-contained.
    # ON CONFLICT DO NOTHING de-duplicates the exact frozen rows.
    for obj in voyages.values():
        for row in obj.get("owners", []):
            insert_record(cur, "atlas.voyage_owner", row)
        for row in obj.get("finance", []):
            insert_record(cur, "atlas.voyage_finance", row)
        for row in obj.get("stops", []):
            insert_record(cur, "atlas.voyage_stop", row)


def restore_coverage(cur, bundle: dict[str, Any]) -> None:
    for obj in bundle["objects"]["coverage_assessments"].values():
        insert_record(
            cur,
            "audit.research_coverage_assessment",
            obj["coverage_assessment"],
        )
    for obj in bundle["objects"]["coverage_assessments"].values():
        for row in obj.get("sources", []):
            insert_record(cur, "audit.research_coverage_source", row)


def restore_research_results(cur, bundle: dict[str, Any]) -> None:
    for obj in bundle["objects"]["research_target_results"].values():
        insert_record(cur, "audit.research_target", obj["target"])
    for obj in bundle["objects"]["research_target_results"].values():
        insert_record(cur, "audit.research_target_result", obj["result"])
    for obj in bundle["objects"]["research_target_results"].values():
        for row in obj.get("reviews", []):
            insert_record(cur, "audit.research_target_review", row)
        for row in obj.get("sources", []):
            insert_record(cur, "audit.research_target_source", row)
        for row in obj.get("claim_bridges", []):
            insert_record(cur, "audit.research_target_claim", row)


def reconcile_cartography_metadata(
    cur, bundle: dict[str, Any], fingerprint: dict[str, Any]
) -> dict[str, Any]:
    frozen = bundle["cartography"]
    if frozen.get("kind") != "land_fabric":
        raise BundleError("Gate-3 recovery proof expects pinned land_fabric cartography")

    payload = dict(frozen["payload"])
    expected_id = str(frozen["id"])

    cur.execute(
        """
        select
          fabric_id,
          source_commit_sha,
          source_blob_sha,
          content_sha256,
          st_srid(geom),
          geometrytype(geom),
          st_numgeometries(geom),
          st_npoints(geom),
          round(st_area(geom::geography)::numeric,3)::text,
          encode(digest(st_asbinary(st_normalize(geom)),'sha256'),'hex'),
          octet_length(st_asbinary(st_normalize(geom))),
          encode(digest(st_asewkb(geom),'sha256'),'hex'),
          octet_length(st_asewkb(geom))
        from cartography.land_fabric
        where active
        """
    )
    rows = cur.fetchall()
    if len(rows) != 1:
        raise BundleError(f"expected exactly one active land fabric; found {len(rows)}")
    row = rows[0]
    observed = {
        "fabric_id": str(row[0]),
        "source_commit_sha": str(row[1]),
        "source_blob_sha": str(row[2]),
        "content_sha256": str(row[3]),
        "srid": int(row[4]),
        "geometry_type": str(row[5]),
        "component_count": int(row[6]),
        "point_count": int(row[7]),
        "geodesic_area_m2_rounded_3": str(row[8]),
        "normalized_wkb_sha256": str(row[9]),
        "normalized_wkb_bytes": int(row[10]),
        "runtime_raw_ewkb_sha256": str(row[11]),
        "runtime_raw_ewkb_bytes": int(row[12]),
    }

    expected = portable_cartography_fingerprint(fingerprint)
    actual = portable_cartography_fingerprint(observed)
    if actual != expected:
        raise BundleError(
            "portable cartography fingerprint mismatch: "
            + json.dumps({"expected": expected, "observed": actual}, sort_keys=True)
        )

    if expected_id != expected["fabric_id"]:
        raise BundleError("bundle/fingerprint land-fabric identity mismatch")
    if str(payload["content_sha256"]) != expected["content_sha256"]:
        raise BundleError("bundle/fingerprint source content SHA mismatch")
    if str(payload["source_commit_sha"]) != expected["source_commit_sha"]:
        raise BundleError("bundle/fingerprint source commit mismatch")
    if str(payload["source_blob_sha"]) != expected["source_blob_sha"]:
        raise BundleError("bundle/fingerprint source blob mismatch")

    # Raw EWKB is retained in the live bundle as an implementation fingerprint, but
    # PostGIS/GEOS versions may serialize equivalent unions differently. The portable
    # recovery invariant is the exact immutable source plus normalized geometry shape.
    cur.execute(
        """
        update cartography.land_fabric
           set created_at=%s
         where fabric_id=%s
        """,
        (payload["created_at"], expected_id),
    )
    return observed


def verify_restored_state(
    cur,
    bundle: dict[str, Any],
    fingerprint: dict[str, Any],
    cartography_observed: dict[str, Any],
) -> dict[str, Any]:
    membership = bundle["membership"]
    objects, cartography = snapshot_objects(cur, membership)
    current = object_digests(objects)
    expected = bundle["object_digests"]
    if current != expected:
        changed: list[str] = []
        for group in sorted(set(expected) | set(current)):
            expected_group = expected.get(group, {})
            current_group = current.get(group, {})
            for object_id in sorted(set(expected_group) | set(current_group)):
                if expected_group.get(object_id) != current_group.get(object_id):
                    changed.append(f"{group}:{object_id}")
        raise BundleError("restored object digest mismatch: " + ", ".join(changed))

    frozen_meta = dict(bundle["cartography"]["payload"])
    runtime_meta = dict(cartography["payload"])
    for key in ("geom_ewkb_sha256", "geom_ewkb_bytes"):
        frozen_meta.pop(key, None)
        runtime_meta.pop(key, None)
    if runtime_meta != frozen_meta:
        raise BundleError("restored cartography metadata differs from frozen bundle")

    portable = portable_cartography_fingerprint(fingerprint)
    logical_state = {
        "bundle_schema": bundle["bundle_schema"],
        "schema_version": bundle["release"]["schema_version"],
        "membership": membership,
        "object_digests": current,
        "cartography_recovery_fingerprint": portable,
    }
    return {
        "production_database_state_sha256": bundle["database_state_sha256"],
        "logical_recovery_state_sha256": sha256_value(logical_state),
        "cartography_portable_fingerprint_sha256": sha256_value(portable),
        "cartography_normalized_wkb_sha256": portable["normalized_wkb_sha256"],
        "runtime_raw_ewkb_sha256": cartography_observed[
            "runtime_raw_ewkb_sha256"
        ],
        "production_raw_ewkb_sha256": fingerprint["production_raw_ewkb_sha256"],
        "counts": {key: len(value) for key, value in membership.items()},
    }

def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("bundle", type=Path)
    parser.add_argument("--dsn", default=os.environ.get("DATABASE_URL"))
    parser.add_argument("--receipt", type=Path)
    args = parser.parse_args()
    if not args.dsn:
        parser.error("--dsn or DATABASE_URL is required")

    bundle = json.loads(args.bundle.read_text(encoding="utf-8"))
    validate_bundle(bundle)

    try:
        with psycopg.connect(args.dsn, autocommit=False) as conn:
            with conn.cursor() as cur:
                require_empty_target(cur)
                cartography_observed = reconcile_cartography_metadata(cur, bundle)
                restore_sources(cur, bundle)
                restore_spatial(cur, bundle)
                restore_actors(cur, bundle)
                restore_claims_and_voyages(cur, bundle)
                restore_coverage(cur, bundle)
                restore_research_results(cur, bundle)
                result = verify_restored_state(cur, bundle, cartography_observed)
            conn.commit()

        receipt = {
            "recovery_contract": "gate3-logical-reviewed-state-recovery-v2",
            "bundle_schema": bundle["bundle_schema"],
            "release_version": bundle["release"]["release_version"],
            "restored": True,
            "verification": "EXACT_OBJECT_DIGESTS_AND_PORTABLE_CARTOGRAPHY_MATCH",
            **result,
        }
        if args.receipt:
            args.receipt.parent.mkdir(parents=True, exist_ok=True)
            args.receipt.write_text(
                json.dumps(receipt, indent=2, sort_keys=True) + "\n",
                encoding="utf-8",
            )
        print(json.dumps(receipt, indent=2, sort_keys=True))
        return 0
    except (OSError, json.JSONDecodeError, BundleError, psycopg.Error) as exc:
        print(f"BLOCK: {exc}", file=__import__("sys").stderr)
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
