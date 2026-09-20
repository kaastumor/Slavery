#!/usr/bin/env python3
"""Classify render-candidate QC without silently promoting outliers."""
from __future__ import annotations

import argparse
import json
from pathlib import Path


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("qc_report", type=Path)
    parser.add_argument("policy", type=Path)
    parser.add_argument("output", type=Path)
    args = parser.parse_args()

    qc = json.loads(args.qc_report.read_text(encoding="utf-8"))
    policy = json.loads(args.policy.read_text(encoding="utf-8"))
    gates = policy["hard_gates"]

    decisions = []
    for row in qc.get("features", []):
        reasons = []
        if gates.get("geometry_valid", True) and not row.get("ok", False):
            reasons.append("invalid_geometry")
        if abs(float(row.get("area_delta_pct", 0.0))) > float(gates["max_abs_area_delta_pct"]):
            reasons.append("area_delta")
        if float(row.get("symmetric_difference_pct", 0.0)) > float(gates["max_symmetric_difference_pct"]):
            reasons.append("symmetric_difference")

        decisions.append(
            {
                "geometry_id": row.get("geometry_id"),
                "name": row.get("name"),
                "status": "quarantined" if reasons else "qc_passed",
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
