"""Compare coastal-fit risk in adjacent pinned Roman source intervals.

This is source-level screening, not release source-to-record matching or approval.
"""
from __future__ import annotations

import hashlib
import json
from pathlib import Path
import zipfile

from pyproj import Transformer
from shapely import from_wkb, make_valid
from shapely.geometry import shape
from shapely.ops import transform, unary_union

from build_coastal_strip_preview import fit_coastal_strip


ARCHIVE_SHA256 = "d01ae3a20d358cc5d54f69d9d725d390767d9c8759ac89ad6f90c58d106f3370"
YEARS = (1, 6, 9, 14)
ROOT = Path(__file__).resolve().parents[1]


def run(archive_path: Path) -> dict:
    if hashlib.sha256(archive_path.read_bytes()).hexdigest() != ARCHIVE_SHA256:
        raise ValueError("Unexpected Cliopatria archive")
    with zipfile.ZipFile(archive_path) as archive:
        features = json.loads(archive.read("cliopatria_polities_only.geojson"))["features"]
    land = shape(json.loads((ROOT / "web/public/source-baseline/land.geojson").read_text(encoding="utf-8"))["geometry"])
    forward = Transformer.from_crs(4326, 8857, always_xy=True).transform
    land_m = make_valid(transform(forward, land))
    authority = json.loads((ROOT / "data/release_candidates/v0.8.1-rome-geometry-authority.bundle.json").read_text(encoding="utf-8"))
    records = authority["objects"]["geometries"].values()
    rows = []
    for year in YEARS:
        active = [feature for feature in features
                  if feature["properties"]["FromYear"] <= year <= feature["properties"]["ToYear"]
                  and not str(feature["properties"].get("MemberOf") or "").strip()]
        roman = [feature for feature in active if feature["properties"]["Name"] == "Roman Empire"]
        if len(roman) != 1:
            raise ValueError(f"Expected one Roman source feature at {year}")
        source = shape(roman[0]["geometry"])
        matches = [record for record in records
                   if record.get("from_year") == roman[0]["properties"]["FromYear"]
                   and record.get("to_year") == roman[0]["properties"]["ToYear"]]
        if len(matches) != 1:
            raise ValueError(f"Expected one released geometry interval match at {year}")
        stored = from_wkb(bytes.fromhex(matches[0]["geom_ewkb_hex"]))
        source_m = make_valid(transform(forward, source))
        fitted_m, _ = fit_coastal_strip(source_m, land_m)
        source_land_m = source_m.intersection(land_m)
        added_m = fitted_m.difference(source_land_m)
        neighbors_m = unary_union([transform(forward, shape(feature["geometry"]))
                                   for feature in active if feature is not roman[0]])
        neighbor_overlap_m = added_m.intersection(neighbors_m)
        parts = list(land_m.geoms) if land_m.geom_type == "MultiPolygon" else [land_m]
        unsupported_m = unary_union([part for part in parts if source_land_m.intersection(part).area < 1])
        rows.append({
            "year": year,
            "roman_interval": [roman[0]["properties"]["FromYear"], roman[0]["properties"]["ToYear"]],
            "active_top_level_features": len(active),
            "stored_source_native_id": matches[0].get("geometry_source_native_id"),
            "github_equals_stored_geometry_exactly": source.equals_exact(stored, 0),
            "added_km2": round(added_m.area / 1e6, 1),
            "added_pct": round(100 * added_m.area / source_land_m.area, 3),
            "added_neighbor_overlap_km2": round(neighbor_overlap_m.area / 1e6, 1),
            "added_unsupported_components_km2": round(added_m.intersection(unsupported_m).area / 1e6, 1),
            "note": "14..22 CE uses a specialist geometry in the reviewed release" if year == 14 else "source-level screen only",
        })
    return {"source_sha256": ARCHIVE_SHA256, "projection": "EPSG:8857", "coastal_strip_m": 25_000,
            "scope": "Pinned GitHub source and local Mediterranean/North Sea land crop; no release substitution", "rows": rows}


if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("archive", type=Path)
    print(json.dumps(run(parser.parse_args().archive), indent=2))
