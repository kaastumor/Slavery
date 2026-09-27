# v0.8.1 migration and reconciliation

- No schema migration is introduced; live schema remains 0034.
- Canonical predecessor v0.8.0 remains immutable.
- v0.8.1 performs an explicit one-for-one geometry and geometry-source-version membership substitution under D-117.
- No claim membership or claim interpretation changes.
- The public serving channel remains on v0.8.0-public-mvp-v2 until a separate v0.8.1 render-asset/materialization gate passes.

## Methodology references

- docs/02_METHOD_AND_ONTOLOGY.md
- docs/03_SOURCE_POLICY.md
- docs/04_DATA_MODEL.md
- docs/05_GEOGRAPHY_AND_MAP.md
- docs/07_QC_AND_VERSIONING.md
- docs/08_DECISIONS_LOG.md — D-116 and D-117
- docs/11_SYSTEM_ARCHITECTURE.md
- release/selections/v0.8.1-rome-geometry-correction.json
- data/research/geometry_reviews/rome_early_principate_ad14_awmc_v1.json
