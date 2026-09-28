#!/usr/bin/env python3
"""Build immutable v0.8.1 map-fix serving materialization candidate.

This builder changes presentation geometry only. It preserves canonical v0.8.1
claim/source/identity membership and historical source geometry. Existing
v0.8.1-public-mvp-v1 files are read-only inputs and are never overwritten.
"""
from __future__ import annotations

import argparse
import copy
import hashlib
import json
from pathlib import Path
from typing import Any

from shapely import from_wkb, set_srid, to_wkb
from shapely.geometry import mapping
from shapely.validation import make_valid

from build_source_land_fidelity_candidates import (
    LAND_FABRIC_ID,
    LOSS_EPSILON_PCT,
    MAX_RECOVERY_ADDED_PCT,
    OUTSIDE_EPSILON_PCT,
    count_points,
    load_land,
    pct,
    polygonal,
    projectors,
    recovery_candidate,
)

ROOT = Path(__file__).resolve().parents[1]
OLD_ID = "v0.8.1-public-mvp-v1"
NEW_ID = "v0.8.1-public-mvp-v2"
AUTHORITY = ROOT / "data" / "release_candidates" / "v0.8.1-rome-geometry-authority.bundle.json"
OLD_PAYLOAD = ROOT / "data" / "serving" / OLD_ID / "atlas-data.json"
OLD_MANIFEST = ROOT / "data" / "serving" / OLD_ID / "materialization-manifest.json"
OLD_INDEX = ROOT / "web" / "public" / "release-geometries" / OLD_ID / "manifest.json"
NEW_SERVING_DIR = ROOT / "data" / "serving" / NEW_ID
NEW_ASSET_DIR = ROOT / "web" / "public" / "release-geometries" / NEW_ID
NEW_TS = ROOT / "supabase" / "functions" / "atlas-data" / "v081_v2_payload.ts"


class MapFixError(ValueError):
    pass


def load_json(path: Path) -> Any:
    return json.loads(path.read_text(encoding="utf-8"))


def compact_bytes(value: Any) -> bytes:
    return json.dumps(
        value,
        ensure_ascii=False,
        sort_keys=True,
        separators=(",", ":"),
    ).encode("utf-8")


def sha256_bytes(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def ewkb_sha256(geom) -> str:
    with_srid = set_srid(geom, 4326)
    data = to_wkb(
        with_srid,
        hex=False,
        output_dimension=2,
        byte_order=1,
        include_srid=True,
    )
    return hashlib.sha256(data).hexdigest()


def policy_for(source_url: str | None) -> str:
    if source_url and "Seshat-Global-History-Databank/cliopatria" in source_url:
        return "cliopatria-source-land-fidelity-v1"
    return "historical-source-land-fidelity-v1"


def semantic_projection(payload: dict[str, Any]) -> list[dict[str, Any]]:
    return [
        {
            "spatial_entity_id": place["spatial_entity_id"],
            "name": place["name"],
            "display_name": place.get("display_name"),
            "entity_type_code": place["entity_type_code"],
            "notes": place.get("notes"),
            "claims": place["claims"],
        }
        for place in payload["places"]
    ]


def stable_geometry_identity(record: dict[str, Any]) -> dict[str, Any]:
    excluded = {
        "geometry",
        "geometry_asset",
        "geometry_asset_materialization_id",
        "render_ewkb_sha256",
        "render_transform",
        "render_land_mask_id",
        "render_policy_id",
        "render_coastal_recovery_m",
        "render_smoothing_iterations",
        "render_qc",
    }
    return {key: value for key, value in record.items() if key not in excluded}


def build(land_path: Path, *, write: bool) -> dict[str, Any]:
    authority = load_json(AUTHORITY)
    old_payload = load_json(OLD_PAYLOAD)
    old_manifest = load_json(OLD_MANIFEST)
    old_index = load_json(OLD_INDEX)

    if old_payload.get("serving_materialization_id") != OLD_ID:
        raise MapFixError("unexpected predecessor materialization")
    if old_payload.get("release_version") != "v0.8.1":
        raise MapFixError("predecessor does not serve canonical v0.8.1")
    if old_payload.get("cartography", {}).get("fabric_id") != LAND_FABRIC_ID:
        raise MapFixError("predecessor land fabric mismatch")

    land_bytes = land_path.read_bytes()
    land_sha = sha256_bytes(land_bytes)
    expected_land_sha = old_payload["cartography"]["content_sha256"]
    if land_sha != expected_land_sha:
        raise MapFixError(
            f"land SHA mismatch expected={expected_land_sha} actual={land_sha}"
        )

    land = load_land(land_path)
    to_metric, to_wgs84 = projectors()
    land_m = to_metric(land)

    authority_geometries = authority["objects"]["geometries"]
    authority_sources = authority["objects"]["source_versions"]
    membership = set(authority["membership"]["geometry_ids"])

    old_records: dict[str, dict[str, Any]] = {}
    for place in old_payload["places"]:
        for record in place.get("geometries", []):
            gid = str(record["geometry_id"])
            if gid in old_records:
                raise MapFixError(f"duplicate geometry record {gid}")
            old_records[gid] = record

    old_index_rows = {
        str(row["geometry_id"]): row for row in old_index["assets"]
    }
    if set(old_records) != set(old_index_rows):
        raise MapFixError("predecessor payload/index geometry membership mismatch")
    if set(old_records) != membership:
        raise MapFixError("predecessor serving geometry membership differs from v0.8.1 authority")

    new_payload = copy.deepcopy(old_payload)
    new_payload["serving_materialization_id"] = NEW_ID
    new_payload["data_boundary"] = (
        "immutable_v081_release_materialization_render_asset_v2_source_land_fidelity"
    )

    new_record_map: dict[str, dict[str, Any]] = {}
    for place in new_payload["places"]:
        for record in place.get("geometries", []):
            new_record_map[str(record["geometry_id"])] = record

    new_index_rows: list[dict[str, Any]] = []
    asset_bytes: dict[str, bytes] = {}
    qc_rows: list[dict[str, Any]] = []
    corrected = 0
    reused = 0

    for old_index_row in old_index["assets"]:
        gid = str(old_index_row["geometry_id"])
        source_row = authority_geometries[gid]
        raw = from_wkb(bytes.fromhex(source_row["geom_ewkb_hex"]))
        record = new_record_map[gid]

        if raw.geom_type not in {"Polygon", "MultiPolygon"}:
            new_index_rows.append(copy.deepcopy(old_index_row))
            reused += 1
            continue

        source_version_id = str(source_row.get("geometry_source_version_id"))
        source_version = authority_sources.get(source_version_id, {})
        source_url = source_version.get("source_version", {}).get("url_or_identifier")
        raw = polygonal(make_valid(raw))
        source_land, candidate, recovery_used_m, added_pct = recovery_candidate(
            raw, land, to_metric, to_wgs84
        )

        source_land_m = polygonal(to_metric(source_land))
        candidate_m = polygonal(to_metric(candidate))
        source_land_loss_pct = pct(
            source_land_m.difference(candidate_m).area,
            source_land_m.area,
        )
        outside_land_pct = pct(
            candidate_m.difference(land_m).area,
            max(candidate_m.area, 1.0),
        )

        if source_land_loss_pct > LOSS_EPSILON_PCT:
            raise MapFixError(
                f"{gid}: candidate source-land loss {source_land_loss_pct}%"
            )
        if outside_land_pct > OUTSIDE_EPSILON_PCT:
            raise MapFixError(
                f"{gid}: candidate outside-land residual {outside_land_pct}%"
            )
        if added_pct > MAX_RECOVERY_ADDED_PCT:
            raise MapFixError(
                f"{gid}: accepted recovery exceeds {MAX_RECOVERY_ADDED_PCT}%"
            )

        predecessor_asset_path = ROOT / "web" / "public" / str(record["geometry_asset"])
        predecessor_asset = load_json(predecessor_asset_path)
        candidate_hash = ewkb_sha256(candidate)
        points = count_points(candidate)
        policy_id = policy_for(source_url)

        asset = copy.deepcopy(predecessor_asset)
        asset["materialization_id"] = NEW_ID
        asset["geometry"] = mapping(candidate)
        asset["render_ewkb_sha256"] = candidate_hash
        asset["render_points"] = points
        asset["render_transform"] = "source_land_fidelity"
        asset["render_land_mask_id"] = LAND_FABRIC_ID
        asset["render_policy_id"] = policy_id
        asset["render_coastal_recovery_m"] = recovery_used_m
        asset["render_smoothing_iterations"] = 0
        asset["render_qc"] = {
            "generator_kind": "offline_geos_source_land_fidelity",
            "source_land_loss_pct": source_land_loss_pct,
            "outside_land_pct": outside_land_pct,
            "coastal_added_vs_source_land_pct": added_pct,
            "source_npoints": count_points(raw),
            "render_npoints": points,
            "predecessor_asset_materialization_id": predecessor_asset.get(
                "materialization_id"
            ),
            "predecessor_render_policy_id": predecessor_asset.get("render_policy_id"),
        }
        asset_rel = f"release-geometries/{NEW_ID}/{gid}.json"
        encoded = compact_bytes(asset) + b"\n"
        asset_bytes[f"{gid}.json"] = encoded

        record["geometry"] = None
        record["geometry_asset"] = asset_rel
        record["geometry_asset_materialization_id"] = NEW_ID
        record["render_ewkb_sha256"] = candidate_hash
        record["render_transform"] = asset["render_transform"]
        record["render_land_mask_id"] = LAND_FABRIC_ID
        record["render_policy_id"] = policy_id
        record["render_coastal_recovery_m"] = recovery_used_m
        record["render_smoothing_iterations"] = 0
        record["render_qc"] = asset["render_qc"]

        index_row = copy.deepcopy(old_index_row)
        index_row["asset_materialization_id"] = NEW_ID
        index_row["path"] = asset_rel
        index_row["render_ewkb_sha256"] = candidate_hash
        index_row["render_points"] = points
        index_row["render_policy_id"] = policy_id
        index_row["render_transform"] = "source_land_fidelity"
        new_index_rows.append(index_row)

        qc_rows.append(
            {
                "geometry_id": gid,
                "source_url": source_url,
                "policy_id": policy_id,
                "source_land_loss_pct": source_land_loss_pct,
                "outside_land_pct": outside_land_pct,
                "coastal_recovery_m_used": recovery_used_m,
                "coastal_added_vs_source_land_pct": added_pct,
                "source_parts": len(raw.geoms),
                "candidate_parts": len(candidate.geoms),
                "source_npoints": count_points(raw),
                "render_npoints": points,
            }
        )
        corrected += 1

    new_index = {
        "asset_schema": "historical-slavery-atlas-render-geometry-index-v1",
        "assets": new_index_rows,
        "canonical_source_release": "v0.8.1",
        "materialization_id": NEW_ID,
        "render_geometry_source": (
            "immutable v0.8.1 authority geometry rendered with D-122 "
            "source-land-fidelity; point assets reused unchanged"
        ),
        "render_land_mask_id": LAND_FABRIC_ID,
    }
    index_bytes = compact_bytes(new_index) + b"\n"

    if semantic_projection(old_payload) != semantic_projection(new_payload):
        raise MapFixError("claim/place semantics changed")

    for gid, old_record in old_records.items():
        new_record = new_record_map[gid]
        if stable_geometry_identity(old_record) != stable_geometry_identity(new_record):
            raise MapFixError(f"{gid}: historical geometry identity/source metadata changed")

    payload_bytes = compact_bytes(new_payload) + b"\n"
    manifest = copy.deepcopy(old_manifest)
    manifest["materialization_id"] = NEW_ID
    manifest["payload_bytes"] = len(payload_bytes)
    manifest["payload_sha256"] = sha256_bytes(payload_bytes)
    manifest["render_geometry_index_sha256"] = sha256_bytes(index_bytes)
    manifest["render_geometry_source"] = (
        "39 new source-land-fidelity polygon assets plus 7 immutable reused point assets"
    )
    manifest["new_render_asset_count"] = corrected
    manifest["reused_render_asset_count"] = reused
    manifest["rollback_materialization"] = OLD_ID
    manifest["map_fix_issue"] = 365
    manifest["render_policy_contract"] = "D-122"
    manifest["raw_atlas_geometry_served"] = False

    qc = {
        "schema": "historical-slavery-atlas-mapfix-serving-qc-v1",
        "materialization_id": NEW_ID,
        "canonical_source_release": "v0.8.1",
        "predecessor_materialization_id": OLD_ID,
        "claim_semantics_unchanged": True,
        "historical_geometry_identity_unchanged": True,
        "land_fabric_id": LAND_FABRIC_ID,
        "land_sha256": land_sha,
        "source_land_loss_epsilon_pct": LOSS_EPSILON_PCT,
        "outside_land_epsilon_pct": OUTSIDE_EPSILON_PCT,
        "max_coastal_recovery_added_pct": MAX_RECOVERY_ADDED_PCT,
        "polygon_asset_count": corrected,
        "reused_point_asset_count": reused,
        "candidate_failures": [],
        "rows": sorted(qc_rows, key=lambda row: row["geometry_id"]),
    }
    qc_bytes = json.dumps(
        qc, indent=2, ensure_ascii=False, sort_keys=True
    ).encode("utf-8") + b"\n"

    ts = (
        "// Generated candidate payload for P0 #365. Not selected by the public channel.\n"
        f'export const V081_V2_MATERIALIZATION_ID = "{NEW_ID}";\n'
        f'export const V081_V2_PAYLOAD_SHA256 = "{manifest["payload_sha256"]}";\n'
        "export const V081_V2_PAYLOAD = "
        + json.dumps(payload_bytes.decode("utf-8"), ensure_ascii=False)
        + ";\n"
    ).encode("utf-8")

    if write:
        NEW_SERVING_DIR.mkdir(parents=True, exist_ok=True)
        NEW_ASSET_DIR.mkdir(parents=True, exist_ok=True)
        for existing in NEW_ASSET_DIR.glob("*.json"):
            existing.unlink()
        for filename, data in asset_bytes.items():
            (NEW_ASSET_DIR / filename).write_bytes(data)
        (NEW_ASSET_DIR / "manifest.json").write_bytes(index_bytes)
        (NEW_SERVING_DIR / "atlas-data.json").write_bytes(payload_bytes)
        (NEW_SERVING_DIR / "materialization-manifest.json").write_bytes(
            compact_bytes(manifest) + b"\n"
        )
        (NEW_SERVING_DIR / "render-qc.json").write_bytes(qc_bytes)
        NEW_TS.write_bytes(ts)

    return {
        "materialization_id": NEW_ID,
        "canonical_source_release": "v0.8.1",
        "polygon_asset_count": corrected,
        "reused_point_asset_count": reused,
        "payload_sha256": manifest["payload_sha256"],
        "render_geometry_index_sha256": manifest["render_geometry_index_sha256"],
        "worst_source_land_loss_pct": max(
            (row["source_land_loss_pct"] for row in qc_rows), default=0.0
        ),
        "worst_outside_land_pct": max(
            (row["outside_land_pct"] for row in qc_rows), default=0.0
        ),
        "max_recovery_added_pct_observed": max(
            (row["coastal_added_vs_source_land_pct"] for row in qc_rows), default=0.0
        ),
        "recovery_fallback_zero_count": sum(
            1 for row in qc_rows if row["coastal_recovery_m_used"] == 0
        ),
        "write": write,
    }


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--land", type=Path, required=True)
    parser.add_argument("--write", action="store_true")
    args = parser.parse_args()
    try:
        result = build(args.land, write=args.write)
    except (OSError, json.JSONDecodeError, MapFixError) as exc:
        print(f"BLOCK: {exc}")
        return 2
    print(json.dumps(result, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
