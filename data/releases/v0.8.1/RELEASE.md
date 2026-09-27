# Historical Slavery Atlas data release v0.8.1

**Release contract:** historical-slavery-atlas-canonical-release-package-v1

This directory contains the exact immutable package approved for canonical historical
release. Canonical publication is recorded by the Decisions Log and
`audit.release_manifest`; promotion must use these exact bytes without rewriting the
package.

## Authority

The release is derived from the explicit D-117 reviewed authority closure,
not from every row currently present in PostgreSQL and not from `review_status` alone.

- Authority decision: D-117
- Authority decision commit: `dbb45102c5e1d810f8f7e84b628456051b12fe5e`
- Authority snapshot release: `v0.8.1-rome-geometry-authority-v1`
- Schema head: `0034`
- Membership SHA-256: `a2f4be081257716310bddaf357667d5b1a8a561198b8f08c6a24c95572a11462`
- Database-state SHA-256: `30f4de289c2402659a2494beb14adef1a31125d2fce4dd60344a3ca9a80460b9`
- Authority bundle SHA-256: `0aa4d4fd9e4bacad0e359b655fbe237d1ef758b63fcb984ead9651d2c8181ea5`

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

Canonical predecessor: `v0.8.0`

Artifact: `data/releases/v0.8.0/manifest.json`

SHA-256: `c73112abea60b0b79bc3b55d9a9540eec5dd1b58e57437c55917f2f4ab808a60`

The predecessor release remains immutable and is not overwritten by this release.

## Review and publication boundary

Internal research-target reviews represented: 26.

Independent historical reviews: **0**.

Creating this package does not move the public UI/API release channel. It remains
`v0.8.0-public-mvp-v2` until a separate serving cutover passes.

`authority-state.json` is a byte-for-byte preservation copy of the reviewed authority
snapshot. `cartography-recovery-fingerprint.json` carries the D-108 portable
cartography reconstruction invariant. These are preservation evidence and do not imply
that unresolved geometry has become mapped.

See `manifest.json`, `SHA256SUMS.txt`, the QC/unresolved-issues documents and the
migration/reconciliation report for the complete release contract.
