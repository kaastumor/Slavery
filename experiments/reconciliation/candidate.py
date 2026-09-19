"""Review-gated reconciliation record proof.

Evaluation code only. No database writes and no automatic match acceptance.
"""
from __future__ import annotations

from copy import deepcopy
from datetime import datetime, timezone
from typing import Any


VALID_JUDGMENTS = {"unreviewed", "accepted", "rejected", "unresolved"}


def make_reconciliation_record(
    *,
    raw_text: str,
    service: dict[str, Any],
    candidates: list[dict[str, Any]],
    query_context: dict[str, Any] | None = None,
) -> dict[str, Any]:
    if not raw_text.strip():
        raise ValueError("raw_text is required")
    if not service.get("name"):
        raise ValueError("service.name is required")

    cleaned: list[dict[str, Any]] = []
    for candidate in candidates:
        if not candidate.get("id"):
            raise ValueError("every reconciliation candidate needs an id")
        cleaned.append(deepcopy(candidate))

    return {
        "raw_text": raw_text,
        "service": deepcopy(service),
        "query_context": deepcopy(query_context or {}),
        "candidates": cleaned,
        "judgment": "unreviewed",
        "accepted_candidate_id": None,
        "reviewer": None,
        "reviewed_at": None,
        "review_note": None,
        "automatic_acceptance_allowed": False,
        "jurisdiction_inference_allowed": False,
        "geometry_adoption_allowed": False,
    }


def review_reconciliation(
    record: dict[str, Any],
    *,
    judgment: str,
    reviewer: str,
    candidate_id: str | None = None,
    note: str | None = None,
) -> dict[str, Any]:
    if judgment not in VALID_JUDGMENTS - {"unreviewed"}:
        raise ValueError("judgment must be accepted, rejected, or unresolved")
    if not reviewer.strip():
        raise ValueError("reviewer is required")

    out = deepcopy(record)
    if judgment == "accepted":
        ids = {str(c.get("id")) for c in out.get("candidates", [])}
        if candidate_id is None or str(candidate_id) not in ids:
            raise ValueError("accepted judgment requires an existing candidate_id")
        out["accepted_candidate_id"] = str(candidate_id)
    else:
        if candidate_id is not None:
            raise ValueError("candidate_id is only valid for accepted judgments")
        out["accepted_candidate_id"] = None

    out["judgment"] = judgment
    out["reviewer"] = reviewer
    out["reviewed_at"] = datetime.now(timezone.utc).isoformat()
    out["review_note"] = note
    return out
