# Current Project Status

**Status date:** 2026-09-19  
**Canonical data version:** v0.6.1  
**Architecture schema draft:** draft-0.11

## 1. What has been completed

### Global research balance

The project deliberately researched the non-Atlantic world before allowing the much denser Atlantic archive to dominate the map.

The v0.5.0 global audit contains 11 broad regions × 9 broad periods = 99 region-period cells. Every cell received at least one targeted pass.

Current first-pass audit:

- Strong: 57
- Provisional: 18
- Disputed: 4
- Researched-Inconclusive: 20
- Not researched: 0

This is a project-management coverage measure only. It is not a slavery-prevalence metric and does not mean every polity within each cell has been researched.

### Atlantic controlled ingestion

v0.6.1 opened the Atlantic gate cautiously after the global first pass.

Implemented in the canonical workbook:

- 8-voyage multi-carrier QA seed
- voyage-level documented versus imputed carrier fields
- normalized OWNER/entity records
- many-to-many VOYAGE_OWNER links
- claim-level OWNER_EVIDENCE
- SOURCE registry
- separate corporate jurisdiction, residence, business base, political/legal affiliation, and owner nationality concepts
- preservation of unresolved values rather than forced completion
- preservation of a pre-1776 "U.S.A." carrier anomaly as raw source data rather than back-projecting the later United States

The seed deliberately includes cases that test difficult attribution problems: multiple owners, missing owners, independently enriched owner identity, company ownership, documented versus imputed flags, and anachronistic source coding.

### Known unresolved item

Fredensborg (voyage 35181): published reconstructions reviewed in the project differ on the St. Croix arrival/disembarkation figure (235 versus about 241 depending on definition/timing). The value should remain unresolved until reconciled against the voyage record and/or archive.

## 2. Architecture foundation adopted for migration planning

Before expanding the previously planned v0.6.2 participation tables, the project has formalized a stronger database target.

Approved migration-target concepts:

- PostgreSQL + PostGIS as the future canonical research store after migration validation
- universal `CLAIM` identity with enforceable `CLAIM_SOURCE` links and claimable relationship rows
- `ACTOR` identity separated from owner/financier/insurer/etc. roles
- generated UUID internal identities with source-native IDs preserved separately
- missing/unknown values represented as status/missingness rather than fake entities
- `SPATIAL_ENTITY` as the generic geography target; `POLITY` is a specialization
- time-bounded spatial relations rather than timeless port-to-polity links
- astronomical signed integer years internally, with BCE/CE conversion in the UI
- explicit temporal precision and queryable year ranges
- `SOURCE` / `SOURCE_VERSION` / optional `SOURCE_ASSET`
- raw/staging/canonical/publish/audit logical layers
- review/publication boundary before data reach the web map
- separate research-coverage assessment structure for S/P/D/RI audit data
- MapLibre GL JS as preferred map client; delivery format chosen by layer size/complexity
- reproducible Docker Compose local database scaffold for runtime validation (development convenience, not production lock-in)

These are architecture decisions only. They do **not** change the canonical meaning or contents of v0.6.1 until a migration is built and reconciled.

## 3. Geography state

The intended production geography backbone remains Cliopatria / Seshat Global History Databank historical political geometry, with time-bounded polygons and identifiers where available.

Resolver hierarchy:

1. Exact Cliopatria polygon valid for selected year
2. Better specialist historical geometry if available
3. Nearest defensible historical geometry, explicitly marked approximate
4. Modern geographic proxy if necessary, explicitly marked proxy
5. No political polygon; neutral world land remains visible

The target architecture now generalizes geometry to `SPATIAL_ENTITY`, allowing polities, regions, cities, ports and sites to be represented without forcing every geographic object to be a state.

## 4. Source families already incorporated into the research strategy

Examples include:

- Seshat / legacy Equinox variables
- Cliopatria historical geometry
- CDLI and ORACC
- Papyri.info and Trismegistos
- Princeton Geniza Project
- CALD / Islamic Law Materialized
- Timbuktu manuscript resources
- ESTA and Indian Ocean slave-trade datasets
- SlaveVoyages
- Legacies of British Slavery
- Freedom on the Move
- regional historical databases for China, Korea, South Asia and other areas
- VOC / Batavia / Cochin archival material
- Rosarchive
- ILO / OHCHR and other modern institutional sources where relevant

Important Seshat clarification: detailed slavery variables used in prior work are legacy/Equinox data and must retain that dataset/version identity rather than being silently relabelled as current Polaris data.

## 5. Database-foundation implementation status

Completed in DB Foundation v0.3:

- executable PostgreSQL/PostGIS migrations through `0012`, including immutable release membership
- read-only automated parser for the canonical v0.6.1 workbook
- full raw preservation plan for all 18 workbook tabs / 288 non-empty rows on database apply
- dry-run migration validation against the actual workbook
- 8 voyages, 11 real actors, 12 voyage-owner/status relations, 17 registered sources, 11 legacy owner-evidence IDs and all 99 coverage cells validated
- semantic evidence split produces 17 evidence-to-claim mappings from 11 legacy evidence rows
- Orestes remains explicit missingness rather than a fabricated actor
- Westmoreland retains raw `U.S.A.` carrier coding
- Fredensborg unresolved disembarkation remains unresolved
- one source-registry gap identified: Fredensborg's exact SlaveVoyages voyage URL occurs in canonical rows but not in the 17-row Atlantic Sources registry; the importer preserves the URL as an explicit migration-generated source/version and QC warning rather than substituting another source
- migration `0009` distinguishes an unassigned P-level (`NULL`) from explicit P0, preventing disputed/RI evidence from being coerced into an intensity classification
- rollback-only non-Atlantic acceptance test `003_non_atlantic_acceptance.sql` now covers strong/direct evidence, disputed classification, RI coverage, law/practice separation, BCE uncertainty, a non-state spatial target, unresolved geometry, and publish filtering
- `RESEARCH_COVERAGE_SOURCE` now links coverage/RI assessments to exact source versions without turning those sources into practice-claim evidence
- generic `EXTERNAL_PARTICIPATION_CLAIM` now represents non-voyage network participation without contaminating territorial practice
- the four global evidence sheets are raw-preserved but remain a blocking semantic-migration item before the database can become canonical

The dry-run passed. Live PostgreSQL/PostGIS execution remains pending because the current execution environment has neither Docker nor PostgreSQL. The workbook therefore remains canonical.

## 6. Immediate next milestone

**Architecture/database foundation before further bulk data growth.**

Next actions:

1. run the exact canonical v0.6.1 artifact through the live PostgreSQL/PostGIS import/reconciliation path after migrations through `0012`
2. run schema smoke tests and fix any runtime issues
3. migrate the v0.6.1 controlled seed without altering the workbook
4. reconcile all migrated values and meanings against v0.6.1
5. execute the implemented non-Atlantic acceptance fixtures against live PostgreSQL/PostGIS
6. complete and review semantic migration of the four global evidence sheets (`v0.4.7 Evidence`–`v0.5.0 Evidence`)
7. build a thin end-to-end map proof with selected-year geometry and evidence click-through

The previously planned participation-normalization work (financiers, ports, source cleanup and Fredensborg reconciliation) remains valid but is deferred until the database foundation passes these tests.

## Development environment checkpoint — v0.4

A reproducible repository/development environment has now been prepared around DB Foundation v0.3:

- local PostgreSQL/PostGIS and Python tooling run in Docker;
- canonical v0.6.1 is identified by immutable release metadata/checksum under `data/releases/v0.6.1/`; the binary remains an external artifact;
- `atlas_meta.schema_migration` records migration filenames/checksums and rejects edited applied migrations;
- one-command Windows bootstrap and repeatable verification scripts exist;
- local backup/restore scripts exist;
- GitHub Actions CI runs migrations, importer, reconciliation and non-Atlantic tests from a clean database;
- optional VS Code Dev Container support exists;
- staging/production requirements are documented but no hosting provider is locked.

This environment has been statically/offline validated here but still requires its first live Docker/PostGIS run on an external machine.

The development environment also pins the exact canonical v0.6.1 workbook SHA-256 (`0a38e4eb6f63c3bb4ce9543be379605d24dd9ff1c1cea1e0a49c0c3db7ba17d4`). The importer rejects a different file presented as v0.6.1.
