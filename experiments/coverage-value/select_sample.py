#!/usr/bin/env python3
"""Deterministically select COV-001 polity-year sample cells from pinned Cliopatria.

Sampling only. This script makes no slavery/coercion claim and no approved
historical-geography claim. Geometry bbox midpoints are used only to distribute
sample rows across coarse sectors.

Usage:
    python experiments/coverage-value/select_sample.py \
      /path/to/cliopatria.geojson.zip \
      --output experiments/coverage-value/sample.json
"""

from __future__ import annotations

import argparse
import hashlib
import json
import zipfile
from pathlib import Path
from typing import Any, Iterable

EXPECTED_SHA256 = "d01ae3a20d358cc5d54f69d9d725d390767d9c8759ac89ad6f90c58d106f3370"
EXPECTED_FEATURES = 13_765
SEED = "COV-001|ac73a560|cliopatria-ad28a691|2026-09-23"
ANCHORS = (-500, 500, 1300, 1800)


def sha256_file(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as fh:
        for chunk in iter(lambda: fh.read(1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest()


def iter_positions(coords: Any) -> Iterable[tuple[float, float]]:
    if not isinstance(coords, list):
        return
    if len(coords) >= 2 and isinstance(coords[0], (int, float)) and isinstance(coords[1], (int, float)):
        yield float(coords[0]), float(coords[1])
        return
    for item in coords:
        yield from iter_positions(item)


def bbox_midpoint(geometry: dict[str, Any]) -> tuple[float, float] | None:
    points = list(iter_positions(geometry.get("coordinates")))
    if not points:
        return None
    xs = [p[0] for p in points]
    ys = [p[1] for p in points]
    # Sampling-only approximation. Dateline-special cases are not interpreted
    # historically; the exact source geometry remains untouched.
    return ((min(xs) + max(xs)) / 2.0, (min(ys) + max(ys)) / 2.0)


def sector(lon: float, lat: float) -> str:
    if lon < -30:
        return "A" if lat >= 0 else "B"
    if lon < 60:
        return "C" if lat < 30 else "D"
    if lon < 100:
        return "E"
    return "F"


def active(props: dict[str, Any], year: int) -> bool:
    try:
        return int(props["FromYear"]) <= year <= int(props["ToYear"])
    except (KeyError, TypeError, ValueError):
        return False


def eligible(feature: dict[str, Any], year: int) -> bool:
    props = feature.get("properties") or {}
    name = str(props.get("Name") or "")
    return (
        props.get("Type") == "POLITY"
        and not str(props.get("Components") or "").strip()
        and not name.startswith("(")
        and active(props, year)
        and bool(feature.get("geometry"))
    )


def digest_for(year: int, sec: str, ordinal: int, props: dict[str, Any]) -> str:
    raw = "|".join(
        [
            SEED,
            str(year),
            sec,
            str(ordinal),
            str(props.get("Name") or ""),
            str(props.get("FromYear") or ""),
            str(props.get("ToYear") or ""),
        ]
    )
    return hashlib.sha256(raw.encode("utf-8")).hexdigest()


def load_geojson(zip_path: Path) -> dict[str, Any]:
    actual = sha256_file(zip_path)
    if actual != EXPECTED_SHA256:
        raise SystemExit(f"source SHA-256 mismatch: expected {EXPECTED_SHA256}, got {actual}")

    with zipfile.ZipFile(zip_path) as zf:
        members = [
            n
            for n in zf.namelist()
            if n.lower().endswith((".geojson", ".json")) and not n.startswith("__MACOSX/")
        ]
        if len(members) != 1:
            raise SystemExit(f"expected exactly one data GeoJSON member, found {members}")
        data = json.loads(zf.read(members[0]))

    features = data.get("features") or []
    if len(features) != EXPECTED_FEATURES:
        raise SystemExit(f"feature count mismatch: expected {EXPECTED_FEATURES}, got {len(features)}")
    return data


def build_sample(data: dict[str, Any]) -> dict[str, Any]:
    features = data["features"]
    result: list[dict[str, Any]] = []

    for year in ANCHORS:
        for sec in "ABCDEF":
            candidates: list[tuple[str, int, dict[str, Any], float, float]] = []
            for ordinal, feature in enumerate(features):
                if not eligible(feature, year):
                    continue
                midpoint = bbox_midpoint(feature["geometry"])
                if midpoint is None:
                    continue
                lon, lat = midpoint
                if sector(lon, lat) != sec:
                    continue
                props = feature["properties"]
                candidates.append((digest_for(year, sec, ordinal, props), ordinal, props, lon, lat))

            if not candidates:
                result.append(
                    {
                        "cell_id": f"{year}:{sec}",
                        "anchor_source_year": year,
                        "sector": sec,
                        "candidate_count": 0,
                        "status": "sampling_gap",
                    }
                )
                continue

            candidates.sort(key=lambda x: x[0])
            digest, ordinal, props, lon, lat = candidates[0]
            result.append(
                {
                    "cell_id": f"{year}:{sec}",
                    "anchor_source_year": year,
                    "sector": sec,
                    "candidate_count": len(candidates),
                    "status": "selected",
                    "selection_digest": digest,
                    "source_row_ordinal": ordinal,
                    "source_name": props.get("Name"),
                    "source_type": props.get("Type"),
                    "source_from_year": props.get("FromYear"),
                    "source_to_year": props.get("ToYear"),
                    "source_seshat_id": props.get("SeshatID"),
                    "source_wikidata": props.get("Wikidata"),
                    "sampling_bbox_midpoint": [lon, lat],
                }
            )

    valid = sum(1 for row in result if row["status"] == "selected")
    return {
        "experiment": "COV-001",
        "purpose": "neutral sampling only; not historical slavery or approved geography evidence",
        "seed": SEED,
        "source_sha256": EXPECTED_SHA256,
        "anchor_source_years": list(ANCHORS),
        "valid_cells": valid,
        "sampling_gaps": len(result) - valid,
        "minimum_viable_valid_cells": 18,
        "viable": valid >= 18,
        "cells": result,
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("source_zip", type=Path)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()

    data = load_geojson(args.source_zip)
    sample = build_sample(data)
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(sample, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    print(json.dumps({k: sample[k] for k in ("valid_cells", "sampling_gaps", "viable")}, indent=2))


if __name__ == "__main__":
    main()
