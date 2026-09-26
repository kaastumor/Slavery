#!/usr/bin/env python3
"""Repair the missing v0.6.1 raw/global-evidence phase in an existing live database.

This tool is deliberately NOT a general importer. It assumes the Atlantic/core portion
of v0.6.1 is already present and reconciled, and restores only the phase that is absent
from the live 2026-09-26 Gate-1 audit:

- all 288 non-empty workbook rows as raw.raw_record/v061_workbook_row;
- exact source/version identity for the 36 global evidence rows;
- 36 research_coverage_source evidence links;
- the explicit 22 S/P/D semantic claim targets from v061_global_evidence.py.

It is atomic, deterministic and idempotent. A partial/conflicting repair state is a hard
error. The canonical workbook is never modified.
"""
from __future__ import annotations

import argparse
from dataclasses import dataclass
import hashlib
import json
import os
from pathlib import Path
import sys
import uuid
from typing import Any

from import_v061 import (
    EXPECTED_WORKBOOK_SHA256,
    clean,
    validate_and_normalize,
)
from v061_global_evidence import POSITIVE_PLAN, temporal_fields


REPAIR_VERSION = "v061-live-semantic-repair-v1"
REPAIR_NAMESPACE = uuid.uuid5(
    uuid.NAMESPACE_URL,
    "https://github.com/kaastumor/Slavery/v061-live-semantic-repair-v1",
)
WORKBOOK_VERSION_ID = uuid.UUID("126cec98-d72b-5d01-8bc1-4e2c9a03b219")
WORKBOOK_ASSET_ID = uuid.UUID("312cb4a0-584a-5a55-a311-de5a3c76e669")
WORKBOOK_INGEST_RUN_ID = uuid.UUID("852b307e-3a0d-52d9-b011-38ba97375b00")


def stable_uuid(kind: str, key: str) -> uuid.UUID:
    return uuid.uuid5(REPAIR_NAMESPACE, f"{kind}:{key}")


def canonical_json(value: Any) -> str:
    return json.dumps(
        value,
        ensure_ascii=False,
        sort_keys=True,
        separators=(",", ":"),
        default=str,
    )


def json_sha256(value: Any) -> str:
    return hashlib.sha256(canonical_json(value).encode("utf-8")).hexdigest()


@dataclass(frozen=True)
class RepairPlan:
    workbook_sha256: str
    raw_rows: tuple[dict[str, Any], ...]
    global_rows: tuple[dict[str, Any], ...]
    unique_urls: tuple[str, ...]
    positive_rows: int
    claim_targets: int
    target_kind_counts: dict[str, int]


def build_plan(workbook: Path) -> tuple[RepairPlan, dict[str, Any]]:
    normalized = validate_and_normalize(workbook)
    report = normalized["report"]
    if not report["ok"]:
        raise RuntimeError(
            "Canonical workbook validation failed: "
            + "; ".join(report["errors"])
        )
    if report["sha256"] != EXPECTED_WORKBOOK_SHA256:
        raise RuntimeError("Canonical workbook SHA-256 mismatch")

    raw_rows = tuple(normalized["tables"]["raw_rows"])
    global_rows = tuple(normalized["tables"]["global_evidence"])
    unique_urls = tuple(sorted({str(row["source_url"]) for row in global_rows}))
    positive = [row for row in global_rows if row["coverage"] != "RI"]
    kind_counts: dict[str, int] = {}
    targets = 0
    for row in positive:
        plan = POSITIVE_PLAN[str(row["evidence_key"])]
        for target in plan["targets"]:
            kind = str(target["kind"])
            kind_counts[kind] = kind_counts.get(kind, 0) + 1
            targets += 1

    expected = {
        "raw_rows": 288,
        "global_rows": 36,
        "unique_urls": 29,
        "positive_rows": 18,
        "claim_targets": 22,
    }
    actual = {
        "raw_rows": len(raw_rows),
        "global_rows": len(global_rows),
        "unique_urls": len(unique_urls),
        "positive_rows": len(positive),
        "claim_targets": targets,
    }
    if actual != expected:
        raise RuntimeError(f"Repair plan counts drifted: expected={expected} actual={actual}")
    if kind_counts != {
        "territorial_practice": 18,
        "external_participation": 3,
        "legal_event": 1,
    }:
        raise RuntimeError(f"Repair target-kind counts drifted: {kind_counts}")

    return (
        RepairPlan(
            workbook_sha256=report["sha256"],
            raw_rows=raw_rows,
            global_rows=global_rows,
            unique_urls=unique_urls,
            positive_rows=len(positive),
            claim_targets=targets,
            target_kind_counts=kind_counts,
        ),
        normalized,
    )


def _db_requirements() -> None:
    try:
        import psycopg  # noqa: F401
        from psycopg.types.json import Jsonb  # noqa: F401
    except ImportError as exc:
        raise SystemExit(
            "Database inspection/apply requires psycopg 3; run through the tooling container"
        ) from exc


def _scalar(cur, sql: str, params: tuple[Any, ...] = ()) -> Any:
    cur.execute(sql, params)
    row = cur.fetchone()
    if row is None:
        raise RuntimeError("Expected one SQL result row")
    return row[0]


def _assert_foundation(cur, plan: RepairPlan) -> dict[str, Any]:
    """Validate the already-live Atlantic/core portion without changing it."""
    checks = {
        "voyages": _scalar(cur, "select count(*) from atlas.voyage"),
        "actors": _scalar(cur, "select count(*) from atlas.actor"),
        "voyage_owners": _scalar(cur, "select count(*) from atlas.voyage_owner"),
        "source_map": _scalar(cur, "select count(*) from audit.v061_source_map"),
        "owner_actor_map": _scalar(cur, "select count(*) from audit.v061_owner_actor_map"),
        "voyage_map": _scalar(cur, "select count(*) from audit.v061_voyage_map"),
        "voyage_owner_map": _scalar(cur, "select count(*) from audit.v061_voyage_owner_map"),
        "coverage_assessments": _scalar(
            cur, "select count(*) from audit.research_coverage_assessment"
        ),
        "atlantic_evidence_map": _scalar(
            cur,
            """select count(*) from audit.v061_evidence_claim_map
               where legacy_evidence_id not like 'v0.% Evidence!%'""",
        ),
    }
    expected = {
        "voyages": 8,
        "actors": 11,
        "voyage_owners": 12,
        "source_map": 17,
        "owner_actor_map": 12,
        "voyage_map": 8,
        "voyage_owner_map": 12,
        "coverage_assessments": 99,
        "atlantic_evidence_map": 17,
    }
    if checks != expected:
        raise RuntimeError(f"Atlantic/core live invariants differ: expected={expected} actual={checks}")

    cur.execute(
        """select sv.source_version_id, sa.source_asset_id, sa.checksum_sha256, ir.ingest_run_id
           from atlas.source_version sv
           join atlas.source_asset sa on sa.source_version_id=sv.source_version_id
           join audit.ingest_run ir on ir.source_version_id=sv.source_version_id
           where sv.source_version_id=%s and sa.source_asset_id=%s and ir.ingest_run_id=%s""",
        (WORKBOOK_VERSION_ID, WORKBOOK_ASSET_ID, WORKBOOK_INGEST_RUN_ID),
    )
    lineage = cur.fetchall()
    if len(lineage) != 1:
        raise RuntimeError("Expected exactly one preserved canonical v0.6.1 ingest lineage")
    if lineage[0][2] != plan.workbook_sha256:
        raise RuntimeError(
            f"Live workbook asset checksum differs: {lineage[0][2]} != {plan.workbook_sha256}"
        )

    coverage_counts = dict(
        cur.execute(
            """select normalized_coverage_state_code,count(*)
               from audit.research_coverage_assessment
               group by normalized_coverage_state_code"""
        ).fetchall()
    )
    expected_coverage = {
        "classified": 57,
        "reviewed": 18,
        "disputed": 4,
        "researched_inconclusive": 20,
    }
    if coverage_counts != expected_coverage:
        raise RuntimeError(
            f"Coverage assessment distribution differs: {coverage_counts}"
        )
    return checks


def _expected_claim_ids(plan: RepairPlan) -> list[uuid.UUID]:
    ids: list[uuid.UUID] = []
    for row in plan.global_rows:
        if row["coverage"] == "RI":
            continue
        evidence_key = str(row["evidence_key"])
        for index, target in enumerate(POSITIVE_PLAN[evidence_key]["targets"], start=1):
            ids.append(stable_uuid("claim", f"{evidence_key}:{index}:{target['kind']}"))
    return ids


def _expected_spatial_ids(plan: RepairPlan) -> list[uuid.UUID]:
    return [
        stable_uuid("spatial", str(row["evidence_key"]))
        for row in plan.global_rows
        if row["coverage"] != "RI"
    ]


def inspect_repair_state(cur, plan: RepairPlan) -> dict[str, Any]:
    claim_ids = _expected_claim_ids(plan)
    spatial_ids = _expected_spatial_ids(plan)

    cur.execute(
        """select
             (select count(*) from raw.raw_record where record_type='v061_workbook_row'),
             (select count(distinct source_native_id) from raw.raw_record where record_type='v061_workbook_row'),
             (select count(*) from audit.v061_evidence_claim_map where legacy_evidence_id like 'v0.% Evidence!%'),
             (select count(*) from audit.research_coverage_source where source_role='evidence_sheet_source')"""
    )
    raw_count, raw_distinct, mapping_count, coverage_source_count = cur.fetchone()

    cur.execute("select count(*) from atlas.claim where claim_id = any(%s)", (claim_ids,))
    deterministic_claims = cur.fetchone()[0]
    cur.execute(
        "select count(*) from atlas.spatial_entity where spatial_entity_id = any(%s)",
        (spatial_ids,),
    )
    deterministic_spatial = cur.fetchone()[0]

    cur.execute(
        """select
             count(*) filter (where c.claim_kind_code='territorial_practice') as territorial,
             count(*) filter (where c.claim_kind_code='external_participation') as external,
             count(*) filter (where c.claim_kind_code='legal_event') as legal
           from audit.v061_evidence_claim_map m
           join atlas.claim c on c.claim_id=m.claim_id
           where m.legacy_evidence_id like 'v0.% Evidence!%'"""
    )
    mapped_kinds = cur.fetchone()

    state = {
        "raw_rows": raw_count,
        "raw_distinct_source_ids": raw_distinct,
        "global_mapping_rows": mapping_count,
        "coverage_source_rows": coverage_source_count,
        "deterministic_claims": deterministic_claims,
        "deterministic_spatial_entities": deterministic_spatial,
        "mapped_kind_counts": {
            "territorial_practice": mapped_kinds[0],
            "external_participation": mapped_kinds[1],
            "legal_event": mapped_kinds[2],
        },
    }

    absent = (
        raw_count == 0
        and mapping_count == 0
        and coverage_source_count == 0
        and deterministic_claims == 0
        and deterministic_spatial == 0
    )
    complete = (
        raw_count == 288
        and raw_distinct == 288
        and mapping_count == 22
        and coverage_source_count == 36
        and deterministic_claims == 22
        and deterministic_spatial == 18
        and state["mapped_kind_counts"]
        == {
            "territorial_practice": 18,
            "external_participation": 3,
            "legal_event": 1,
        }
    )
    if absent:
        state["classification"] = "READY_TO_REPAIR"
    elif complete:
        state["classification"] = "COMPLETE"
    else:
        state["classification"] = "PARTIAL_OR_CONFLICTING"
    return state


def _coverage_index(cur) -> dict[tuple[str, str], uuid.UUID]:
    cur.execute(
        """select region_label_raw,period_label_raw,coverage_assessment_id
           from audit.research_coverage_assessment"""
    )
    out: dict[tuple[str, str], uuid.UUID] = {}
    for region, period, cid in cur.fetchall():
        key = (str(region), str(period))
        if key in out:
            raise RuntimeError(f"Duplicate live coverage assessment key: {key}")
        out[key] = cid
    return out


def _source_versions(cur, plan: RepairPlan) -> dict[str, uuid.UUID]:
    """Reuse one exact URL match; create deterministic identity when absent."""
    first_by_url: dict[str, dict[str, Any]] = {}
    for row in plan.global_rows:
        first_by_url.setdefault(str(row["source_url"]), row)

    result: dict[str, uuid.UUID] = {}
    for url in plan.unique_urls:
        cur.execute(
            "select source_version_id from atlas.source_version where url_or_identifier=%s order by source_version_id",
            (url,),
        )
        found = [row[0] for row in cur.fetchall()]
        if len(found) > 1:
            raise RuntimeError(f"Ambiguous exact source URL has {len(found)} versions: {url}")
        if len(found) == 1:
            result[url] = found[0]
            continue

        row = first_by_url[url]
        source_id = stable_uuid("source", url)
        source_version_id = stable_uuid("source-version", url)
        cur.execute("select title from atlas.source where source_id=%s", (source_id,))
        existing_source = cur.fetchone()
        expected_title = f"v0.6.1 global evidence source — {row['area']}"
        if existing_source and existing_source[0] != expected_title:
            raise RuntimeError(f"Deterministic source ID conflict for {url}")
        if not existing_source:
            cur.execute(
                """insert into atlas.source(
                     source_id,title,source_type,source_classification,
                     geographic_scope,temporal_scope,notes)
                   values (%s,%s,%s,%s,%s,%s,%s)""",
                (
                    source_id,
                    expected_title,
                    "Workbook-linked historical source",
                    None,
                    row["region"],
                    row["period"],
                    f"Migration-generated bibliographic label for {row['evidence_key']}; "
                    "exact cited URL preserved. Bibliographic enrichment must not replace "
                    "or merge this source version silently.",
                ),
            )
        cur.execute(
            "select source_id,url_or_identifier from atlas.source_version where source_version_id=%s",
            (source_version_id,),
        )
        existing_version = cur.fetchone()
        if existing_version:
            if existing_version[0] != source_id or existing_version[1] != url:
                raise RuntimeError(f"Deterministic source-version ID conflict for {url}")
        else:
            cur.execute(
                """insert into atlas.source_version(
                     source_version_id,source_id,version_label,url_or_identifier,notes)
                   values (%s,%s,%s,%s,%s)""",
                (
                    source_version_id,
                    source_id,
                    f"exact URL cited by canonical v0.6.1 ({row['sheet_name']})",
                    url,
                    "Exact URL as recorded in the canonical workbook global evidence sheet.",
                ),
            )
        result[url] = source_version_id
    return result


def _insert_raw_rows(cur, plan: RepairPlan) -> None:
    from psycopg.types.json import Jsonb

    for entry in plan.raw_rows:
        source_native_id = f"{entry['sheet_name']}!{entry['row_number']}"
        record_id = stable_uuid("raw-workbook-row", source_native_id)
        payload_hash = json_sha256(entry)
        cur.execute(
            """insert into raw.raw_record(
                 raw_record_id,ingest_run_id,record_type,source_native_id,
                 raw_payload,checksum_sha256)
               values (%s,%s,'v061_workbook_row',%s,%s,%s)""",
            (
                record_id,
                WORKBOOK_INGEST_RUN_ID,
                source_native_id,
                Jsonb(entry),
                payload_hash,
            ),
        )


def _insert_global_evidence(cur, plan: RepairPlan, source_versions: dict[str, uuid.UUID]) -> None:
    coverage = _coverage_index(cur)

    for row in plan.global_rows:
        evidence_key = str(row["evidence_key"])
        source_version_id = source_versions[str(row["source_url"])]
        coverage_key = (str(row["region"]), str(row["period"]))
        coverage_id = coverage.get(coverage_key)
        if coverage_id is None:
            raise RuntimeError(
                f"No live coverage assessment for {evidence_key}: {coverage_key}"
            )
        cur.execute(
            """insert into audit.research_coverage_source(
                 coverage_assessment_id,source_version_id,source_role,locator,notes)
               values (%s,%s,'evidence_sheet_source',%s,%s)""",
            (
                coverage_id,
                source_version_id,
                evidence_key,
                f"Reviewed source cited by {evidence_key}; coverage={row['coverage']}.",
            ),
        )
        if row["coverage"] == "RI":
            continue

        evidence_plan = POSITIVE_PLAN[evidence_key]
        spatial_id = stable_uuid("spatial", evidence_key)
        cur.execute(
            """insert into atlas.spatial_entity(
                 spatial_entity_id,entity_type_code,canonical_name,display_name,
                 from_year,to_year,notes,review_status)
               values (%s,%s,%s,%s,%s,%s,%s,'reviewed')""",
            (
                spatial_id,
                evidence_plan["spatial_type"],
                row["area"],
                row["area"],
                row["from_year"],
                row["to_year"],
                f"Migrated historical/analytical target from {evidence_key}; "
                "geometry unresolved pending the documented resolver hierarchy.",
            ),
        )
        from_year, to_year, date_text, precision = temporal_fields(row, evidence_plan)

        for index, target in enumerate(evidence_plan["targets"], start=1):
            kind = target["kind"]
            claim_id = stable_uuid("claim", f"{evidence_key}:{index}:{kind}")
            cur.execute(
                """insert into atlas.claim(
                     claim_id,claim_kind_code,from_year,to_year,date_text_original,
                     temporal_precision,spatial_precision,summary,confidence,
                     review_status,publication_status,notes)
                   values (%s,%s,%s,%s,%s,%s,%s,%s,%s,'reviewed','unpublished',%s)""",
                (
                    claim_id,
                    kind,
                    from_year,
                    to_year,
                    date_text,
                    precision,
                    "workbook area/region label",
                    str(row["decision"]),
                    row["coverage"],
                    (
                        f"v061_global_evidence={evidence_key}; "
                        + (
                            f"practice_issue={row['practice_issue']}."
                            if kind != "legal_event"
                            else "legal context split from practice claim."
                        )
                    ),
                ),
            )

            if kind == "territorial_practice":
                cur.execute(
                    """insert into atlas.territorial_practice_claim(
                         claim_id,spatial_entity_id,practice_type_code,practice_level,
                         coverage_state_code,classification_status,notes)
                       values (%s,%s,%s,NULL,%s,%s,%s)""",
                    (
                        claim_id,
                        spatial_id,
                        target["practice_type"],
                        target["coverage_state"],
                        target["classification_status"],
                        "P-level intentionally unassigned during workbook semantic migration.",
                    ),
                )
                mapping_role = f"territorial_practice:{target['practice_type']}"
            elif kind == "external_participation":
                cur.execute(
                    """insert into atlas.external_participation_claim(
                         claim_id,spatial_entity_id,participation_type_code,role_text,notes)
                       values (%s,%s,%s,%s,%s)""",
                    (
                        claim_id,
                        spatial_id,
                        target["participation_type"],
                        target.get("role_text"),
                        "External/network participation is analytically separate from territorial practice.",
                    ),
                )
                mapping_role = f"external_participation:{target['participation_type']}"
            elif kind == "legal_event":
                cur.execute(
                    """insert into atlas.legal_event(
                         claim_id,jurisdiction_spatial_entity_id,event_type,
                         legal_status_after,scope,notes)
                       values (%s,%s,%s,%s,%s,%s)""",
                    (
                        claim_id,
                        spatial_id,
                        target["event_type"],
                        target.get("legal_status_after"),
                        target.get("scope"),
                        "Workbook row describes a legal/suppression process, not a single clean abolition date.",
                    ),
                )
                mapping_role = f"legal_event:{target['event_type']}"
            else:
                raise RuntimeError(f"Unknown target kind {kind!r}")

            claim_source_id = stable_uuid("claim-source", f"{evidence_key}:{index}:{kind}")
            cur.execute(
                """insert into atlas.claim_source(
                     claim_source_id,claim_id,source_version_id,evidence_role,
                     directness,direction,locator,notes)
                   values (%s,%s,%s,%s,%s,'supports',%s,%s)""",
                (
                    claim_source_id,
                    claim_id,
                    source_version_id,
                    "global workbook evidence row",
                    "exact source URL cited by workbook",
                    evidence_key,
                    f"{evidence_key}; legacy_coverage={row['coverage']}; area={row['area']}.",
                ),
            )
            cur.execute(
                """insert into audit.v061_evidence_claim_map(
                     legacy_evidence_id,claim_id,mapping_role,notes)
                   values (%s,%s,%s,%s)""",
                (
                    evidence_key,
                    claim_id,
                    mapping_role,
                    "Explicit semantic migration of canonical global evidence row.",
                ),
            )


def _assert_postconditions(cur, plan: RepairPlan) -> dict[str, Any]:
    state = inspect_repair_state(cur, plan)
    if state["classification"] != "COMPLETE":
        raise RuntimeError(f"Repair postconditions failed: {state}")

    checks = {
        "global_territorial_claims": _scalar(
            cur,
            """select count(*) from audit.v061_evidence_claim_map m
               join atlas.territorial_practice_claim t on t.claim_id=m.claim_id
               where m.legacy_evidence_id like 'v0.% Evidence!%'""",
        ),
        "global_nonnull_p_levels": _scalar(
            cur,
            """select count(*) from audit.v061_evidence_claim_map m
               join atlas.territorial_practice_claim t on t.claim_id=m.claim_id
               where m.legacy_evidence_id like 'v0.% Evidence!%'
                 and t.practice_level is not null""",
        ),
        "global_external_claims": _scalar(
            cur,
            """select count(*) from audit.v061_evidence_claim_map m
               join atlas.external_participation_claim e on e.claim_id=m.claim_id
               where m.legacy_evidence_id like 'v0.% Evidence!%'""",
        ),
        "global_legal_events": _scalar(
            cur,
            """select count(*) from audit.v061_evidence_claim_map m
               join atlas.legal_event l on l.claim_id=m.claim_id
               where m.legacy_evidence_id like 'v0.% Evidence!%'""",
        ),
        "global_source_versions": _scalar(
            cur,
            """select count(distinct rcs.source_version_id)
               from audit.research_coverage_source rcs
               where rcs.source_role='evidence_sheet_source'""",
        ),
        "anshan_external_only": _scalar(
            cur,
            """select count(*) from audit.v061_evidence_claim_map
               where legacy_evidence_id='v0.4.9 Evidence!5'
                 and mapping_role='external_participation:slave_trade_network'""",
        ),
        "shang_split": _scalar(
            cur,
            """select count(*) from audit.v061_evidence_claim_map
               where legacy_evidence_id='v0.4.9 Evidence!10'
                 and mapping_role in (
                   'territorial_practice:captive_taking_incorporation',
                   'territorial_practice:slavery_enslavement'
                 )""",
        ),
    }
    expected = {
        "global_territorial_claims": 18,
        "global_nonnull_p_levels": 0,
        "global_external_claims": 3,
        "global_legal_events": 1,
        "global_source_versions": 29,
        "anshan_external_only": 1,
        "shang_split": 2,
    }
    if checks != expected:
        raise RuntimeError(f"Repair semantic checks failed: expected={expected} actual={checks}")
    return {"repair_state": state, "semantic_checks": checks}


def run(workbook: Path, dsn: str, apply: bool) -> dict[str, Any]:
    _db_requirements()
    import psycopg

    plan, _normalized = build_plan(workbook)
    report: dict[str, Any] = {
        "repair_version": REPAIR_VERSION,
        "workbook": workbook.name,
        "workbook_sha256": plan.workbook_sha256,
        "plan": {
            "raw_rows": len(plan.raw_rows),
            "global_rows": len(plan.global_rows),
            "unique_urls": len(plan.unique_urls),
            "positive_rows": plan.positive_rows,
            "claim_targets": plan.claim_targets,
            "target_kind_counts": plan.target_kind_counts,
        },
        "apply_requested": apply,
    }

    with psycopg.connect(dsn, autocommit=False) as conn:
        try:
            with conn.cursor() as cur:
                report["foundation"] = _assert_foundation(cur, plan)
                before = inspect_repair_state(cur, plan)
                report["before"] = before

                if before["classification"] == "PARTIAL_OR_CONFLICTING":
                    raise RuntimeError(
                        "Refusing repair because live state is partial/conflicting: "
                        + json.dumps(before, sort_keys=True)
                    )
                if before["classification"] == "COMPLETE":
                    report["disposition"] = "ALREADY_COMPLETE"
                    report["postconditions"] = _assert_postconditions(cur, plan)
                    conn.rollback()
                    return report

                # READY_TO_REPAIR
                if not apply:
                    report["disposition"] = "DRY_RUN_READY"
                    conn.rollback()
                    return report

                source_versions = _source_versions(cur, plan)
                _insert_raw_rows(cur, plan)
                _insert_global_evidence(cur, plan, source_versions)
                report["postconditions"] = _assert_postconditions(cur, plan)
                report["source_versions"] = {
                    "unique_urls": len(source_versions),
                    "reused_or_created_exact_versions": len(source_versions),
                }
                report["disposition"] = "REPAIR_APPLIED"
            conn.commit()
        except Exception:
            conn.rollback()
            raise

    return report


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--workbook", required=True, type=Path)
    parser.add_argument("--dsn", default=os.environ.get("DATABASE_URL"))
    parser.add_argument("--apply", action="store_true")
    parser.add_argument("--report", type=Path)
    args = parser.parse_args(argv)
    if not args.dsn:
        parser.error("--dsn or DATABASE_URL is required")

    report = run(args.workbook, args.dsn, args.apply)
    output = json.dumps(report, ensure_ascii=False, indent=2, default=str)
    print(output)
    if args.report:
        args.report.parent.mkdir(parents=True, exist_ok=True)
        args.report.write_text(output + "\n", encoding="utf-8")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
