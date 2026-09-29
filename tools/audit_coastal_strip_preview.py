"""Audit the 6 CE coastal preview against other pinned source features.

This reports presentation conflicts; it does not decide historical territory.
"""
from __future__ import annotations

import argparse
import json
from pathlib import Path

from pyproj import Transformer
from shapely.geometry import shape
from shapely.ops import transform


ROOT = Path(__file__).resolve().parents[1] / "web/public/source-baseline"


def read(name: str):
    return json.loads((ROOT / name).read_text(encoding="utf-8"))


def main(candidate: str) -> None:
    features = read("features.geojson")["features"]
    roman = [feature for feature in features if feature["properties"]["Name"] == "Roman Empire"]
    if len(roman) != 1 or len(features) != 46:
        raise ValueError("Expected the pinned 46-feature 6 CE source selection")
    source = shape(roman[0]["geometry"])
    land = shape(read("land.geojson")["geometry"])
    fitted = shape(read(candidate)["geometry"])
    source_land = source.intersection(land)
    added = fitted.difference(source_land)
    equal_area = Transformer.from_crs(4326, 6933, always_xy=True).transform

    def km2(geometry):
        return transform(equal_area, geometry).area / 1_000_000

    overlaps = []
    for feature in features:
        if feature is roman[0]:
            continue
        overlap = added.intersection(shape(feature["geometry"])).intersection(land)
        if km2(overlap) > 0.01:
            overlaps.append({
                "name": feature["properties"]["Name"],
                "from_year": feature["properties"]["FromYear"],
                "to_year": feature["properties"]["ToYear"],
                "added_overlap_km2": round(km2(overlap), 2),
            })
    overlaps.sort(key=lambda item: item["added_overlap_km2"], reverse=True)

    land_parts = list(land.geoms) if land.geom_type == "MultiPolygon" else [land]
    newly_colored = [part for part in land_parts
                     if source_land.intersection(part).area < 1e-12
                     and added.intersection(part).area > 1e-10]
    report = {
        "candidate": candidate,
        "scope": "Pinned Cliopatria GitHub 6 CE top-level selection only",
        "source_feature_count": len(features),
        "source_interval": [roman[0]["properties"]["FromYear"], roman[0]["properties"]["ToYear"]],
        "fitted_valid": fitted.is_valid,
        "added_land_km2_equal_area": round(km2(added), 2),
        "overlap_with_other_source_features_km2_sum": round(sum(item["added_overlap_km2"] for item in overlaps), 2),
        "overlaps": overlaps,
        "newly_colored_land_components_without_source_coverage": len(newly_colored),
        "newly_colored_component_area_km2_sum": round(sum(km2(added.intersection(part)) for part in newly_colored), 2),
        "caution": "Overlaps may be present in source; component counts and areas do not establish historical claims.",
    }
    print(json.dumps(report, indent=2))


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--candidate", default="coastal-fit.geojson",
                        choices=["coastal-fit.geojson", "coastal-fit-constrained.geojson"])
    main(parser.parse_args().candidate)
