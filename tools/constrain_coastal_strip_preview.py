"""Constrain the pinned 6 CE coastal candidate without changing source or release.

The exclusions are presentation safeguards, not historical border decisions.
"""
from __future__ import annotations

import hashlib
import json
from pathlib import Path

from pyproj import Transformer
from shapely import make_valid
from shapely.geometry import mapping, shape
from shapely.ops import transform, unary_union


ROOT = Path(__file__).resolve().parents[1] / "web/public/source-baseline"
SOURCE_SHA256 = "8cb3b8d0458a1b3d3ac485a83466bb75d4e2cf28669b10f76af49e8e4af18df1"


def polygonal(geometry):
    valid = make_valid(geometry)
    if valid.geom_type in {"Polygon", "MultiPolygon"}:
        return valid
    return unary_union([part for part in getattr(valid, "geoms", [])
                        if part.geom_type in {"Polygon", "MultiPolygon"}])


def constrain_additions(source, fitted, land, neighbors):
    """Retain source land, excluding only unsupported coastal additions."""
    source_land = source.intersection(land)
    additions = polygonal(fitted.difference(source_land))
    components = list(land.geoms) if land.geom_type == "MultiPolygon" else [land]
    supported = unary_union([part for part in components
                             if source_land.intersection(part).area > 1e-12])
    neighbor_land = unary_union(neighbors).intersection(land)
    accepted = polygonal(additions.intersection(supported).difference(neighbor_land))
    result = polygonal(source_land.union(accepted))
    return result, additions, accepted, supported, neighbor_land


def build(root: Path = ROOT):
    source_bytes = (root / "features.geojson").read_bytes()
    if hashlib.sha256(source_bytes).hexdigest() != SOURCE_SHA256:
        raise ValueError("Unexpected pinned source selection")
    features = json.loads(source_bytes)["features"]
    roman = [feature for feature in features if feature["properties"]["Name"] == "Roman Empire"]
    if len(roman) != 1 or len(features) != 46:
        raise ValueError("Expected one Roman feature in the pinned 46-feature selection")
    source = shape(roman[0]["geometry"])
    land = shape(json.loads((root / "land.geojson").read_text(encoding="utf-8"))["geometry"])
    fitted = shape(json.loads((root / "coastal-fit.geojson").read_text(encoding="utf-8"))["geometry"])
    neighbors = [shape(feature["geometry"]) for feature in features if feature is not roman[0]]
    result, additions, accepted, supported, neighbor_land = constrain_additions(
        source, fitted, land, neighbors)
    equal_area = Transformer.from_crs(4326, 6933, always_xy=True).transform
    km2 = lambda geometry: transform(equal_area, geometry).area / 1_000_000
    checks = {
        "valid": result.is_valid,
        "outside_land_degrees2": result.difference(land).area,
        "lost_source_land_degrees2": source.intersection(land).difference(result).area,
        "added_neighbor_overlap_degrees2": accepted.intersection(neighbor_land).area,
        "added_unsupported_land_degrees2": accepted.difference(supported).area,
        "original_additions_km2": round(km2(additions), 2),
        "accepted_additions_km2": round(km2(accepted), 2),
        "excluded_additions_km2": round(km2(additions.difference(accepted)), 2),
        "accepted_additions_pct_of_source_land": round(100 * km2(accepted) / km2(source.intersection(land)), 3),
    }
    if not checks["valid"] or any(checks[key] > 1e-9 for key in checks if key.endswith("_degrees2")):
        raise ValueError(f"Constrained fit failed: {checks}")
    payload = {"type": "Feature", "properties": {
        **roman[0]["properties"], "presentation_only": True,
        "method": "coastal-strip-fit-constrained", "distance_m": 25_000,
        "source_variant": "pinned Cliopatria GitHub; differs from stored Seshat API record",
    }, "geometry": mapping(result)}
    output = root / "coastal-fit-constrained.geojson"
    encoded = json.dumps(payload, separators=(",", ":")).encode("utf-8")
    output.write_bytes(encoded)
    report = {
        "status": "local presentation candidate; not released historical authority",
        "scope": "Roman Empire 6..8 CE only",
        "source_features_sha256": SOURCE_SHA256,
        "base_fit_sha256": hashlib.sha256((root / "coastal-fit.geojson").read_bytes()).hexdigest(),
        "output_sha256": hashlib.sha256(encoded).hexdigest(),
        "checks": checks,
        "limits": ["Other dates source-screened only; regional visual and release matching pending", "Source-to-record difference unresolved",
                   "Historical island and border review pending", "Prior 2% policy exception pending release review"],
    }
    (root / "coastal-fit-constrained-report.json").write_text(json.dumps(report, indent=2) + "\n", encoding="utf-8")
    return report


if __name__ == "__main__":
    print(json.dumps(build(), indent=2))
