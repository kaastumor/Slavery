"""Offline 6 CE preview of coastal-strip fitting; never writes release assets.

Independent implementation of the approach described by History Atlas:
https://github.com/laurencefwhite/history-atlas#coastlines
The referenced implementation was unavailable (HTTP 404); no code was copied.
"""
from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path

from pyproj import Transformer
from shapely import make_valid
from shapely.geometry import box, mapping, shape
from shapely.ops import transform, unary_union

DISTANCE_M = 25_000
LAND_SHA256 = "1ac90796408bc6ad6911d69448485d3c4dbf2190370080368a09976e1c9f7416"


def polygonal(geometry):
    geometry = make_valid(geometry)
    if geometry.geom_type in {"Polygon", "MultiPolygon"}:
        return geometry
    return unary_union([polygonal(part) for part in getattr(geometry, "geoms", [])
                        if part.geom_type in {"Polygon", "MultiPolygon", "GeometryCollection"}])


def fit_coastal_strip(source, land, distance=DISTANCE_M):
    """Operate in metres; add only nearby coastal land, retaining all source land."""
    coastal_land = land.difference(land.buffer(-distance))
    addition = source.buffer(distance).intersection(coastal_land)
    fitted = source.union(addition).intersection(land)
    return fitted, coastal_land


def build(land_path: Path, output: Path):
    land_bytes = land_path.read_bytes()
    if hashlib.sha256(land_bytes).hexdigest() != LAND_SHA256:
        raise ValueError("Unexpected coastline asset")
    inputs = json.loads((output / "features.geojson").read_text(encoding="utf-8"))
    feature = next(f for f in inputs["features"] if f["properties"]["Name"] == "Roman Empire")
    source = shape(feature["geometry"])
    land = unary_union([shape(f["geometry"]) for f in json.loads(land_bytes)["features"]])
    # Margin is far larger than the fitting distance; crop affects background only.
    land = land.intersection(box(-20, 15, 55, 65))
    forward = Transformer.from_crs(4326, 8857, always_xy=True).transform
    reverse = Transformer.from_crs(8857, 4326, always_xy=True).transform
    source_m = make_valid(transform(forward, source))
    land_m = make_valid(transform(forward, land))
    fitted_m, coastal_m = fit_coastal_strip(source_m, land_m)
    source_land = source_m.intersection(land_m)
    added = fitted_m.difference(source_land)
    checks = {
        "valid": fitted_m.is_valid,
        "outside_land_m2": fitted_m.difference(land_m).area,
        "lost_source_land_m2": source_land.difference(fitted_m).area,
        "added_beyond_coastal_strip_m2": added.difference(coastal_m).area,
        "added_beyond_source_distance_m2": added.difference(source_m.buffer(DISTANCE_M)).area,
        "added_land_km2": added.area / 1e6,
        "added_land_pct": 100 * added.area / source_land.area,
    }
    if not checks["valid"] or any(checks[k] > 1 for k in checks if k.endswith("_m2")):
        raise ValueError(f"Coastal fitting invariants failed: {checks}")
    # Export only the additions: round-tripping an entire source polygon can
    # introduce chords along long inland edges. Preserve the original there.
    coastal_wgs = polygonal(transform(reverse, coastal_m)).intersection(land)
    additions_wgs = polygonal(transform(reverse, added)).intersection(coastal_wgs)
    source_land_wgs = source.intersection(land)
    fitted = source_land_wgs.union(additions_wgs)
    checks["final_valid"] = fitted.is_valid
    checks["final_outside_land_degrees2"] = fitted.difference(land).area
    checks["final_lost_source_land_degrees2"] = source.intersection(land).difference(fitted).area
    checks["final_change_outside_strip_degrees2"] = fitted.symmetric_difference(source_land_wgs).difference(coastal_wgs).area
    if not fitted.is_valid or any(checks[k] > 1e-10 for k in checks if k.endswith("_degrees2")):
        raise ValueError(f"Serialized-geometry checks failed: {checks}")
    payloads = {
        "coastal-fit.geojson": {"type": "Feature", "properties": {
            **feature["properties"], "presentation_only": True,
            "method": "coastal-strip-fit", "distance_m": DISTANCE_M,
        }, "geometry": mapping(fitted)},
        "land.geojson": {"type": "Feature", "properties": {}, "geometry": mapping(land)},
    }
    release_path = Path(__file__).resolve().parents[1] / "web/public/release-geometries/v0.8.1-public-mvp-v2/edb239a8-4d54-44e4-970a-affb7c9af22e.json"
    published = json.loads(release_path.read_text())
    payloads["published-v2.geojson"] = {"type": "Feature", "properties": {
        "Name": "Published v2", "FromYear": 6, "ToYear": 8,
    }, "geometry": published["geometry"]}
    hashes = {}
    for name, data in payloads.items():
        encoded = json.dumps(data, separators=(",", ":")).encode()
        (output / name).write_bytes(encoded)
        hashes[name] = hashlib.sha256(encoded).hexdigest()
    report = {
        "status": "local presentation preview; not historical authority or published release",
        "approach_reference": "https://github.com/laurencefwhite/history-atlas#coastlines",
        "implementation": "independent; reference code unavailable",
        "projection": "EPSG:8857", "coastal_strip_m": DISTANCE_M,
        "source": "Pinned Cliopatria GitHub feature, Roman Empire, 6..8 CE",
        "land_sha256": LAND_SHA256, "checks": checks, "output_sha256": hashes,
    }
    (output / "coastal-fit-report.json").write_text(json.dumps(report, indent=2) + "\n")
    return report


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("land", type=Path)
    parser.add_argument("--output", type=Path, default=Path("web/public/source-baseline"))
    args = parser.parse_args()
    print(json.dumps(build(args.land, args.output), indent=2))
