#!/usr/bin/env python3
"""Build a deterministic static fallback from one published atlas API payload."""
from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path
from typing import Any


class SnapshotError(ValueError):
    pass


def validate_payload(payload: Any) -> dict[str, Any]:
    if not isinstance(payload, dict):
        raise SnapshotError("atlas payload must be a JSON object")

    required_strings = ("release_version", "schema_version", "status", "data_boundary", "date_model")
    for key in required_strings:
        value = payload.get(key)
        if not isinstance(value, str) or not value.strip():
            raise SnapshotError(f"{key} must be a non-empty string")

    if not isinstance(payload.get("canonical"), bool):
        raise SnapshotError("canonical must be boolean")

    places = payload.get("places")
    if not isinstance(places, list) or not places:
        raise SnapshotError("places must be a non-empty array")

    cartography = payload.get("cartography")
    if not isinstance(cartography, dict):
        raise SnapshotError("cartography must be an object")
    for key in ("fabric_id", "source_url", "content_sha256"):
        value = cartography.get(key)
        if not isinstance(value, str) or not value.strip():
            raise SnapshotError(f"cartography.{key} must be a non-empty string")

    for index, place in enumerate(places):
        if not isinstance(place, dict):
            raise SnapshotError(f"places[{index}] must be an object")
        if not isinstance(place.get("claims"), list):
            raise SnapshotError(f"places[{index}].claims must be an array")
        if not isinstance(place.get("geometries"), list):
            raise SnapshotError(f"places[{index}].geometries must be an array")

    return payload


def canonical_bytes(payload: dict[str, Any]) -> bytes:
    return (
        json.dumps(
            payload,
            ensure_ascii=False,
            sort_keys=True,
            separators=(",", ":"),
        )
        + "\n"
    ).encode("utf-8")


def build_snapshot(
    payload: dict[str, Any],
    output_dir: Path,
    *,
    source_url: str,
    source_git_sha: str,
) -> dict[str, Any]:
    validate_payload(payload)
    output_dir.mkdir(parents=True, exist_ok=True)

    body = canonical_bytes(payload)
    digest = hashlib.sha256(body).hexdigest()
    payload_path = output_dir / "atlas-data.json"
    payload_path.write_bytes(body)

    places = payload["places"]
    claim_count = sum(len(place["claims"]) for place in places)
    geometry_count = sum(len(place["geometries"]) for place in places)
    mapped_geometry_count = sum(
        1
        for place in places
        for geometry in place["geometries"]
        if isinstance(geometry, dict) and geometry.get("geometry") is not None
    )

    manifest = {
        "snapshot_schema": "historical-slavery-atlas-public-snapshot-v1",
        "release_version": payload["release_version"],
        "release_schema_version": payload["schema_version"],
        "canonical": payload["canonical"],
        "source_api_url": source_url,
        "source_git_sha": source_git_sha,
        "payload_file": payload_path.name,
        "payload_sha256": digest,
        "payload_bytes": len(body),
        "place_count": len(places),
        "claim_count": claim_count,
        "geometry_record_count": geometry_count,
        "mapped_geometry_count": mapped_geometry_count,
        "cartography_fabric_id": payload["cartography"]["fabric_id"],
        "cartography_content_sha256": payload["cartography"]["content_sha256"],
    }
    (output_dir / "snapshot-manifest.json").write_text(
        json.dumps(manifest, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )
    return manifest


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("input_json", type=Path)
    parser.add_argument("output_dir", type=Path)
    parser.add_argument("--source-url", required=True)
    parser.add_argument("--source-git-sha", required=True)
    args = parser.parse_args()

    try:
        payload = json.loads(args.input_json.read_text(encoding="utf-8"))
        manifest = build_snapshot(
            payload,
            args.output_dir,
            source_url=args.source_url,
            source_git_sha=args.source_git_sha,
        )
    except (OSError, json.JSONDecodeError, SnapshotError) as exc:
        raise SystemExit(f"invalid published atlas snapshot input: {exc}") from exc

    print(json.dumps(manifest, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
