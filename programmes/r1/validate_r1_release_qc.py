#!/usr/bin/env python3
"""Deterministic R1.6 candidate-package QC.

This validates release assembly semantics only. It does not perform historical
research, geometry resolution, publication, or canonical promotion.
"""
from __future__ import annotations

import hashlib
import importlib.util
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
R1 = ROOT / "programmes" / "r1"

FINAL_FILES = [
    R1 / "c1_tranche_01_final.json",
    R1 / "c1_tranche_02_final.json",
    R1 / "c1_tranche_03_final.json",
]
REGISTRY = R1 / "r1_candidate_target_registry.json"
DEPENDENCIES = R1 / "r1_source_dependencies.json"
MANIFEST = R1 / "r1_release_qc_manifest.json"
TEMPORAL = R1 / "r1_temporal_render_annotations.json"
CORE_VALIDATOR = R1 / "validate_core_contract.py"

ALLOWED_TEMPORAL_STATES = {
    "supported_exact_cross_section",
    "supported_period_level",
    "supported_near_anchor_approximate",
    "unknown",
    "not_applicable_aggregate",
}


def load(path: Path):
    return json.loads(path.read_text(encoding="utf-8"))


def git_blob_sha(path: Path) -> str:
    data = path.read_bytes()
    payload = f"blob {len(data)}\0".encode("utf-8") + data
    return hashlib.sha1(payload).hexdigest()


def core_module():
    spec = importlib.util.spec_from_file_location("r1core", CORE_VALIDATOR)
    module = importlib.util.module_from_spec(spec)
    assert spec.loader is not None
    spec.loader.exec_module(module)
    return module


def validate_release():
    errors = []
    warnings = []

    rows = []
    for path in FINAL_FILES:
        rows.extend(load(path)["rows"])

    registry = load(REGISTRY)
    deps = load(DEPENDENCIES)
    manifest = load(MANIFEST)
    temporal = load(TEMPORAL)
    core = core_module()

    # Membership / Core Contract.
    ids = [r["target_id"] for r in rows]
    if len(rows) != 19:
        errors.append(f"expected 19 C1 rows, found {len(rows)}")
    if len(set(ids)) != len(ids):
        errors.append("duplicate C1 target ids")

    for row in rows:
        row_errors = core.validate_row(row)
        if row_errors:
            errors.append(f'{row["target_id"]}: ' + "; ".join(row_errors))
        if row.get("research_stage") != "review_complete":
            errors.append(f'{row["target_id"]}: research not review_complete')
        if row.get("review_state") != "internally_adversarially_reviewed":
            errors.append(f'{row["target_id"]}: missing full internal adversarial review')

    # C2 closure.
    completed_c2 = [r for r in rows if r.get("c2_completed")]
    if len(completed_c2) != 4:
        errors.append(f"expected 4 completed C2 packets, found {len(completed_c2)}")
    unresolved = [r["target_id"] for r in rows if r.get("c2_required")]
    if unresolved:
        errors.append("unresolved C2 rows: " + ", ".join(unresolved))

    # Candidate publication gates for positive rows.
    temporal_rows = temporal["rows"]
    temporal_by_id = {r["target_id"]: r for r in temporal_rows}
    if len(temporal_by_id) != 19:
        errors.append("temporal rendering annotations must cover exactly 19 unique C1 rows")
    if set(temporal_by_id) != set(ids):
        errors.append("temporal rendering membership differs from C1 membership")

    for item in temporal_rows:
        if item.get("state") not in ALLOWED_TEMPORAL_STATES:
            errors.append(f'{item.get("target_id")}: invalid temporal render state')

    for row in rows:
        if row.get("classification_outcome") != "classified":
            continue
        decisive = [s for s in row.get("sources", []) if s.get("decisive")]
        if not decisive:
            errors.append(f'{row["target_id"]}: classified row has no decisive source')
        if decisive and all(
            s.get("claim_fitness") in {"context_only", "review_required"}
            for s in decisive
        ):
            errors.append(f'{row["target_id"]}: positive relies only on weak decisive sources')
        if any(s.get("claim_fitness") == "usable_with_limitation" for s in decisive):
            if row.get("review_state") != "internally_adversarially_reviewed":
                errors.append(f'{row["target_id"]}: usable-with-limitation positive not replayed')
        state = temporal_by_id[row["target_id"]]["state"]
        if not state.startswith("supported_"):
            errors.append(f'{row["target_id"]}: classified row lacks supported temporal render state')

    # Source/version/dependency reconstruction.
    relation_count = sum(len(r.get("sources", [])) for r in rows)
    if deps.get("source_relation_count") != relation_count:
        errors.append("source dependency relation count mismatch")
    if deps.get("unique_source_version_count") != len(deps.get("source_versions", [])):
        errors.append("source dependency unique-version count mismatch")

    seen_dependency_pairs = set()
    for source in deps.get("source_versions", []):
        if not source.get("source_version_ref"):
            errors.append("dependency source missing source_version_ref")
        if not source.get("url"):
            errors.append(f'{source.get("source_version_ref")}: missing recoverable URL')
        if not source.get("locators"):
            errors.append(f'{source.get("source_version_ref")}: missing locator')
        if not source.get("independence_groups"):
            errors.append(f'{source.get("source_version_ref")}: missing independence group')
        if not source.get("dependents"):
            errors.append(f'{source.get("source_version_ref")}: no dependent target')
        for dep in source.get("dependents", []):
            pair = (source["source_version_ref"], dep["target_id"])
            seen_dependency_pairs.add(pair)
            if dep["target_id"] not in ids:
                errors.append(f'{source["source_version_ref"]}: unknown dependent target')

    expected_pairs = {
        (s["source_version_ref"], row["target_id"])
        for row in rows
        for s in row.get("sources", [])
    }
    if seen_dependency_pairs != expected_pairs:
        errors.append("source dependency table does not reconstruct all row/source relations")

    # Frozen target/research-state registry.
    targets = registry.get("targets", [])
    states = {}
    for target in targets:
        states[target["release_research_state"]] = states.get(target["release_research_state"], 0) + 1
        if not target.get("geometry_requirement"):
            errors.append(f'{target["target_id"]}: missing geometry requirement')
        if not target.get("geometry_release_state"):
            errors.append(f'{target["target_id"]}: missing geometry release state')
        if not target.get("geometry_truth_rule"):
            errors.append(f'{target["target_id"]}: missing geometry truth guard')
        if target["release_research_state"] != "c1_review_complete":
            if target.get("classification_outcome") != "unassessed":
                errors.append(f'{target["target_id"]}: unresearched/held target has assessed outcome')
            if target.get("absence_inference_prohibited") is not True:
                errors.append(f'{target["target_id"]}: missing non-absence guard')

    expected_states = {
        "c1_review_complete": 19,
        "planned_c1_unresearched_ready": 15,
        "held_identity_or_time": 2,
        "c0_registered_unresearched": 41,
    }
    if states != expected_states:
        errors.append(f"registry state counts changed: {states!r}")
    if len(targets) != 77 or len({t["target_id"] for t in targets}) != 77:
        errors.append("candidate registry must contain 77 unique frozen targets")

    registry_by_id = {t["target_id"]: t for t in targets}
    if any(registry_by_id.get(i, {}).get("release_research_state") != "c1_review_complete" for i in ids):
        errors.append("reviewed C1 membership not reflected in candidate registry")

    # Frozen balance gate among researched polity rows.
    sectors = {}
    for target in targets:
        if target["release_research_state"] != "c1_review_complete":
            continue
        sector = target.get("sampling_sector")
        if sector:
            sectors[sector] = sectors.get(sector, 0) + 1
    if set(sectors) != set("ABCDEF"):
        errors.append(f"researched polity sectors incomplete: {sectors!r}")
    sector_total = sum(sectors.values())
    if sector_total != 12:
        errors.append(f"expected 12 researched polity rows, found {sector_total}")
    if sectors and max(sectors.values()) / sector_total > 0.25:
        errors.append(f"polity sector exceeds 25%: {sectors!r}")

    # Immutable-input reconstruction: verify Git blob SHAs pinned in manifest.
    manifest_inputs = {x["path"]: x["blob_sha"] for x in manifest["immutable_inputs"]}
    for rel, expected_sha in manifest_inputs.items():
        path = ROOT / rel
        if not path.exists():
            errors.append(f"manifest input missing: {rel}")
            continue
        actual = git_blob_sha(path)
        if actual != expected_sha:
            errors.append(f"manifest input blob mismatch: {rel} expected {expected_sha} got {actual}")

    # Geometry is deliberately a R1.7 materialization boundary, not hidden completeness.
    geometry_states = {t["geometry_release_state"] for t in targets}
    if geometry_states == {"not_materialized_in_r1_6_qc"}:
        warnings.append(
            "concrete geometry materialization is deferred to R1.7; "
            "candidate map publication must not proceed until explicit geometry/proxy/unresolved states are resolved"
        )

    return {
        "errors": errors,
        "warnings": warnings,
        "counts": {
            "c1_rows": len(rows),
            "classified": sum(r["classification_outcome"] == "classified" for r in rows),
            "inconclusive": sum(r["classification_outcome"] == "inconclusive" for r in rows),
            "c2_completed": len(completed_c2),
            "adversarially_reviewed": sum(
                r.get("review_state") == "internally_adversarially_reviewed" for r in rows
            ),
            "source_relations": relation_count,
            "source_versions": len(deps.get("source_versions", [])),
            "independence_groups": len(deps.get("independence_groups", [])),
            "frozen_targets": len(targets),
        },
        "registry_states": states,
        "polity_sectors": sectors,
    }


def main():
    result = validate_release()
    print(json.dumps(result, indent=2, sort_keys=True))
    raise SystemExit(1 if result["errors"] else 0)


if __name__ == "__main__":
    main()
