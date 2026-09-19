"""Tiny content-addressed object-store baseline for tooling evaluation.

This uses the local filesystem only. It models the semantics we want from a
future object store: immutable bytes addressed by SHA-256 and verified on read.
It is NOT production storage.
"""
from __future__ import annotations

import hashlib
from pathlib import Path
import shutil


def sha256_file(path: str | Path) -> str:
    h = hashlib.sha256()
    with Path(path).open("rb") as f:
        for chunk in iter(lambda: f.read(1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest()


def object_key_for_sha256(digest: str) -> str:
    digest = digest.lower()
    if len(digest) != 64 or any(c not in "0123456789abcdef" for c in digest):
        raise ValueError("digest must be 64 lowercase/uppercase hexadecimal characters")
    return f"sha256/{digest[:2]}/{digest[2:]}"


def put_immutable(source: str | Path, store_root: str | Path) -> dict[str, object]:
    source = Path(source)
    root = Path(store_root)
    if not source.is_file():
        raise FileNotFoundError(source)

    digest = sha256_file(source)
    key = object_key_for_sha256(digest)
    target = root / key
    target.parent.mkdir(parents=True, exist_ok=True)

    if target.exists():
        if sha256_file(target) != digest:
            raise RuntimeError(f"existing object failed checksum verification: {key}")
        created = False
    else:
        shutil.copyfile(source, target)
        if sha256_file(target) != digest:
            target.unlink(missing_ok=True)
            raise RuntimeError("copied object failed checksum verification")
        created = True

    return {
        "algorithm": "sha256",
        "sha256": digest,
        "object_key": key,
        "size_bytes": source.stat().st_size,
        "created": created,
    }


def retrieve_verified(
    store_root: str | Path,
    object_key: str,
    destination: str | Path,
    expected_sha256: str,
) -> Path:
    source = Path(store_root) / object_key
    if not source.is_file():
        raise FileNotFoundError(source)
    if sha256_file(source) != expected_sha256.lower():
        raise RuntimeError("stored object checksum mismatch")

    destination = Path(destination)
    destination.parent.mkdir(parents=True, exist_ok=True)
    shutil.copyfile(source, destination)
    if sha256_file(destination) != expected_sha256.lower():
        destination.unlink(missing_ok=True)
        raise RuntimeError("retrieved object checksum mismatch")
    return destination
