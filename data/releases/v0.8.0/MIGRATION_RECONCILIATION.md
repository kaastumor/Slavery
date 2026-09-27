# v0.8.0 migration and reconciliation

- No schema migration is introduced by v0.8.0; live schema remains 0034.
- Canonical predecessor v0.7.0 remains immutable and is identified by exact manifest SHA-256.
- The D-115 authority is an explicit union of immutable v0.7.0 membership plus exact selected additions and deterministic source/spatial dependency closure.
- No reviewed-row query is used to discover release membership.
- Historical geometry is release membership only when separately reviewed and resolved; unresolved geometry remains explicit research state.
- Public serving promotion remains a separate compare-and-set release-channel operation after release and serving QC.

## Methodology references

- docs/02_METHOD_AND_ONTOLOGY.md
- docs/03_SOURCE_POLICY.md
- docs/04_DATA_MODEL.md
- docs/05_GEOGRAPHY_AND_MAP.md
- docs/07_QC_AND_VERSIONING.md
- docs/08_DECISIONS_LOG.md — D-108, D-114 and D-115
- docs/11_SYSTEM_ARCHITECTURE.md
- release/selections/v0.8.0-expansion-02.json
