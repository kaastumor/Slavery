# Historical Slavery Atlas data release v0.7.0

**Release contract:** historical-slavery-atlas-canonical-release-package-v1

This directory contains the exact bytes proposed and approved for the first
PostgreSQL/PostGIS-backed canonical historical release. Canonical publication is a
governed state recorded by the Decisions Log and `audit.release_manifest`; promotion
must use these exact bytes without rewriting the package.

## Authority

The historical release is derived from the explicit D-109 canonical-research authority
closure, not from every row currently present in PostgreSQL and not from
`review_status` alone.

- Authority decision: D-109
- Authority decision commit: `295a108d9e46f0c3f0e6a867dc06cbae5eda1356`
- Authority snapshot release: `gate3-db-authority-proof-v1`
- Schema head: `0033`
- Membership SHA-256: `ebc9d32f09857744841a0cf92699c41739b624ac4bd94c43798eb1f61e3b0dd3`
- Database-state SHA-256: `31b7a7b675445e5758ffd68d64ff0f0cde83df1b0ea65f29835246deb2ae26ff`
- Authority bundle SHA-256: `e26bc9243c71226e6107162d15c44a0fa13d063ed7708bb12627e4ee8f13c54b`

Membership counts:

- claims: 40
- actors: 11
- spatial entities: 18
- reviewed historical geometries: 0
- voyages: 8
- coverage assessments: 99
- source versions: 211
- research-target results: 26

## Predecessor

Canonical predecessor: `v0.6.1`

Artifact: `Historical_Slavery_Atlas_v0.6.1_Controlled_Atlantic_Ingestion.xlsx`

SHA-256: `0a38e4eb6f63c3bb4ce9543be379605d24dd9ff1c1cea1e0a49c0c3db7ba17d4`

The predecessor release remains immutable and is not overwritten by this release.

## Review and publication boundary

Internal research-target reviews represented: 26.

Independent historical reviews: **0**.

Gate 4 does not move the public UI/API release channel. It remains
`mvp-preview-ancient-v2` until a separate Gate-5 cutover passes.

`authority-state.json` is a byte-for-byte preservation copy of the reviewed Gate-3
authority snapshot. `cartography-recovery-fingerprint.json` carries the exact D-108
portable cartography reconstruction invariant. These are preservation evidence, not a
signal that every member must be exposed by the current public UI.

See `manifest.json`, `SHA256SUMS.txt`, the QC/unresolved-issues documents and the
migration/reconciliation report for the complete release contract.
