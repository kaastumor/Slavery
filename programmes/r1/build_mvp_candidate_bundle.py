#!/usr/bin/env python3
"""Build the read-only R1.6 web candidate bundle without new historical inference."""
from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path

from build_mvp_geometry_manifest import build as build_geometry_manifest

ROOT = Path(__file__).resolve().parents[2]
R1 = ROOT / "programmes" / "r1"
DEFAULT_OUTPUT = ROOT / "web" / "public" / "data" / "r1-mvp-candidate.json"

INPUTS = {
    "manifest": R1 / "r1_release_qc_manifest.json",
    "registry": R1 / "r1_candidate_target_registry.json",
    "dependencies": R1 / "r1_source_dependencies.json",
    "temporal": R1 / "r1_temporal_render_annotations.json",
    "c1_tranche_01": R1 / "c1_tranche_01_final.json",
    "c1_tranche_02": R1 / "c1_tranche_02_final.json",
    "c1_tranche_03": R1 / "c1_tranche_03_final.json",
}


RESEARCH_STATE_DEFINITIONS = [
    {
        "id": "reviewed_classified",
        "label": "Reviewed · bounded-supported",
        "description": "C1 research and adversarial replay completed with a bounded-supported outcome. This is not an intensity score.",
    },
    {
        "id": "reviewed_inconclusive",
        "label": "Reviewed · inconclusive",
        "description": "C1 research and adversarial replay completed, but the exact frozen target/year/frame question remains inconclusive. This is not absence.",
    },
    {
        "id": "planned_unresearched",
        "label": "Planned · unresearched",
        "description": "Identity/time QA permits subject research, but slavery/coercion research has not been performed. This is not absence.",
    },
    {
        "id": "held",
        "label": "Held",
        "description": "Identity/time/frame QA blocks subject research until the issue is resolved. This is not absence and no substitute target is used.",
    },
    {
        "id": "c0_only",
        "label": "Registered only · C0",
        "description": "Registered/research-state target only. C0 is never evidence of historical presence or absence.",
    },
]

GEOMETRY_STATE_DEFINITIONS = [
    {
        "id": "unresolved_no_geometry",
        "label": "Geometry unresolved",
        "description": "No reviewed target geometry is materialized. The neutral world land layer remains visible; unresolved geometry does not imply historical absence.",
    },
]


def overview_research_state(target: dict) -> str:
    state = target["release_research_state"]
    if state == "c1_review_complete":
        outcome = target["classification_outcome"]
        if outcome == "classified":
            return "reviewed_classified"
        if outcome == "inconclusive":
            return "reviewed_inconclusive"
        raise AssertionError(f"unsupported reviewed outcome for MVP overview: {outcome}")
    mapping = {
        "planned_c1_unresearched_ready": "planned_unresearched",
        "held_identity_or_time": "held",
        "c0_registered_unresearched": "c0_only",
    }
    if state not in mapping:
        raise AssertionError(f"unsupported research state for MVP overview: {state}")
    return mapping[state]


def load(path: Path):
    return json.loads(path.read_text(encoding="utf-8"))


def blob_sha(path: Path) -> str:
    data = path.read_bytes()
    return hashlib.sha1(f"blob {len(data)}\0".encode() + data).hexdigest()


def build() -> dict:
    manifest = load(INPUTS["manifest"])
    registry = load(INPUTS["registry"])
    dependencies = load(INPUTS["dependencies"])
    temporal = load(INPUTS["temporal"])
    geometry = build_geometry_manifest()
    rows = []
    for key in ("c1_tranche_01", "c1_tranche_02", "c1_tranche_03"):
        rows.extend(load(INPUTS[key])["rows"])

    targets = registry["targets"]
    target_ids = [t["target_id"] for t in targets]
    row_ids = [r["target_id"] for r in rows]
    temporal_ids = [r["target_id"] for r in temporal["rows"]]
    geometry_ids = [r["target_id"] for r in geometry["rows"]]
    expected_states = {
        "c1_review_complete": 19,
        "planned_c1_unresearched_ready": 15,
        "held_identity_or_time": 2,
        "c0_registered_unresearched": 41,
    }
    states = {}
    for target in targets:
        states[target["release_research_state"]] = states.get(target["release_research_state"], 0) + 1

    assert len(targets) == len(set(target_ids)) == 77, "frozen target membership drift"
    assert len(rows) == len(set(row_ids)) == 19, "reviewed C1 membership drift"
    assert set(row_ids) == set(temporal_ids), "temporal annotation membership drift"
    assert set(target_ids) == set(geometry_ids), "geometry manifest membership drift"
    assert states == expected_states, f"research-state drift: {states}"
    assert all(t.get("absence_inference_prohibited") is True for t in targets), "non-absence guard missing"
    assert all(r.get("review_state") == "internally_adversarially_reviewed" for r in rows), "review label drift"
    assert manifest["canonical_release"] == "v0.6.1"

    geometry_by_id = {row["target_id"]: row for row in geometry["rows"]}
    overview_targets = []
    research_counts = {item["id"]: 0 for item in RESEARCH_STATE_DEFINITIONS}
    geometry_counts = {item["id"]: 0 for item in GEOMETRY_STATE_DEFINITIONS}
    for target in targets:
        tid = target["target_id"]
        research_state = overview_research_state(target)
        geometry_state = geometry_by_id[tid]["representation_state"]
        assert research_state in research_counts, f"unregistered overview research state: {research_state}"
        assert geometry_state in geometry_counts, f"unregistered overview geometry state: {geometry_state}"
        research_counts[research_state] += 1
        geometry_counts[geometry_state] += 1
        overview_targets.append(
            {
                "target_id": tid,
                "research_state": research_state,
                "geometry_state": geometry_state,
            }
        )

    assert research_counts == {
        "reviewed_classified": 5,
        "reviewed_inconclusive": 14,
        "planned_unresearched": 15,
        "held": 2,
        "c0_only": 41,
    }, f"overview research-state drift: {research_counts}"
    assert geometry_counts == {"unresolved_no_geometry": 77}, f"overview geometry-state drift: {geometry_counts}"

    pinned = {item["path"]: item["blob_sha"] for item in manifest["immutable_inputs"]}
    for key in ("c1_tranche_01", "c1_tranche_02", "c1_tranche_03"):
        path = INPUTS[key]
        rel = path.relative_to(ROOT).as_posix()
        assert pinned[rel] == blob_sha(path), f"immutable input drift: {rel}"

    return {
        "schema": "historical-slavery-atlas.r1-mvp-candidate.v1",
        "candidate_id": manifest["candidate_id"],
        "publication_state": "candidate_not_published_not_canonical",
        "canonical_historical_release": "v0.6.1",
        "review_scope": "internal_adversarial_review_only_not_independent_review",
        "non_absence_rule": registry["rule"],
        "source_identity": {name: {"path": path.relative_to(ROOT).as_posix(), "blob_sha": blob_sha(path)} for name, path in INPUTS.items()},
        "counts": {"targets": 77, "reviewed_c1": 19, "source_relations": dependencies["source_relation_count"], "independence_groups": len({g for s in dependencies["source_versions"] for g in s.get("independence_groups", [])})},
        "overview_semantics": {
            "rule": "Research state and geometry state are independent presentation dimensions. Neither is a historical intensity or absence scale.",
            "research_states": [
                {**definition, "count": research_counts[definition["id"]]}
                for definition in RESEARCH_STATE_DEFINITIONS
            ],
            "geometry_states": [
                {**definition, "count": geometry_counts[definition["id"]]}
                for definition in GEOMETRY_STATE_DEFINITIONS
            ],
            "targets": overview_targets,
        },
        "targets": targets,
        "reviewed_c1": rows,
        "source_dependencies": dependencies,
        "temporal_render_annotations": temporal,
        "geometry_manifest": geometry,
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
            raise SystemExit(f"stale or missing generated candidate bundle: {args.output}")
        print(f"candidate bundle current: {args.output}")
        return 0
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_bytes(expected)
    print(f"wrote {args.output} ({len(expected)} bytes)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
