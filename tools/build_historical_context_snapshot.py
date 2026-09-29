#!/usr/bin/env python3
"""Build review-only neutral historical-polity context snapshots.

The source is the exact pinned Cliopatria corpus. Context features have no slavery
claim semantics and are clipped only to the canonical Natural Earth land fabric.
"""
from __future__ import annotations

import argparse
import hashlib
import io
import json
from pathlib import Path
import urllib.request
import zipfile

from shapely.geometry import GeometryCollection, MultiPolygon, Polygon, mapping, shape
from shapely.ops import unary_union
from shapely.validation import make_valid

CLIOPATRIA_URL = (
    "https://raw.githubusercontent.com/Seshat-Global-History-Databank/"
    "cliopatria/ad28a691b7c07c1fca89d0e0636d324667d2a258/"
    "cliopatria.geojson.zip"
)
CLIOPATRIA_COMMIT = "ad28a691b7c07c1fca89d0e0636d324667d2a258"
CLIOPATRIA_BLOB = "cefab0f4b622e2e7fb3daf68d4f461f83991204c"
CLIOPATRIA_SHA256 = "d01ae3a20d358cc5d54f69d9d725d390767d9c8759ac89ad6f90c58d106f3370"
CLIOPATRIA_SIZE = 44_231_317
CLIOPATRIA_FEATURES = 13_765
LAND_SHA256 = "1ac90796408bc6ad6911d69448485d3c4dbf2190370080368a09976e1c9f7416"
LAND_ID = "natural-earth-ne_10m_land-v5.1.1-ca96624"


def git_blob_sha1(data: bytes) -> str:
    return hashlib.sha1(f"blob {len(data)}\0".encode() + data).hexdigest()


def canonical_json(value: object) -> str:
    return json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(",", ":"))


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


def atlas_to_source_year(atlas_year: int) -> int:
    return atlas_year - 1 if atlas_year <= 0 else atlas_year


def load_cliopatria() -> list[dict]:
    req = urllib.request.Request(
        CLIOPATRIA_URL,
        headers={"User-Agent": "historical-slavery-atlas-context-prototype/1"},
    )
    with urllib.request.urlopen(req, timeout=120) as response:
        data = response.read()
    observed = {
        "size": len(data),
        "blob": git_blob_sha1(data),
        "sha256": hashlib.sha256(data).hexdigest(),
    }
    expected = {
        "size": CLIOPATRIA_SIZE,
        "blob": CLIOPATRIA_BLOB,
        "sha256": CLIOPATRIA_SHA256,
    }
    if observed != expected:
        raise SystemExit(f"Cliopatria identity mismatch: {observed!r}")
    with zipfile.ZipFile(io.BytesIO(data)) as archive:
        members = [
            name for name in archive.namelist()
            if name.lower().endswith(".geojson")
            and not name.startswith("__MACOSX/")
            and not name.rsplit("/", 1)[-1].startswith("._")
        ]
        if len(members) != 1:
            raise SystemExit(f"expected one GeoJSON member, got {members!r}")
        payload = json.loads(archive.read(members[0]).decode("utf-8"))
    features = payload["features"]
    if len(features) != CLIOPATRIA_FEATURES:
        raise SystemExit(f"feature count mismatch: {len(features)}")
    return features


def load_land(path: Path):
    data = path.read_bytes()
    digest = hashlib.sha256(data).hexdigest()
    if digest != LAND_SHA256:
        raise SystemExit(f"land SHA mismatch: {digest}")
    payload = json.loads(data)
    geoms = [
        shape(feature["geometry"])
        for feature in payload.get("features", [])
        if feature.get("geometry")
    ]
    if not geoms:
        raise SystemExit("land fabric contains no geometry")
    return make_valid(unary_union(geoms))


def build_snapshot(features: list[dict], land, atlas_year: int) -> dict:
    source_year = atlas_to_source_year(atlas_year)
    out = []
    duplicate_keys: dict[tuple[str, int, int], int] = {}
    for ordinal, feature in enumerate(features, start=1):
        props = feature.get("properties") or {}
        if props.get("Type") != "POLITY":
            continue
        if str(props.get("MemberOf") or "").strip():
            continue
        start, end = props.get("FromYear"), props.get("ToYear")
        if not isinstance(start, int) or not isinstance(end, int):
            continue
        if not (start <= source_year <= end):
            continue
        geom = polygonal(shape(feature["geometry"]).intersection(land))
        if geom.is_empty:
            continue
        name = str(props.get("Name") or "")
        key = (name, start, end)
        duplicate_keys[key] = duplicate_keys.get(key, 0) + 1
        out.append(
            {
                "type": "Feature",
                "properties": {
                    "context_layer": "neutral_historical_polity",
                    "claim_semantics": "none",
                    "name": name,
                    "source_row_ordinal_1_based": ordinal,
                    "source_feature_sha256": hashlib.sha256(
                        canonical_json(feature).encode("utf-8")
                    ).hexdigest(),
                    "source_native_from": start,
                    "source_native_to": end,
                    "seshat_id": props.get("SeshatID"),
                    "wikidata": props.get("Wikidata"),
                    "member_of": props.get("MemberOf"),
                    "selected_atlas_year": atlas_year,
                    "selected_source_year": source_year,
                    "context_review_state": "prototype_unapproved",
                },
                "geometry": mapping(geom),
            }
        )
    return {
        "type": "FeatureCollection",
        "features": out,
        "_meta": {
            "schema": "historical-slavery-atlas-neutral-polity-context-v1",
            "claim_semantics": "none",
            "selected_atlas_year": atlas_year,
            "selected_source_year": source_year,
            "selection": "active top-level Cliopatria POLITY rows (MemberOf empty)",
            "cliopatria_commit": CLIOPATRIA_COMMIT,
            "cliopatria_blob_sha1": CLIOPATRIA_BLOB,
            "cliopatria_sha256": CLIOPATRIA_SHA256,
            "land_fabric_id": LAND_ID,
            "land_sha256": LAND_SHA256,
            "feature_count": len(out),
            "duplicate_name_interval_keys": sorted(
                [list(key) + [count] for key, count in duplicate_keys.items() if count > 1]
            ),
            "publication_state": "review_only_prototype",
        },
    }


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--land", type=Path, required=True)
    parser.add_argument("--output-dir", type=Path, required=True)
    parser.add_argument("--year", type=int, action="append", required=True)
    args = parser.parse_args()

    features = load_cliopatria()
    land = load_land(args.land)
    args.output_dir.mkdir(parents=True, exist_ok=True)

    summaries = []
    for year in args.year:
        snapshot = build_snapshot(features, land, year)
        path = args.output_dir / f"context-{year}.geojson"
        path.write_text(
            json.dumps(snapshot, ensure_ascii=False, separators=(",", ":"), sort_keys=True)
            + "\n",
            encoding="utf-8",
        )
        names = sorted(
            str(feature["properties"]["name"])
            for feature in snapshot["features"]
        )
        summaries.append(
            {
                "atlas_year": year,
                "source_year": snapshot["_meta"]["selected_source_year"],
                "feature_count": len(snapshot["features"]),
                "names": names,
                "file": path.name,
            }
        )

    report = {
        "schema": "historical-slavery-atlas-neutral-context-prototype-report-v1",
        "claim_semantics": "none",
        "publication_state": "review_only_prototype",
        "source": {
            "repository": "Seshat-Global-History-Databank/cliopatria",
            "commit": CLIOPATRIA_COMMIT,
            "blob_sha1": CLIOPATRIA_BLOB,
            "sha256": CLIOPATRIA_SHA256,
            "feature_count": CLIOPATRIA_FEATURES,
        },
        "land_fabric_id": LAND_ID,
        "snapshots": summaries,
    }
    (args.output_dir / "context-report.json").write_text(
        json.dumps(report, indent=2, ensure_ascii=False, sort_keys=True) + "\n",
        encoding="utf-8",
    )
    print(json.dumps(
        {
            "snapshots": [
                {
                    "atlas_year": row["atlas_year"],
                    "feature_count": row["feature_count"],
                    "roman_frontier_names": [
                        name for name in row["names"]
                        if any(token in name.lower() for token in (
                            "roman", "cappad", "commag", "armenia", "mauretan",
                            "thrac", "nabat"
                        ))
                    ],
                }
                for row in summaries
            ]
        },
        indent=2,
    ))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
