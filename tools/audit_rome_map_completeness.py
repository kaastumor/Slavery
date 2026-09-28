#!/usr/bin/env python3
"""Diagnose Roman map completeness against the exact pinned Cliopatria corpus.

Read-only diagnostic for #365. It verifies the pinned Cliopatria asset, extracts
Roman Empire rows around 1–22 CE with exact row/feature hashes, and compares
semantic control points against the currently served 14–22 CE D-117 geometry.
"""
from __future__ import annotations

import hashlib
import io
import json
from pathlib import Path
import urllib.request
import zipfile

UPSTREAM_URL = (
    "https://raw.githubusercontent.com/Seshat-Global-History-Databank/"
    "cliopatria/ad28a691b7c07c1fca89d0e0636d324667d2a258/"
    "cliopatria.geojson.zip"
)
UPSTREAM_COMMIT = "ad28a691b7c07c1fca89d0e0636d324667d2a258"
UPSTREAM_GIT_BLOB_SHA1 = "cefab0f4b622e2e7fb3daf68d4f461f83991204c"
UPSTREAM_SHA256 = "d01ae3a20d358cc5d54f69d9d725d390767d9c8759ac89ad6f90c58d106f3370"
UPSTREAM_SIZE = 44_231_317
UPSTREAM_FEATURES = 13_765

SERVED = Path(
    "web/public/release-geometries/v0.8.1-public-mvp-v1/"
    "b3066705-616e-42c7-a50d-656c6926813c.json"
)

CONTROL_POINTS = {
    # stable core / provincial centers
    "Rome": (12.4964, 41.9028),
    "Lugdunum_Lyon": (4.8357, 45.7640),
    "Tarraco_Tarragona": (1.2445, 41.1189),
    "Carthage_Tunis": (10.3230, 36.8529),
    "Corinth": (22.9322, 37.9386),
    "Thessaloniki": (22.9444, 40.6401),
    "Ephesus": (27.3410, 37.9390),
    "Antioch": (36.1600, 36.2000),
    "Caesarea_Maritima": (34.8900, 32.5000),
    "Jerusalem": (35.2137, 31.7683),
    "Alexandria": (29.9187, 31.2001),
    "Memphis_Egypt": (31.2500, 29.8500),
    "Aswan": (32.8998, 24.0889),
    "Cyrene": (21.8570, 32.8250),
    "Leptis_Magna": (14.2930, 32.6380),
    # points expected outside in/after Augustus
    "London": (-0.1276, 51.5072),
    "Central_Germania": (10.0, 51.0),
    "Armenia_interior": (44.5, 40.2),
    "Central_Arabia": (42.0, 25.0),
    "Central_Sahara": (10.0, 25.0),
}

EXPECTED_IN = {
    "Rome", "Lugdunum_Lyon", "Tarraco_Tarragona", "Carthage_Tunis",
    "Corinth", "Thessaloniki", "Ephesus", "Antioch", "Caesarea_Maritima",
    "Jerusalem", "Alexandria", "Memphis_Egypt", "Aswan", "Cyrene",
    "Leptis_Magna",
}
EXPECTED_OUT = {
    "London", "Central_Germania", "Armenia_interior", "Central_Arabia",
    "Central_Sahara",
}


def git_blob_sha1(data: bytes) -> str:
    return hashlib.sha1(f"blob {len(data)}\0".encode() + data).hexdigest()


def canonical_json(value: object) -> str:
    return json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(",", ":"))


def load_asset() -> list[dict]:
    request = urllib.request.Request(
        UPSTREAM_URL,
        headers={"User-Agent": "historical-slavery-atlas-rome-completeness/1"},
    )
    with urllib.request.urlopen(request, timeout=120) as response:
        data = response.read()

    observed = {
        "size": len(data),
        "blob": git_blob_sha1(data),
        "sha256": hashlib.sha256(data).hexdigest(),
    }
    expected = {
        "size": UPSTREAM_SIZE,
        "blob": UPSTREAM_GIT_BLOB_SHA1,
        "sha256": UPSTREAM_SHA256,
    }
    if observed != expected:
        raise SystemExit(f"Pinned source identity mismatch: {observed!r}")

    with zipfile.ZipFile(io.BytesIO(data)) as archive:
        members = [
            name for name in archive.namelist()
            if name.lower().endswith(".geojson")
            and not name.startswith("__MACOSX/")
            and not name.rsplit("/", 1)[-1].startswith("._")
        ]
        if len(members) != 1:
            raise SystemExit(f"Expected one data GeoJSON, got {members!r}")
        payload = json.loads(archive.read(members[0]).decode("utf-8"))
    features = payload["features"]
    if len(features) != UPSTREAM_FEATURES:
        raise SystemExit(f"Feature count mismatch: {len(features)}")
    return features


def point_in_ring(point: tuple[float, float], ring: list[list[float]]) -> bool:
    x, y = point
    inside = False
    j = len(ring) - 1
    for i in range(len(ring)):
        xi, yi = ring[i][0], ring[i][1]
        xj, yj = ring[j][0], ring[j][1]
        crosses = (yi > y) != (yj > y)
        if crosses and x < (xj - xi) * (y - yi) / (yj - yi) + xi:
            inside = not inside
        j = i
    return inside


def covers(point: tuple[float, float], geometry: dict | None) -> bool:
    if not geometry:
        return False
    if geometry["type"] == "Polygon":
        polygons = [geometry["coordinates"]]
    elif geometry["type"] == "MultiPolygon":
        polygons = geometry["coordinates"]
    else:
        return False
    for poly in polygons:
        if not poly or not point_in_ring(point, poly[0]):
            continue
        if not any(point_in_ring(point, hole) for hole in poly[1:]):
            return True
    return False


def geometry_summary(geometry: dict) -> dict:
    polygons = (
        [geometry["coordinates"]]
        if geometry["type"] == "Polygon"
        else geometry["coordinates"]
    )
    holes = sum(max(0, len(poly) - 1) for poly in polygons)
    points = sum(len(ring) for poly in polygons for ring in poly)
    return {
        "type": geometry["type"],
        "components": len(polygons),
        "holes": holes,
        "points": points,
    }


def control_matrix(geometry: dict) -> dict[str, bool]:
    return {name: covers(point, geometry) for name, point in CONTROL_POINTS.items()}


def score(matrix: dict[str, bool]) -> dict:
    missing_expected = sorted(name for name in EXPECTED_IN if not matrix[name])
    unexpected_inside = sorted(name for name in EXPECTED_OUT if matrix[name])
    return {
        "expected_inside_count": len(EXPECTED_IN),
        "missing_expected_inside": missing_expected,
        "unexpected_inside": unexpected_inside,
        "pass": not missing_expected and not unexpected_inside,
    }


def main() -> int:
    features = load_asset()
    roman = []
    for ordinal, feature in enumerate(features, start=1):
        props = feature.get("properties") or {}
        if props.get("Name") != "Roman Empire":
            continue
        start, end = props.get("FromYear"), props.get("ToYear")
        if not isinstance(start, int) or not isinstance(end, int):
            continue
        if end < 1 or start > 22:
            continue
        roman.append({
            "source_row_ordinal_1_based": ordinal,
            "source_native_from": start,
            "source_native_to": end,
            "seshat_id": props.get("SeshatID"),
            "wikidata": props.get("Wikidata"),
            "feature_sha256": hashlib.sha256(
                canonical_json(feature).encode("utf-8")
            ).hexdigest(),
            "geometry_summary": geometry_summary(feature["geometry"]),
            "control_matrix": control_matrix(feature["geometry"]),
            "control_score": score(control_matrix(feature["geometry"])),
            "feature": feature,
        })

    frontier_keywords = (
        "cappad", "commag", "juda", "jude", "mauretan", "thrac", "nabat", "armenia"
    )
    frontier_rows = []
    annexation17_features = []
    for ordinal, feature in enumerate(features, start=1):
        props = feature.get("properties") or {}
        name = str(props.get("Name") or "")
        if not any(key in name.lower() for key in frontier_keywords):
            continue
        start, end = props.get("FromYear"), props.get("ToYear")
        if not isinstance(start, int) or not isinstance(end, int):
            continue
        if end < 1 or start > 60:
            continue
        if (
            name in {"Kingdom of Cappadocia", "Kingdom of Commagene"}
            and start <= 17 <= end
        ):
            annexation17_features.append(feature)

        frontier_rows.append({
            "source_row_ordinal_1_based": ordinal,
            "name": name,
            "type": props.get("Type"),
            "source_native_from": start,
            "source_native_to": end,
            "member_of": props.get("MemberOf"),
            "components": props.get("Components"),
            "seshat_id": props.get("SeshatID"),
            "wikidata": props.get("Wikidata"),
            "feature_sha256": hashlib.sha256(
                canonical_json(feature).encode("utf-8")
            ).hexdigest(),
            "geometry_summary": geometry_summary(feature["geometry"]),
        })

    served = json.loads(SERVED.read_text(encoding="utf-8"))
    served_matrix = control_matrix(served["geometry"])
    report = {
        "schema": "atlas-rome-map-completeness-diagnostic-v1",
        "issue": 365,
        "pinned_cliopatria": {
            "commit": UPSTREAM_COMMIT,
            "git_blob_sha1": UPSTREAM_GIT_BLOB_SHA1,
            "sha256": UPSTREAM_SHA256,
            "feature_count": UPSTREAM_FEATURES,
        },
        "roman_source_rows_1_22_ce": [
            {k: v for k, v in row.items() if k != "feature"} for row in roman
        ],
        "frontier_related_source_rows_1_60_ce": frontier_rows,
        "served_14_22": {
            "geometry_id": served.get("geometry_id"),
            "from_year": served.get("from_year"),
            "to_year": served.get("to_year"),
            "accuracy_status": served.get("accuracy_status"),
            "geometry_summary": geometry_summary(served["geometry"]),
            "control_matrix": served_matrix,
            "control_score": score(served_matrix),
        },
    }

    active14 = [
        row for row in roman
        if row["source_native_from"] <= 14 <= row["source_native_to"]
    ]
    if len(active14) != 1:
        report["candidate_14_disposition"] = "BLOCK_AMBIGUOUS_PINNED_SOURCE_ROW"
    else:
        candidate = active14[0]
        report["candidate_14"] = {
            k: v for k, v in candidate.items() if k != "feature"
        }
        report["candidate_14_disposition"] = (
            "CANDIDATE_SEMANTIC_BASELINE_PASSES"
            if candidate["control_score"]["pass"]
            else "BLOCK_PINNED_SOURCE_SEMANTIC_FAILURE"
        )

    Path("rome-annexation-17-source-features.geojson").write_text(
        json.dumps(
            {
                "type": "FeatureCollection",
                "features": annexation17_features,
            },
            ensure_ascii=False,
            sort_keys=True,
        )
        + "\n",
        encoding="utf-8",
    )

    Path("rome-map-completeness-report.json").write_text(
        json.dumps(report, indent=2, ensure_ascii=False, sort_keys=True) + "\n",
        encoding="utf-8",
    )
    if active14:
        Path("rome-cliopatria-ad14-candidate.geojson").write_text(
            json.dumps(active14[0]["feature"], ensure_ascii=False, sort_keys=True) + "\n",
            encoding="utf-8",
        )

    print("ROME_MAP_COMPLETENESS_BEGIN")
    print(json.dumps(report, indent=2, ensure_ascii=False, sort_keys=True))
    print("ROME_MAP_COMPLETENESS_END")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
