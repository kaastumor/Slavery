"""Read-only Zotero -> atlas source candidate mapping proof.

Evaluation code only. This module never writes to Zotero or PostgreSQL.
"""
from __future__ import annotations

from typing import Any


def _clean(value: Any) -> str | None:
    if value is None:
        return None
    text = str(value).strip()
    return text or None


def _creators(data: dict[str, Any]) -> list[dict[str, str]]:
    out: list[dict[str, str]] = []
    for creator in data.get("creators") or []:
        if not isinstance(creator, dict):
            continue
        entry = {"creator_type": _clean(creator.get("creatorType")) or "unknown"}
        if _clean(creator.get("name")):
            entry["name"] = _clean(creator.get("name"))  # type: ignore[assignment]
        else:
            first = _clean(creator.get("firstName"))
            last = _clean(creator.get("lastName"))
            display = " ".join(x for x in (first, last) if x)
            if display:
                entry["name"] = display
        if "name" in entry:
            out.append(entry)
    return out


def zotero_item_to_source_candidate(item: dict[str, Any]) -> dict[str, Any]:
    """Map one Zotero bibliographic item to a non-canonical atlas candidate.

    The result intentionally refuses to assert that the exact reviewed
    SOURCE_VERSION has been resolved.
    """
    data = item.get("data") if isinstance(item.get("data"), dict) else item
    key = _clean(item.get("key") or data.get("key"))
    title = _clean(data.get("title"))
    if not key:
        raise ValueError("Zotero item key is required")
    if not title:
        raise ValueError("Zotero item title is required")

    identifiers = {
        "doi": _clean(data.get("DOI")),
        "isbn": _clean(data.get("ISBN")),
        "issn": _clean(data.get("ISSN")),
        "url": _clean(data.get("url")),
    }
    identifiers = {k: v for k, v in identifiers.items() if v}

    source = {
        "status": "candidate",
        "title": title,
        "source_type": _clean(data.get("itemType")) or "unknown",
        "creators": _creators(data),
        "container_title": _clean(data.get("publicationTitle")),
        "publisher": _clean(data.get("publisher")),
        "language": _clean(data.get("language")),
        "identifiers": identifiers,
        "external_identifiers": {
            "zotero_item_key": key,
            "zotero_object_version": item.get("version"),
        },
    }

    version = {
        "status": "candidate_needs_exact_version_review",
        "publication_or_creation_date_text": _clean(data.get("date")),
        "accessed_at_text": _clean(data.get("accessDate")),
        "url_or_identifier": identifiers.get("doi") or identifiers.get("url"),
        "resolution_note": (
            "Zotero metadata identifies a bibliographic item, but the exact edition, "
            "PDF, archive object, dataset snapshot, or reviewed web state must still "
            "be confirmed before creating a reviewed atlas SOURCE_VERSION."
        ),
    }

    return {
        "integration": "zotero_read_only_proof",
        "source_candidate": source,
        "source_version_candidate": version,
        "canonical_write_allowed": False,
    }


def zotero_attachment_to_asset_candidate(item: dict[str, Any]) -> dict[str, Any]:
    """Map a Zotero attachment item to a non-canonical SOURCE_ASSET candidate."""
    data = item.get("data") if isinstance(item.get("data"), dict) else item
    key = _clean(item.get("key") or data.get("key"))
    if not key:
        raise ValueError("Zotero attachment key is required")
    if data.get("itemType") != "attachment":
        raise ValueError("Expected a Zotero attachment item")

    return {
        "integration": "zotero_read_only_proof",
        "status": "asset_candidate_needs_checksum_and_rights_review",
        "external_identifiers": {
            "zotero_attachment_key": key,
            "zotero_parent_item_key": _clean(data.get("parentItem")),
            "zotero_object_version": item.get("version"),
        },
        "title": _clean(data.get("title")),
        "media_type": _clean(data.get("contentType")),
        "source_url": _clean(data.get("url")),
        "filename": _clean(data.get("filename")),
        "canonical_write_allowed": False,
    }
