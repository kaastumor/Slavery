#!/usr/bin/env python3
"""Build/verify the non-canonical EXP-06 candidate package and browser bundle."""
from __future__ import annotations

import argparse
import csv
import hashlib
import json
from collections import Counter, defaultdict
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
EXP = ROOT / "experiments" / "exp06-balanced-evidence"
CAND = EXP / "candidate"
WEB = ROOT / "web" / "public" / "data" / "exp06-candidate.json"
SOURCE_COMMIT = "16906affed159722cf940e6723401c7ab4e5d9f4"

NAV = {
    "R1:L:500:F": [{"label": "Phú Yên · regional navigation reference", "lat": 13.0955, "lon": 109.3209}],
    "R1:P:-500:E:r1": [{"label": "Rājagaha / Rajgir · reference locus", "lat": 25.026, "lon": 85.421}],
    "R1:P:1300:A:r1": [{"label": "Mayapán · member-locus reference", "lat": 20.629, "lon": -89.46}],
    "R1:N:mongol_yam_1300": [
        {"label": "Karakorum · network reference", "lat": 47.197, "lon": 102.84},
        {"label": "Dadu / Beijing · network reference", "lat": 39.9042, "lon": 116.4074},
        {"label": "Lhasa · regional network reference", "lat": 29.652, "lon": 91.172},
        {"label": "Tabriz · regional network reference", "lat": 38.08, "lon": 46.291},
    ],
    "R1:N:yaghan_1800": [{"label": "Beagle Channel · regional navigation reference", "lat": -54.86, "lon": -68.1}],
    "R1:P:1300:F:r1": [{"label": "Angkor · capital/core evidence locus", "lat": 13.4125, "lon": 103.867}],
}


def digest_bytes(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def digest(path: Path) -> str:
    return digest_bytes(path.read_bytes())


def read_csv(path: Path) -> list[dict[str, str]]:
    with path.open("r", encoding="utf-8", newline="") as handle:
        return list(csv.DictReader(handle))


def display_state(row: dict[str, str]) -> str:
    if row["research_stage"] == "under_review":
        return "under_review"
    if row["research_outcome"].startswith("researched_inconclusive"):
        return "researched_inconclusive"
    return "researched_bounded"


def build_bundle(target_bytes: bytes, source_bytes: bytes) -> dict:
    targets = read_csv(EXP / "targets_extended.csv")
    sources = read_csv(EXP / "source_relations.csv")

    assert len(targets) == 6
    assert len(sources) == 36
    assert len({row["target_id"] for row in targets}) == 6
    assert set(NAV) == {row["target_id"] for row in targets}

    groups: dict[str, list[dict[str, str]]] = defaultdict(list)
    for row in sources:
        groups[row["target_id"]].append(row)

    enriched = []
    counts: Counter[str] = Counter()
    for row in targets:
        state = display_state(row)
        counts[state] += 1
        enriched.append({
            **row,
            "display_state": state,
            "navigation_references": [{
                **ref,
                "role": "navigation_reference_only",
                "geometry_claim_role": "none",
                "note": "Reference locator only; not historical geometry, practice extent, jurisdiction, prevalence, or evidence weight.",
            } for ref in NAV[row["target_id"]]],
            "sources": groups[row["target_id"]],
        })

    assert counts == Counter({"researched_bounded": 3, "under_review": 2, "researched_inconclusive": 1})

    return {
        "schema": "historical-slavery-atlas.exp06-candidate.v1",
        "candidate_id": "exp06-candidate-v1",
        "publication_state": "published_candidate_noncanonical",
        "canonical_historical_release": "v0.6.1",
        "source_historical_commit": SOURCE_COMMIT,
        "review_scope": "internal_research_only_not_independent_historical_review",
        "non_absence_rule": "Under-review, researched-inconclusive, unresolved, missing or genre-limited evidence is never rendered as historical absence.",
        "map_semantics": {
            "neutral_world_land_always_visible": True,
            "navigation_references_are_not_historical_geometry": True,
            "practice_polygons_materialized": False,
            "visual_intensity_from_source_counts": False,
            "rule": "Map markers are fixed-size navigation/context references only. Historical claims live in the evidence register.",
        },
        "counts": {
            "targets": 6,
            "researched_bounded": 3,
            "researched_inconclusive": 1,
            "under_review": 2,
            "independently_reviewed": 0,
            "source_relation_rows": 36,
        },
        "targets": enriched,
    }


def json_bytes(value: dict, *, sort_keys: bool) -> bytes:
    return (json.dumps(value, ensure_ascii=False, indent=2, sort_keys=sort_keys) + "\n").encode("utf-8")


def build_manifest(bundle_bytes: bytes) -> dict:
    artifacts = [
        ("README.md", CAND / "README.md", "candidate_readme"),
        ("QC_SUMMARY.md", CAND / "QC_SUMMARY.md", "qc_summary"),
        ("UNRESOLVED_ISSUES.md", CAND / "UNRESOLVED_ISSUES.md", "unresolved_issues"),
        ("REVIEW_DECISION.md", CAND / "REVIEW_DECISION.md", "release_gate_decision"),
        ("targets_extended.csv", CAND / "targets_extended.csv", "portable_targets"),
        ("source_relations.csv", CAND / "source_relations.csv", "portable_source_relations"),
        ("../RESULT.md", EXP / "RESULT.md", "research_result"),
        ("../CHECKPOINT.md", EXP / "CHECKPOINT.md", "research_checkpoint"),
    ]
    rows = [{"path": rel, "sha256": digest(path), "role": role} for rel, path, role in artifacts]
    rows.append({
        "path": "../../../web/public/data/exp06-candidate.json",
        "sha256": digest_bytes(bundle_bytes),
        "role": "browser_candidate_bundle",
    })
    return {
        "candidate_id": "exp06-candidate-v1",
        "candidate_status": "noncanonical_publish_candidate_approved",
        "source_historical_commit": SOURCE_COMMIT,
        "canonical_historical_release": "v0.6.1",
        "created_date": "2026-09-24",
        "counts": {
            "targets": 6,
            "researched_bounded": 3,
            "researched_inconclusive": 1,
            "under_review": 2,
            "independently_reviewed": 0,
            "source_relations": 36,
        },
        "release_effect": {
            "canonical_release_change": False,
            "r1_review_state_change": False,
            "p_level_assignment": False,
            "historical_geometry_promotion": False,
            "database_or_api_change": False,
        },
        "artifacts": rows,
        "review_gate": {
            "issue": 227,
            "allowed_dispositions": ["PUBLISH_CANDIDATE", "HOLD_NO_RELEASE", "REWORK"],
            "current_disposition": "PUBLISH_CANDIDATE",
        },
    }


def expected() -> tuple[bytes, bytes, bytes, bytes]:
    source_targets = (EXP / "targets_extended.csv").read_bytes()
    source_relations = (EXP / "source_relations.csv").read_bytes()
    bundle_bytes = json_bytes(build_bundle(source_targets, source_relations), sort_keys=True)
    manifest_bytes = json_bytes(build_manifest(bundle_bytes), sort_keys=False)
    return source_targets, source_relations, bundle_bytes, manifest_bytes


def check() -> None:
    source_targets, source_relations, bundle_bytes, manifest_bytes = expected()
    assertions = {
        CAND / "targets_extended.csv": source_targets,
        CAND / "source_relations.csv": source_relations,
        WEB: bundle_bytes,
        CAND / "manifest.json": manifest_bytes,
    }
    stale = [str(path) for path, data in assertions.items() if not path.exists() or path.read_bytes() != data]
    if stale:
        raise SystemExit("stale EXP-06 candidate artifact(s): " + ", ".join(stale))
    print("EXP-06 candidate package current")


def write() -> None:
    source_targets, source_relations, bundle_bytes, manifest_bytes = expected()
    CAND.mkdir(parents=True, exist_ok=True)
    WEB.parent.mkdir(parents=True, exist_ok=True)
    (CAND / "targets_extended.csv").write_bytes(source_targets)
    (CAND / "source_relations.csv").write_bytes(source_relations)
    WEB.write_bytes(bundle_bytes)
    (CAND / "manifest.json").write_bytes(manifest_bytes)
    print("wrote EXP-06 candidate package")


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--check", action="store_true")
    args = parser.parse_args()
    check() if args.check else write()
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
