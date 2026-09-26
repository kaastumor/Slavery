#!/usr/bin/env python3
"""Build and verify immutable canonical historical release packages.

Gate 4 deliberately packages the exact D-109 canonical-research authority snapshot
rather than rediscovering membership from mutable database rows.  The source authority
bundle must already pass the Gate-3 full-state preservation contract.

The package is channel-neutral: creating or validating it never changes database
publication_status values and never moves a public release channel.
"""
from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path
import shutil
import sys
import tempfile
from typing import Any

from full_state_release_bundle import validate_bundle as validate_authority_bundle


PACKAGE_CONTRACT = "historical-slavery-atlas-canonical-release-package-v1"
MANIFEST_SCHEMA = "historical-slavery-atlas-canonical-release-manifest-v1"
AUTHORITY_FILENAME = "authority-state.json"
CARTOGRAPHY_FILENAME = "cartography-recovery-fingerprint.json"

GENERATED_DOCS = (
    "RELEASE.md",
    "CHANGELOG.md",
    "QC_SUMMARY.md",
    "UNRESOLVED_ISSUES.md",
    "MIGRATION_RECONCILIATION.md",
)


class ReleaseError(ValueError):
    pass


def sha256_bytes(value: bytes) -> str:
    return hashlib.sha256(value).hexdigest()


def sha256_file(path: Path) -> str:
    return sha256_bytes(path.read_bytes())


def canonical_json_bytes(value: Any) -> bytes:
    return (
        json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(",", ":"))
        + "\n"
    ).encode("utf-8")


def load_json(path: Path) -> dict[str, Any]:
    value = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(value, dict):
        raise ReleaseError(f"{path}: top-level JSON must be an object")
    return value


def require_text_list(spec: dict[str, Any], key: str) -> list[str]:
    value = spec.get(key)
    if not isinstance(value, list) or not value or not all(
        isinstance(item, str) and item.strip() for item in value
    ):
        raise ReleaseError(f"spec.{key} must be a non-empty string array")
    return value


def validate_spec(spec: dict[str, Any]) -> None:
    required = (
        "release_version",
        "release_date",
        "schema_version",
        "purpose",
        "canonical_predecessor",
        "authority",
        "cartography_recovery",
        "review",
        "public_channel",
        "methodology_references",
        "changelog",
        "qc_summary",
        "unresolved_issues",
        "migration_summary",
    )
    for key in required:
        if key not in spec:
            raise ReleaseError(f"spec.{key} is required")

    if spec["purpose"] != "canonical_historical_release":
        raise ReleaseError("spec purpose must be canonical_historical_release")
    if spec.get("canonical") is not True:
        raise ReleaseError("spec canonical must be true")

    predecessor = spec["canonical_predecessor"]
    if not isinstance(predecessor, dict):
        raise ReleaseError("spec.canonical_predecessor must be an object")
    for key in ("version", "filename", "sha256"):
        if not predecessor.get(key):
            raise ReleaseError(f"spec.canonical_predecessor.{key} is required")

    authority = spec["authority"]
    if not isinstance(authority, dict):
        raise ReleaseError("spec.authority must be an object")
    for key in (
        "decision",
        "decision_commit",
        "authority_release_version",
        "membership_sha256",
        "database_state_sha256",
        "reviewed_candidate_id",
        "authority_bundle_sha256",
        "expected_counts",
    ):
        if authority.get(key) in (None, ""):
            raise ReleaseError(f"spec.authority.{key} is required")
    if authority["decision"] != "D-109":
        raise ReleaseError("Gate-4 release must be rooted in D-109 authority")
    if not isinstance(authority["expected_counts"], dict):
        raise ReleaseError("spec.authority.expected_counts must be an object")

    cartography = spec["cartography_recovery"]
    if not isinstance(cartography, dict):
        raise ReleaseError("spec.cartography_recovery must be an object")
    for key in ("decision", "fingerprint_sha256"):
        if not cartography.get(key):
            raise ReleaseError(f"spec.cartography_recovery.{key} is required")
    if cartography["decision"] != "D-108":
        raise ReleaseError("Gate-4 cartography recovery must be rooted in D-108")

    review = spec["review"]
    if not isinstance(review, dict):
        raise ReleaseError("spec.review must be an object")
    if review.get("independent_historical_reviews") != 0:
        raise ReleaseError("independent historical review count must remain truthful")

    channel = spec["public_channel"]
    if not isinstance(channel, dict) or channel.get("moved_by_release") is not False:
        raise ReleaseError("Gate 4 must not move a public release channel")

    require_text_list(spec, "methodology_references")
    require_text_list(spec, "changelog")
    require_text_list(spec, "qc_summary")
    require_text_list(spec, "unresolved_issues")
    require_text_list(spec, "migration_summary")


def authority_counts(bundle: dict[str, Any]) -> dict[str, int]:
    membership = bundle["membership"]
    return {key: len(value) for key, value in sorted(membership.items())}


def validate_authority(spec: dict[str, Any], path: Path) -> dict[str, Any]:
    bundle = load_json(path)
    validate_authority_bundle(bundle)

    authority = spec["authority"]
    digest = sha256_file(path)
    if digest != authority["authority_bundle_sha256"]:
        raise ReleaseError(
            "authority bundle SHA-256 mismatch: "
            f"{digest} != {authority['authority_bundle_sha256']}"
        )

    release = bundle["release"]
    checks = {
        "release_version": (
            release.get("release_version"),
            authority["authority_release_version"],
        ),
        "schema_version": (release.get("schema_version"), spec["schema_version"]),
        "canonical_predecessor_version": (
            release.get("canonical_predecessor_version"),
            spec["canonical_predecessor"]["version"],
        ),
        "workbook_sha256": (
            release.get("workbook_sha256"),
            spec["canonical_predecessor"]["sha256"],
        ),
        "reviewed_candidate_id": (
            release.get("reviewed_candidate_id"),
            authority["reviewed_candidate_id"],
        ),
        "membership_sha256": (
            bundle.get("membership_sha256"),
            authority["membership_sha256"],
        ),
        "database_state_sha256": (
            bundle.get("database_state_sha256"),
            authority["database_state_sha256"],
        ),
    }
    for label, (actual, expected) in checks.items():
        if actual != expected:
            raise ReleaseError(
                f"authority {label} mismatch: {actual!r} != {expected!r}"
            )

    counts = authority_counts(bundle)
    expected_counts = {
        str(key): int(value)
        for key, value in authority["expected_counts"].items()
    }
    if counts != expected_counts:
        raise ReleaseError(
            f"authority membership counts mismatch: {counts} != {expected_counts}"
        )
    return bundle



def validate_cartography_fingerprint(
    spec: dict[str, Any],
    authority: dict[str, Any],
    path: Path,
) -> dict[str, Any]:
    fingerprint = load_json(path)
    expected_sha = spec["cartography_recovery"]["fingerprint_sha256"]
    actual_sha = sha256_file(path)
    if actual_sha != expected_sha:
        raise ReleaseError(
            "cartography fingerprint SHA-256 mismatch: "
            f"{actual_sha} != {expected_sha}"
        )
    if fingerprint.get("fingerprint_schema") != "gate3-cartography-portable-recovery-v1":
        raise ReleaseError("unsupported portable cartography fingerprint schema")

    payload = authority["cartography"]["payload"]
    checks = {
        "fabric_id": (fingerprint.get("fabric_id"), authority["cartography"]["id"]),
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
        "srid": (fingerprint.get("srid"), payload.get("geom_srid")),
        "production_raw_ewkb_sha256": (
            fingerprint.get("production_raw_ewkb_sha256"),
            payload.get("geom_ewkb_sha256"),
        ),
        "production_raw_ewkb_bytes": (
            fingerprint.get("production_raw_ewkb_bytes"),
            payload.get("geom_ewkb_bytes"),
        ),
    }
    for label, (actual, expected) in checks.items():
        if actual != expected:
            raise ReleaseError(
                f"cartography {label} mismatch: {actual!r} != {expected!r}"
            )

    required_portable = (
        "geometry_type",
        "component_count",
        "point_count",
        "geodesic_area_m2_rounded_3",
        "normalized_wkb_sha256",
        "normalized_wkb_bytes",
    )
    for key in required_portable:
        if fingerprint.get(key) in (None, ""):
            raise ReleaseError(f"cartography fingerprint {key} is required")
    return fingerprint

def bullets(items: list[str]) -> str:
    return "\n".join(f"- {item}" for item in items)


def release_md(spec: dict[str, Any], authority: dict[str, Any]) -> str:
    counts = authority_counts(authority)
    p = spec["canonical_predecessor"]
    a = spec["authority"]
    channel = spec["public_channel"]
    return f"""# Historical Slavery Atlas data release {spec['release_version']}

**Release contract:** {PACKAGE_CONTRACT}

This directory contains the exact bytes proposed and approved for the first
PostgreSQL/PostGIS-backed canonical historical release. Canonical publication is a
governed state recorded by the Decisions Log and `audit.release_manifest`; promotion
must use these exact bytes without rewriting the package.

## Authority

The historical release is derived from the explicit D-109 canonical-research authority
closure, not from every row currently present in PostgreSQL and not from
`review_status` alone.

- Authority decision: {a['decision']}
- Authority decision commit: `{a['decision_commit']}`
- Authority snapshot release: `{a['authority_release_version']}`
- Schema head: `{spec['schema_version']}`
- Membership SHA-256: `{a['membership_sha256']}`
- Database-state SHA-256: `{a['database_state_sha256']}`
- Authority bundle SHA-256: `{a['authority_bundle_sha256']}`

Membership counts:

- claims: {counts['claim_ids']}
- actors: {counts['actor_ids']}
- spatial entities: {counts['spatial_entity_ids']}
- reviewed historical geometries: {counts['geometry_ids']}
- voyages: {counts['voyage_ids']}
- coverage assessments: {counts['coverage_assessment_ids']}
- source versions: {counts['source_version_ids']}
- research-target results: {counts['research_target_result_ids']}

## Predecessor

Canonical predecessor: `{p['version']}`

Artifact: `{p['filename']}`

SHA-256: `{p['sha256']}`

The predecessor release remains immutable and is not overwritten by this release.

## Review and publication boundary

Internal research-target reviews represented: {spec['review']['internal_research_target_reviews']}.

Independent historical reviews: **{spec['review']['independent_historical_reviews']}**.

Gate 4 does not move the public UI/API release channel. It remains
`{channel['current_release']}` until a separate Gate-5 cutover passes.

`authority-state.json` is a byte-for-byte preservation copy of the reviewed Gate-3
authority snapshot. `cartography-recovery-fingerprint.json` carries the exact D-108
portable cartography reconstruction invariant. These are preservation evidence, not a
signal that every member must be exposed by the current public UI.

See `manifest.json`, `SHA256SUMS.txt`, the QC/unresolved-issues documents and the
migration/reconciliation report for the complete release contract.
"""


def changelog_md(spec: dict[str, Any]) -> str:
    return f"""# {spec['release_version']} changelog

Compared with canonical predecessor `{spec['canonical_predecessor']['version']}`:

{bullets(spec['changelog'])}

No predecessor bytes are modified.
"""


def qc_md(spec: dict[str, Any], authority: dict[str, Any]) -> str:
    a = spec["authority"]
    return f"""# {spec['release_version']} QC summary

{bullets(spec['qc_summary'])}

## Frozen identities

- Membership SHA-256: `{a['membership_sha256']}`
- Production database-state SHA-256: `{a['database_state_sha256']}`
- Authority bundle SHA-256: `{a['authority_bundle_sha256']}`
- Schema head: `{spec['schema_version']}`
- Independent historical reviews: {spec['review']['independent_historical_reviews']}

The release package does not infer absence from P0, HOLD, researched-inconclusive or
unresolved geometry, and does not derive territorial practice intensity from archive,
document or voyage counts.
"""


def unresolved_md(spec: dict[str, Any]) -> str:
    return f"""# {spec['release_version']} unresolved issues

{bullets(spec['unresolved_issues'])}

These unresolved items remain explicit release state. They are not interpreted as
absence and are not silently normalized away.
"""


def migration_md(spec: dict[str, Any]) -> str:
    return f"""# {spec['release_version']} migration and reconciliation

{bullets(spec['migration_summary'])}

## Methodology references

{bullets(spec['methodology_references'])}
"""


def build_manifest(
    spec: dict[str, Any],
    authority: dict[str, Any],
    output_dir: Path,
) -> dict[str, Any]:
    file_entries = []
    for filename in (AUTHORITY_FILENAME, CARTOGRAPHY_FILENAME, *GENERATED_DOCS):
        path = output_dir / filename
        file_entries.append(
            {
                "filename": filename,
                "sha256": sha256_file(path),
                "size_bytes": path.stat().st_size,
            }
        )

    return {
        "manifest_schema": MANIFEST_SCHEMA,
        "package_contract": PACKAGE_CONTRACT,
        "release_version": spec["release_version"],
        "release_date": spec["release_date"],
        "canonical": True,
        "purpose": spec["purpose"],
        "schema_version": spec["schema_version"],
        "canonical_predecessor": spec["canonical_predecessor"],
        "authority": {
            **spec["authority"],
            "membership": authority["membership"],
        },
        "cartography_recovery": spec["cartography_recovery"],
        "review": spec["review"],
        "public_channel": spec["public_channel"],
        "methodology_references": spec["methodology_references"],
        "files": file_entries,
    }


def write_sums(output_dir: Path) -> None:
    filenames = [
        AUTHORITY_FILENAME,
        CARTOGRAPHY_FILENAME,
        *GENERATED_DOCS,
        "manifest.json",
    ]
    lines = [
        f"{sha256_file(output_dir / filename)}  {filename}"
        for filename in sorted(filenames)
    ]
    (output_dir / "SHA256SUMS.txt").write_text(
        "\n".join(lines) + "\n", encoding="utf-8"
    )


def build_package(
    spec_path: Path,
    authority_path: Path,
    cartography_path: Path,
    output_dir: Path,
) -> None:
    spec = load_json(spec_path)
    validate_spec(spec)
    authority = validate_authority(spec, authority_path)
    validate_cartography_fingerprint(spec, authority, cartography_path)

    if output_dir.exists():
        shutil.rmtree(output_dir)
    output_dir.mkdir(parents=True)

    shutil.copyfile(authority_path, output_dir / AUTHORITY_FILENAME)
    shutil.copyfile(cartography_path, output_dir / CARTOGRAPHY_FILENAME)
    (output_dir / "RELEASE.md").write_text(
        release_md(spec, authority), encoding="utf-8"
    )
    (output_dir / "CHANGELOG.md").write_text(changelog_md(spec), encoding="utf-8")
    (output_dir / "QC_SUMMARY.md").write_text(
        qc_md(spec, authority), encoding="utf-8"
    )
    (output_dir / "UNRESOLVED_ISSUES.md").write_text(
        unresolved_md(spec), encoding="utf-8"
    )
    (output_dir / "MIGRATION_RECONCILIATION.md").write_text(
        migration_md(spec), encoding="utf-8"
    )

    manifest = build_manifest(spec, authority, output_dir)
    (output_dir / "manifest.json").write_bytes(canonical_json_bytes(manifest))
    write_sums(output_dir)


def expected_files() -> set[str]:
    return {
        AUTHORITY_FILENAME,
        *GENERATED_DOCS,
        "manifest.json",
        "SHA256SUMS.txt",
    }


def verify_package(
    spec_path: Path,
    authority_path: Path,
    cartography_path: Path,
    release_dir: Path,
) -> None:
    spec = load_json(spec_path)
    validate_spec(spec)
    authority = validate_authority(spec, authority_path)
    validate_cartography_fingerprint(spec, authority, cartography_path)

    actual_files = {
        path.name for path in release_dir.iterdir() if path.is_file()
    }
    if actual_files != expected_files():
        raise ReleaseError(
            f"release file set mismatch: {actual_files} != {expected_files()}"
        )

    manifest = load_json(release_dir / "manifest.json")
    if manifest.get("manifest_schema") != MANIFEST_SCHEMA:
        raise ReleaseError("unsupported canonical release manifest schema")
    if manifest.get("release_version") != spec["release_version"]:
        raise ReleaseError("manifest release version mismatch")
    if manifest.get("canonical") is not True:
        raise ReleaseError("manifest canonical designation must be true")
    if manifest.get("authority", {}).get("membership") != authority["membership"]:
        raise ReleaseError("manifest authority membership differs from frozen closure")
    if manifest.get("public_channel", {}).get("moved_by_release") is not False:
        raise ReleaseError("Gate-4 package must remain channel-neutral")

    if (release_dir / AUTHORITY_FILENAME).read_bytes() != authority_path.read_bytes():
        raise ReleaseError("authority-state.json is not a byte-for-byte authority copy")
    if (release_dir / CARTOGRAPHY_FILENAME).read_bytes() != cartography_path.read_bytes():
        raise ReleaseError(
            "cartography-recovery-fingerprint.json is not a byte-for-byte D-108 copy"
        )

    for entry in manifest.get("files", []):
        path = release_dir / entry["filename"]
        if not path.is_file():
            raise ReleaseError(f"manifest file missing: {entry['filename']}")
        if sha256_file(path) != entry["sha256"]:
            raise ReleaseError(f"manifest checksum mismatch: {entry['filename']}")
        if path.stat().st_size != entry["size_bytes"]:
            raise ReleaseError(f"manifest size mismatch: {entry['filename']}")

    sums = {}
    for line in (release_dir / "SHA256SUMS.txt").read_text(encoding="utf-8").splitlines():
        digest, filename = line.split("  ", 1)
        sums[filename] = digest
    expected_sum_files = expected_files() - {"SHA256SUMS.txt"}
    if set(sums) != expected_sum_files:
        raise ReleaseError("SHA256SUMS file set mismatch")
    for filename, digest in sums.items():
        if sha256_file(release_dir / filename) != digest:
            raise ReleaseError(f"SHA256SUMS mismatch: {filename}")

    with tempfile.TemporaryDirectory() as tmp:
        rebuilt = Path(tmp) / spec["release_version"]
        build_package(spec_path, authority_path, cartography_path, rebuilt)
        rebuilt_files = {
            path.name for path in rebuilt.iterdir() if path.is_file()
        }
        if rebuilt_files != actual_files:
            raise ReleaseError("deterministic rebuild file set mismatch")
        for filename in sorted(actual_files):
            if (rebuilt / filename).read_bytes() != (release_dir / filename).read_bytes():
                raise ReleaseError(f"deterministic rebuild mismatch: {filename}")


def main() -> int:
    parser = argparse.ArgumentParser()
    sub = parser.add_subparsers(dest="command", required=True)

    build = sub.add_parser("build")
    build.add_argument("spec", type=Path)
    build.add_argument("authority_bundle", type=Path)
    build.add_argument("cartography_fingerprint", type=Path)
    build.add_argument("output_dir", type=Path)

    verify = sub.add_parser("verify")
    verify.add_argument("spec", type=Path)
    verify.add_argument("authority_bundle", type=Path)
    verify.add_argument("cartography_fingerprint", type=Path)
    verify.add_argument("release_dir", type=Path)

    args = parser.parse_args()
    try:
        if args.command == "build":
            build_package(
                args.spec,
                args.authority_bundle,
                args.cartography_fingerprint,
                args.output_dir,
            )
            print(
                json.dumps(
                    {
                        "release_dir": str(args.output_dir),
                        "release_version": load_json(args.spec)["release_version"],
                        "files": sorted(expected_files()),
                    },
                    indent=2,
                )
            )
        else:
            verify_package(
                args.spec,
                args.authority_bundle,
                args.cartography_fingerprint,
                args.release_dir,
            )
            print(
                json.dumps(
                    {
                        "release_dir": str(args.release_dir),
                        "release_version": load_json(args.spec)["release_version"],
                        "verification": "DETERMINISTIC_CANONICAL_RELEASE_PACKAGE_PASS",
                    },
                    indent=2,
                )
            )
        return 0
    except (OSError, json.JSONDecodeError, ReleaseError, ValueError) as exc:
        print(f"BLOCK: {exc}", file=sys.stderr)
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
