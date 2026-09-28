#!/usr/bin/env python3
"""Build the immutable Gate-5 public serving materialization from canonical v0.7.0.

The materialization is a presentation adapter, not a new historical release.  It is
derived only from the immutable canonical release package and never queries mutable
research/publish tables.  The existing map UI receives territorial-practice place
records; other release dimensions and research states are reported explicitly so their
absence from the map cannot be read as historical absence.
"""
from __future__ import annotations

import argparse
from collections import Counter, defaultdict
import hashlib
import json
from pathlib import Path
import shutil
import sys
import tempfile
from typing import Any

from full_state_release_bundle import validate_bundle as validate_authority_bundle


MATERIALIZATION_ID = "v0.7.0-public-mvp-v1"
MATERIALIZATION_SCHEMA = "historical-slavery-atlas-public-materialization-v1"
PAYLOAD_FILENAME = "atlas-data.json"
MANIFEST_FILENAME = "materialization-manifest.json"


class MaterializationError(ValueError):
    pass


def canonical_bytes(value: Any) -> bytes:
    return (
        json.dumps(
            value,
            ensure_ascii=False,
            sort_keys=True,
            separators=(",", ":"),
        )
        + "\n"
    ).encode("utf-8")


def sha256_file(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def load_json(path: Path) -> dict[str, Any]:
    value = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(value, dict):
        raise MaterializationError(f"{path}: expected top-level JSON object")
    return value


def validate_inputs(
    release_dir: Path,
    cartography_fingerprint_path: Path,
) -> tuple[dict[str, Any], dict[str, Any], dict[str, Any]]:
    release_manifest_path = release_dir / "manifest.json"
    authority_path = release_dir / "authority-state.json"
    if not release_manifest_path.is_file() or not authority_path.is_file():
        raise MaterializationError("canonical release package is incomplete")

    release_manifest = load_json(release_manifest_path)
    authority = load_json(authority_path)
    fingerprint = load_json(cartography_fingerprint_path)
    validate_authority_bundle(authority)

    if release_manifest.get("release_version") != "v0.7.0":
        raise MaterializationError("Gate-5 materialization source must be v0.7.0")
    if release_manifest.get("canonical") is not True:
        raise MaterializationError("source release must be canonical")
    if release_manifest.get("purpose") != "canonical_historical_release":
        raise MaterializationError("source release purpose mismatch")
    if release_manifest.get("authority", {}).get("membership") != authority["membership"]:
        raise MaterializationError("release manifest membership differs from authority state")
    if release_manifest.get("schema_version") != authority["release"]["schema_version"]:
        raise MaterializationError("release/authority schema version mismatch")

    release_files = {
        row["filename"]: row
        for row in release_manifest.get("files", [])
        if isinstance(row, dict) and isinstance(row.get("filename"), str)
    }
    authority_entry = release_files.get("authority-state.json")
    if authority_entry is None:
        raise MaterializationError("release manifest omits authority-state.json")
    if authority_entry.get("sha256") != sha256_file(authority_path):
        raise MaterializationError("authority-state.json checksum differs from release manifest")

    if fingerprint.get("fingerprint_schema") != "gate3-cartography-portable-recovery-v1":
        raise MaterializationError("unsupported cartography recovery fingerprint")
    fp_entry = release_files.get("cartography-recovery-fingerprint.json")
    if fp_entry is None:
        raise MaterializationError("release manifest omits cartography recovery fingerprint")
    if fp_entry.get("sha256") != sha256_file(cartography_fingerprint_path):
        raise MaterializationError("cartography fingerprint checksum differs from release manifest")

    cartography = authority["cartography"]
    payload = cartography["payload"]
    checks = {
        "fabric_id": (fingerprint.get("fabric_id"), cartography.get("id")),
        "content_sha256": (
            fingerprint.get("content_sha256"),
            payload.get("content_sha256"),
        ),
        "source_commit_sha": (
            fingerprint.get("source_commit_sha"),
            payload.get("source_commit_sha"),
        ),
        "source_blob_sha": (
            fingerprint.get("source_blob_sha"),
            payload.get("source_blob_sha"),
        ),
    }
    for label, (actual, expected) in checks.items():
        if actual != expected:
            raise MaterializationError(
                f"cartography {label} mismatch: {actual!r} != {expected!r}"
            )

    if authority["membership"]["geometry_ids"] != []:
        raise MaterializationError(
            "v0.7.0 Gate-5 contract expects zero reviewed historical geometries"
        )
    return release_manifest, authority, fingerprint


def source_ref(
    claim_source: dict[str, Any],
    source_versions: dict[str, Any],
) -> dict[str, Any]:
    source_version_id = str(claim_source["source_version_id"])
    source_object = source_versions.get(source_version_id)
    if source_object is None:
        raise MaterializationError(
            f"claim source references non-release source version {source_version_id}"
        )
    source_version = source_object["source_version"]
    source = source_object["source"]
    return {
        "source_version_id": source_version_id,
        "title": source.get("title"),
        "author_or_institution": source.get("author_or_institution"),
        "source_type": source.get("source_type"),
        "source_classification": source.get("source_classification"),
        "version_label": source_version.get("version_label"),
        "url": source_version.get("url_or_identifier"),
        "direction": claim_source.get("direction"),
        "locator": claim_source.get("locator"),
        "directness": claim_source.get("directness"),
        "evidence_role": claim_source.get("evidence_role"),
        "claim_fitness": claim_source.get("claim_fitness"),
        "independence_group": claim_source.get("independence_group"),
    }


def temporal_fields_for_serving(
    claim: dict[str, Any], release_version: str,
) -> dict[str, Any]:
    """Keep the frozen v0.7.0 projection stable; carry existing date meaning forward.

    The full-state authority projects atlas.claim with to_jsonb(c), so these
    values come from the governed record, never from inferred year endpoints.
    """
    if release_version == "v0.7.0":
        return {}
    return {
        key: claim.get(key)
        for key in ("date_text_original", "temporal_precision", "temporal_certainty")
    }


def build_payload(
    release_manifest: dict[str, Any],
    authority: dict[str, Any],
) -> dict[str, Any]:
    claim_objects = authority["objects"]["claims"]
    source_versions = authority["objects"]["source_versions"]
    spatial_objects = authority["objects"]["spatial_entities"]

    claim_kind_counts = Counter(
        obj["claim"]["claim_kind_code"] for obj in claim_objects.values()
    )
    research_results = authority["objects"]["research_target_results"].values()
    research_stage_counts = Counter(
        obj["result"]["research_stage"] for obj in research_results
    )
    research_outcomes = [
        str(obj["result"].get("research_outcome") or "")
        for obj in authority["objects"]["research_target_results"].values()
    ]
    independent_review_count = sum(
        1
        for obj in authority["objects"]["research_target_results"].values()
        for review in obj.get("reviews", [])
        if review.get("review_level") == "independent"
    )

    claims_by_spatial: dict[str, list[dict[str, Any]]] = defaultdict(list)
    for obj in claim_objects.values():
        claim = obj["claim"]
        if claim["claim_kind_code"] != "territorial_practice":
            continue
        practice = obj.get("territorial_practice")
        if not isinstance(practice, dict):
            raise MaterializationError(
                f"territorial claim {claim['claim_id']} lacks subtype record"
            )
        spatial_id = str(practice["spatial_entity_id"])
        if spatial_id not in authority["membership"]["spatial_entity_ids"]:
            raise MaterializationError(
                f"territorial claim references non-release spatial entity {spatial_id}"
            )
        refs = [
            source_ref(row, source_versions)
            for row in sorted(
                obj.get("claim_sources", []),
                key=lambda row: str(row.get("claim_source_id") or ""),
            )
        ]
        if not refs:
            raise MaterializationError(
                f"territorial claim {claim['claim_id']} has no frozen source relation"
            )

        claims_by_spatial[spatial_id].append(
            {
                "claim_id": claim["claim_id"],
                **temporal_fields_for_serving(claim, release_manifest["release_version"]),
                "from_year": claim.get("from_year"),
                "to_year": claim.get("to_year"),
                "summary": claim.get("summary"),
                "review_status": claim.get("review_status"),
                "publication_status": claim.get("publication_status"),
                "practice_type": practice.get("practice_type_code"),
                "practice_level": practice.get("practice_level"),
                "coverage_state": practice.get("coverage_state_code"),
                "classification_status": practice.get("classification_status"),
                "sources": refs,
            }
        )

    places: list[dict[str, Any]] = []
    for spatial_id, claims in claims_by_spatial.items():
        spatial_object = spatial_objects.get(spatial_id)
        if spatial_object is None:
            raise MaterializationError(
                f"missing frozen spatial entity for territorial claim: {spatial_id}"
            )
        entity = spatial_object["spatial_entity"]
        claims.sort(
            key=lambda row: (
                row["from_year"] is None,
                row["from_year"] if row["from_year"] is not None else 0,
                str(row["claim_id"]),
            )
        )
        places.append(
            {
                "spatial_entity_id": spatial_id,
                "name": entity.get("canonical_name"),
                "display_name": entity.get("display_name"),
                "entity_type_code": entity.get("entity_type_code"),
                "notes": entity.get("notes"),
                "claims": claims,
                "geometries": [],
            }
        )

    places.sort(key=lambda row: (str(row["name"]), str(row["spatial_entity_id"])))

    non_mapped = {
        key: value
        for key, value in sorted(claim_kind_counts.items())
        if key != "territorial_practice"
    }
    cartography_payload = authority["cartography"]["payload"]
    return {
        "status": "canonical_release_materialization",
        "release_channel": "public_mvp_preview",
        "release_version": release_manifest["release_version"],
        "serving_materialization_id": MATERIALIZATION_ID,
        "schema_version": release_manifest["schema_version"],
        "canonical": True,
        "data_boundary": "immutable_v070_release_materialization",
        "date_model": "astronomical_year_numbering",
        "display_scope": "territorial_practice_only",
        "release_dimensions": {
            "claim_kind_counts": dict(sorted(claim_kind_counts.items())),
            "non_mapped_claim_kind_counts": non_mapped,
            "research_stage_counts": dict(sorted(research_stage_counts.items())),
            "researched_inconclusive_count": sum(
                "inconclusive" in outcome.lower() for outcome in research_outcomes
            ),
            "independent_historical_reviews": independent_review_count,
            "reviewed_historical_geometry_count": len(
                authority["membership"]["geometry_ids"]
            ),
            "coverage_assessment_count": len(
                authority["membership"]["coverage_assessment_ids"]
            ),
            "source_version_count": len(authority["membership"]["source_version_ids"]),
            "non_absence_note": (
                "Under-review, HOLD, researched-inconclusive and unresolved geometry "
                "states are not historical absence. Non-territorial claim families "
                "remain part of canonical v0.7.0 but are not rendered as territorial "
                "map claims by this adapter."
            ),
        },
        "cartography": {
            "fabric_id": authority["cartography"]["id"],
            "source_name": cartography_payload.get("source_name"),
            "source_version": cartography_payload.get("source_version"),
            "source_url": cartography_payload.get("source_url"),
            "source_commit_sha": cartography_payload.get("source_commit_sha"),
            "source_blob_sha": cartography_payload.get("source_blob_sha"),
            "content_md5": cartography_payload.get("content_md5"),
            "content_sha256": cartography_payload.get("content_sha256"),
        },
        "places": places,
    }


def build_materialization(
    release_dir: Path,
    cartography_fingerprint_path: Path,
    output_dir: Path,
) -> dict[str, Any]:
    release_manifest, authority, fingerprint = validate_inputs(
        release_dir,
        cartography_fingerprint_path,
    )
    payload = build_payload(release_manifest, authority)

    if output_dir.exists():
        shutil.rmtree(output_dir)
    output_dir.mkdir(parents=True)

    payload_path = output_dir / PAYLOAD_FILENAME
    payload_path.write_bytes(canonical_bytes(payload))

    claim_count = sum(len(place["claims"]) for place in payload["places"])
    manifest = {
        "materialization_schema": MATERIALIZATION_SCHEMA,
        "materialization_id": MATERIALIZATION_ID,
        "purpose": "public_mvp_preview",
        "canonical": False,
        "canonical_source_release": release_manifest["release_version"],
        "canonical_source_release_manifest_sha256": sha256_file(
            release_dir / "manifest.json"
        ),
        "canonical_source_authority_sha256": sha256_file(
            release_dir / "authority-state.json"
        ),
        "cartography_fingerprint_sha256": sha256_file(
            cartography_fingerprint_path
        ),
        "payload_file": PAYLOAD_FILENAME,
        "payload_sha256": sha256_file(payload_path),
        "payload_bytes": payload_path.stat().st_size,
        "place_count": len(payload["places"]),
        "territorial_claim_count": claim_count,
        "reviewed_historical_geometry_count": 0,
        "claim_kind_counts": payload["release_dimensions"]["claim_kind_counts"],
        "research_stage_counts": payload["release_dimensions"][
            "research_stage_counts"
        ],
        "researched_inconclusive_count": payload["release_dimensions"][
            "researched_inconclusive_count"
        ],
        "independent_historical_reviews": payload["release_dimensions"][
            "independent_historical_reviews"
        ],
        "rollback_release": "mvp-preview-ancient-v2",
        "source_membership_sha256": authority["membership_sha256"],
        "source_database_state_sha256": authority["database_state_sha256"],
        "source_cartography_content_sha256": fingerprint["content_sha256"],
    }
    (output_dir / MANIFEST_FILENAME).write_bytes(canonical_bytes(manifest))
    return manifest


def verify_materialization(
    release_dir: Path,
    cartography_fingerprint_path: Path,
    materialization_dir: Path,
) -> None:
    expected_files = {PAYLOAD_FILENAME, MANIFEST_FILENAME}
    actual_files = {
        path.name for path in materialization_dir.iterdir() if path.is_file()
    }
    if actual_files != expected_files:
        raise MaterializationError(
            f"materialization file set mismatch: {actual_files} != {expected_files}"
        )

    manifest = load_json(materialization_dir / MANIFEST_FILENAME)
    if manifest.get("materialization_schema") != MATERIALIZATION_SCHEMA:
        raise MaterializationError("materialization schema mismatch")
    if manifest.get("materialization_id") != MATERIALIZATION_ID:
        raise MaterializationError("materialization identity mismatch")
    if manifest.get("purpose") != "public_mvp_preview":
        raise MaterializationError("materialization purpose mismatch")
    if manifest.get("canonical") is not False:
        raise MaterializationError("serving materialization must remain non-canonical")

    payload_path = materialization_dir / PAYLOAD_FILENAME
    payload = load_json(payload_path)
    if sha256_file(payload_path) != manifest.get("payload_sha256"):
        raise MaterializationError("materialization payload checksum mismatch")
    if payload_path.stat().st_size != manifest.get("payload_bytes"):
        raise MaterializationError("materialization payload size mismatch")
    if payload.get("release_version") != "v0.7.0" or payload.get("canonical") is not True:
        raise MaterializationError("payload does not identify canonical v0.7.0")
    if payload.get("serving_materialization_id") != MATERIALIZATION_ID:
        raise MaterializationError("payload materialization identity mismatch")
    if any(place.get("geometries") != [] for place in payload["places"]):
        raise MaterializationError("Gate-5 materialization invented historical geometry")

    with tempfile.TemporaryDirectory() as tmp:
        rebuilt = Path(tmp) / MATERIALIZATION_ID
        build_materialization(
            release_dir,
            cartography_fingerprint_path,
            rebuilt,
        )
        for filename in sorted(expected_files):
            if (rebuilt / filename).read_bytes() != (
                materialization_dir / filename
            ).read_bytes():
                raise MaterializationError(
                    f"deterministic rebuild mismatch: {filename}"
                )


def main() -> int:
    parser = argparse.ArgumentParser()
    sub = parser.add_subparsers(dest="command", required=True)
    for name in ("build", "verify"):
        cmd = sub.add_parser(name)
        cmd.add_argument("release_dir", type=Path)
        cmd.add_argument("cartography_fingerprint", type=Path)
        cmd.add_argument("materialization_dir", type=Path)
    args = parser.parse_args()

    try:
        if args.command == "build":
            manifest = build_materialization(
                args.release_dir,
                args.cartography_fingerprint,
                args.materialization_dir,
            )
            print(json.dumps(manifest, indent=2, sort_keys=True))
        else:
            verify_materialization(
                args.release_dir,
                args.cartography_fingerprint,
                args.materialization_dir,
            )
            print(
                json.dumps(
                    {
                        "verification": "EXACT_V070_PUBLIC_MATERIALIZATION_PASS",
                        "materialization_id": MATERIALIZATION_ID,
                    },
                    indent=2,
                )
            )
        return 0
    except (OSError, json.JSONDecodeError, MaterializationError) as exc:
        print(f"BLOCK: {exc}", file=sys.stderr)
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
