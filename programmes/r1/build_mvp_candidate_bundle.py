#!/usr/bin/env python3
"""Build the read-only R1.6 web candidate bundle without new historical inference."""
from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path

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
    rows = []
    for key in ("c1_tranche_01", "c1_tranche_02", "c1_tranche_03"):
        rows.extend(load(INPUTS[key])["rows"])

    targets = registry["targets"]
    target_ids = [t["target_id"] for t in targets]
    row_ids = [r["target_id"] for r in rows]
    temporal_ids = [r["target_id"] for r in temporal["rows"]]
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
    assert states == expected_states, f"research-state drift: {states}"
    assert all(t.get("absence_inference_prohibited") is True for t in targets), "non-absence guard missing"
    assert all(r.get("review_state") == "internally_adversarially_reviewed" for r in rows), "review label drift"
    assert manifest["canonical_release"] == "v0.6.1"

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
        "targets": targets,
        "reviewed_c1": rows,
        "source_dependencies": dependencies,
        "temporal_render_annotations": temporal,
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
