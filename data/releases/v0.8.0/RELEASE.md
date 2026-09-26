# Historical Slavery Atlas data release v0.8.0

**Release contract:** historical-slavery-atlas-canonical-release-package-v1

This directory contains the exact immutable package approved for canonical historical
release. Canonical publication is recorded by the Decisions Log and
`audit.release_manifest`; promotion must use these exact bytes without rewriting the
package.

## Authority

The release is derived from the explicit D-115 reviewed authority closure,
not from every row currently present in PostgreSQL and not from `review_status` alone.

- Authority decision: D-115
- Authority decision commit: `66fe05593e25cf2793c16172534a4ef07a775909`
- Authority snapshot release: `v0.8.0-expansion-02-authority-v1`
- Schema head: `0034`
- Membership SHA-256: `708f9f9d2a7cac185e17bfc3773fa1543d43f6fd7898529bff1583e08ffb6076`
- Database-state SHA-256: `3954fe4fb9b4e2f3d91915f90a142103963a07f12688ebebe39f91adaf3d2c89`
- Authority bundle SHA-256: `89f22a44ab70505c728f6e9c0a7d8591bd6b2b7ddd8c82b21a266c86fd265cb7`

Membership counts:

- claims: 75
- actors: 11
- spatial entities: 50
- reviewed historical geometries: 46
- voyages: 8
- coverage assessments: 99
- source versions: 294
- research-target results: 26

## Predecessor

Canonical predecessor: `v0.7.0`

Artifact: `data/releases/v0.7.0/manifest.json`

SHA-256: `f65964221cbe2045d75303a5940c75f4526e9110a2b2cf323a9d0979e2f5e57a`

The predecessor release remains immutable and is not overwritten by this release.

## Review and publication boundary

Internal research-target reviews represented: 26.

Independent historical reviews: **0**.

Creating this package does not move the public UI/API release channel. It remains
`v0.7.0-public-mvp-v1` until a separate serving cutover passes.

`authority-state.json` is a byte-for-byte preservation copy of the reviewed authority
snapshot. `cartography-recovery-fingerprint.json` carries the D-108 portable
cartography reconstruction invariant. These are preservation evidence and do not imply
that unresolved geometry has become mapped.

See `manifest.json`, `SHA256SUMS.txt`, the QC/unresolved-issues documents and the
migration/reconciliation report for the complete release contract.
