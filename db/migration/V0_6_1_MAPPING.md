# v0.6.1 workbook → database migration mapping

**Source workbook:** `Historical_Slavery_Atlas_v0.6.1_Controlled_Atlantic_Ingestion.xlsx`  
**Canonical status:** the workbook remains canonical until migration reconciliation passes.  
**Target schema:** database-foundation draft-0.10.

## 1. Workbook sheets and migration role

| Workbook sheet | Migration role | Target |
|---|---|---|
| Coverage Matrix | project research-coverage metadata | `audit.research_coverage_assessment` |
| Regional Balance | derived project-management summary | recompute/report; do not treat as historical prevalence |
| Research Queue | project-management backlog | keep outside canonical historical tables |
| v0.4.7 Evidence | historical evidence rows | later/fixture migration to `CLAIM` + subtype + `CLAIM_SOURCE` |
| Method | methodology | governed by Project `.md` files, not migrated as historical rows |
| v0.4.8 Evidence | historical evidence rows | later/fixture migration to `CLAIM` + subtype + `CLAIM_SOURCE` |
| v0.4.9 Evidence | historical evidence rows | later/fixture migration to `CLAIM` + subtype + `CLAIM_SOURCE` |
| v0.5.0 Evidence | historical evidence rows | later/fixture migration to `CLAIM` + subtype + `CLAIM_SOURCE` |
| Atlantic Seed - Voyages | immediate foundation migration | `atlas.voyage`; normalized places later through `atlas.voyage_stop` |
| Atlantic Seed - Owners | immediate foundation migration | real identities → `atlas.actor`; names → `atlas.actor_name`; attribute claims separately |
| Atlantic Estimate Context | analytical context only | do not use to set P-level; migrate later only if needed for analytics |
| Atlantic Field Rules | methodology/data dictionary | Project docs/schema, not canonical historical rows |
| Atlantic Voyage Owners | immediate foundation migration | `atlas.voyage_owner` + relationship `CLAIM` + `CLAIM_SOURCE` |
| Atlantic Owner Evidence | immediate foundation migration | split by semantic target into actor-attribute or relationship claims |
| Atlantic Sources | immediate foundation migration | `atlas.source` + `atlas.source_version` (initially 1:1 is acceptable) |
| Atlantic Summary | QC expectations | reconciliation tests, not source-of-truth historical rows |
| Atlantic Schema | legacy schema description | migration documentation only |
| v0.6.1 Change Log | release provenance | release/changelog documentation |

## 2. Internal IDs versus source IDs

Database identities use generated UUIDs. Source-native and legacy project identifiers are preserved separately.

Examples:

- SlaveVoyages `Voyage ID = 90080` → `atlas.voyage.source_native_voyage_id = '90080'`; it is **not** the database primary key.
- `OWN-0006` → migration crosswalk → one `ACTOR` UUID.
- `SRC-013` → crosswalk → one `SOURCE` UUID plus one exact `SOURCE_VERSION` UUID.
- `E-003` may map to more than one claim if one legacy evidence row bundles more than one independently queryable assertion.

## 3. OWNER migration

Real people/organizations become `ACTOR` identities. Dataset/raw names are preserved in `ACTOR_NAME`.

The legacy row `OWN-0011 — Unknown owner — Orestes` is **not an actor**. It represents documented missingness. The target representation is:

- no ACTOR row;
- one `VOYAGE_OWNER` row for Orestes with `actor_id = NULL` and `relationship_status = 'missing_owner'`;
- one claim recording that the reviewed voyage record does not name an owner;
- source evidence attached through `CLAIM_SOURCE`.

This prevents an unknown value from becoming a fictional historical entity.

Expected real actors after migration: **11**.

## 4. VOYAGE_OWNER migration

Each legacy relationship gets an explicit target relation and claim.

- documented owner/co-owner/company relation → `actor_id` populated;
- missing owner placeholder → `actor_id = NULL`, `relationship_status = 'missing_owner'`;
- raw owner text preserved verbatim;
- ownership share remains NULL when the workbook says unknown;
- the relationship claim receives its exact source version(s).

Expected rows: **12 total**, of which **11 actor-linked** and **1 missing-owner**.

## 5. OWNER_EVIDENCE migration is semantic, not mechanical

Do **not** map every legacy OWNER_EVIDENCE row to `ACTOR_ATTRIBUTE_CLAIM`.

Examples:

- business base / nationality / corporate-jurisdiction assertions → `ACTOR_ATTRIBUTE_CLAIM`;
- ownership evidence → supports the claim attached to `VOYAGE_OWNER`;
- Fredensborg archival ship record → supports the Guinea Company/Fredensborg ownership relation claim;
- Orestes missing-owner evidence → supports the missing-owner voyage relation claim;
- one bundled legacy evidence row may split into multiple target claims when it contains distinct assertions.

`audit.v061_evidence_claim_map` is intentionally many-to-many so this split remains auditable.

## 6. SOURCE migration

Each `SRC-###` record must have a crosswalk.

For foundation migration it is acceptable to create one `SOURCE` and one `SOURCE_VERSION` per legacy source row, because the workbook often already describes an exact voyage page, article, authority record, catalogue item or methodology version. Later deduplication may consolidate conceptual sources **only if exact source-version provenance remains intact**.

Expected mapped legacy source rows: **17**.

## 7. Voyage invariants

- 8 voyages.
- documented and imputed flag/carrier fields remain separate.
- `36144 Westmoreland`: raw documented flag remains exactly `U.S.A.`; no later-state identity is inferred from it.
- `557 Orestes`: no documented flag; Spain/Uruguay remains an imputed carrier value and does not create an owner nationality.
- `35181 Fredensborg`: `disembarked_count` stays NULL and status remains `Needs source reconciliation` until the 235/~241 issue is resolved.
- `32359 Aurore`: French owner nationality is represented by an independent actor-attribute claim, not copied from the French vessel flag.

## 8. Coverage Matrix

The broad S/P/D/RI matrix is **research coverage metadata**, not territorial P0–P4 historical intensity.

Store it separately in `audit.research_coverage_assessment`. The legacy code is preserved verbatim while a normalized project coverage state may also be assigned. Coverage points remain project-management values only.

## 9. Migration completion rule

The migration is incomplete until:

1. every immediate-migration workbook row is crosswalked or explicitly excluded with a reason;
2. `002_v061_reconciliation.sql` passes;
3. selected non-Atlantic evidence rows can be represented without category collapse or false precision;
4. the migration report lists unresolved differences;
5. the workbook remains unchanged throughout validation.

## 10. Global evidence semantic migration — explicit row mapping

The four historical evidence sheets contain **36 substantive rows**:

- 14 Strong (`S`)
- 3 Provisional (`P`)
- 1 Disputed (`D`)
- 18 Researched-inconclusive (`RI`)
- 29 unique source URLs

The migration is intentionally explicit rather than classifier-driven.

### General rules

- Every row remains preserved in `raw.raw_record`.
- Every exact source URL becomes or resolves to an exact `SOURCE_VERSION`.
- `RI` rows create **research-coverage provenance only** through `RESEARCH_COVERAGE_SOURCE`; they do not create positive territorial-practice claims.
- `S`, `P`, and `D` rows may create one or more historical claims where the workbook text supports them.
- `practice_level` stays **NULL** for all migrated global evidence rows. P0–P4 requires a separate interpreted evidence-package assessment.
- All migrated historical claims remain `unpublished` until later public-release review.
- Compound workbook rows may split into multiple claims when they bundle analytically distinct assertions.
- A trade/network row does not become a territorial-practice claim merely because enslaved people moved through or from the named region.

### Positive / disputed rows

Row keys below use the importer's preserved **logical row sequence** (blank worksheet rows are skipped), matching `raw.raw_record.source_native_id`.


| Workbook row | Area | Legacy | Semantic target |
|---|---|---:|---|
| v0.4.7 Evidence!4 | Carolingian Empire | S | territorial practice: `slavery_enslavement` |
| v0.4.7 Evidence!5 | Anglo-Saxon England / Northern Europe | S | territorial practice: `slavery_enslavement`; preserve compound spatial scope and unresolved geometry |
| v0.4.7 Evidence!6 | Eastern Europe / Baltic–Black Sea networks | S | external participation: `trade_route` / slave-trade network; **not** territorial prevalence |
| v0.4.7 Evidence!7 | Ottoman Middle East | S | split: territorial `slavery_enslavement` + legal/suppression event |
| v0.4.7 Evidence!8 | Soviet Kazakhstan / Central Asia | S | territorial practice: `state_forced_labour` |
| v0.4.7 Evidence!9 | People's Republic of China, early decades | S | territorial practice: `penal_labour` |
| v0.4.7 Evidence!10 | DPRK | S | territorial practice: `state_forced_labour`; possible slavery language remains a qualification, not a second automatic classification |
| v0.4.7 Evidence!11 | Xinjiang / China | S | territorial practice candidate: `forced_labour`; retain contested/current-rights qualification |
| v0.4.7 Evidence!12 | Brazil | S | territorial practice: `debt_bondage` |
| v0.4.7 Evidence!13 | Peruvian Amazon | S | territorial practice: `debt_bondage` |
| v0.4.8 Evidence!4 | Nazi Germany and occupied Europe, 1933–1945 | S | territorial practice: `state_forced_labour` |
| v0.4.8 Evidence!5 | Europe and Central Asia, contemporary | S | territorial practice: `forced_labour` |
| v0.4.8 Evidence!6 | Iraq/Syria under ISIL, Yazidi population from 2014 | S | split: territorial `slavery_enslavement`, `sexual_slavery`, and external/network `slave_trade_network`; forced-labour wording retained in notes pending finer review |
| v0.4.9 Evidence!4 | Mycenaean Greece (Pylos/Knossos) | S | territorial practice: `slavery_enslavement`; preserve internally differentiated status note |
| v0.4.9 Evidence!5 | Anshan / Elam, c. 2130–2110 BCE | P | external participation: `slave_trade_network`; no territorial prevalence claim |
| v0.4.9 Evidence!8 | Vedic-period South Asia | P | territorial practice candidate: `other_servile_dependency`; terminology uncertainty preserved |
| v0.4.9 Evidence!10 | Shang China | D | split: secure `captive_taking_incorporation` context + disputed `slavery_enslavement` interpretation; no P-level |
| v0.5.0 Evidence!4 | Late Proto-Indo-European / Early Bronze Age Europe | P | territorial/regional practice candidate: `other_servile_dependency`; provisional linguistic reconstruction, no high-intensity inference |

### Researched-inconclusive rows

The following rows create no positive historical practice claim. Their exact source versions are attached to the matching research-coverage assessment through `audit.research_coverage_source`.

- v0.4.8 Evidence!7 — Prehistoric / Iron Age Southeast Asia
- v0.4.8 Evidence!8 — Early West/Central African societies, 1000–1 BCE
- v0.4.8 Evidence!9 — Early northeastern/eastern African societies, 1000–1 BCE
- v0.4.9 Evidence!6 — Middle Elam / Susa–Anshan
- v0.4.9 Evidence!7 — Indus Civilization
- v0.4.9 Evidence!9 — Longshan / Erlitou transition
- v0.4.9 Evidence!11 — Formative Mesoamerica
- v0.4.9 Evidence!12 — Proto-Oceanic / Lapita societies, 1000–1 BCE
- v0.5.0 Evidence!5 — Neolithic mainland/island Southeast Asia
- v0.5.0 Evidence!6 — Neolithic–Bronze Age Southeast Asia
- v0.5.0 Evidence!7 — Early West/Central African societies, 3000–2001 BCE
- v0.5.0 Evidence!8 — Early West/Central African societies, 2000–1001 BCE
- v0.5.0 Evidence!9 — Northeastern / eastern African societies, 3000–2001 BCE
- v0.5.0 Evidence!10 — Northeastern / eastern African societies, 2000–1001 BCE
- v0.5.0 Evidence!11 — Archaic / early Formative Americas
- v0.5.0 Evidence!12 — Early Formative Americas
- v0.5.0 Evidence!13 — Near Oceania before Lapita expansion
- v0.5.0 Evidence!14 — Lapita / Proto-Oceanic world, 2000–1001 BCE

### Temporal handling

Use the workbook period only as the normalized broad interval when the row itself provides no narrower defensible interval, and preserve the original wording/precision.

Astronomical-year conversions:

- 3000–2001 BCE → -2999 to -2000
- 2000–1001 BCE → -1999 to -1000
- 1000–1 BCE → -999 to 0
- 500–999 CE → 500 to 999
- 1800–1899 → 1800 to 1899
- 1900–present → 1900 to open-ended

Use narrower explicit row text when available:

- Anshan / Elam c. 2130–2110 BCE → -2129 to -2109
- Nazi Germany / occupied Europe 1933–1945 → 1933 to 1945
- ISIL/Yazidi evidence “from 2014” → 2014 to open-ended, subject to later source-specific refinement

### Source handling

The 36 rows contain 29 unique exact URLs. During migration:

1. preserve the URL exactly;
2. create/reuse one exact `SOURCE_VERSION` per unique reviewed URL;
3. keep migration-generated bibliographic labels clearly marked when the workbook does not contain enough metadata for a polished conceptual source record;
4. do not silently merge different URLs/versions;
5. add later bibliographic enrichment without changing the original evidence-row lineage.

### Completion check for this section

The global-evidence migration is complete only when:

- all 36 substantive rows are crosswalked;
- all 18 RI rows have coverage-source provenance and no fabricated positive claim;
- all 18 S/P/D rows are represented by the explicit semantic targets above;
- all 29 unique source URLs resolve to exact source-version records;
- all territorial claims have `practice_level IS NULL`;
- the Anshan/Elam row creates no territorial-practice claim;
- the Shang row preserves the distinction between secure captivity evidence and disputed slavery interpretation;
- all rows remain unpublished until later release review.

