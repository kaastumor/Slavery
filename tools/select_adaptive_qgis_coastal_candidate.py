#!/usr/bin/env python3
"""Select a bounded adaptive QGIS coastal-snap render candidate.

This does not create geometry. QGIS creates every candidate with standard
smooth/snap/fix/clip operations. This helper only measures candidate deltas
against the conservative baseline and selects the largest safe tolerance.
"""
from __future__ import annotations

import argparse
import json
from pathlib import Path
import shutil

try:
    from pyproj import Transformer
    from shapely.geometry import shape
    from shapely.ops import transform, unary_union
except ImportError as exc:
    raise SystemExit(
        "pyproj and shapely are required for adaptive QGIS candidate QC"
    ) from exc


def load_union(path: Path):
    payload = json.loads(path.read_text(encoding="utf-8"))
    features = payload.get("features") or []
    geometries = [shape(f["geometry"]) for f in features if f.get("geometry")]
    if not geometries:
        raise ValueError(f"{path} contains no geometry")
    return unary_union(geometries)


def equal_earth(geom):
    transformer = Transformer.from_crs("EPSG:4326", "EPSG:8857", always_xy=True)
    return transform(transformer.transform, geom)


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--baseline", type=Path, required=True)
    parser.add_argument("--candidate", action="append", required=True,
                        help="TOLERANCE_M=PATH; may be repeated")
    parser.add_argument("--max-extra-pct", type=float, default=2.0)
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--report", type=Path, required=True)
    args = parser.parse_args()

    baseline = equal_earth(load_union(args.baseline))
    baseline_area = baseline.area
    if baseline_area <= 0:
        raise SystemExit("baseline area is zero")

    rows = []
    for item in args.candidate:
        tolerance_text, path_text = item.split("=", 1)
        tolerance = int(tolerance_text)
        path = Path(path_text)
        candidate = equal_earth(load_union(path))
        extra = candidate.difference(baseline).area
        missing = baseline.difference(candidate).area
        extra_pct = 100.0 * extra / baseline_area
        missing_pct = 100.0 * missing / baseline_area
        rows.append({
            "tolerance_m": tolerance,
            "path": str(path),
            "area_m2": candidate.area,
            "extra_vs_baseline_pct": extra_pct,
            "missing_vs_baseline_pct": missing_pct,
            "valid": candidate.is_valid,
            "empty": candidate.is_empty,
        })

    safe = [
        row for row in rows
        if row["valid"]
        and not row["empty"]
        and row["extra_vs_baseline_pct"] <= args.max_extra_pct
    ]
    if not safe:
        raise SystemExit("no adaptive QGIS candidate passed the area-bound QC")

    chosen = max(safe, key=lambda row: row["tolerance_m"])
    shutil.copyfile(chosen["path"], args.output)

    report = {
        "schema": "atlas-qgis-adaptive-coastal-selection-v1",
        "baseline_path": str(args.baseline),
        "baseline_area_m2": baseline_area,
        "max_extra_pct": args.max_extra_pct,
        "candidates": rows,
        "chosen_tolerance_m": chosen["tolerance_m"],
        "chosen_extra_vs_baseline_pct": chosen["extra_vs_baseline_pct"],
        "chosen_missing_vs_baseline_pct": chosen["missing_vs_baseline_pct"],
        "output": str(args.output),
    }
    args.report.write_text(
        json.dumps(report, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )
    print(json.dumps(report, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
