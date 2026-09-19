"""Explicit semantic plan for the four v0.6.1 global evidence sheets.

No database writes live here. The mapping is intentionally hand-authored so the
canonical workbook cannot be semantically classified by heuristics.
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
    """Normalize the four evidence tabs.

    The lightweight XLSX reader skips physically blank worksheet rows, so
    evidence_key uses the same logical row sequence already used by raw lineage.
    """
    out: list[dict[str, Any]] = []
    for sheet_name in GLOBAL_EVIDENCE_SHEETS:
        rows = sheet_rows[sheet_name]
        header_index = next(
            i for i, row in enumerate(rows)
            if row and _clean(row[0]) == "Region" and "Coverage" in [_clean(x) for x in row]
        )
        headers = [_clean(x) for x in rows[header_index]]
        for logical_index, values in enumerate(rows[header_index + 1 :], start=header_index + 1):
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
            out.append({
                "evidence_key": f"{sheet_name}!{logical_index + 1}",
                "sheet_name": sheet_name,
                "row_number": logical_index + 1,
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


def _tp(practice_type: str, coverage_state: str, classification_status: str) -> dict[str, Any]:
    return {
        "kind": "territorial_practice",
        "practice_type": practice_type,
        "coverage_state": coverage_state,
        "classification_status": classification_status,
    }


def _ext(participation_type: str, role_text: str) -> dict[str, Any]:
    return {
        "kind": "external_participation",
        "participation_type": participation_type,
        "role_text": role_text,
    }


POSITIVE_PLAN: dict[str, dict[str, Any]] = {
    "v0.4.7 Evidence!4": {
        "spatial_type": "polity",
        "targets": [_tp("slavery_enslavement", "classified", "strong workbook classification")],
    },
    "v0.4.7 Evidence!5": {
        "spatial_type": "region",
        "targets": [_tp("slavery_enslavement", "classified", "strong compound regional classification; geometry unresolved")],
    },
    "v0.4.7 Evidence!6": {
        "spatial_type": "region",
        "targets": [_ext("trade_route", "slave-trade / captive-movement route")],
    },
    "v0.4.7 Evidence!7": {
        "spatial_type": "region",
        "targets": [
            _tp("slavery_enslavement", "classified", "strong workbook classification"),
            {
                "kind": "legal_event",
                "event_type": "suppression_restrictions",
                "legal_status_after": "mixed_conflicting_or_subnational",
                "scope": "piecemeal restrictions on markets and trade routes; not a single clean abolition date",
            },
        ],
    },
    "v0.4.7 Evidence!8": {
        "spatial_type": "region",
        "targets": [_tp("state_forced_labour", "classified", "strong workbook classification")],
    },
    "v0.4.7 Evidence!9": {
        "spatial_type": "polity",
        "targets": [_tp("penal_labour", "classified", "strong workbook classification; not chattel slavery")],
    },
    "v0.4.7 Evidence!9": {
        "spatial_type": "polity",
        "targets": [_tp("penal_labour", "classified", "strong workbook classification; not chattel slavery")],
    },
    "v0.4.7 Evidence!10": {
        "spatial_type": "polity",
        "targets": [_tp("state_forced_labour", "classified", "forced labour secure; possible slavery/servitude language retained as qualification")],
    },
    "v0.4.7 Evidence!11": {
        "spatial_type": "region",
        "targets": [_tp("forced_labour", "reviewed", "current rights evidence with contested/alleged elements")],
    },
    "v0.4.7 Evidence!12": {
        "spatial_type": "polity",
        "targets": [_tp("debt_bondage", "classified", "strong workbook classification")],
    },
    "v0.4.7 Evidence!13": {
        "spatial_type": "region",
        "targets": [_tp("debt_bondage", "classified", "strong workbook classification")],
    },
    "v0.4.8 Evidence!4": {
        "spatial_type": "region",
        "from_year": 1933,
        "to_year": 1945,
        "date_text_original": "1933–1945",
        "temporal_precision": "year_range",
        "targets": [_tp("state_forced_labour", "classified", "strong workbook classification")],
    },
    "v0.4.8 Evidence!5": {
        "spatial_type": "region",
        "targets": [_tp("forced_labour", "classified", "strong contemporary regional classification")],
    },
    "v0.4.8 Evidence!6": {
        "spatial_type": "region",
        "from_year": 2014,
        "to_year": None,
        "date_text_original": "from 2014",
        "temporal_precision": "open_ended_from_year",
        "targets": [
            _tp("slavery_enslavement", "classified", "strong workbook classification"),
            _tp("sexual_slavery", "classified", "strong workbook classification"),
            _ext("slave_trade_network", "sale / transfer of enslaved Yazidi women and girls"),
        ],
    },
    "v0.4.9 Evidence!4": {
        "spatial_type": "region",
        "targets": [_tp("slavery_enslavement", "classified", "slavery secure; status internally differentiated")],
    },
    "v0.4.9 Evidence!5": {
        "spatial_type": "polity",
        "from_year": -2129,
        "to_year": -2109,
        "date_text_original": "c. 2130–2110 BCE",
        "temporal_precision": "approximate_range",
        "targets": [_ext("slave_trade_network", "captive/slave influx, export, purchase, tribute and gifting network")],
    },
    "v0.4.9 Evidence!8": {
        "spatial_type": "region",
        "targets": [_tp("other_servile_dependency", "reviewed", "provisional; dāsa/dāsī terminology semantically unstable")],
    },
    "v0.4.9 Evidence!10": {
        "spatial_type": "polity",
        "targets": [
            _tp("captive_taking_incorporation", "reviewed", "captivity/sacrifice secure; not itself proof of slave society"),
            _tp("slavery_enslavement", "disputed", "disputed interpretation of captives as slaves"),
        ],
    },
    "v0.5.0 Evidence!4": {
        "spatial_type": "region",
        "targets": [_tp("other_servile_dependency", "reviewed", "provisional linguistic reconstruction; no high-intensity inference")],
    },
}


def validate_global_evidence(rows: list[dict[str, Any]]) -> dict[str, Any]:
    counts = Counter(str(r["coverage"]) for r in rows)
    unique_urls = {str(r["source_url"]) for r in rows}
    positive_keys = {str(r["evidence_key"]) for r in rows if r["coverage"] != "RI"}
    plan_keys = set(POSITIVE_PLAN)
    target_count = sum(len(item["targets"]) for item in POSITIVE_PLAN.values())

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
