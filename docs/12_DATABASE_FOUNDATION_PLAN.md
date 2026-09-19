# Database Foundation Plan

**Purpose:** execute the architecture migration safely without changing the meaning of canonical v0.6.1 data.


## Implementation checkpoint — 2026-09-19

DB Foundation v0.3 now includes executable migrations through `0011`, an automated v0.6.1 importer, and rollback-only non-Atlantic acceptance fixtures. A dry run against the canonical workbook passed the current count and special-case invariants. One workbook provenance issue was discovered: the exact Fredensborg SlaveVoyages voyage URL is referenced in voyage/ownership rows but absent from the 17-row Atlantic Sources registry. The importer creates an explicit source/version plus QC warning rather than silently substituting a related source.

Migration `0009` corrects one acceptance-test issue discovered before live execution: an unassigned P-level is now stored as NULL rather than forcing P0–P4. P0 remains an explicit unknown/no-usable-classification assessment.

Research-coverage provenance is kept separate from claim evidence through `RESEARCH_COVERAGE_SOURCE`, allowing RI/disputed assessments to cite exact reviewed sources without fabricating a positive practice claim.

The importer also validates all 18 tabs / 288 non-empty rows and preserves each row in raw ingest lineage on apply. The four global evidence sheets remain a blocking semantic-normalization task; raw preservation alone does not satisfy canonical-switch criteria.

The non-Atlantic acceptance SQL uses existing workbook cases and rolls back all fixture rows. Live PostgreSQL/PostGIS execution is still required before any canonical switch.

## 1. Foundation sequence

### Phase A — schema implementation

Create PostgreSQL/PostGIS migrations for, in dependency order:

1. database extensions, schemas, stable technical domains and temporal helper
2. evolving reference vocabularies
3. `SOURCE`, `SOURCE_VERSION`, optional `SOURCE_ASSET`
4. `ACTOR` + `ACTOR_NAME`
5. `SPATIAL_ENTITY`, `POLITY`, `SPATIAL_RELATION`
6. `GEOMETRY`
7. base `CLAIM`
8. `TERRITORIAL_PRACTICE_CLAIM`, `LEGAL_EVENT`, `ACTOR_ATTRIBUTE_CLAIM`
9. `CLAIM_SOURCE`
10. `INGEST_RUN`, optional `RAW_RECORD`, research-coverage audit table
11. `VOYAGE`
12. `VOYAGE_OWNER`, `VOYAGE_FINANCE`, `VOYAGE_STOP`
13. v0.6.1 crosswalk tables and publish views
14. nullable P-level correction (`0009`)
15. research-coverage source provenance (`0010`)
16. generic external-participation claims (`0011`) and non-Atlantic acceptance test

Do not create a standalone long-term `FINANCIER` identity table.

## 2. Migration of v0.6.1

Migrate the current eight-voyage controlled seed first.

Required checks:

- every non-empty workbook row from all 18 tabs is preserved in raw ingest lineage
- substantive global evidence sheets are either semantically normalized or explicitly block canonical cut-over
- all voyage IDs preserved
- raw documented versus imputed carrier values preserved
- every real legacy OWNER becomes exactly one intended ACTOR unless a documented normalization issue requires otherwise
- the legacy `Unknown owner — Orestes` placeholder becomes explicit missingness with no ACTOR
- every VOYAGE_OWNER relation preserved
- ownership share remains unknown where it was unknown
- every OWNER_EVIDENCE statement becomes one or more explicit claims without gaining unsupported meaning; legacy OWNER_EVIDENCE may split across actor-attribute and relationship claims
- exact source URLs/identifiers remain traceable to SOURCE_VERSION
- the pre-1776 `U.S.A.` anomaly remains a raw/source value rather than becoming a historical polity assertion
- Fredensborg unresolved disembarkation remains unresolved

## 3. Non-Atlantic schema tests

Do not approve the database merely because the Atlantic seed migrates cleanly.

Select existing project cases covering at least:

- one strong/systemic territorial-practice case
- one isolated/repeated-attestation case
- one disputed classification
- one researched-inconclusive case
- one legal event where law and practice must remain separate
- one BCE case with uncertain/broad dating
- one claim whose spatial target is not naturally a modern state
- one geometry that is approximate/proxy/unresolved

The schema passes only if these cases can be represented without collapsing categories or inventing precision.

## 4. Temporal acceptance tests

Verify:

- conversion between conventional BCE/CE labels and internal astronomical years
- 1 BCE -> 0 and 1 CE -> 1 with no public display of year zero
- selected-year containment queries
- claim/geometry interval overlap queries
- open-ended intervals
- broad/approximate dating with precision metadata
- no false exactness introduced during import

## 5. Spatial acceptance tests

Verify:

- PostGIS geometry uses an explicit SRID
- spatial indexes exist on production geometry columns
- a spatial entity can have multiple time-bounded geometries
- a port/place can change polity relation over time
- modern proxies remain marked as proxies
- unresolved historical geometry leaves neutral land visible

## 6. Provenance acceptance tests

For every migrated substantive claim, verify:

- stable claim ID
- exact source version
- locator where available
- supports/challenges role
- independence group where relevant
- raw/source-native value traceability for imported data
- no source version silently substituted

## 7. Publication acceptance tests

Verify:

- draft records do not appear in publish views
- reviewed/published records can be queried independently
- superseded records remain historically reconstructible
- one release manifest can identify the schema version, source versions, QC result and unresolved issues

## 8. Thin map proof

After database acceptance tests, build one minimal end-to-end slice:

1. static neutral land base
2. one selected-year historical geometry layer
3. one territorial-practice display layer
4. geometry-accuracy metadata
5. click a feature
6. retrieve claim detail from API
7. retrieve source/evidence detail

This test is successful when the map proves the data architecture rather than when the interface looks polished.

## 9. Stop conditions

Do not make the database canonical if:

- any v0.6.1 distinction is lost
- raw/imputed/documented fields are conflated
- an unsupported nationality/role is introduced
- a broad historical interval becomes falsely exact
- spatial control is back-projected from a later polity
- claim evidence cannot be traced to an exact source version
- disputed/RI states cannot be represented cleanly
- publication filtering is unreliable

## 10. Canonical switch criteria

The database can replace the workbook as canonical only after:

- schema migrations are versioned
- v0.6.1 migration reconciliation passes
- non-Atlantic tests pass
- temporal/spatial/provenance QC passes
- unresolved differences are documented
- a migration changelog/report exists
- a reproducible database backup/export is produced

Until then, v0.6.1 remains the canonical data release.
