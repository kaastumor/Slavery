#!/usr/bin/env python3
"""Small dependency-free validator for Core Contract v1 release rows.

This is a release-contract guard, not the canonical database schema.
"""

REQUIRED_C1 = {
    "research_stage",
    "classification_outcome",
    "bounded_proposition",
    "required_abstention",
    "temporal_applicability",
    "temporal_precision",
    "evidence_locus",
    "inference_extent",
    "language_access_limitations",
    "coverage_confidence",
    "review_state",
    "release_id",
    "sources",
}

ALLOWED_RESEARCH_STAGE = {"not_researched", "source_identified", "under_review", "review_complete"}
ALLOWED_OUTCOME = {"unassessed", "classified", "disputed", "inconclusive"}
ALLOWED_SOURCE_QUALITY = {
    "production_grade",
    "usable_with_limitation",
    "context_only",
    "access_limited",
    "review_required",
}

def validate_row(row):
    errors = []
    tier = row.get("tier")
    if tier not in {"C0", "C1", "C2"}:
        errors.append("tier must be C0/C1/C2")
        return errors

    if row.get("research_stage") not in ALLOWED_RESEARCH_STAGE:
        errors.append("invalid research_stage")
    if row.get("classification_outcome") not in ALLOWED_OUTCOME:
        errors.append("invalid classification_outcome")

    if tier == "C0":
        if row.get("classification_outcome") != "unassessed":
            errors.append("C0 must be unassessed")
        for k in ("bounded_proposition", "territorial_practice", "legal_state", "network_participation"):
            if row.get(k):
                errors.append(f"C0 must not assert {k}")
        return errors

    missing = sorted(k for k in REQUIRED_C1 if k not in row)
    if missing:
        errors.append("missing C1 fields: " + ", ".join(missing))

    if not str(row.get("required_abstention", "")).strip():
        errors.append("C1/C2 requires explicit abstention")

    sources = row.get("sources", [])
    if not sources:
        errors.append("C1/C2 requires at least one recoverable source relation")

    proposition = bool(str(row.get("bounded_proposition", "")).strip())
    decisive = [s for s in sources if s.get("decisive")]
    if proposition:
        if not decisive:
            errors.append("bounded proposition requires at least one decisive source relation")
        elif all(s.get("claim_fitness") in {"context_only", "review_required"} for s in decisive):
            errors.append("bounded proposition cannot rely only on context/review-required decisive sources")

    for s in row.get("sources", []):
        if s.get("claim_fitness") not in ALLOWED_SOURCE_QUALITY:
            errors.append("invalid source claim_fitness")
        if not s.get("source_version_ref"):
            errors.append("source relation missing source_version_ref")

    if row.get("network_participation") and row.get("territorial_practice_inferred_from_network") is True:
        errors.append("network participation cannot mechanically create territorial practice")

    if row.get("research_stage") == "review_complete" and row.get("classification_outcome") == "unassessed":
        errors.append("review_complete cannot remain unassessed without explicit exception")

    return errors
