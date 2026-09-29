#!/usr/bin/env python3
"""Extract a selected-year Cliopatria baseline without any geometry operations."""
from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path
import zipfile

SOURCE_SHA256 = "d01ae3a20d358cc5d54f69d9d725d390767d9c8759ac89ad6f90c58d106f3370"
SOURCE_COMMIT = "ad28a691b7c07c1fca89d0e0636d324667d2a258"


def extract(archive_path: Path, year: int, output: Path, authority_path: Path | None = None) -> dict:
    if hashlib.sha256(archive_path.read_bytes()).hexdigest() != SOURCE_SHA256:
        raise ValueError("Cliopatria archive does not match the pinned source")
    with zipfile.ZipFile(archive_path) as archive:
        members = [name for name in archive.namelist()
                   if name.endswith(".geojson") and not name.startswith("__MACOSX/")]
        if len(members) != 1:
            raise ValueError("Expected exactly one source GeoJSON member")
        source = json.loads(archive.read(members[0]))
    # Same full-polity selection as the upstream notebook, in source-native years.
    features = [feature for feature in source["features"]
                if feature["properties"]["FromYear"] <= year <= feature["properties"]["ToYear"]
                and not str(feature["properties"].get("MemberOf") or "").strip()]
    payload = {"type": "FeatureCollection", "features": features}
    output.mkdir(parents=True, exist_ok=True)
    data = json.dumps(payload, ensure_ascii=False, separators=(",", ":")).encode("utf-8")
    (output / "features.geojson").write_bytes(data)
    manifest = {
        "purpose": "raw-source inspection; no historical claim or release promotion",
        "source_commit": SOURCE_COMMIT,
        "source_archive_sha256": SOURCE_SHA256,
        "source_native_year": year,
        "selection": "FromYear <= year <= ToYear; MemberOf empty (upstream notebook)",
        "feature_count": len(features),
        "geometry_operations": [],
        "features_sha256": hashlib.sha256(data).hexdigest(),
    }
    if authority_path is not None:
        # Decode the stored source coordinates only; no spatial operations.
        from shapely import from_wkb
        from shapely.geometry import mapping

        authority = json.loads(authority_path.read_text(encoding="utf-8"))
        geometry_id = "edb239a8-4d54-44e4-970a-affb7c9af22e"
        record = authority["objects"]["geometries"][geometry_id]
        if not record["from_year"] <= year <= record["to_year"]:
            raise ValueError("Stored Roman slice does not cover the selected year")
        geometry = from_wkb(bytes.fromhex(record["geom_ewkb_hex"]))
        feature = {
            "type": "Feature",
            "properties": {
                "Name": "Roman Empire (stored Seshat API source)",
                "FromYear": record["from_year"], "ToYear": record["to_year"],
                "source_native_id": record["geometry_source_native_id"],
            },
            "geometry": mapping(geometry),
        }
        source_bytes = json.dumps(feature, separators=(",", ":")).encode("utf-8")
        (output / "stored-rome.geojson").write_bytes(source_bytes)
        manifest["stored_rome"] = {
            "geometry_id": geometry_id,
            "source_native_id": record["geometry_source_native_id"],
            "authority_sha256": hashlib.sha256(authority_path.read_bytes()).hexdigest(),
            "source_ewkb_sha256": hashlib.sha256(bytes.fromhex(record["geom_ewkb_hex"])).hexdigest(),
            "geojson_sha256": hashlib.sha256(source_bytes).hexdigest(),
            "geometry_operations": [],
            "serialization": "EWKB to GeoJSON; no rounding or spatial transformations",
        }
    (output / "manifest.json").write_text(json.dumps(manifest, indent=2) + "\n", encoding="utf-8")
    return manifest


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("archive", type=Path)
    parser.add_argument("--year", type=int, default=6)
    parser.add_argument("--output", type=Path, default=Path("web/public/source-baseline"))
    parser.add_argument("--authority", type=Path, required=True,
                        help="Canonical bundle containing the unmodified Seshat API Roman slice")
    args = parser.parse_args()
    print(json.dumps(extract(args.archive, args.year, args.output, args.authority), indent=2))
