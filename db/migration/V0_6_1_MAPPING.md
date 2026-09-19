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
