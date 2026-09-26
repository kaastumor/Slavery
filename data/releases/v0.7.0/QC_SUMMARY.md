# v0.7.0 QC summary

- Gate 0 migration-history reconciliation: PASS.
- Gate 1 v0.6.1 semantic reconciliation and source-native lineage checks: PASS.
- Gate 2 frozen-v3 exact payload round trip and representative idempotent rerun: PASS.
- Gate 3 exact membership/object-digest preservation and fresh-database logical recovery: PASS.
- D-108 portable cartography fingerprint reconstruction across a different PostGIS/GEOS runtime: PASS.
- Private Data API boundary: PASS; anon/authenticated have no internal schema/table access in the verified live state.
- Supabase security advisor at Gate 3: 0 lints.
- Legacy preview/prototype rows outside D-109 membership are excluded from the canonical release closure.
- Independent historical review remains exactly 0 and is not inferred from internal review.

## Frozen identities

- Membership SHA-256: `ebc9d32f09857744841a0cf92699c41739b624ac4bd94c43798eb1f61e3b0dd3`
- Production database-state SHA-256: `31b7a7b675445e5758ffd68d64ff0f0cde83df1b0ea65f29835246deb2ae26ff`
- Authority bundle SHA-256: `e26bc9243c71226e6107162d15c44a0fa13d063ed7708bb12627e4ee8f13c54b`
- Schema head: `0033`
- Independent historical reviews: 0

The release package does not infer absence from P0, HOLD, researched-inconclusive or
unresolved geometry, and does not derive territorial practice intensity from archive,
document or voyage counts.
