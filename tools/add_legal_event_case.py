#!/usr/bin/env python3
"""Validate and ingest one bounded legal-event research case.

This is the legal/state-event counterpart to add_research_case.py. It uses the
existing claim/source, legal_event, research-target, review and ingest-ledger
tables; it does not create or alter schema and never publishes a claim.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import os
from pathlib import Path
import re
import sys
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from tools.add_research_case import (
    CASE_KEY_RE,
    EVIDENCE_DIRECTIONS,
    REVIEW_STATUSES,
    ensure_source_version,
    ensure_spatial_entity,
    existing_case_ingest,
)

TARGET_KEY_RE = re.compile(r"^[a-z0-9][a-z0-9._/-]{2,191}$")


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


def canonical_json(value: Any) -> str:
    return json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(",", ":"))


def content_sha256(value: Any) -> str:
    return hashlib.sha256(canonical_json(value).encode("utf-8")).hexdigest()


def validate_spec(spec: dict[str, Any], *, require_case_key: bool = False) -> None:
    case_key = spec.get("case_key")
    if case_key is None:
        if require_case_key:
            raise SpecError("case.case_key is required")
    elif not isinstance(case_key, str) or not CASE_KEY_RE.fullmatch(case_key):
        raise SpecError("case.case_key does not satisfy the stable case-key contract")

    spatial = required(spec, "spatial_entity", "case")
    if not isinstance(spatial, dict):
        raise SpecError("case.spatial_entity must be an object")
    required(spatial, "canonical_name", "case.spatial_entity")
    required(spatial, "entity_type_code", "case.spatial_entity")
    check_years(spatial, "case.spatial_entity")
    if spatial.get("review_status", "draft") not in REVIEW_STATUSES:
        raise SpecError("unsupported spatial review status")

    claim = required(spec, "claim", "case")
    if not isinstance(claim, dict):
        raise SpecError("case.claim must be an object")
    required(claim, "summary", "case.claim")
    check_years(claim, "case.claim")
    if claim.get("review_status", "draft") not in REVIEW_STATUSES:
        raise SpecError("unsupported claim review status")
    if claim.get("publication_status") not in (None, "unpublished"):
        raise SpecError("legal-event ingestion may only create unpublished claims")

    event = required(spec, "legal_event", "case")
    if not isinstance(event, dict):
        raise SpecError("case.legal_event must be an object")
    required(event, "event_type", "case.legal_event")
    required(event, "scope", "case.legal_event")

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
            raise SpecError(f"unsupported evidence direction in {where}")

    research = required(spec, "research_target", "case")
    if not isinstance(research, dict):
        raise SpecError("case.research_target must be an object")
    target_key = required(research, "target_key", "case.research_target")
    if not isinstance(target_key, str) or not TARGET_KEY_RE.fullmatch(target_key):
        raise SpecError("research_target.target_key does not satisfy stable-key contract")
    required(research, "target_label", "case.research_target")
    required(research, "anchor_label", "case.research_target")
    required(research, "frame_class", "case.research_target")
    if research.get("anchor_year") is not None and not isinstance(research["anchor_year"], int):
        raise SpecError("research_target.anchor_year must be integer or null")
    result = required(research, "result", "case.research_target")
    if not isinstance(result, dict):
        raise SpecError("research_target.result must be an object")
    required(result, "research_stage", "case.research_target.result")
    required(result, "research_outcome", "case.research_target.result")
    if result.get("review_status", "draft") not in REVIEW_STATUSES:
        raise SpecError("unsupported research-result review status")
    review = required(research, "internal_review", "case.research_target")
    if not isinstance(review, dict):
        raise SpecError("research_target.internal_review must be an object")
    required(review, "review_disposition", "case.research_target.internal_review")
    if not isinstance(review.get("admitted"), bool):
        raise SpecError("research_target.internal_review.admitted must be boolean")
    required(review, "review_reason", "case.research_target.internal_review")


def load_spec(path: Path, *, require_case_key: bool = False) -> dict[str, Any]:
    spec = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(spec, dict):
        raise SpecError("top-level JSON value must be an object")
    validate_spec(spec, require_case_key=require_case_key)
    return spec


def plan(spec: dict[str, Any]) -> dict[str, Any]:
    return {
        "case_key": spec.get("case_key"),
        "content_sha256": content_sha256(spec),
        "spatial_entity": spec["spatial_entity"]["canonical_name"],
        "claim_kind": "legal_event",
        "claim_interval": [spec["claim"].get("from_year"), spec["claim"].get("to_year")],
        "event_type": spec["legal_event"]["event_type"],
        "review_status": spec["claim"].get("review_status", "draft"),
        "publication_status": "unpublished",
        "evidence_sources": len(spec["evidence"]),
        "research_target_key": spec["research_target"]["target_key"],
        "research_outcome": spec["research_target"]["result"]["research_outcome"],
        "internally_admitted": spec["research_target"]["internal_review"]["admitted"],
    }


def ensure_target(cur, research: dict[str, Any], spatial_id: str) -> None:
    cur.execute(
        """select target_label, anchor_label, anchor_year, frame_class,
                  spatial_entity_id::text, origin, review_status::text
             from audit.research_target where target_key=%s""",
        (research["target_key"],),
    )
    row = cur.fetchone()
    expected = (
        research["target_label"],
        research["anchor_label"],
        research.get("anchor_year"),
        research["frame_class"],
        spatial_id,
        research.get("origin"),
        research.get("review_status", "draft"),
    )
    if row:
        if tuple(row) != expected:
            raise RuntimeError("existing research target differs from legal-event spec")
        return
    cur.execute(
        """insert into audit.research_target(
             target_key,target_label,anchor_label,anchor_year,frame_class,
             spatial_entity_id,origin,review_status)
           values (%s,%s,%s,%s,%s,%s,%s,%s::atlas.review_status)""",
        (research["target_key"],) + expected,
    )


def insert_case(conn, spec: dict[str, Any], *, source_path: str | None = None,
                git_revision: str | None = None) -> tuple[str, bool]:
    case_key = spec.get("case_key")
    if not case_key:
        raise SpecError("case.case_key is required for database ingestion")
    digest = content_sha256(spec)

    with conn.cursor() as cur:
        existing = existing_case_ingest(cur, case_key)
        if existing:
            old_digest, claim_id = existing
            if old_digest == digest:
                return str(claim_id), False
            raise RuntimeError(
                f"research case {case_key!r} was already applied with different content; "
                "create a new case_key and use review/supersession"
            )

        spatial_id = ensure_spatial_entity(cur, spec["spatial_entity"])
        source_rows: list[tuple[str, dict[str, Any]]] = []
        for evidence in spec["evidence"]:
            source_rows.append(
                (ensure_source_version(cur, evidence["source"], evidence["version"]), evidence)
            )

        claim = spec["claim"]
        cur.execute(
            """insert into atlas.claim(
                 claim_kind_code,from_year,to_year,date_text_original,temporal_precision,
                 temporal_certainty,spatial_precision,summary,confidence,review_status,
                 publication_status,notes)
               values ('legal_event',%s,%s,%s,%s,%s,%s,%s,%s,
                       %s::atlas.review_status,'unpublished'::atlas.publication_status,%s)
               returning claim_id""",
            (
                claim.get("from_year"), claim.get("to_year"), claim.get("date_text_original"),
                claim.get("temporal_precision"), claim.get("temporal_certainty"),
                claim.get("spatial_precision"), claim["summary"], claim.get("confidence"),
                claim.get("review_status", "draft"), claim.get("notes"),
            ),
        )
        claim_id = str(cur.fetchone()[0])

        event = spec["legal_event"]
        cur.execute(
            """insert into atlas.legal_event(
                 claim_id,jurisdiction_spatial_entity_id,event_type,legal_status_after,
                 instrument_name,scope,effective_date_text,notes)
               values (%s,%s,%s,%s,%s,%s,%s,%s)""",
            (
                claim_id, spatial_id, event["event_type"], event.get("legal_status_after"),
                event.get("instrument_name"), event["scope"], event.get("effective_date_text"),
                event.get("notes"),
            ),
        )

        for source_version_id, evidence in source_rows:
            cur.execute(
                """insert into atlas.claim_source(
                     claim_id,source_version_id,evidence_role,independence_group,directness,
                     direction,locator,notes,claim_fitness)
                   values (%s,%s,%s,%s,%s,%s::atlas.evidence_direction,%s,%s,%s)""",
                (
                    claim_id, source_version_id, evidence.get("evidence_role"),
                    evidence.get("independence_group"), evidence.get("directness"),
                    evidence.get("direction", "supports"), evidence.get("locator"),
                    evidence.get("notes"), evidence.get("claim_fitness"),
                ),
            )

        research = spec["research_target"]
        ensure_target(cur, research, spatial_id)
        result = research["result"]
        result_digest = content_sha256({"target_key": research["target_key"], "result": result})
        cur.execute(
            """insert into audit.research_target_result(
                 target_key,research_stage,research_outcome,bounded_proposition,
                 required_abstention,evidence_locus_summary,inference_extent_summary,
                 temporal_state,law_practice_note,network_territorial_note,historical_terms,
                 category_mapping_status,category_mapping_note,language_access_limitations,
                 coverage_confidence,geometry_resolved_form,geometry_claim_role,
                 geometry_unresolved_note,source_path,source_blob_ref,content_sha256,review_status)
               values (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,
                       %s::atlas.review_status)
               returning research_target_result_id""",
            (
                research["target_key"], result["research_stage"], result["research_outcome"],
                result.get("bounded_proposition"), result.get("required_abstention"),
                result.get("evidence_locus_summary"), result.get("inference_extent_summary"),
                result.get("temporal_state"), result.get("law_practice_note"),
                result.get("network_territorial_note"), result.get("historical_terms"),
                result.get("category_mapping_status"), result.get("category_mapping_note"),
                result.get("language_access_limitations"), result.get("coverage_confidence"),
                result.get("geometry_resolved_form"), result.get("geometry_claim_role"),
                result.get("geometry_unresolved_note"), source_path, result.get("source_blob_ref"),
                result_digest, result.get("review_status", "draft"),
            ),
        )
        result_id = str(cur.fetchone()[0])

        for index, (source_version_id, evidence) in enumerate(source_rows):
            cur.execute(
                """insert into audit.research_target_source(
                     research_target_result_id,source_version_id,source_relation_key,
                     source_version_ref_raw,evidence_role,independence_group,claim_fitness,
                     direction_raw,normalized_direction,locator,notes)
                   values (%s,%s,%s,%s,%s,%s,%s,%s,%s::atlas.evidence_direction,%s,%s)""",
                (
                    result_id, source_version_id, f"evidence-{index+1}",
                    evidence["version"]["url_or_identifier"], evidence.get("evidence_role"),
                    evidence.get("independence_group"), evidence.get("claim_fitness"),
                    evidence.get("direction", "supports"), evidence.get("direction", "supports"),
                    evidence.get("locator"), evidence.get("notes"),
                ),
            )

        cur.execute(
            """insert into audit.research_target_claim(
                 research_target_result_id,claim_id,claim_role,notes)
               values (%s,%s,'primary',%s)""",
            (result_id, claim_id, "Bounded legal event admitted; broader territorial practice remains separate."),
        )
        review = research["internal_review"]
        cur.execute(
            """insert into audit.research_target_review(
                 research_target_result_id,candidate_id,review_level,review_disposition,
                 admitted,review_reason,failure_guards,dependency_or_scope_note,notes)
               values (%s,%s,'internal',%s,%s,%s,%s,%s,%s)""",
            (
                result_id, case_key, review["review_disposition"], review["admitted"],
                review["review_reason"], review.get("failure_guards", []),
                review.get("dependency_or_scope_note"), review.get("notes"),
            ),
        )

        cur.execute(
            """insert into audit.research_case_ingest(
                 case_key,content_sha256,claim_id,source_path,git_revision)
               values (%s,%s,%s,%s,%s)""",
            (case_key, digest, claim_id, source_path, git_revision),
        )
    return claim_id, True


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("case_file", type=Path)
    parser.add_argument("--dsn", default=os.environ.get("DATABASE_URL"))
    parser.add_argument("--apply", action="store_true")
    parser.add_argument("--require-case-key", action="store_true")
    parser.add_argument("--git-revision", default=os.environ.get("GITHUB_SHA"))
    args = parser.parse_args()
    try:
        spec = load_spec(args.case_file, require_case_key=(args.require_case_key or args.apply))
    except (OSError, json.JSONDecodeError, SpecError) as exc:
        raise SystemExit(f"invalid legal-event case: {exc}") from exc
    print(json.dumps(plan(spec), indent=2, ensure_ascii=False))
    if not args.apply:
        print("DRY RUN: no database changes made")
        return 0
    if not args.dsn:
        parser.error("--dsn or DATABASE_URL is required with --apply")
    import psycopg
    with psycopg.connect(args.dsn, autocommit=False) as conn:
        try:
            with conn.transaction():
                claim_id, inserted = insert_case(
                    conn, spec, source_path=str(args.case_file), git_revision=args.git_revision
                )
        except Exception:
            conn.rollback()
            raise
    print(
        f"inserted unpublished legal-event claim {claim_id}"
        if inserted else
        f"NO-OP: legal-event case already applied unchanged as claim {claim_id}"
    )
    return 0


if __name__ == "__main__":
    sys.exit(main())
