"""Provider-neutral release manifest proof.

Evaluation code only. It performs local hashing/verification and deterministic
membership digests. It does not write to PostgreSQL or object storage.
"""
from __future__ import annotations

import hashlib
from pathlib import Path
from typing import Any


def sha256_file(path: str | Path) -> str:
    h = hashlib.sha256()
    with Path(path).open("rb") as f:
        for chunk in iter(lambda: f.read(1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest()


def membership_digest(ids: list[str]) -> str:
    """Digest a set-like stable-ID membership list deterministically."""
    normalized = sorted({str(x).strip() for x in ids if str(x).strip()})
    payload = ("\n".join(normalized) + ("\n" if normalized else "")).encode("utf-8")
    return hashlib.sha256(payload).hexdigest()


def artifact_entry(
    path: str | Path,
    *,
    role: str,
    media_type: str,
    storage_status: str = "external",
    storage_locator: str | None = None,
) -> dict[str, Any]:
    p = Path(path)
    if not p.is_file():
        raise FileNotFoundError(p)
    return {
        "role": role,
        "filename": p.name,
        "sha256": sha256_file(p),
        "size_bytes": p.stat().st_size,
        "media_type": media_type,
        "storage": {
            "status": storage_status,
            "locator": storage_locator,
        },
    }


def membership_entry(object_type: str, ids: list[str]) -> dict[str, Any]:
    normalized = sorted({str(x).strip() for x in ids if str(x).strip()})
    return {
        "object_type": object_type,
        "count": len(normalized),
        "membership_sha256": membership_digest(normalized),
    }


def verify_artifact(path: str | Path, expected: dict[str, Any]) -> list[str]:
    p = Path(path)
    errors: list[str] = []
    if not p.is_file():
        return [f"artifact missing: {p}"]

    if p.name != expected.get("filename"):
        errors.append(
            f"filename mismatch: expected {expected.get('filename')!r}, found {p.name!r}"
        )
    actual_size = p.stat().st_size
    if actual_size != expected.get("size_bytes"):
        errors.append(
            f"size mismatch: expected {expected.get('size_bytes')}, found {actual_size}"
        )
    actual_hash = sha256_file(p)
    if actual_hash.lower() != str(expected.get("sha256", "")).lower():
        errors.append(
            f"sha256 mismatch: expected {expected.get('sha256')}, found {actual_hash}"
        )
    return errors


def validate_manifest(manifest: dict[str, Any]) -> list[str]:
    errors: list[str] = []
    if not manifest.get("release_version"):
        errors.append("release_version is required")
    if not manifest.get("status"):
        errors.append("status is required")

    artifacts = manifest.get("artifacts")
    if not isinstance(artifacts, list) or not artifacts:
        errors.append("at least one artifact entry is required")
    else:
        seen = set()
        for i, artifact in enumerate(artifacts):
            for field in ("role", "filename", "sha256", "size_bytes", "media_type"):
                if artifact.get(field) in (None, ""):
                    errors.append(f"artifacts[{i}].{field} is required")
            digest = str(artifact.get("sha256", ""))
            if len(digest) != 64 or any(c not in "0123456789abcdefABCDEF" for c in digest):
                errors.append(f"artifacts[{i}].sha256 must be 64 hex characters")
            key = (artifact.get("role"), artifact.get("filename"))
            if key in seen:
                errors.append(f"duplicate artifact role/filename: {key}")
            seen.add(key)

    membership = manifest.get("database_membership", [])
    if not isinstance(membership, list):
        errors.append("database_membership must be a list")
    else:
        seen_types = set()
        for i, item in enumerate(membership):
            typ = item.get("object_type")
            if not typ:
                errors.append(f"database_membership[{i}].object_type is required")
            elif typ in seen_types:
                errors.append(f"duplicate database membership type: {typ}")
            seen_types.add(typ)
            if not isinstance(item.get("count"), int) or item.get("count", -1) < 0:
                errors.append(f"database_membership[{i}].count must be a non-negative integer")
            digest = str(item.get("membership_sha256", ""))
            if len(digest) != 64 or any(c not in "0123456789abcdefABCDEF" for c in digest):
                errors.append(
                    f"database_membership[{i}].membership_sha256 must be 64 hex characters"
                )
    return errors
