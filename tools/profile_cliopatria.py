#!/usr/bin/env python3
"""Profile a pinned Cliopatria corpus without promoting geometry into atlas state."""
from __future__ import annotations

import argparse
import hashlib
import json
import subprocess
import urllib.request
import zipfile
from collections import Counter
from pathlib import Path

UPSTREAM_REPO = "Seshat-Global-History-Databank/cliopatria"
UPSTREAM_RELEASE = "v0.2.0-duplicate"
UPSTREAM_COMMIT = "ad28a691b7c07c1fca89d0e0636d324667d2a258"
UPSTREAM_PATH = "cliopatria.geojson.zip"
UPSTREAM_URL = f"https://raw.githubusercontent.com/{UPSTREAM_REPO}/{UPSTREAM_COMMIT}/{UPSTREAM_PATH}"
# Git blob identity is an immutable content checksum supplied by the pinned upstream tree.
UPSTREAM_GIT_BLOB_SHA1 = ""


def git_blob_sha1(data: bytes) -> str:
    return hashlib.sha1(f"blob {len(data)}\0".encode() + data).hexdigest()


def load_features(zip_bytes: bytes):
    import io
    with zipfile.ZipFile(io.BytesIO(zip_bytes)) as zf:
        names = [n for n in zf.namelist() if n.endswith(".geojson")]
        if len(names) != 1:
            raise ValueError(f"expected exactly one GeoJSON member, found {names}")
        payload = json.loads(zf.read(names[0]))
    if payload.get("type") != "FeatureCollection":
        raise ValueError("Cliopatria payload is not a FeatureCollection")
    return payload["features"]


def profile(features):
    types = Counter()
    geometry_types = Counter()
    property_keys = Counter()
    min_year = None
    max_year = None
    negative_year_rows = 0
    crossing_year_zero = 0
    invalid_ranges = 0
    names = set()
    for feature in features:
        props = feature.get("properties") or {}
        property_keys.update(props.keys())
        types[str(props.get("Type", "<missing>"))] += 1
        geometry_types[str((feature.get("geometry") or {}).get("type", "<missing>"))] += 1
        if props.get("Name") is not None:
            names.add(str(props["Name"]))
        fy, ty = props.get("FromYear"), props.get("ToYear")
        if isinstance(fy, int) and isinstance(ty, int):
            min_year = fy if min_year is None else min(min_year, fy)
            max_year = ty if max_year is None else max(max_year, ty)
            negative_year_rows += int(fy < 0 or ty < 0)
            crossing_year_zero += int(fy < 0 < ty)
            invalid_ranges += int(fy > ty)
    return {
        "feature_count": len(features),
        "distinct_names": len(names),
        "type_counts": dict(sorted(types.items())),
        "geometry_type_counts": dict(sorted(geometry_types.items())),
        "property_presence_counts": dict(sorted(property_keys.items())),
        "source_native_years": {
            "minimum": min_year,
            "maximum": max_year,
            "rows_with_negative_year": negative_year_rows,
            "rows_crossing_numeric_zero": crossing_year_zero,
            "invalid_from_to_ranges": invalid_ranges,
            "interpretation": "preserved source-native signed integers; negative=BCE, positive=CE; no atlas normalization performed",
        },
    }


def main():
    p = argparse.ArgumentParser()
    p.add_argument("--input", type=Path, help="local pinned zip; otherwise download immutable URL")
    p.add_argument("--output", type=Path)
    p.add_argument("--expected-git-blob-sha1", default=UPSTREAM_GIT_BLOB_SHA1)
    args = p.parse_args()
    data = args.input.read_bytes() if args.input else urllib.request.urlopen(UPSTREAM_URL, timeout=60).read()
    blob_sha = git_blob_sha1(data)
    if args.expected_git_blob_sha1 and blob_sha != args.expected_git_blob_sha1:
        raise SystemExit(f"upstream blob mismatch: expected {args.expected_git_blob_sha1}, got {blob_sha}")
    result = {
        "source": {
            "repository": UPSTREAM_REPO,
            "release": UPSTREAM_RELEASE,
            "commit": UPSTREAM_COMMIT,
            "path": UPSTREAM_PATH,
            "url": UPSTREAM_URL,
            "git_blob_sha1": blob_sha,
            "sha256": hashlib.sha256(data).hexdigest(),
        },
        "profile": profile(load_features(data)),
        "promotion": "none; raw geography profile only",
    }
    text = json.dumps(result, indent=2, sort_keys=True) + "\n"
    if args.output:
        args.output.write_text(text, encoding="utf-8")
    else:
        print(text, end="")


if __name__ == "__main__":
    main()
