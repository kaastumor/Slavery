# Current Project Status

**Status date:** 2026-09-19  
**Canonical data version:** v0.6.1  
**Working research database:** PostgreSQL + PostGIS, migrations through `0011`  
**Current public preview:** `mvp-preview-ancient-v1` (non-canonical)

## 1. Project position

The Historical Slavery Atlas has moved beyond database-foundation prototyping into a working **research → review → publication → MapLibre** pipeline.

The canonical historical data release remains the preserved v0.6.1 workbook. The live PostgreSQL/PostGIS database is the working normalized research system, but reviewed database growth does not automatically redefine the canonical release.

The project now explicitly defines itself as an **evidence-synthesis and data-curation project**. It collects and digests existing historical evidence and specialist scholarship; it is not intended to act as an independent historical research institute.

## 2. Current live research database

Current verified database state:

- 34 territorial-practice claims
- 11 published claims in the current non-canonical preview
- 23 reviewed but unpublished claims
- 30 spatial entities
- 60 geometry records
- 0 invalid PostGIS geometries
- 71 exact source-version records
- latest public preview release: `mvp-preview-ancient-v1`

The public API is release-gated and does not expose arbitrary reviewed research rows.

## 3. Global research balance

The project deliberately researched the non-Atlantic world before allowing the much denser Atlantic archive to dominate the map.

The v0.5.0 global audit contains 11 broad regions × 9 broad periods = 99 region-period cells. Every cell received at least one targeted pass.

First-pass audit:

- Strong: 57
- Provisional: 18
- Disputed: 4
- Researched-Inconclusive: 20
- Not researched: 0

This is a project-management coverage measure only. It is not a slavery-prevalence metric and does not mean every polity within each cell has been researched.

## 4. Canonical workbook and Atlantic controlled ingestion

v0.6.1 remains preserved as the canonical workbook release.

It contains:

- the controlled 8-voyage multi-carrier Atlantic QA seed
- voyage-level documented versus imputed carrier fields
- normalized owner/entity records
- many-to-many voyage-owner links
- claim-level owner evidence
- source registry
- separate corporate jurisdiction, residence, business base, political/legal affiliation and owner-nationality concepts
- unresolved values preserved rather than forced complete

The workbook must not be overwritten by database research activity.

The previously known Fredensborg disembarkation discrepancy remains a legacy reconciliation issue and is not allowed to block unrelated historical research.

## 5. Database and application foundation

Implemented and live:

- PostgreSQL + PostGIS working research database
- repository migrations through `0011`
- universal `CLAIM` identity
- claim-specific `CLAIM_SOURCE`
- `SOURCE` / `SOURCE_VERSION` separation
- generic `SPATIAL_ENTITY`
- time-bounded historical geometry
- nullable P-level distinct from P0
- research/publication separation
- immutable preview-release membership
- MapLibre GL JS web application in `web/`
- release-gated `atlas-data` API
- direct research-case ingestion tooling
- publication-gate tooling
- GitHub CI for foundation/database checks and web builds

The old throwaway `atlas-mvp` endpoint has been retired.

## 6. Current ancient research expansion

### Published preview slice

`mvp-preview-ancient-v1` is an explicitly non-canonical end-to-end product-validation release containing 11 ancient claims across 8 spatial targets.

It exists to prove the release pipeline and map behavior. It does not replace v0.6.1 as the canonical historical data release.

### Reviewed unpublished expansion

Two subsequent ancient research batches have been added as reviewed research without changing the public preview.

#### Ancient expansion 01

Includes:

- Ur III Garshana
- Old Assyrian Kanesh/Kültepe
- Hittite slavery
- Hittite servile dependency
- Neo-Babylonian slavery
- Neo-Babylonian temple dependency
- Western Han slavery
- Qin penal labour

#### Ancient expansion 02

Includes:

- Middle Ganga valley slavery
- Mauryan slavery classification
- Baekje 369 war-captive enslavement
- Silla Village Register slavery

These remain unpublished pending later release decisions.

## 7. Current methodology reset

The core methodology now follows these rules:

1. No usable historical claim for a place/time means **unknown**, not absence.
2. Primary/source-native evidence anchors bounded facts.
3. Specialist historical scholarship is normally the interpretive backbone for classification, prevalence, continuity and structural significance.
4. Conflicting sources do not automatically create a `disputed` or blank atlas designation.
5. Source conflicts are synthesized using ordinary historical source criticism and the treatment found in specialist historiography.
6. Contrary evidence remains linked through `supports`, `challenges`, `qualifies` and `context`.
7. `disputed` is reserved for genuinely unresolved material disagreement in credible specialist scholarship.
8. The atlas synthesizes existing scholarship; it does not attempt to become the scholarly authority that independently settles major historical controversies.

The Mauryan record is an explicit re-review candidate under this revised rule: the current reviewed/unpublished disputed classification should not be published until its indigenous legal/epigraphic evidence and specialist historiography have been reassessed under the new synthesis standard.

## 8. Geography state

The production geography backbone remains Cliopatria / Seshat Global History Databank historical political geometry where appropriate.

Resolver hierarchy:

1. Exact Cliopatria polygon valid for selected year
2. Better specialist historical geometry if available
3. Nearest defensible historical geometry, explicitly marked approximate
4. Modern geographic proxy if necessary, explicitly marked proxy
5. Explicit unresolved geometry / no political polygon; neutral world land remains visible

Evidence geometry is resolved independently from historical classification.

Narrow evidence targets must not be enlarged to whole-polity polygons merely because such polygons are convenient.

## 9. Current source strategy

Important source families include:

- specialist historical monographs and journal literature
- source editions and translations
- inscriptions and legal/administrative corpora
- CDLI and ORACC
- Papyri.info and Trismegistos
- Princeton Geniza Project
- CALD / Islamic Law Materialized
- Timbuktu manuscript resources
- Seshat / legacy Equinox variables
- Cliopatria historical geometry
- Indian Ocean and Atlantic datasets
- SlaveVoyages
- Legacies of British Slavery
- Freedom on the Move
- regional historical databases for China, Korea, South Asia and other areas
- modern institutional sources such as ILO/OHCHR where chronologically relevant

Detailed Seshat slavery variables previously used remain legacy/Equinox data and must retain that dataset/version identity rather than being relabelled as current Polaris data.

## 10. Immediate next milestone

The next work should prioritize **methodology-consistent historical synthesis**, not infrastructure expansion.

Immediate actions:

1. audit the recently reviewed ancient claims against the revised conflict-resolution rule
2. correct the Mauryan claim before it can enter a public release
3. ensure future research batches identify the relevant specialist historiography before broad classification
4. continue globally balanced ancient research, with Africa and Arabia as strong next candidates
5. keep new research reviewed/unpublished until QC and deliberate release selection
6. cut a new public preview only when a coherent reviewed slice is ready

Vector-tile optimization, additional hosting infrastructure and large Atlantic bulk ingestion remain secondary until data volume or product use actually requires them.
