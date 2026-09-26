# v0.7.0 migration and reconciliation

- Canonical predecessor v0.6.1 is retained by immutable filename and SHA-256 and is not rewritten.
- Gate 0 reconciled repository and live migration history through the schema line that later advanced to 0033.
- Gate 1 reproduced v0.6.1 semantics in PostgreSQL/PostGIS while preserving raw/source-native values and unresolved cases.
- Gate 2 represented the frozen v3 research package losslessly without inventing target-to-claim bridges, spatial links or independent review.
- Gate 3 froze exact governed membership, composite object digests and database-state identity, then restored the closure into a fresh migrated PostgreSQL/PostGIS database.
- Source-native v0.6.1 lineage remains reconstructible through the immutable predecessor artifact plus Gate-1 ingest/reconciliation tooling; authority-state.json does not replace that predecessor artifact.
- The Supabase Free plan did not provide verified managed backup/PITR inventory to the project probe; the proven recovery guarantee is preservation-grade logical recovery of the governed research closure, not physical cluster/PITR recovery.

## Methodology references

- docs/02_METHOD_AND_ONTOLOGY.md
- docs/03_SOURCE_POLICY.md
- docs/04_DATA_MODEL.md
- docs/05_GEOGRAPHY_AND_MAP.md
- docs/07_QC_AND_VERSIONING.md
- docs/08_DECISIONS_LOG.md — D-108 and D-109
- docs/11_SYSTEM_ARCHITECTURE.md
- reviews/db-canonicalization/gate3/GATE3_AUTHORITY_REVIEW.md
