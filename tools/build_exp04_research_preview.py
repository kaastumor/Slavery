#!/usr/bin/env python3
"""Build the non-canonical EXP-04 research-preview bundle.

This is a presentation adapter only. It performs no new historical inference and
never promotes experimental rows into canonical/public data.
"""
from __future__ import annotations

import argparse
import csv
import hashlib
import json
from collections import Counter, defaultdict
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
EXP = ROOT / "experiments" / "exp04-blind-frontier"
TARGETS = EXP / "targets_extended.csv"
SOURCES = EXP / "source_relations.csv"
MANIFEST = EXP / "manifest.json"
DEFAULT_OUTPUT = ROOT / "web" / "public" / "data" / "exp04-research-preview.json"

# Navigation references are deliberately presentation-only. They are familiar site/node
# locators so the eight research targets are inspectable on a world map. They are not
# historical boundaries, territorial centroids, practice extents, or evidence weights.
NAVIGATION_REFERENCES = {
    "R1:P:-2000:E:r1": [
        {"label": "Harappa · navigation reference", "lat": 30.6280, "lon": 72.8639},
    ],
    "R1:P:-2000:D:r1": [
        {"label": "Ur · navigation reference", "lat": 30.9625, "lon": 46.1031},
    ],
    "R1:L:COV2:-500:C": [
        {"label": "Shabwa · navigation reference", "lat": 15.3667, "lon": 47.0167},
    ],
    "R1:L:1300:B": [
        {"label": "Cuzco · navigation reference", "lat": -13.5319, "lon": -71.9675},
    ],
    "R1:L:viking_900": [
        {"label": "Birka · network reference", "lat": 59.3350, "lon": 17.5450},
        {"label": "Hedeby · network reference", "lat": 54.4910, "lon": 9.5650},
        {"label": "Dublin · network reference", "lat": 53.3498, "lon": -6.2603},
    ],
    "R1:L:andaman_1800": [
        {"label": "Andaman Islands · navigation reference", "lat": 11.7401, "lon": 92.6586},
    ],
    "R1:N:angkor_1200": [
        {"label": "Angkor · site reference", "lat": 13.4125, "lon": 103.8670},
    ],
    "R1:P:1800:C:r1": [
        {"label": "Gondar · regional reference", "lat": 12.6030, "lon": 37.4520},
        {"label": "Massawa · network reference", "lat": 15.6097, "lon": 39.4500},
    ],
}

EXPECTED_TARGET_COLUMNS = 21
EXPECTED_SOURCE_COLUMNS = 16
EXPECTED_STAGES = {"researched_internal": 5, "under_review": 3}


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def read_csv(path: Path) -> list[dict[str, str]]:
    with path.open("r", encoding="utf-8", newline="") as handle:
        return list(csv.DictReader(handle))


def build() -> dict:
    targets = read_csv(TARGETS)
    sources = read_csv(SOURCES)
    manifest = json.loads(MANIFEST.read_text(encoding="utf-8"))

    assert len(targets) == 8, f"EXP-04 target drift: {len(targets)}"
    assert len({row["target_id"] for row in targets}) == 8, "duplicate EXP-04 target_id"
    assert set(NAVIGATION_REFERENCES) == {row["target_id"] for row in targets}, "navigation reference membership drift"
    assert Counter(row["research_stage"] for row in targets) == EXPECTED_STAGES, "research-stage drift"
    assert manifest["state"] == "complete_method_test_with_historical_cases_under_review"
    assert manifest["canonical_effect"] == "none"
    assert manifest["reviewed_targets"] == 0
    assert manifest["researched_internal_targets"] == 5
    assert manifest["targets_under_review"] == 3
    assert manifest["not_started"] == 0

    with TARGETS.open("r", encoding="utf-8", newline="") as handle:
        assert len(next(csv.reader(handle))) == EXPECTED_TARGET_COLUMNS, "target CSV shape drift"
    with SOURCES.open("r", encoding="utf-8", newline="") as handle:
        assert len(next(csv.reader(handle))) == EXPECTED_SOURCE_COLUMNS, "source CSV shape drift"

    sources_by_target: dict[str, list[dict[str, str]]] = defaultdict(list)
    for source in sources:
        sources_by_target[source["target_id"]].append(source)

    bundle_targets = []
    for target in targets:
        target_id = target["target_id"]
        bundle_targets.append(
            {
                **target,
                "navigation_references": [
                    {
                        **reference,
                        "role": "navigation_reference_only",
                        "geometry_claim_role": "none",
                        "note": "Reference locator only; not historical geometry, practice extent, jurisdiction, prevalence, or evidence weight.",
                    }
                    for reference in NAVIGATION_REFERENCES[target_id]
                ],
                "sources": sources_by_target.get(target_id, []),
            }
        )

    return {
        "schema": "historical-slavery-atlas.exp04-research-preview.v1",
        "preview_id": "exp04-research-preview",
        "publication_state": "experimental_non_canonical_research_preview",
        "canonical_historical_release": "v0.6.1",
        "review_scope": "internal_research_only_not_independent_historical_review",
        "method_disposition": manifest["method_disposition"],
        "non_absence_rule": "Under-review, unresolved, missing or genre-limited evidence is never rendered as historical absence.",
        "map_semantics": {
            "neutral_world_land_always_visible": True,
            "navigation_references_are_not_historical_geometry": True,
            "practice_polygons_materialized": False,
            "visual_intensity_from_source_counts": False,
            "rule": "The map is navigation/context only. Historical claims live in the evidence table/detail view.",
        },
        "counts": {
            "targets": 8,
            "researched_internal": 5,
            "under_review": 3,
            "independently_reviewed": 0,
            "source_relation_rows": len(sources),
        },
        "source_identity": {
            "targets_extended.csv": sha256(TARGETS),
            "source_relations.csv": sha256(SOURCES),
            "manifest.json": sha256(MANIFEST),
        },
        "targets": bundle_targets,
    }


def canonical_bytes(bundle: dict) -> bytes:
    return (json.dumps(bundle, ensure_ascii=False, sort_keys=True, indent=2) + "\n").encode("utf-8")


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", type=Path, default=DEFAULT_OUTPUT)
    parser.add_argument("--check", action="store_true")
    args = parser.parse_args()

    expected = canonical_bytes(build())
    if args.check:
        if not args.output.exists() or args.output.read_bytes() != expected:
            raise SystemExit(f"stale or missing generated EXP-04 preview bundle: {args.output}")
        print(f"EXP-04 preview bundle current: {args.output}")
        return 0

    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_bytes(expected)
    print(f"wrote {args.output} ({len(expected)} bytes)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
