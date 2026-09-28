#!/usr/bin/env python3
"""Build source-land-fidelity render candidates from immutable v0.8.1 authority.

This is an offline/read-only cartographic diagnostic. It never mutates source
geometry, the database, a release, or the public channel.

For each released polygon:
  source_land = raw source geometry ∩ canonical Natural Earth land
  candidate   = source_land + bounded 25 km recovery originating only from
                source geometry that overhangs the canonical coastline

No inland/general-boundary smoothing is applied. The report compares the
current served render to source_land and fails if the candidate erases any
material source_land or renders material area outside canonical land.
"""
from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path
from typing import Any

from pyproj import Transformer
from shapely import from_wkb, make_valid, to_geojson
from shapely.geometry import GeometryCollection, MultiPolygon, Polygon, shape
from shapely.ops import transform, unary_union

BUNDLE_SCHEMA = "historical-slavery-atlas-full-state-bundle-v2"
LAND_FABRIC_ID = "natural-earth-ne_10m_land-v5.1.1-ca96624"
RECOVERY_M = 25_000
LOSS_EPSILON_PCT = 1e-7
OUTSIDE_EPSILON_PCT = 1e-7


def load_json(path: Path) -> Any:
    return json.loads(path.read_text(encoding="utf-8"))


def polygonal(geom):
    if geom.is_empty:
        return MultiPolygon([])
    geom = make_valid(geom)
    if isinstance(geom, Polygon):
        return MultiPolygon([geom])
    if isinstance(geom, MultiPolygon):
        return geom
    if isinstance(geom, GeometryCollection):
        polys = []
        for part in geom.geoms:
            if isinstance(part, Polygon):
                polys.append(part)
            elif isinstance(part, MultiPolygon):
                polys.extend(part.geoms)
        return MultiPolygon(polys)
    return MultiPolygon([])


def count_parts(geom) -> int:
    p = polygonal(geom)
    return len(p.geoms)


def count_holes(geom) -> int:
    p = polygonal(geom)
    return sum(len(poly.interiors) for poly in p.geoms)


def count_points(geom) -> int:
    p = polygonal(geom)
    total = 0
    for poly in p.geoms:
        total += len(poly.exterior.coords)
        total += sum(len(ring.coords) for ring in poly.interiors)
    return total


def load_land(path: Path):
    payload = load_json(path)
    geoms = [
        shape(feature["geometry"])
        for feature in payload.get("features", [])
        if feature.get("geometry")
    ]
    if not geoms:
        raise ValueError("canonical land file contains no geometry")
    return make_valid(unary_union(geoms))


def projectors():
    fwd = Transformer.from_crs("EPSG:4326", "EPSG:8857", always_xy=True)
    inv = Transformer.from_crs("EPSG:8857", "EPSG:4326", always_xy=True)
    return (
        lambda g: transform(fwd.transform, g),
        lambda g: transform(inv.transform, g),
    )


def recovery_candidate(source, land, to_metric, to_wgs84):
    source_m = make_valid(to_metric(source))
    land_m = make_valid(to_metric(land))
    source_land_m = polygonal(source_m.intersection(land_m))
    overhang_m = polygonal(source_m.difference(land_m))

    if source_land_m.is_empty:
        return source_land_m, source_land_m

    if overhang_m.is_empty:
        candidate_m = source_land_m
    else:
        recovered_m = polygonal(
            land_m.intersection(overhang_m.buffer(RECOVERY_M))
        )
        candidate_m = polygonal(unary_union([source_land_m, recovered_m]))

        # Match the durable normalize_coastal_polygon contract: do not retain
        # disconnected recovered islands that have no contact with source_land.
        kept = [
            part for part in candidate_m.geoms
            if part.intersects(source_land_m)
        ]
        candidate_m = polygonal(unary_union(kept)) if kept else source_land_m

    return source_land_m, polygonal(to_wgs84(candidate_m))


def pct(numerator: float, denominator: float) -> float:
    return 0.0 if denominator <= 0 else 100.0 * numerator / denominator


def geometry_asset_for_record(root: Path, record: dict[str, Any]):
    asset = record.get("geometry_asset")
    if not asset:
        return None
    path = root / "web" / "public" / str(asset)
    if not path.is_file():
        raise FileNotFoundError(f"render asset missing: {path}")
    return shape(load_json(path)["geometry"])


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--root", type=Path, default=Path("."))
    parser.add_argument(
        "--bundle",
        type=Path,
        default=Path("data/release_candidates/v0.8.1-rome-geometry-authority.bundle.json"),
    )
    parser.add_argument(
        "--serving",
        type=Path,
        default=Path("data/serving/v0.8.1-public-mvp-v1/atlas-data.json"),
    )
    parser.add_argument("--land", type=Path, required=True)
    parser.add_argument("--output-dir", type=Path, required=True)
    args = parser.parse_args()

    root = args.root.resolve()
    bundle = load_json(root / args.bundle)
    serving = load_json(root / args.serving)
    if bundle.get("bundle_schema") != BUNDLE_SCHEMA:
        raise SystemExit("unexpected authority bundle schema")
    if serving.get("release_version") != "v0.8.1":
        raise SystemExit("serving payload is not v0.8.1")
    if serving.get("cartography", {}).get("fabric_id") != LAND_FABRIC_ID:
        raise SystemExit("serving payload land fabric does not match expected v0.8.1 fabric")

    land_path = args.land.resolve()
    land_bytes = land_path.read_bytes()
    land = load_land(land_path)
    to_metric, to_wgs84 = projectors()
    land_m = to_metric(land)

    geometries = bundle["objects"]["geometries"]
    source_versions = bundle["objects"]["source_versions"]

    serving_records: dict[str, dict[str, Any]] = {}
    for place in serving["places"]:
        for record in place.get("geometries", []):
            serving_records[str(record["geometry_id"])] = record

    out = args.output_dir.resolve()
    out.mkdir(parents=True, exist_ok=True)
    candidate_features = []
    rows = []

    for geometry_id in bundle["membership"]["geometry_ids"]:
        source_row = geometries[geometry_id]
        raw = from_wkb(bytes.fromhex(source_row["geom_ewkb_hex"]))
        if raw.geom_type not in {"Polygon", "MultiPolygon"}:
            continue

        record = serving_records.get(geometry_id)
        if record is None:
            raise SystemExit(f"released geometry missing from serving payload: {geometry_id}")
        current = geometry_asset_for_record(root, record)
        if current is None:
            raise SystemExit(f"polygon has no versioned render asset: {geometry_id}")

        source_version_id = source_row.get("geometry_source_version_id")
        source_version = source_versions.get(str(source_version_id), {})
        source_url = (
            source_version.get("source_version", {}).get("url_or_identifier")
        )

        raw = polygonal(make_valid(raw))
        source_m = to_metric(raw)
        source_land_m = polygonal(source_m.intersection(land_m))
        current_m = polygonal(make_valid(to_metric(current)))
        _, candidate = recovery_candidate(raw, land, to_metric, to_wgs84)
        candidate_m = polygonal(make_valid(to_metric(candidate)))

        base_area = source_land_m.area
        current_loss_pct = pct(
            source_land_m.difference(current_m).area,
            base_area,
        )
        candidate_loss_pct = pct(
            source_land_m.difference(candidate_m).area,
            base_area,
        )
        current_outside_pct = pct(
            current_m.difference(land_m).area,
            max(current_m.area, 1.0),
        )
        candidate_outside_pct = pct(
            candidate_m.difference(land_m).area,
            max(candidate_m.area, 1.0),
        )
        candidate_added_pct = pct(
            candidate_m.difference(source_land_m).area,
            base_area,
        )

        family = "other"
        if source_url and "Seshat-Global-History-Databank/cliopatria" in source_url:
            family = "cliopatria"
        elif source_url and "sfsheath/roman-maps" in source_url:
            family = "awmc_derived"

        row = {
            "geometry_id": geometry_id,
            "spatial_entity_id": source_row["spatial_entity_id"],
            "from_year": source_row.get("from_year"),
            "to_year": source_row.get("to_year"),
            "source_family": family,
            "source_url": source_url,
            "accuracy_status": source_row.get("accuracy_status"),
            "current_policy_id": record.get("render_policy_id"),
            "current_transform": record.get("render_transform"),
            "source_parts": count_parts(raw),
            "current_parts": count_parts(current),
            "candidate_parts": count_parts(candidate),
            "source_holes": count_holes(raw),
            "current_holes": count_holes(current),
            "candidate_holes": count_holes(candidate),
            "source_points": count_points(raw),
            "current_points": count_points(current),
            "candidate_points": count_points(candidate),
            "current_source_land_loss_pct": current_loss_pct,
            "candidate_source_land_loss_pct": candidate_loss_pct,
            "current_outside_land_pct": current_outside_pct,
            "candidate_outside_land_pct": candidate_outside_pct,
            "candidate_coastal_added_vs_source_land_pct": candidate_added_pct,
            "candidate_pass": (
                candidate_loss_pct <= LOSS_EPSILON_PCT
                and candidate_outside_pct <= OUTSIDE_EPSILON_PCT
            ),
        }
        rows.append(row)

        candidate_features.append(
            {
                "type": "Feature",
                "properties": {
                    "geometry_id": geometry_id,
                    "source_family": family,
                    "from_year": source_row.get("from_year"),
                    "to_year": source_row.get("to_year"),
                    "render_policy_id": (
                        "cliopatria-source-land-fidelity-v1"
                        if family == "cliopatria"
                        else "source-land-fidelity-diagnostic-v1"
                    ),
                    "render_coastal_recovery_m": RECOVERY_M,
                    "source_land_loss_pct": candidate_loss_pct,
                    "coastal_added_vs_source_land_pct": candidate_added_pct,
                },
                "geometry": json.loads(to_geojson(candidate)),
            }
        )

    rows.sort(key=lambda row: (-row["current_source_land_loss_pct"], row["geometry_id"]))
    report = {
        "schema": "historical-slavery-atlas-source-land-fidelity-report-v1",
        "canonical_source_release": "v0.8.1",
        "serving_materialization": serving.get("serving_materialization_id"),
        "land_fabric_id": LAND_FABRIC_ID,
        "land_file_sha256": hashlib.sha256(land_bytes).hexdigest(),
        "coastal_recovery_m": RECOVERY_M,
        "polygon_count": len(rows),
        "candidate_failures": [
            row["geometry_id"] for row in rows if not row["candidate_pass"]
        ],
        "current_material_loss_count": sum(
            1 for row in rows if row["current_source_land_loss_pct"] > 0.001
        ),
        "rows": rows,
    }

    (out / "source-land-fidelity-report.json").write_text(
        json.dumps(report, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )
    (out / "source-land-fidelity-candidates.geojson").write_text(
        json.dumps(
            {"type": "FeatureCollection", "features": candidate_features},
            separators=(",", ":"),
            sort_keys=True,
        )
        + "\n",
        encoding="utf-8",
    )

    print(json.dumps({
        "polygon_count": report["polygon_count"],
        "current_material_loss_count": report["current_material_loss_count"],
        "candidate_failures": report["candidate_failures"],
        "worst_current_losses": [
            {
                "geometry_id": row["geometry_id"],
                "family": row["source_family"],
                "loss_pct": row["current_source_land_loss_pct"],
                "current_parts": row["current_parts"],
                "source_parts": row["source_parts"],
            }
            for row in rows[:10]
        ],
    }, indent=2))

    if report["candidate_failures"]:
        return 2
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
