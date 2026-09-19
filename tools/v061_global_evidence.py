"""Explicit semantic plan for the four v0.6.1 global evidence sheets.

This module contains no database writes. It normalizes workbook rows and states
which positive/disputed rows may become which existing claim subtypes.
"""
from __future__ import annotations

from collections import Counter
from typing import Any

GLOBAL_EVIDENCE_SHEETS = (
    "v0.4.7 Evidence",
    "v0.4.8 Evidence",
    "v0.4.9 Evidence",
    "v0.5.0 Evidence",
)

EXPECTED_GLOBAL_COUNTS = {
    "rows": 36,
    "unique_source_urls": 29,
    "S": 14,
    "P": 3,
    "D": 1,
    "RI": 18,
    "claim_targets": 22,
}

PERIODS = {
    "3000–2001 BCE": (-2999, -2000),
    "2000–1001 BCE": (-1999, -1000),
    "1000–1 BCE": (-999, 0),
    "500–999": (500, 999),
    "1800–1899": (1800, 1899),
    "1900–present": (1900, None),
}


def _clean(value: Any) -> Any:
    if isinstance(value, str):
        value = value.strip()
        return value if value else None
    return value


def _first(row: dict[str, Any], *keys: str) -> Any:
    for key in keys:
        value = _clean(row.get(key))
        if value is not None:
            return value
    return None


def extract_global_evidence(sheet_rows: dict[str, list[list[Any]]]) -> list[dict[str, Any]]:
    out: list[dict[str, Any]] = []
    for sheet_name in GLOBAL_EVIDENCE_SHEETS:
        rows = sheet_rows[sheet_name]
        header_index = next(
            i for i, row in enumerate(rows)
            if row and _clean(row[0]) == "Region" and "Coverage" in [_clean(x) for x in row]
        )
        headers = [_clean(x) for x in rows[header_index]]
        for zero_index, values in enumerate(rows[header_index + 1 :], start=header_index + 1):
            if not values or _clean(values[0]) is None:
                continue
            record = {
                str(headers[i]): _clean(values[i]) if i < len(values) else None
                for i in range(len(headers))
                if headers[i] is not None
            }
            period = str(_first(record, "Period"))
            if period not in PERIODS:
                raise ValueError(f"Unknown global evidence period {period!r} in {sheet_name}")
            from_year, to_year = PERIODS[period]
            row_number = zero_index + 1
            out.append({
                "evidence_key": f"{sheet_name}!{row_number}",
                "sheet_name": sheet_name,
                "row_number": row_number,
                "region": _first(record, "Region"),
                "period": period,
                "from_year": from_year,
                "to_year": to_year,
                "area": _first(record, "Polity / area", "Polity / culture", "Culture / evidence universe"),
                "practice_issue": _first(record, "Practice type", "Practice / issue", "Issue"),
                "coverage": _first(record, "Coverage"),
                "decision": _first(record, "Evidence decision", "Decision"),
                "source_url": _first(record, "Source URL"),
                "raw": record,
            })
    return out


POSITIVE_PLAN: dict[str, dict[str, Any]] = {
    "v0.4.7 Evidence!5": {
        "spatial_type": "polity",
        "targets": [{"kind": "territorial_practice", "practice_type": "slavery_enslavement", "coverage_state": "classified", "classification_status": "strong workbook classification"}],
    },
    "v0.4.7 Evidence!6": {
        "spatial_type": "region",
        "targets": [{"kind": "territorial_practice", "practice_type": "slavery_enslavement", "coverage_state": "classified", "classification_status": "strong compound regional classification; geometry unresolved"}],
    },
    "v0.4.7 Evidence!7": {
        "spatial_type": "region",
        "targets": [{"kind": "external_participation", "participation_type": "trade_route", "role_text": "slave-trade / captive-movement route"}],
    },
    "v0.4.7 Evidence!8": {
        "spatial_type": "region",
        "targets": [
            {"kind": "territorial_practice", "practice_type": "slavery_enslavement", "coverage_state": "classified", "classification_status": "strong workbook classification"},
            {"kind": "legal_event", "event_type": "suppression_restrictions", "legal_status_after": "mixed_conflicting_or_subnational", "scope": "piecemeal restrictions on markets and trade routes; not a single clean abolition date"},
        ],
    },
    "v0.4.7 Evidence!9": {
        "spatial_type": "region",
        "targets": [{"kind": "territorial_practice", "practice_type": "state_forced_labour", "coverage_state": "classified", "classification_status": "strong workbook classification"}],
    },
    "v0.4.7 Evidence!10": {
        "spatial_type": "polity",
        "targets": [{"kind": "territorial_practice", "practice_type": "penal_labour", "coverage_state": "classified", "classification_status": "strong workbook classification; not chattel slavery"}],
    },
    "v0.4.7 Evidence!11": {
        "spatial_type": "polity",
        "targets": [{"kind": "territorial_practice", "practice_type": "state_forced_labour", "coverage_state": "classified", "classification_status": "forced labour secure; possible slavery/servitude language retained as qualification"}],
    },
    "v0.4.7 Evidence!12": {
        "spatial_type": "region",
        "targets": [{"kind": "territorial_practice", "practice_type": "forced_labour", "coverage_state": "reviewed", "classification_status": "current rights evidence with contested/alleged elements"}],
    },
    "v0.4.7 Evidence!13": {
        "spatial_type": "polity",
        "targets": [{"kind": "territorial_practice", "practice_type": "debt_bondage", "coverage_state": "classified", "classification_status": "strong workbook classification"}],
    },
    "v0.4.7 Evidence!14": {
        "spatial_type": "region",
        "targets": [{"kind": "territorial_practice", "practice_type": "debt_bondage", "coverage_state": "classified", "classification_status": "strong workbook classification"}],
    },
    "v0.4.8 Evidence!5": {
        "spatial_type": "region",
        "from_year": 1933,
        "to_year": 1945,
        "date_text_original": "1933–1945",
        "temporal_precision": "year_range",
        "targets": [{"kind": "territorial_practice", "practice_type": "state_forced_labour", "coverage_state": "classified", "classification_status": "strong workbook classification"}],
    },
    "v0.4.8 Evidence!6": {
        "spatial_type": "region",
        "targets": [{"kind": "territorial_practice", "practice_type": "forced_labour", "coverage_state": "classified", "classification_status": "strong contemporary regional classification"}],
    },
    "v0.4.8 Evidence!7": {
        "spatial_type": "region",
        "from_year": 2014,
        "to_year": None,
        "date_text_original": "from 2014",
        "temporal_precision": "open_ended_from_year",
        "targets": [
            {"kind": "territorial_practice", "practice_type": "slavery_enslavement", "coverage_state": "classified", "classification_status": "strong workbook classification"},
            {"kind": "territorial_practice", "practice_type": "sexual_slavery", "coverage_state": "classified", "classification_status": "strong workbook classification"},
            {"kind": "external_participation", "participation_type": "slave_trade_network", "role_text": "sale / transfer of enslaved Yazidi women and girls"},
        ],
    },
    "v0.4.9 Evidence!5": {
        "spatial_type": "region",
        "targets": [{"kind": "territorial_practice", "practice_type": "slavery_enslavement", "coverage_state": "classified", "classification_status": "slavery secure; status internally differentiated"}],
    },
    "v0.4.9 Evidence!6": {
        "spatial_type": "polity",
        "from_year": -2129,
        "to_year": -2109,
        "date_text_original": "c. 2130–2110 BCE",
        "temporal_precision": "approximate_range",
        "targets": [{"kind": "external_participation", "participation_type": "slave_trade_network", "role_text": "captive/slave influx, export, purchase, tribute and gifting network"}],
    },
    "v0.4.9 Evidence!9": {
        "spatial_type": "region",
        "targets": [{"kind": "territorial_practice", "practice_type": "other_servile_dependency", "coverage_state": "reviewed", "classification_status": "provisional; dāsa/dāsī terminology semantically unstable"}],
    },
    "v0.4.9 Evidence!11": {
        "spatial_type": "polity",
        "targets": [
            {"kind": "territorial_practice", "practice_type": "captive_taking_incorporation", "coverage_state": "reviewed", "classification_status": "captivity/sacrifice secure; not itself proof of slave society"},
            {"kind": "territorial_practice", "practice_type": "slavery_enslavement", "coverage_state": "disputed", "classification_status": "disputed interpretation of captives as slaves"},
        ],
    },
    "v0.5.0 Evidence!5": {
        "spatial_type": "region",
        "targets": [{"kind": "territorial_practice", "practice_type": "other_servile_dependency", "coverage_state": "reviewed", "classification_status": "provisional linguistic reconstruction; no high-intensity inference"}],
    },
}


def validate_global_evidence(rows: list[dict[str, Any]]) -> dict[str, Any]:
    counts = Counter(str(r["coverage"]) for r in rows)
    unique_urls = {str(r["source_url"]) for r in rows}
    positive_keys = {r["evidence_key"] for r in rows if r["coverage"] != "RI"}
    plan_keys = set(POSITIVE_PLAN)
    target_count = sum(len(v["targets"]) for v in POSITIVE_PLAN.values())

    errors: list[str] = []
    if len(rows) != EXPECTED_GLOBAL_COUNTS["rows"]:
        errors.append(f"global evidence rows: expected 36, found {len(rows)}")
    if len(unique_urls) != EXPECTED_GLOBAL_COUNTS["unique_source_urls"]:
        errors.append(f"global evidence unique URLs: expected 29, found {len(unique_urls)}")
    for code in ("S", "P", "D", "RI"):
        if counts.get(code, 0) != EXPECTED_GLOBAL_COUNTS[code]:
            errors.append(f"global evidence {code}: expected {EXPECTED_GLOBAL_COUNTS[code]}, found {counts.get(code,0)}")
    if positive_keys != plan_keys:
        errors.append(f"global positive mapping keys differ: workbook={sorted(positive_keys)} plan={sorted(plan_keys)}")
    if target_count != EXPECTED_GLOBAL_COUNTS["claim_targets"]:
        errors.append(f"global claim targets: expected 22, found {target_count}")

    return {
        "counts": dict(counts),
        "rows": len(rows),
        "unique_source_urls": len(unique_urls),
        "claim_targets": target_count,
        "errors": errors,
        "ok": not errors,
    }


def temporal_fields(row: dict[str, Any], plan: dict[str, Any]) -> tuple[int | None, int | None, str, str]:
    return (
        plan.get("from_year", row["from_year"]),
        plan.get("to_year", row["to_year"]),
        plan.get("date_text_original", row["period"]),
        plan.get("temporal_precision", "broad_period"),
    )
