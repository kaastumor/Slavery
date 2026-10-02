# v0.8.2 migration and reconciliation

- No schema migration; governed schema remains 0034.
- v0.8.1 and all previous canonical/serving artifacts are preserved.
- Exact 17 additions extend 75 predecessor claims. Two previously committed evidence-locus augmentations are frozen without changing historical interpretation.
- D-121 holds apply individually to three geometry IDs; they do not remove their cases.
- Canonical registration remains channel-neutral; immutable serving registration, deployment and compare-and-set cutover are separate verified steps. Rollback target is v0.8.1-public-mvp-v2.

## Methodology references

- docs/02_METHOD_AND_ONTOLOGY.md
- docs/03_SOURCE_POLICY.md
- docs/04_DATA_MODEL.md
- docs/05_GEOGRAPHY_AND_MAP.md
- docs/07_QC_AND_VERSIONING.md
- docs/08_DECISIONS_LOG.md - D-109, D-117, D-121, D-124, D-125
- docs/11_SYSTEM_ARCHITECTURE.md
- release/selections/v0.8.2-requested-corpus.json
- data/research/geometry_reviews/v082_exact_api_source_bindings.json.gz
- data/research/geometry_reviews/v082_non_api_source_bindings.json
