#!/usr/bin/env python3
"""Validate staged external/network participation research cases.

This validator is deliberately read-only. External participation is analytically
separate from territorial practice and must never acquire a P-level or inferred
nationality merely because an actor/place participates in a network.
"""
from __future__ import annotations

import argparse
import json
from pathlib import Path
import re
import sys
from typing import Any

CASE_KEY_RE = re.compile(r"^[a-z0-9][a-z0-9._/-]{2,127}$")
REVIEW_STATUSES = {"draft", "reviewed"}
GEOMETRY_ACCURACY = {"exact", "specialist", "approximate_historical", "modern_proxy", "unresolved"}
EVIDENCE_DIRECTIONS = {"supports", "challenges", "qualifies", "context"}
PARTICIPATION_TYPES = {
    "slave_trade_network", "captive_export", "captive_import", "trade_route",
    "market", "commercial_finance", "state_institutional_participation", "other",
}

class SpecError(ValueError):
    pass

def required(obj: dict[str, Any], key: str, where: str) -> Any:
    value = obj.get(key)
    if value is None or value == "":
        raise SpecError(f"{where}.{key} is required")
    return value

def check_years(obj: dict[str, Any], where: str) -> None:
    start, end = obj.get("from_year"), obj.get("to_year")
    if start is not None and not isinstance(start, int):
        raise SpecError(f"{where}.from_year must be an integer or null")
    if end is not None and not isinstance(end, int):
        raise SpecError(f"{where}.to_year must be an integer or null")
    if start is not None and end is not None and start > end:
        raise SpecError(f"{where}.from_year must be <= to_year")

def validate(spec: dict[str, Any]) -> None:
    key = required(spec, "case_key", "case")
    if not isinstance(key, str) or not CASE_KEY_RE.fullmatch(key):
        raise SpecError("case.case_key must be a stable lowercase case key")
    if spec.get("claim_kind") != "external_participation":
        raise SpecError("case.claim_kind must be external_participation")

    spatial = required(spec, "spatial_entity", "case")
    if not isinstance(spatial, dict):
        raise SpecError("case.spatial_entity must be an object")
    required(spatial, "canonical_name", "case.spatial_entity")
    required(spatial, "entity_type_code", "case.spatial_entity")
    check_years(spatial, "case.spatial_entity")

    claim = required(spec, "claim", "case")
    if not isinstance(claim, dict):
        raise SpecError("case.claim must be an object")
    required(claim, "summary", "case.claim")
    check_years(claim, "case.claim")
    if claim.get("review_status", "draft") not in REVIEW_STATUSES:
        raise SpecError("case.claim.review_status must be draft or reviewed")
    if claim.get("publication_status") not in (None, "unpublished"):
        raise SpecError("research staging may only contain unpublished claims")
    if "territorial_practice" in claim:
        raise SpecError("external participation must not embed territorial_practice")
    if "practice_level" in claim:
        raise SpecError("external participation must not carry a P-level")

    external = required(claim, "external_participation", "case.claim")
    if not isinstance(external, dict):
        raise SpecError("case.claim.external_participation must be an object")
    participation_type = required(external, "participation_type_code", "case.claim.external_participation")
    if participation_type not in PARTICIPATION_TYPES:
        raise SpecError(f"unsupported participation type: {participation_type}")
    required(external, "role_text", "case.claim.external_participation")

    evidence = required(spec, "evidence", "case")
    if not isinstance(evidence, list) or not evidence:
        raise SpecError("case.evidence must be a non-empty array")
    for index, item in enumerate(evidence):
        where = f"case.evidence[{index}]"
        if not isinstance(item, dict):
            raise SpecError(f"{where} must be an object")
        source = required(item, "source", where)
        version = required(item, "version", where)
        if not isinstance(source, dict) or not isinstance(version, dict):
            raise SpecError(f"{where}.source and .version must be objects")
        required(source, "title", f"{where}.source")
        required(version, "url_or_identifier", f"{where}.version")
        if item.get("direction", "supports") not in EVIDENCE_DIRECTIONS:
            raise SpecError(f"unsupported evidence direction: {item.get('direction')}")

    geometry = spec.get("geometry")
    if geometry is not None:
        if not isinstance(geometry, dict):
            raise SpecError("case.geometry must be an object or null")
        check_years(geometry, "case.geometry")
        accuracy = required(geometry, "accuracy_status", "case.geometry")
        if accuracy not in GEOMETRY_ACCURACY:
            raise SpecError(f"unsupported geometry accuracy: {accuracy}")
        required(geometry, "resolution_method", "case.geometry")
        geojson = geometry.get("geojson")
        if accuracy == "unresolved" and geojson is not None:
            raise SpecError("unresolved geometry must have geojson=null")
        if accuracy != "unresolved" and not isinstance(geojson, dict):
            raise SpecError("resolved geometry requires a GeoJSON geometry object")

    guardrails = required(spec, "guardrails", "case")
    if not isinstance(guardrails, dict):
        raise SpecError("case.guardrails must be an object")
    for key in ("territorial_practice_inferred", "practice_level_assigned", "nationality_inferred", "absence_inferred"):
        if guardrails.get(key) is not False:
            raise SpecError(f"case.guardrails.{key} must be false")

def load(path: Path) -> dict[str, Any]:
    payload = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(payload, dict):
        raise SpecError("top-level JSON value must be an object")
    validate(payload)
    return payload

def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("case_file", type=Path)
    args = parser.parse_args()
    try:
        spec = load(args.case_file)
    except (OSError, json.JSONDecodeError, SpecError) as exc:
        raise SystemExit(f"invalid external participation case: {exc}") from exc
    print(json.dumps({
        "case_key": spec["case_key"],
        "claim_kind": spec["claim_kind"],
        "participation_type": spec["claim"]["external_participation"]["participation_type_code"],
        "publication_status": "unpublished",
        "evidence_sources": len(spec["evidence"]),
        "geometry_accuracy": (spec.get("geometry") or {}).get("accuracy_status"),
    }, indent=2, ensure_ascii=False))
    print("VALIDATION ONLY: no database changes made")
    return 0

if __name__ == "__main__":
    sys.exit(main())
