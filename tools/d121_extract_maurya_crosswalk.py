#!/usr/bin/env python3
"""Bounded D-121 diagnostic for the Maurya source record behind Atlas geometry 15654.

This script downloads only the exact Cliopatria asset already pinned by the
repository, verifies the complete asset identity, and emits a small source
crosswalk candidate. It does not access the Atlas database or mutate release
state.
"""
from __future__ import annotations

import argparse
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
UPSTREAM_REPOSITORY = "Seshat-Global-History-Databank/cliopatria"
UPSTREAM_RELEASE = "v0.2.0-duplicate"
UPSTREAM_COMMIT = "ad28a691b7c07c1fca89d0e0636d324667d2a258"
UPSTREAM_PATH = "cliopatria.geojson.zip"
EXPECTED_SIZE = 44_231_317
EXPECTED_GIT_BLOB_SHA1 = "cefab0f4b622e2e7fb3daf68d4f461f83991204c"
EXPECTED_SHA256 = "d01ae3a20d358cc5d54f69d9d725d390767d9c8759ac89ad6f90c58d106f3370"
EXPECTED_FEATURE_COUNT = 13_765

ATLAS_GEOMETRY_ID = "7dc611d1-4b29-4163-b723-0a597459d298"
LEGACY_API_NATIVE_ID = "15654"
LEGACY_SOURCE_NATIVE_FROM = -256
LEGACY_SOURCE_NATIVE_TO = -226
LEGACY_ATLAS_FROM = -255
LEGACY_ATLAS_TO = -225
LEGACY_RAW_GEOMETRY_MD5 = "ef5fbfded0d89c587308578d51f5089e"

EXPECTED_SPLIT_INTERVALS = [(-256, -248), (-247, -226)]


def git_blob_sha1(data: bytes) -> str:
    prefix = f"blob {len(data)}\0".encode("ascii")
    return hashlib.sha1(prefix + data).hexdigest()


def canonical_json(value: object) -> str:
    return json.dumps(
        value,
        ensure_ascii=False,
        sort_keys=True,
        separators=(",", ":"),
    )


def feature_sha256(feature: dict) -> str:
    return hashlib.sha256(canonical_json(feature).encode("utf-8")).hexdigest()


def geometry_python_default_bytes(geometry: object) -> bytes:
    # The historical batch recorded raw_geojson_md5. The frozen v0.8.1 EWKB
    # independently reproduces all 28 surviving raw MD5s when geometry is
    # serialized with Python's default json.dumps formatting and insertion order.
    return json.dumps(geometry).encode("utf-8")


def load_asset() -> bytes:
    request = urllib.request.Request(
        UPSTREAM_URL,
        headers={"User-Agent": "historical-slavery-atlas-d121-diagnostic/1"},
    )
    with urllib.request.urlopen(request, timeout=120) as response:
        data = response.read()

    observed = {
        "size_bytes": len(data),
        "git_blob_sha1": git_blob_sha1(data),
        "sha256": hashlib.sha256(data).hexdigest(),
    }
    expected = {
        "size_bytes": EXPECTED_SIZE,
        "git_blob_sha1": EXPECTED_GIT_BLOB_SHA1,
        "sha256": EXPECTED_SHA256,
    }
    if observed != expected:
        raise SystemExit(
            "Pinned Cliopatria asset identity mismatch: "
            + json.dumps({"observed": observed, "expected": expected}, sort_keys=True)
        )
    return data


def load_features(data: bytes) -> tuple[str, list[dict]]:
    with zipfile.ZipFile(io.BytesIO(data)) as archive:
        members = [
            name
            for name in archive.namelist()
            if name.lower().endswith(".geojson")
        ]
        if len(members) != 1:
            raise SystemExit(f"Expected one GeoJSON member, found {members!r}")
        member = members[0]
        payload = json.loads(archive.read(member).decode("utf-8"))

    features = payload.get("features") if isinstance(payload, dict) else None
    if not isinstance(features, list) or len(features) != EXPECTED_FEATURE_COUNT:
        raise SystemExit(
            f"Feature count mismatch: {len(features) if isinstance(features, list) else None}"
        )
    return member, features


def row_projection(ordinal: int, feature: dict) -> dict:
    properties = feature.get("properties") or {}
    geometry = feature.get("geometry")
    geometry_bytes = geometry_python_default_bytes(geometry)
    return {
        "source_row_ordinal_1_based": ordinal,
        "source_feature_id": feature.get("id"),
        "name": properties.get("Name"),
        "type": properties.get("Type"),
        "source_native_from": properties.get("FromYear"),
        "source_native_to": properties.get("ToYear"),
        "seshat_id": properties.get("SeshatID"),
        "wikidata": properties.get("Wikidata"),
        "wikipedia": properties.get("Wikipedia"),
        "member_of": properties.get("MemberOf"),
        "components": properties.get("Components"),
        "feature_sha256": feature_sha256(feature),
        "geometry_python_default_md5": hashlib.md5(geometry_bytes).hexdigest(),
        "geometry_python_default_sha256": hashlib.sha256(geometry_bytes).hexdigest(),
        "matches_legacy_raw_geometry_md5": (
            hashlib.md5(geometry_bytes).hexdigest() == LEGACY_RAW_GEOMETRY_MD5
        ),
    }


def build_report(member: str, features: list[dict]) -> dict:
    candidates = []
    all_maurya = []
    for ordinal, feature in enumerate(features, start=1):
        props = feature.get("properties") or {}
        name = str(props.get("Name") or "")
        if "maur" not in name.lower():
            continue
        row = row_projection(ordinal, feature)
        all_maurya.append(row)
        start = props.get("FromYear")
        end = props.get("ToYear")
        if (
            isinstance(start, int)
            and isinstance(end, int)
            and start <= LEGACY_SOURCE_NATIVE_TO
            and end >= LEGACY_SOURCE_NATIVE_FROM
        ):
            candidates.append(row)

    intervals = [
        (row["source_native_from"], row["source_native_to"])
        for row in candidates
    ]
    expected_split_present = intervals == EXPECTED_SPLIT_INTERVALS
    contiguous = bool(candidates) and all(
        candidates[i]["source_native_to"] + 1
        == candidates[i + 1]["source_native_from"]
        for i in range(len(candidates) - 1)
    )
    matches = [
        row for row in candidates if row["matches_legacy_raw_geometry_md5"]
    ]

    if expected_split_present and len(matches) == 1:
        disposition = "PROVISIONAL_PINNED_FEATURE_GEOMETRY_MATCH"
    elif expected_split_present and len(matches) == 2:
        disposition = "PROVISIONAL_TWO_FEATURE_GEOMETRY_MATCH"
    else:
        disposition = "HOLD_SOURCE_BINDING_NOT_CLOSED"

    return {
        "schema": "atlas-d121-maurya-15654-source-extract-v1",
        "scope": "read_only_source_diagnostic",
        "source_asset": {
            "repository": UPSTREAM_REPOSITORY,
            "release": UPSTREAM_RELEASE,
            "commit": UPSTREAM_COMMIT,
            "path": UPSTREAM_PATH,
            "archive_member": member,
            "size_bytes": EXPECTED_SIZE,
            "git_blob_sha1": EXPECTED_GIT_BLOB_SHA1,
            "sha256": EXPECTED_SHA256,
            "feature_count": EXPECTED_FEATURE_COUNT,
        },
        "legacy_atlas_geometry": {
            "geometry_id": ATLAS_GEOMETRY_ID,
            "legacy_api_native_id": LEGACY_API_NATIVE_ID,
            "source_native_interval": [
                LEGACY_SOURCE_NATIVE_FROM,
                LEGACY_SOURCE_NATIVE_TO,
            ],
            "atlas_interval": [LEGACY_ATLAS_FROM, LEGACY_ATLAS_TO],
            "legacy_raw_geometry_md5": LEGACY_RAW_GEOMETRY_MD5,
            "historical_access_contract": (
                "Seshat API name__icontains + pagination + explicit returned-record ID match"
            ),
            "calendar_translation": (
                "negative source-native BCE year + 1 -> Atlas astronomical year; CE unchanged"
            ),
        },
        "candidate_rows": candidates,
        "candidate_count": len(candidates),
        "candidate_intervals": [list(item) for item in intervals],
        "expected_split_intervals": [list(item) for item in EXPECTED_SPLIT_INTERVALS],
        "expected_split_present": expected_split_present,
        "candidate_intervals_contiguous": contiguous,
        "legacy_geometry_match_count": len(matches),
        "legacy_geometry_matching_rows": [
            row["source_row_ordinal_1_based"] for row in matches
        ],
        "all_maurya_row_count": len(all_maurya),
        "disposition": disposition,
        "interpretation_limit": (
            "A pinned ZIP feature match can support a reviewed successor crosswalk. "
            "It does not retroactively recreate or authenticate the missing 2026-09-19 "
            "API response, and it does not by itself close D-121 or authorize release."
        ),
    }


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()

    data = load_asset()
    member, features = load_features(data)
    report = build_report(member, features)
    rendered = json.dumps(report, indent=2, ensure_ascii=False, sort_keys=True) + "\n"
    args.output.write_text(rendered, encoding="utf-8")
    # Logs are deliberately complete for independent readback even if artifact
    # download is unavailable.
    print("D121_REPORT_BEGIN")
    print(rendered, end="")
    print("D121_REPORT_END")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
