#!/usr/bin/env python3
"""Validate and migrate the canonical v0.6.1 workbook into the foundation schema.

Dry-run mode has no third-party dependencies. Applying to PostgreSQL requires
psycopg 3 (`pip install -r requirements.txt`). The workbook is never modified.
"""
from __future__ import annotations

import argparse
from collections import Counter
from datetime import datetime, timezone
import hashlib
import json
import os
from pathlib import Path
import re
import sys
from typing import Any

from xlsx_minimal import XlsxReader, table_dicts
from v061_global_evidence import (
    POSITIVE_PLAN,
    extract_global_evidence,
    temporal_fields,
    validate_global_evidence,
)

EXPECTED_WORKBOOK_SHA256 = "0a38e4eb6f63c3bb4ce9543be379605d24dd9ff1c1cea1e0a49c0c3db7ba17d4"

EXPECTED = {
    "voyages": 8,
    "owner_registry_rows": 12,
    "real_actors": 11,
    "voyage_owner_rows": 12,
    "actor_linked_owner_rows": 11,
    "missing_owner_rows": 1,
    "legacy_sources": 17,
    "legacy_owner_evidence_ids": 11,
    "coverage_cells": 99,
    "workbook_sheets": 18,
    "workbook_nonempty_rows": 288,
}

PERIODS = {
    "3000–2001 BCE": (-2999, -2000),
    "2000–1001 BCE": (-1999, -1000),
    "1000–1 BCE": (-999, 0),
    "1–499 CE": (1, 499),
    "500–999": (500, 999),
    "1000–1499": (1000, 1499),
    "1500–1799": (1500, 1799),
    "1800–1899": (1800, 1899),
    "1900–present": (1900, None),
}

COVERAGE_NORMALIZATION = {
    "S": ("classified", 3),
    "P": ("reviewed", 2),
    "D": ("disputed", 1),
    "RI": ("researched_inconclusive", 1),
    "—": ("not_researched", 0),
}

ACTOR_TYPE = {
    "Person": "person",
    "Firm": "partnership",
    "Company": "company",
}


def sha256_file(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as f:
        for chunk in iter(lambda: f.read(1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest()


def clean(value: Any) -> Any:
    if isinstance(value, str):
        value = value.strip()
        return value if value else None
    return value


def as_int(value: Any) -> int | None:
    value = clean(value)
    if value is None:
        return None
    if isinstance(value, int):
        return value
    if isinstance(value, float) and value.is_integer():
        return int(value)
    return int(str(value))


def parse_claim_period(text: Any) -> tuple[int | None, int | None, str | None]:
    text = clean(text)
    if text is None:
        return None, None, None
    s = str(text).strip()
    m = re.fullmatch(r"(\d{3,4})", s)
    if m:
        y = int(m.group(1))
        return y, y, "exact_year"
    m = re.fullmatch(r"(\d{3,4})[–-](\d{3,4})", s)
    if m:
        return int(m.group(1)), int(m.group(2)), "year_range"
    m = re.fullmatch(r"c\.\s*(\d{3,4})[–-](\d{3,4})", s, flags=re.I)
    if m:
        return int(m.group(1)), int(m.group(2)), "approximate_range"
    m = re.fullmatch(r"(\d{1,2})(?:st|nd|rd|th) century", s, flags=re.I)
    if m:
        c = int(m.group(1))
        return (c - 1) * 100, c * 100 - 1, "century"
    return None, None, "textual_unparsed"


def workbook_tables(path: Path) -> dict[str, Any]:
    with XlsxReader(path) as xlsx:
        sheet_rows = {name: xlsx.rows(name) for name in xlsx.sheet_names}

        raw_rows: list[dict[str, Any]] = []
        raw_sheet_row_counts: dict[str, int] = {}
        for sheet_name, rows in sheet_rows.items():
            count = 0
            for row_number, row in enumerate(rows, start=1):
                if not any(clean(v) is not None for v in row):
                    continue
                raw_rows.append({
                    "sheet_name": sheet_name,
                    "row_number": row_number,
                    "values": row,
                })
                count += 1
            raw_sheet_row_counts[sheet_name] = count

        voyages = table_dicts(sheet_rows["Atlantic Seed - Voyages"], "Dataset")
        owners = table_dicts(sheet_rows["Atlantic Seed - Owners"], "Owner ID")
        voyage_owners = table_dicts(sheet_rows["Atlantic Voyage Owners"], "Voyage ID")
        evidence = table_dicts(sheet_rows["Atlantic Owner Evidence"], "Evidence ID")
        sources = table_dicts(sheet_rows["Atlantic Sources"], "Source ID")
        coverage_rows = table_dicts(sheet_rows["Coverage Matrix"], "Region")
        global_evidence = extract_global_evidence(sheet_rows)
    return {
        "voyages": voyages,
        "owners": owners,
        "voyage_owners": voyage_owners,
        "evidence": evidence,
        "sources": sources,
        "coverage_rows": coverage_rows,
        "global_evidence": global_evidence,
        "workbook_sheets": list(sheet_rows),
        "raw_rows": raw_rows,
        "raw_sheet_row_counts": raw_sheet_row_counts,
    }


def flatten_coverage(rows: list[dict[str, Any]]) -> list[dict[str, Any]]:
    out: list[dict[str, Any]] = []
    for row in rows:
        region = clean(row.get("Region"))
        if not region:
            continue
        for period_label, (from_year, to_year) in PERIODS.items():
            code = clean(row.get(period_label))
            if code is None:
                code = "—"
            if code not in COVERAGE_NORMALIZATION:
                raise ValueError(f"Unknown coverage code {code!r} for {region} / {period_label}")
            normalized, points = COVERAGE_NORMALIZATION[code]
            out.append({
                "region_label_raw": region,
                "period_label_raw": period_label,
                "from_year": from_year,
                "to_year": to_year,
                "legacy_coverage_code": code,
                "normalized_coverage_state_code": normalized,
                "coverage_points": points,
            })
    return out


def source_url_index(sources: list[dict[str, Any]]) -> dict[str, dict[str, Any]]:
    out = {}
    for row in sources:
        url = clean(row.get("URL"))
        if url:
            out[url] = row
    return out


def evidence_plan() -> dict[str, list[dict[str, Any]]]:
    """Explicit semantic mapping for the 11 v0.6.1 OWNER_EVIDENCE rows."""
    return {
        "E-001": [{"kind": "actor_attribute", "attribute_type": "business_base", "value": "Rotterdam"}],
        "E-002": [{"kind": "actor_attribute", "attribute_type": "commercial_role", "value": "Private slave-trading firm"}],
        "E-003": [
            {"kind": "actor_attribute", "attribute_type": "commercial_role", "value": "Bahia armador"},
            {"kind": "actor_attribute", "attribute_type": "business_base", "value": "Bahia"},
        ],
        "E-004": [{"kind": "voyage_owner", "voyage": "2364", "owner": "OWN-0008"}],
        "E-005": [{"kind": "voyage_owner", "voyage": "36144", "owner": "OWN-0009"}],
        "E-006": [
            {"kind": "actor_attribute", "attribute_type": "corporate_jurisdiction", "value": "Denmark–Norway"},
            {"kind": "voyage_owner", "voyage": "35181", "owner": "OWN-0010"},
        ],
        "E-007": [{"kind": "voyage_owner", "voyage": "35181", "owner": "OWN-0010"}],
        "E-008": [{"kind": "voyage_owner", "voyage": "557", "owner": "OWN-0011"}],
        "E-009": [{"kind": "actor_attribute", "attribute_type": "nationality_political_identity", "value": "French"}],
        "E-010": [{"kind": "voyage_owner", "voyage": "32359", "owner": "OWN-0012"}],
        "E-011": [
            {"kind": "voyage_owner", "voyage": "90080", "owner": f"OWN-000{i}"}
            for i in range(1, 6)
        ],
    }


def validate_and_normalize(path: Path) -> dict[str, Any]:
    t = workbook_tables(path)
    coverage = flatten_coverage(t["coverage_rows"])
    global_validation = validate_global_evidence(t["global_evidence"])
    url_index = source_url_index(t["sources"])

    owner_rows = t["owners"]
    real_owners = [r for r in owner_rows if clean(r.get("Owner ID")) != "OWN-0011"]
    rel_rows = t["voyage_owners"]
    actor_linked = [r for r in rel_rows if clean(r.get("Relationship status")) == "Documented"]
    missing = [r for r in rel_rows if clean(r.get("Relationship status")) == "Missing owner placeholder"]

    actual = {
        "voyages": len(t["voyages"]),
        "owner_registry_rows": len(owner_rows),
        "real_actors": len(real_owners),
        "voyage_owner_rows": len(rel_rows),
        "actor_linked_owner_rows": len(actor_linked),
        "missing_owner_rows": len(missing),
        "legacy_sources": len(t["sources"]),
        "legacy_owner_evidence_ids": len(t["evidence"]),
        "coverage_cells": len(coverage),
        "workbook_sheets": len(t["workbook_sheets"]),
        "workbook_nonempty_rows": len(t["raw_rows"]),
    }
    errors = [f"{k}: expected {EXPECTED[k]}, found {v}" for k, v in actual.items() if EXPECTED[k] != v]
    errors.extend(global_validation["errors"])

    voyages_by_id = {str(as_int(r["Voyage ID"])): r for r in t["voyages"]}
    owners_by_id = {str(clean(r["Owner ID"])): r for r in owner_rows}
    evidence_by_id = {str(clean(r["Evidence ID"])): r for r in t["evidence"]}

    # Special-case invariants from the canonical workbook.
    west = voyages_by_id.get("36144")
    if not west or clean(west.get("Flag documented")) != "U.S.A.":
        errors.append("Westmoreland must preserve raw documented flag 'U.S.A.'")
    orestes = voyages_by_id.get("557")
    if not orestes or clean(orestes.get("Flag documented")) is not None or clean(orestes.get("Flag imputed")) != "Spain / Uruguay":
        errors.append("Orestes documented/imputed flag control failed")
    fred = voyages_by_id.get("35181")
    if not fred or clean(fred.get("Disembarked")) is not None or clean(fred.get("Disembarked status")) != "Needs source reconciliation":
        errors.append("Fredensborg unresolved disembarkation control failed")
    aurore_owner = owners_by_id.get("OWN-0012")
    if not aurore_owner or clean(aurore_owner.get("Person nationality")) != "French":
        errors.append("Aurore owner nationality positive control missing")

    plan = evidence_plan()
    if set(plan) != set(evidence_by_id):
        errors.append(f"Evidence mapping IDs differ: plan={sorted(plan)} workbook={sorted(evidence_by_id)}")

    # All directly cited voyage/relationship URLs must be resolvable. A registry gap is
    # preserved as an explicit migration-generated source rather than silently substituted.
    referenced_urls = set()
    for r in t["voyages"]:
        if clean(r.get("Source URL")):
            referenced_urls.add(clean(r.get("Source URL")))
    for r in t["voyage_owners"]:
        if clean(r.get("Source URL")):
            referenced_urls.add(clean(r.get("Source URL")))
    registry_gaps = sorted(u for u in referenced_urls if u not in url_index)

    code_counts = Counter(c["legacy_coverage_code"] for c in coverage)
    expected_coverage = {"S": 57, "P": 18, "D": 4, "RI": 20, "—": 0}
    # Zero-count — cells do not appear explicitly in Counter.
    for code, n in expected_coverage.items():
        if code_counts.get(code, 0) != n:
            errors.append(f"Coverage {code}: expected {n}, found {code_counts.get(code,0)}")

    mapping_rows = sum(len(v) for v in plan.values())
    workbook_sha256 = sha256_file(path)
    if workbook_sha256 != EXPECTED_WORKBOOK_SHA256:
        errors.append(
            f"Canonical workbook checksum mismatch: expected {EXPECTED_WORKBOOK_SHA256}, found {workbook_sha256}. "
            "Do not overwrite/re-save v0.6.1; create a new release instead."
        )
    report = {
        "workbook": path.name,
        "sha256": workbook_sha256,
        "validated_at_utc": datetime.now(timezone.utc).isoformat(),
        "counts": actual,
        "coverage_code_counts": dict(code_counts),
        "evidence_mapping": plan,
        "evidence_mapping_rows": mapping_rows,
        "source_registry_gaps": registry_gaps,
        "raw_sheet_row_counts": t["raw_sheet_row_counts"],
        "global_evidence": global_validation,
        "warnings": (
            (["Fredensborg's exact SlaveVoyages voyage URL is referenced by workbook rows but absent from the 17-row Atlantic Sources registry; migration will create an explicit unregistered-source record and QC warning."]
             if "https://www.slavevoyages.org/voyage/35181/variables" in registry_gaps else [])
            + ["Global evidence rows are explicitly semantically mapped; conceptual bibliographic metadata for workbook-only URLs remains migration-generated until enriched from the cited publications."]
        ),
        "errors": errors,
        "ok": not errors,
    }
    return {"tables": t, "coverage": coverage, "report": report}


def _db_requirements():
    try:
        import psycopg  # noqa: F401
        from psycopg.types.json import Jsonb  # noqa: F401
    except ImportError as exc:
        raise SystemExit("Database apply requires psycopg 3. Install with: pip install -r requirements.txt") from exc


def apply_to_database(path: Path, dsn: str, normalized: dict[str, Any]) -> dict[str, Any]:
    _db_requirements()
    import psycopg
    from psycopg.types.json import Jsonb

    t = normalized["tables"]
    coverage = normalized["coverage"]
    global_evidence = t["global_evidence"]
    report = normalized["report"]
    if not report["ok"]:
        raise SystemExit("Refusing database apply because dry-run validation failed")

    with psycopg.connect(dsn) as conn:
        with conn.cursor() as cur:
            cur.execute("SELECT to_regclass('audit.v061_source_map'), to_regclass('audit.research_coverage_source'), to_regclass('atlas.external_participation_claim')")
            migration_regs = cur.fetchone()
            if any(v is None for v in migration_regs):
                raise SystemExit("Foundation migrations 0001-0011 have not been applied")
            cur.execute("SELECT count(*) FROM audit.v061_voyage_map")
            if cur.fetchone()[0] != 0:
                raise SystemExit("v0.6.1 migration crosswalks already contain data; use a fresh/reset foundation database")

            # Project workbook provenance / ingest lineage.
            cur.execute(
                """INSERT INTO atlas.source(title, source_type, source_classification, notes)
                   VALUES (%s,%s,%s,%s) RETURNING source_id""",
                ("Historical Slavery Atlas v0.6.1 canonical workbook", "Project dataset", "dataset",
                 "Canonical workbook remains authoritative until database reconciliation passes."),
            )
            workbook_source_id = cur.fetchone()[0]
            cur.execute(
                """INSERT INTO atlas.source_version(source_id, version_label, notes)
                   VALUES (%s,%s,%s) RETURNING source_version_id""",
                (workbook_source_id, "0.6.1", path.name),
            )
            workbook_version_id = cur.fetchone()[0]
            cur.execute(
                """INSERT INTO atlas.source_asset(source_version_id, filename_or_object_key, media_type,
                                                   checksum_sha256, storage_location, redistribution_status, notes)
                   VALUES (%s,%s,%s,%s,%s,%s,%s) RETURNING source_asset_id""",
                (workbook_version_id, path.name,
                 "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
                 report["sha256"], f"local-import:{path.name}", "project-internal",
                 "Imported read-only; source workbook is not modified by this tool."),
            )
            workbook_asset_id = cur.fetchone()[0]
            cur.execute(
                """INSERT INTO audit.ingest_run(source_version_id, source_asset_id, code_version, status, notes)
                   VALUES (%s,%s,%s,'started',%s) RETURNING ingest_run_id""",
                (workbook_version_id, workbook_asset_id, "db-foundation-v0.3/import-v061", "Canonical v0.6.1 foundation migration"),
            )
            ingest_run_id = cur.fetchone()[0]

            # Historical evidence source registry.
            source_by_legacy: dict[str, tuple[Any, Any]] = {}
            source_version_by_url: dict[str, Any] = {}
            for row in t["sources"]:
                legacy = str(clean(row["Source ID"]))
                title = str(clean(row["Source name"]))
                cur.execute(
                    """INSERT INTO atlas.source(title, source_type, source_classification,
                                                independence_notes, notes)
                       VALUES (%s,%s,%s,%s,%s) RETURNING source_id""",
                    (title, clean(row.get("Source type")), clean(row.get("Primary / secondary")),
                     clean(row.get("Independence role")),
                     "Supports: " + str(clean(row.get("Supports")) or "") + "\nVerification: " + str(clean(row.get("Verification note")) or "")),
                )
                source_id = cur.fetchone()[0]
                url = clean(row.get("URL"))
                version_label = f"{legacy} reference captured in canonical v0.6.1"
                cur.execute(
                    """INSERT INTO atlas.source_version(source_id, version_label, url_or_identifier, notes)
                       VALUES (%s,%s,%s,%s) RETURNING source_version_id""",
                    (source_id, version_label, url, "Exact source reference as recorded in Atlantic Sources sheet."),
                )
                source_version_id = cur.fetchone()[0]
                source_by_legacy[legacy] = (source_id, source_version_id)
                if url:
                    source_version_by_url[str(url)] = source_version_id
                cur.execute(
                    "INSERT INTO audit.v061_source_map(legacy_source_id, source_id, source_version_id) VALUES (%s,%s,%s)",
                    (legacy, source_id, source_version_id),
                )

            # Explicitly preserve source URLs referenced by immediate-migration rows but absent from the registry.
            for gap_url in report["source_registry_gaps"]:
                title = "Unregistered v0.6.1 source reference"
                if "35181" in gap_url:
                    title = "SlaveVoyages voyage 35181 — Fredensborg"
                cur.execute(
                    """INSERT INTO atlas.source(title, source_type, source_classification, notes)
                       VALUES (%s,'Voyage record','Structured dataset',%s) RETURNING source_id""",
                    (title, "Migration-generated source identity because the exact URL occurs in canonical rows but not in the 17-row Atlantic Sources registry."),
                )
                sid = cur.fetchone()[0]
                cur.execute(
                    """INSERT INTO atlas.source_version(source_id, version_label, url_or_identifier, notes)
                       VALUES (%s,%s,%s,%s) RETURNING source_version_id""",
                    (sid, "exact URL referenced by v0.6.1", gap_url, "Not silently substituted with related scholarship/archive sources."),
                )
                svid = cur.fetchone()[0]
                source_version_by_url[gap_url] = svid
                cur.execute(
                    """INSERT INTO audit.qc_issue(ingest_run_id, severity, issue_code, object_type,
                                                  object_identifier, description)
                       VALUES (%s,'warning','V061_SOURCE_REGISTRY_GAP','source_url',%s,%s)""",
                    (ingest_run_id, gap_url,
                     "Canonical workbook references this source URL outside the Atlantic Sources registry; migration created an explicit source/version so provenance remains exact."),
                )

            # Exact source versions cited by the four global evidence sheets.
            # The workbook contains URLs but not full bibliographic metadata, so titles are
            # deliberately migration-generated and may be enriched later without changing
            # the exact URL/version lineage.
            first_global_row_by_url: dict[str, dict[str, Any]] = {}
            for row in global_evidence:
                first_global_row_by_url.setdefault(str(row["source_url"]), row)
            for url, row in first_global_row_by_url.items():
                if url in source_version_by_url:
                    continue
                cur.execute(
                    """INSERT INTO atlas.source(title, source_type, source_classification, geographic_scope,
                                                temporal_scope, notes)
                       VALUES (%s,%s,%s,%s,%s,%s) RETURNING source_id""",
                    (
                        f"v0.6.1 global evidence source — {row['area']}",
                        "Workbook-linked historical source",
                        None,
                        row["region"],
                        row["period"],
                        f"Migration-generated bibliographic label for {row['evidence_key']}; exact cited URL preserved. "
                        "Bibliographic enrichment must not replace or merge the source version silently.",
                    ),
                )
                sid = cur.fetchone()[0]
                cur.execute(
                    """INSERT INTO atlas.source_version(source_id, version_label, url_or_identifier, notes)
                       VALUES (%s,%s,%s,%s) RETURNING source_version_id""",
                    (
                        sid,
                        f"exact URL cited by canonical v0.6.1 ({row['sheet_name']})",
                        url,
                        "Exact URL as recorded in the canonical workbook global evidence sheet.",
                    ),
                )
                source_version_by_url[url] = cur.fetchone()[0]

            # Raw source rows should remain queryable independent of normalization.
            def raw(record_type: str, source_native_id: str | None, payload: dict[str, Any]):
                cur.execute(
                    """INSERT INTO raw.raw_record(ingest_run_id, record_type, source_native_id, raw_payload)
                       VALUES (%s,%s,%s,%s)""",
                    (ingest_run_id, record_type, source_native_id, Jsonb(payload)),
                )

            # Preserve every non-empty row from every workbook tab before normalization.
            # The source asset/checksum remains the byte-level authority; these records make
            # workbook content queryable without pretending every sheet has been semantically normalized.
            for entry in t["raw_rows"]:
                raw(
                    "v061_workbook_row",
                    f"{entry['sheet_name']}!{entry['row_number']}",
                    entry,
                )

            for row in t["sources"]:
                raw("v061_source", str(clean(row.get("Source ID"))), row)

            # Research coverage is project-transparency metadata, never territorial P-level.
            # Keep IDs so evidence-sheet sources can be linked to the exact assessment they informed.
            coverage_assessment_by_key: dict[tuple[str, str], Any] = {}
            for item in coverage:
                raw("v061_coverage_cell", f"{item['region_label_raw']}|{item['period_label_raw']}", item)
                cur.execute(
                    """INSERT INTO audit.research_coverage_assessment(
                         region_label_raw,period_label_raw,from_year,to_year,legacy_coverage_code,
                         normalized_coverage_state_code,coverage_points,release_version,review_status,publication_status,notes)
                       VALUES (%s,%s,%s,%s,%s,%s,%s,'0.6.1','reviewed','unpublished',%s)
                       RETURNING coverage_assessment_id""",
                    (
                        item["region_label_raw"], item["period_label_raw"], item["from_year"], item["to_year"],
                        item["legacy_coverage_code"], item["normalized_coverage_state_code"], item["coverage_points"],
                        "Project research-coverage metadata; not historical prevalence or territorial P-level.",
                    ),
                )
                coverage_assessment_by_key[(item["region_label_raw"], item["period_label_raw"])] = cur.fetchone()[0]

            # Actors: OWN-0011 is documented missingness, never an identity.
            actor_by_legacy: dict[str, Any] = {}
            for row in t["owners"]:
                legacy = str(clean(row["Owner ID"]))
                raw("v061_owner_registry", legacy, row)
                if legacy == "OWN-0011":
                    cur.execute(
                        """INSERT INTO audit.v061_owner_actor_map(legacy_owner_id, actor_id, migration_action, notes)
                           VALUES (%s,NULL,'missing_placeholder_no_actor',%s)""",
                        (legacy, "Orestes owner-not-recorded placeholder preserved as missingness."),
                    )
                    continue
                legacy_type = str(clean(row.get("Entity type")))
                actor_type = ACTOR_TYPE.get(legacy_type, "other")
                notes = "Evidence status: " + str(clean(row.get("Evidence status")) or "")
                if clean(row.get("Notes")):
                    notes += "\n" + str(clean(row.get("Notes")))
                cur.execute(
                    """INSERT INTO atlas.actor(actor_type_code, canonical_name, display_name, notes, review_status)
                       VALUES (%s,%s,%s,%s,'reviewed') RETURNING actor_id""",
                    (actor_type, clean(row.get("Normalized owner / entity")), clean(row.get("Normalized owner / entity")), notes),
                )
                actor_id = cur.fetchone()[0]
                actor_by_legacy[legacy] = actor_id
                cur.execute(
                    """INSERT INTO audit.v061_owner_actor_map(legacy_owner_id, actor_id, migration_action)
                       VALUES (%s,%s,'mapped_actor')""",
                    (legacy, actor_id),
                )
                cur.execute(
                    """INSERT INTO atlas.actor_name(actor_id, name_text, name_type, is_preferred)
                       VALUES (%s,%s,'canonical',true)""",
                    (actor_id, clean(row.get("Normalized owner / entity"))),
                )
                raw_name = clean(row.get("Raw owner text"))
                if raw_name:
                    raw_url = clean(row.get("Voyage-source URL"))
                    cur.execute(
                        """INSERT INTO atlas.actor_name(actor_id, name_text, name_type, source_version_id, is_preferred)
                           VALUES (%s,%s,'source_raw',%s,false)""",
                        (actor_id, raw_name, source_version_by_url.get(str(raw_url)) if raw_url else None),
                    )

            # Voyages.
            voyage_by_legacy: dict[str, Any] = {}
            voyage_year_by_legacy: dict[str, int | None] = {}
            for row in t["voyages"]:
                legacy = str(as_int(row["Voyage ID"]))
                raw("v061_voyage", legacy, row)
                url = str(clean(row.get("Source URL")))
                svid = source_version_by_url.get(url)
                if svid is None:
                    raise RuntimeError(f"No source version for voyage URL: {url}")
                vals = (
                    clean(row.get("Dataset")), legacy, svid, clean(row.get("Vessel")), as_int(row.get("Year arrived")), clean(row.get("Year status")),
                    clean(row.get("Flag documented")), clean(row.get("Flag imputed")), clean(row.get("Seed carrier bucket")), clean(row.get("Carrier bucket basis")),
                    clean(row.get("Flag / carrier note")), clean(row.get("Constructed at")), clean(row.get("Registered at")), as_int(row.get("Registration year")),
                    clean(row.get("Voyage origin")), clean(row.get("Origin status")), clean(row.get("Principal embarkation")), clean(row.get("Embarkation status")),
                    clean(row.get("Principal landing")), clean(row.get("Landing status")), as_int(row.get("Embarked")), clean(row.get("Embarked status")),
                    as_int(row.get("Disembarked")), clean(row.get("Disembarked status")), clean(row.get("Outcome"))
                )
                cur.execute(
                    """INSERT INTO atlas.voyage(
                         source_dataset,source_native_voyage_id,primary_source_version_id,vessel_name,year_arrived,year_status,
                         flag_documented,flag_imputed,seed_carrier_bucket,carrier_bucket_basis,flag_carrier_note,
                         constructed_at_raw,registered_at_raw,registration_year,voyage_origin_raw,origin_status,
                         principal_embarkation_raw,embarkation_status,principal_landing_raw,landing_status,
                         embarked_count,embarked_status,disembarked_count,disembarked_status,outcome,review_status)
                       VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,'reviewed')
                       RETURNING voyage_id""",
                    vals,
                )
                voyage_id = cur.fetchone()[0]
                voyage_by_legacy[legacy] = voyage_id
                voyage_year_by_legacy[legacy] = as_int(row.get("Year arrived"))
                cur.execute("INSERT INTO audit.v061_voyage_map(legacy_voyage_id,voyage_id) VALUES (%s,%s)", (legacy, voyage_id))

            # Claim source de-duplication by claim+source+direction. Notes are aggregated so a
            # repeated workbook reference does not masquerade as independent evidence.
            def ensure_claim_source(claim_id, source_version_id, evidence_role, directness, direction, notes):
                cur.execute(
                    """SELECT claim_source_id, notes FROM atlas.claim_source
                       WHERE claim_id=%s AND source_version_id=%s AND direction=%s
                       ORDER BY created_at LIMIT 1""",
                    (claim_id, source_version_id, direction),
                )
                existing = cur.fetchone()
                if existing:
                    merged = (existing[1] or "")
                    if notes and notes not in merged:
                        merged = (merged + "\n" + notes).strip()
                        cur.execute("UPDATE atlas.claim_source SET notes=%s WHERE claim_source_id=%s", (merged, existing[0]))
                    return existing[0]
                cur.execute(
                    """INSERT INTO atlas.claim_source(claim_id,source_version_id,evidence_role,directness,direction,notes)
                       VALUES (%s,%s,%s,%s,%s,%s) RETURNING claim_source_id""",
                    (claim_id, source_version_id, evidence_role, directness, direction, notes),
                )
                return cur.fetchone()[0]

            # Semantic migration of the four global evidence sheets.
            # Every row contributes research-coverage provenance. RI rows stop there.
            spatial_by_global_key: dict[str, Any] = {}
            global_claim_count = 0
            for row in global_evidence:
                evidence_key = str(row["evidence_key"])
                url = str(row["source_url"])
                source_version_id = source_version_by_url[url]
                coverage_key = (str(row["region"]), str(row["period"]))
                coverage_assessment_id = coverage_assessment_by_key.get(coverage_key)
                if coverage_assessment_id is None:
                    raise RuntimeError(f"No research coverage assessment for global evidence row {evidence_key}: {coverage_key}")
                cur.execute(
                    """INSERT INTO audit.research_coverage_source(
                         coverage_assessment_id,source_version_id,source_role,locator,notes)
                       VALUES (%s,%s,'evidence_sheet_source',%s,%s)
                       ON CONFLICT DO NOTHING""",
                    (
                        coverage_assessment_id, source_version_id, evidence_key,
                        f"Reviewed source cited by {evidence_key}; coverage={row['coverage']}.",
                    ),
                )
                if row["coverage"] == "RI":
                    continue

                plan = POSITIVE_PLAN[evidence_key]
                cur.execute(
                    """INSERT INTO atlas.spatial_entity(
                         entity_type_code,canonical_name,display_name,from_year,to_year,notes,review_status)
                       VALUES (%s,%s,%s,%s,%s,%s,'reviewed') RETURNING spatial_entity_id""",
                    (
                        plan["spatial_type"], row["area"], row["area"], row["from_year"], row["to_year"],
                        f"Migrated historical/analytical target from {evidence_key}; geometry unresolved pending the documented resolver hierarchy.",
                    ),
                )
                spatial_id = cur.fetchone()[0]
                spatial_by_global_key[evidence_key] = spatial_id
                from_year, to_year, date_text, precision = temporal_fields(row, plan)

                for target in plan["targets"]:
                    kind = target["kind"]
                    if kind == "territorial_practice":
                        summary = str(row["decision"])
                        cur.execute(
                            """INSERT INTO atlas.claim(
                                 claim_kind_code,from_year,to_year,date_text_original,temporal_precision,
                                 spatial_precision,summary,confidence,review_status,publication_status,notes)
                               VALUES ('territorial_practice',%s,%s,%s,%s,%s,%s,%s,'reviewed','unpublished',%s)
                               RETURNING claim_id""",
                            (
                                from_year, to_year, date_text, precision, "workbook area/region label",
                                summary, row["coverage"],
                                f"v061_global_evidence={evidence_key}; practice_issue={row['practice_issue']}.",
                            ),
                        )
                        claim_id = cur.fetchone()[0]
                        cur.execute(
                            """INSERT INTO atlas.territorial_practice_claim(
                                 claim_id,spatial_entity_id,practice_type_code,practice_level,
                                 coverage_state_code,classification_status,notes)
                               VALUES (%s,%s,%s,NULL,%s,%s,%s)""",
                            (
                                claim_id, spatial_id, target["practice_type"], target["coverage_state"],
                                target["classification_status"],
                                "P-level intentionally unassigned during workbook semantic migration.",
                            ),
                        )
                        mapping_role = f"territorial_practice:{target['practice_type']}"
                    elif kind == "external_participation":
                        summary = str(row["decision"])
                        cur.execute(
                            """INSERT INTO atlas.claim(
                                 claim_kind_code,from_year,to_year,date_text_original,temporal_precision,
                                 spatial_precision,summary,confidence,review_status,publication_status,notes)
                               VALUES ('external_participation',%s,%s,%s,%s,%s,%s,%s,'reviewed','unpublished',%s)
                               RETURNING claim_id""",
                            (
                                from_year, to_year, date_text, precision, "workbook area/region label",
                                summary, row["coverage"],
                                f"v061_global_evidence={evidence_key}; practice_issue={row['practice_issue']}.",
                            ),
                        )
                        claim_id = cur.fetchone()[0]
                        cur.execute(
                            """INSERT INTO atlas.external_participation_claim(
                                 claim_id,spatial_entity_id,participation_type_code,role_text,notes)
                               VALUES (%s,%s,%s,%s,%s)""",
                            (
                                claim_id, spatial_id, target["participation_type"], target.get("role_text"),
                                "External/network participation is analytically separate from territorial practice.",
                            ),
                        )
                        mapping_role = f"external_participation:{target['participation_type']}"
                    elif kind == "legal_event":
                        summary = str(row["decision"])
                        cur.execute(
                            """INSERT INTO atlas.claim(
                                 claim_kind_code,from_year,to_year,date_text_original,temporal_precision,
                                 spatial_precision,summary,confidence,review_status,publication_status,notes)
                               VALUES ('legal_event',%s,%s,%s,%s,%s,%s,%s,'reviewed','unpublished',%s)
                               RETURNING claim_id""",
                            (
                                from_year, to_year, date_text, precision, "workbook area/region label",
                                summary, row["coverage"],
                                f"v061_global_evidence={evidence_key}; legal context split from practice claim.",
                            ),
                        )
                        claim_id = cur.fetchone()[0]
                        cur.execute(
                            """INSERT INTO atlas.legal_event(
                                 claim_id,jurisdiction_spatial_entity_id,event_type,legal_status_after,scope,notes)
                               VALUES (%s,%s,%s,%s,%s,%s)""",
                            (
                                claim_id, spatial_id, target["event_type"], target.get("legal_status_after"),
                                target.get("scope"), "Workbook row describes a legal/suppression process, not a single clean abolition date.",
                            ),
                        )
                        mapping_role = f"legal_event:{target['event_type']}"
                    else:
                        raise RuntimeError(f"Unknown global evidence target kind {kind!r} for {evidence_key}")

                    ensure_claim_source(
                        claim_id, source_version_id, "global workbook evidence row",
                        "exact source URL cited by workbook", "supports",
                        f"{evidence_key}; legacy_coverage={row['coverage']}; area={row['area']}.",
                    )
                    cur.execute(
                        """INSERT INTO audit.v061_evidence_claim_map(
                             legacy_evidence_id,claim_id,mapping_role,notes)
                           VALUES (%s,%s,%s,%s)""",
                        (
                            evidence_key, claim_id, mapping_role,
                            "Explicit semantic migration of canonical global evidence row.",
                        ),
                    )
                    global_claim_count += 1

            if global_claim_count != report["global_evidence"]["claim_targets"]:
                raise RuntimeError(
                    f"Global evidence claim target count mismatch: expected {report['global_evidence']['claim_targets']}, "
                    f"inserted {global_claim_count}"
                )

            relation_claim: dict[tuple[str, str], Any] = {}
            for row in t["voyage_owners"]:
                legacy_voyage = str(as_int(row["Voyage ID"]))
                legacy_owner = str(clean(row["Owner ID"]))
                raw("v061_voyage_owner", f"{legacy_voyage}:{legacy_owner}", row)
                status_raw = str(clean(row.get("Relationship status")))
                status = "missing_owner" if status_raw == "Missing owner placeholder" else "documented"
                actor_id = actor_by_legacy.get(legacy_owner)
                year = voyage_year_by_legacy[legacy_voyage]
                vessel = next(clean(v.get("Vessel")) for v in t["voyages"] if str(as_int(v["Voyage ID"])) == legacy_voyage)
                if status == "missing_owner":
                    summary = f"No owner is recorded for voyage {legacy_voyage} ({vessel}) in the reviewed voyage record."
                else:
                    actor_name = next(clean(o.get("Normalized owner / entity")) for o in t["owners"] if clean(o.get("Owner ID")) == legacy_owner)
                    summary = f"{actor_name} is recorded as {clean(row.get('Relationship role')) or 'owner'} for voyage {legacy_voyage} ({vessel})."
                cur.execute(
                    """INSERT INTO atlas.claim(claim_kind_code,from_year,to_year,date_text_original,temporal_precision,
                                               summary,review_status,publication_status,notes)
                       VALUES ('voyage_owner',%s,%s,%s,'voyage_year',%s,'reviewed','unpublished',%s)
                       RETURNING claim_id""",
                    (year, year, str(year) if year is not None else None, summary,
                     f"Migrated from Atlantic Voyage Owners; legacy status={status_raw}."),
                )
                claim_id = cur.fetchone()[0]
                relation_claim[(legacy_voyage, legacy_owner)] = claim_id
                source_url = str(clean(row.get("Source URL")))
                ensure_claim_source(claim_id, source_version_by_url[source_url], "voyage ownership/status", "structured voyage record", "supports", "Atlantic Voyage Owners relation row")
                cur.execute(
                    """INSERT INTO atlas.voyage_owner(voyage_id,actor_id,claim_id,raw_owner_text,relationship_role,
                                                      owner_sequence,ownership_share,share_status,relationship_status,notes)
                       VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s) RETURNING voyage_owner_id""",
                    (voyage_by_legacy[legacy_voyage], actor_id, claim_id, clean(row.get("Raw owner text")), clean(row.get("Relationship role")),
                     as_int(row.get("Owner sequence")), None, clean(row.get("Share status")), status, clean(row.get("Notes"))),
                )
                vo_id = cur.fetchone()[0]
                cur.execute(
                    """INSERT INTO audit.v061_voyage_owner_map(legacy_voyage_id,legacy_owner_id,owner_sequence,voyage_owner_id)
                       VALUES (%s,%s,%s,%s)""",
                    (legacy_voyage, legacy_owner, as_int(row.get("Owner sequence")), vo_id),
                )

            # Semantic migration of OWNER_EVIDENCE.
            plan = evidence_plan()
            evidence_by_id = {str(clean(r["Evidence ID"])): r for r in t["evidence"]}
            for evidence_id, targets in plan.items():
                row = evidence_by_id[evidence_id]
                raw("v061_owner_evidence", evidence_id, row)
                legacy_owner = str(clean(row.get("Owner ID")))
                src_legacy = str(clean(row.get("Source ID")))
                source_version_id = source_by_legacy[src_legacy][1]
                from_year, to_year, precision = parse_claim_period(row.get("Claim period"))
                for target in targets:
                    if target["kind"] == "actor_attribute":
                        actor_id = actor_by_legacy.get(legacy_owner)
                        if actor_id is None:
                            raise RuntimeError(f"Actor attribute target has no real actor: {evidence_id}/{legacy_owner}")
                        summary = str(clean(row.get("Evidence statement")))
                        notes = f"Legacy claim type: {clean(row.get('Claim type'))}; legacy claim value: {clean(row.get('Claim value'))}."
                        if clean(row.get("Research note")):
                            notes += " " + str(clean(row.get("Research note")))
                        cur.execute(
                            """INSERT INTO atlas.claim(claim_kind_code,from_year,to_year,date_text_original,temporal_precision,
                                                       summary,confidence,review_status,publication_status,notes)
                               VALUES ('actor_attribute',%s,%s,%s,%s,%s,%s,'reviewed','unpublished',%s)
                               RETURNING claim_id""",
                            (from_year,to_year,clean(row.get("Claim period")),precision,summary,clean(row.get("Confidence")),notes),
                        )
                        claim_id = cur.fetchone()[0]
                        cur.execute(
                            """INSERT INTO atlas.actor_attribute_claim(claim_id,actor_id,attribute_type_code,value_text,notes)
                               VALUES (%s,%s,%s,%s,%s)""",
                            (claim_id, actor_id, target["attribute_type"], target["value"], f"Migrated from {evidence_id}."),
                        )
                        ensure_claim_source(
                            claim_id, source_version_id, "legacy OWNER_EVIDENCE", clean(row.get("Source type")), "supports",
                            f"{evidence_id}; independent_of_voyage_flag={clean(row.get('Independent of voyage flag?'))}; supports_person_nationality={clean(row.get('Supports person nationality?'))}",
                        )
                    else:
                        key = (target["voyage"], target["owner"])
                        claim_id = relation_claim[key]
                        ensure_claim_source(
                            claim_id, source_version_id, "legacy OWNER_EVIDENCE", clean(row.get("Source type")), "supports",
                            f"{evidence_id}: {clean(row.get('Evidence statement'))}",
                        )
                    cur.execute(
                        """INSERT INTO audit.v061_evidence_claim_map(legacy_evidence_id,claim_id,mapping_role,notes)
                           VALUES (%s,%s,%s,%s)""",
                        (evidence_id, claim_id, target["kind"], f"Semantic migration from {clean(row.get('Claim type'))}."),
                    )

            # Candidate migration manifest, explicitly not the canonical switch.
            manifest_version = "0.6.1-db-migration-candidate"
            cur.execute(
                """INSERT INTO audit.release_manifest(release_version,schema_version,status,changelog,qc_summary,unresolved_issues,manifest)
                   VALUES (%s,'draft-0.10','draft',%s,%s,%s,%s)""",
                (manifest_version,
                 "Foundation migration candidate generated from canonical v0.6.1 workbook.",
                 json.dumps(report["counts"], ensure_ascii=False),
                 "Fredensborg disembarkation unresolved; Fredensborg voyage URL absent from legacy source registry; global evidence bibliographic metadata remains partially migration-generated pending enrichment.",
                 Jsonb({"workbook_sha256": report["sha256"], "canonical_workbook_version": "0.6.1"})),
            )
            # Link historical evidence source versions, including migration-generated direct references; exclude workbook ingest provenance.
            historical_versions = set(v for _, v in source_by_legacy.values()) | set(source_version_by_url.values())
            for svid in historical_versions:
                cur.execute(
                    "INSERT INTO audit.release_source_version(release_version,source_version_id) VALUES (%s,%s) ON CONFLICT DO NOTHING",
                    (manifest_version, svid),
                )

            cur.execute(
                "UPDATE audit.ingest_run SET status='completed', completed_at=now(), notes=notes || %s WHERE ingest_run_id=%s",
                ("\nDry-run invariants passed before apply.", ingest_run_id),
            )

        conn.commit()

    return {
        "applied": True,
        "workbook_sha256": report["sha256"],
        "counts": report["counts"],
        "source_registry_gaps": report["source_registry_gaps"],
        "candidate_release": "0.6.1-db-migration-candidate",
    }


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--workbook", required=True, type=Path)
    parser.add_argument("--report", type=Path)
    parser.add_argument("--dsn", default=os.environ.get("DATABASE_URL"))
    parser.add_argument("--apply", action="store_true", help="Apply to PostgreSQL after validation")
    args = parser.parse_args(argv)

    normalized = validate_and_normalize(args.workbook)
    report = normalized["report"]
    if args.report:
        args.report.parent.mkdir(parents=True, exist_ok=True)
        args.report.write_text(json.dumps(report, ensure_ascii=False, indent=2), encoding="utf-8")
    print(json.dumps(report, ensure_ascii=False, indent=2))
    if not report["ok"]:
        return 2
    if args.apply:
        if not args.dsn:
            raise SystemExit("--apply requires --dsn or DATABASE_URL")
        applied = apply_to_database(args.workbook, args.dsn, normalized)
        print(json.dumps(applied, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
