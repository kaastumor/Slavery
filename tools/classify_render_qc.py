#!/usr/bin/env python3
"""Classify render-candidate QC without silently promoting outliers."""
from __future__ import annotations

import argparse
import json
from pathlib import Path


def candidate_selection(policy: dict, snap_tolerance_m: int | None) -> dict:
    selection = policy.get("candidate_selection") or {}
    preferred = selection.get("preferred_snap_tolerance_m")
    evaluated = selection.get("evaluated_snap_tolerances_m") or []

    if snap_tolerance_m is None:
        role = "unspecified"
    elif preferred is not None and snap_tolerance_m == int(preferred):
        role = "preferred_baseline"
    elif snap_tolerance_m in [int(v) for v in evaluated]:
        role = "alternate_candidate"
    else:
        role = "nonstandard_candidate"

    return {
        "snap_tolerance_m": snap_tolerance_m,
        "selection_role": role,
        "preferred_snap_tolerance_m": preferred,
        "alternate_tolerance_rule": selection.get("alternate_tolerance_rule"),
        "preferred_failure_rule": selection.get("preferred_failure_rule"),
    }


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("qc_report", type=Path)
    parser.add_argument("policy", type=Path)
    parser.add_argument("output", type=Path)
    parser.add_argument("--snap-tolerance-m", type=int)
    args = parser.parse_args()

    qc = json.loads(args.qc_report.read_text(encoding="utf-8"))
    policy = json.loads(args.policy.read_text(encoding="utf-8"))
    gates = policy["hard_gates"]
    selection = candidate_selection(policy, args.snap_tolerance_m)

    decisions = []
    for row in qc.get("features", []):
        reasons = []
        if gates.get("geometry_valid", True) and not row.get("ok", False):
            reasons.append("invalid_geometry")
        if abs(float(row.get("area_delta_pct", 0.0))) > float(gates["max_abs_area_delta_pct"]):
            reasons.append("area_delta")
        if float(row.get("symmetric_difference_pct", 0.0)) > float(gates["max_symmetric_difference_pct"]):
            reasons.append("symmetric_difference")

        status = "quarantined" if reasons else "qc_passed"
        decisions.append(
            {
                "geometry_id": row.get("geometry_id"),
                "name": row.get("name"),
                "status": status,
                "review_state": "not_eligible" if reasons else "awaiting_visual_review",
                "reasons": reasons,
                "metrics": {
                    "area_delta_pct": row.get("area_delta_pct"),
                    "symmetric_difference_pct": row.get("symmetric_difference_pct"),
                    "hausdorff_m": row.get("hausdorff_m"),
                    "source_npoints": row.get("source_npoints"),
                    "render_npoints": row.get("render_npoints"),
                },
            }
        )

    result = {
        "policy_id": policy["policy_id"],
        "source_qc_report": str(args.qc_report),
        "candidate_selection": selection,
        "visual_review_required_before_promotion": policy.get(
            "visual_review_required_before_promotion", True
        ),
        "summary": {
            "qc_passed": sum(1 for d in decisions if d["status"] == "qc_passed"),
            "quarantined": sum(1 for d in decisions if d["status"] == "quarantined"),
        },
        "features": decisions,
    }

    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(json.dumps(result, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
