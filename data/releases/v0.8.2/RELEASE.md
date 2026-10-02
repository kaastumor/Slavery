# Historical Slavery Atlas data release v0.8.2

**Release contract:** historical-slavery-atlas-canonical-release-package-v1

This directory contains the exact immutable package approved for canonical historical
release. Canonical publication is recorded by the Decisions Log and
`audit.release_manifest`; promotion must use these exact bytes without rewriting the
package.

## Authority

The release is derived from the explicit D-125 reviewed authority closure,
not from every row currently present in PostgreSQL and not from `review_status` alone.

- Authority decision: D-125
- Authority decision commit: `063b94efdbcc9daff2534cb67b68a57fdc903302`
- Authority snapshot release: `v0.8.2-requested-corpus-authority-v1`
- Schema head: `0034`
- Membership SHA-256: `1d361708952207a82152eab84cb85f4040a93b498c5732dc67f614f6eb0de88c`
- Database-state SHA-256: `ea4235d7fb933f847d40f406c62d5790df88502ef8531eaec8a03cfadc2f471b`
- Authority bundle SHA-256: `e41320690a4fca3c6112ae7661e1efc10197ed0b6dc37e77cd8a911aaed68b03`

Membership counts:

- claims: 92
- actors: 11
- spatial entities: 70
- reviewed historical geometries: 61
- voyages: 8
- coverage assessments: 99
- source versions: 335
- research-target results: 26

## Predecessor

Canonical predecessor: `v0.8.1`

Artifact: `data/releases/v0.8.1/manifest.json`

SHA-256: `773bae962e19d4674a9aab7bfe8995667db2295d3c5ddc93448d8ba48d71fc52`

The predecessor release remains immutable and is not overwritten by this release.

## Review and publication boundary

Internal research-target reviews represented: 26.

Independent historical reviews: **0**.

Creating this package does not move the public UI/API release channel. It remains
`v0.8.1-public-mvp-v2` until a separate serving cutover passes.

`authority-state.json` is a byte-for-byte preservation copy of the reviewed authority
snapshot. `cartography-recovery-fingerprint.json` carries the D-108 portable
cartography reconstruction invariant. These are preservation evidence and do not imply
that unresolved geometry has become mapped.

See `manifest.json`, `SHA256SUMS.txt`, the QC/unresolved-issues documents and the
migration/reconciliation report for the complete release contract.
