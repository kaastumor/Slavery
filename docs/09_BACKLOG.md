# Backlog

## Completed foundation design / dry-run

Current implementation state: **DB Foundation v0.3, Docker Compose local runtime scaffold, the automated v0.6.1 importer, and rollback-only non-Atlantic acceptance fixtures are implemented. The importer dry-run against the canonical workbook passed. Live PostgreSQL/PostGIS execution, transactional import, and database-level execution of the schema/v0.6.1/non-Atlantic tests are still pending.**

Completed:

- draft-0.10 executable relational schema defined
- migrations `0001`–`0011` created
- ACTOR identity and actor-role migration model defined
- SPATIAL_ENTITY / POLITY / SPATIAL_RELATION / GEOMETRY defined
- universal CLAIM + specialized claims + CLAIM_SOURCE defined
- SOURCE / SOURCE_VERSION / SOURCE_ASSET + ingest lineage defined
- review/publication states and publish views defined
- separate research-coverage audit structure added
- automated v0.6.1 importer implemented
- migration 0009 makes P-level nullable until explicitly assessed, preserving the distinction between NULL and P0
- rollback-only non-Atlantic acceptance fixtures implemented from existing v0.6.1 evidence cases
- research-coverage source provenance bridge implemented so RI/disputed assessments retain exact reviewed sources without creating positive practice claims
- importer validates and raw-preserves all 18 workbook tabs / 288 non-empty rows on apply
- generic external-participation claim type implemented for non-voyage network evidence
- canonical workbook dry-run and semantic crosswalk validation passed
- Orestes missing-owner placeholder mapped to explicit missingness rather than a fake actor
- Fredensborg exact-voyage-URL source-registry gap preserved as an explicit QC warning

Still required before the database can be considered validated:

- execute the migrations against live PostgreSQL/PostGIS
- run schema and temporal/spatial smoke tests
- apply the importer transactionally
- reconcile database output against v0.6.1
- execute `003_non_atlantic_acceptance.sql` before declaring the schema fit for canonical migration

## Priority 0 — live database migration / reconciliation

- provision/run local PostgreSQL + PostGIS development database
- apply migrations `0001`–`0011` and schema smoke test
- run the validated v0.6.1 importer against the eight-voyage QA seed without changing the workbook
- migrate OWNER -> ACTOR
- migrate OWNER_EVIDENCE -> actor-attribute claims + claim-source links
- preserve raw versus normalized/imputed carrier fields
- reconcile every migrated record against v0.6.1
- produce migration QC report and unresolved-issues list
- keep v0.6.1 canonical until reconciliation passes

## Priority 2 — thin end-to-end map proof

Build a deliberately minimal technical prototype:

- neutral world land
- one or more historical geometries selected by year
- one territorial-practice claim
- visible geometry-accuracy status
- click feature -> claim/evidence/source details
- verify that missing data remains neutral land

This prototype validates architecture; it is not the production UI design.

## Priority 3 — participation normalization previously planned for v0.6.2

Resume only after database-foundation validation:

- migrate/add financiers as ACTOR + VOYAGE_FINANCE relationships
- normalize ports as SPATIAL_ENTITY records
- add time-bounded port/polity relationships
- reconcile Fredensborg 235 vs ~241 arrival/disembarkation issue
- standardize source versions/access dates
- verify all raw versus normalized carrier fields

## Priority 4 — territorial and legal model

- populate TERRITORIAL_PRACTICE_CLAIM under the universal claim model
- populate LEGAL_EVENT independently
- define stable practice-type controlled vocabulary and aliases
- connect all claims to exact SOURCE_VERSION records
- attach temporal/spatial precision fields
- test disputed and researched-inconclusive cases explicitly

## Priority 5 — geography production pipeline

- ingest/prepare Cliopatria historical polygons
- map source polity IDs / Wikidata IDs / Seshat IDs to SPATIAL_ENTITY/POLITY
- implement selected-year geometry resolution
- record approximate/proxy status
- keep neutral land outline beneath all historical layers
- add spatial indexes and geometry QC

## Priority 6 — deepen globally weak cells

Do not interpret the v0.5.0 first pass as complete historical coverage. Prioritize disputed, provisional and researched-inconclusive cells where better evidence is realistically recoverable.

Particular caution remains necessary for deep-history periods in the Americas, sub-Saharan Africa, Southeast Asia, Oceania and other areas where direct status evidence is sparse or difficult to distinguish from captivity, hierarchy or dependency.

## Priority 7 — production application/UI

After data semantics and the thin map proof are validated:

- timeline selector
- layer toggles
- evidence inspector
- source/provenance panel
- P0–P4 legend
- separate legal overlay
- separate participation network overlay
- coverage/uncertainty toggle
- geometry approximation indicator
- performance/caching strategy
- accessibility and mobile interaction design

## Deferred on purpose

- full Atlantic bulk import before the database migration and role/place/source semantics are stable
- any ranking of societies by raw number of surviving records
- automatic actor-nationality inference
- automatic P-level calculation from row counts
- choosing a permanent web framework/cloud provider before query patterns are proven
- making Excel a required release format

## Development / deployment environment

- [x] containerize Python migration/import tooling
- [x] include canonical v0.6.1 under immutable repository release path
- [x] add checksum migration ledger
- [x] add one-command Windows development bootstrap
- [x] add local backup/restore scripts
- [x] add GitHub Actions foundation CI
- [x] document local / CI / staging / production boundaries
- [ ] complete first live Docker/PostGIS bootstrap and archive output
- [x] establish private GitHub repository as the persistent engineering home
- [ ] select staging/production hosting provider only after query/API/map patterns are proven
- [ ] add provider-specific infrastructure-as-code after hosting decision
