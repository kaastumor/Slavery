#!/usr/bin/env python3
"""Build the R1 MVP geometry/representation manifest without inventing geometry."""
from __future__ import annotations

import argparse
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
R1 = ROOT / "programmes" / "r1"
DEFAULT_OUTPUT = R1 / "r1_mvp_geometry_manifest.json"


def load(name: str):
    return json.loads((R1 / name).read_text(encoding="utf-8"))


def collect_frame_targets(frame: dict) -> dict[str, dict]:
    found: dict[str, dict] = {}
    def walk(value):
        if isinstance(value, dict):
            tid = value.get("target_id")
            if tid:
                found[tid] = value
            for child in value.values():
                walk(child)
        elif isinstance(value, list):
            for child in value:
                walk(child)
    walk(frame)
    return found


def build() -> dict:
    registry = load("r1_candidate_target_registry.json")
    c0 = {r["target_id"]: r for r in load("c0_register.json")}
    frame_doc = load("target_frame.json")
    frame = collect_frame_targets(frame_doc)
    source_meta = frame_doc["source"]

    rows = []
    for target in registry["targets"]:
        tid = target["target_id"]
        source = c0.get(tid, {}).get("source_native")
        frame_row = frame.get(tid, {})
        requirement = target["geometry_requirement"]

        # Strong adversarial default: a source row or sampling midpoint is not a reviewed
        # map geometry. Until an existing repository artifact explicitly establishes a
        # representation, unresolved is safer than silently territorializing the target.
        row = {
            "target_id": tid,
            "target_label": target["target_label"],
            "representation_state": "unresolved_no_geometry",
            "expected_geometry_form": requirement,
            "neutral_world_fallback": True,
            "historical_claim_effect": "none",
            "representation_note": "No reviewed geometry artifact is materialized for this frozen target in the R1 candidate package; render neutral world land and an explicit unresolved state.",
        }
        if source:
            row["source_provenance"] = {
                "dataset": source["dataset"],
                "version_commit": source["commit"],
                "dataset_sha256": source["sha256"],
                "native_row_ordinal": source["row_ordinal"],
                "native_name": source["name"],
                "native_type": source["type"],
                "native_from_year": source["from_year"],
                "native_to_year": source["to_year"],
                "seshat_id": source.get("seshat_id", ""),
                "wikidata": source.get("wikidata", ""),
            }
            anchor = c0[tid]["temporal_frame"]["source_anchor_year"]
            row["temporal_fit"] = {
                "source_anchor_year": anchor,
                "within_native_interval": source["from_year"] <= anchor <= source["to_year"],
            }
        elif frame_row:
            row["source_provenance"] = {
                "dataset": "Cliopatria" if frame_row.get("source_row_ordinal") is not None else "repository_frozen_frame",
                "version_commit": source_meta.get("cliopatria_commit", "") if frame_row.get("source_row_ordinal") is not None else "",
                "dataset_sha256": source_meta.get("cliopatria_sha256", "") if frame_row.get("source_row_ordinal") is not None else "",
                "native_row_ordinal": frame_row.get("source_row_ordinal"),
                "native_name": frame_row.get("source_name", ""),
                "native_from_year": frame_row.get("source_from_year"),
                "native_to_year": frame_row.get("source_to_year"),
                "seshat_id": frame_row.get("source_seshat_id", ""),
                "wikidata": frame_row.get("source_wikidata", ""),
            }
            if frame_row.get("source_anchor_year") is not None:
                start, end = frame_row.get("source_from_year"), frame_row.get("source_to_year")
                row["temporal_fit"] = {
                    "source_anchor_year": frame_row["source_anchor_year"],
                    "within_native_interval": bool(start is not None and end is not None and start <= frame_row["source_anchor_year"] <= end),
                }
        rows.append(row)

    ids = [r["target_id"] for r in rows]
    assert len(rows) == len(set(ids)) == 77, "every frozen target must have exactly one representation state"
    assert all(r["representation_state"] for r in rows), "missing representation state"
    assert all(r["neutral_world_fallback"] is True for r in rows), "neutral fallback must remain universal"
    assert all(r["historical_claim_effect"] == "none" for r in rows), "geometry must not alter historical claims"

    return {
        "schema": "historical-slavery-atlas.r1-mvp-geometry-manifest.v1",
        "candidate_id": registry.get("candidate_id", "R1-candidate-qc-2026-09-24"),
        "canonical_historical_release": "v0.6.1",
        "policy": {
            "unresolved_is_not_absence": True,
            "modern_proxy_must_be_explicit": True,
            "geometry_cannot_strengthen_historical_claim": True,
            "neutral_world_land_always_visible": True,
            "sampling_midpoint_is_not_reviewed_geometry": True,
        },
        "counts": {"targets": 77, "unresolved_no_geometry": len(rows)},
        "rows": rows,
    }


def canonical_bytes(value: dict) -> bytes:
    return (json.dumps(value, ensure_ascii=False, sort_keys=True, indent=2) + "\n").encode("utf-8")


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", type=Path, default=DEFAULT_OUTPUT)
    parser.add_argument("--check", action="store_true")
    args = parser.parse_args()
    expected = canonical_bytes(build())
    if args.check:
        if not args.output.exists() or args.output.read_bytes() != expected:
            raise SystemExit(f"stale or missing geometry manifest: {args.output}")
        print(f"geometry manifest current: {args.output}")
        return 0
    args.output.write_bytes(expected)
    print(f"wrote {args.output} ({len(expected)} bytes)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
