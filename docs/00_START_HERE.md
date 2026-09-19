# Historical Slavery Atlas — Start Here

## Project purpose

Build an interactive global historical atlas of slavery, slavery-like systems, coerced labour, servile dependency, and participation in slave-trading networks from roughly 3000 BCE to the present.

The atlas must not reduce the question to a binary "slavery / no slavery" map. It must represent separate dimensions of evidence and keep uncertainty visible.

## Canonical current state

- Current canonical **data** release: `Historical_Slavery_Atlas_v0.6.1_Controlled_Atlantic_Ingestion.xlsx`
- Global research baseline: v0.5.0
- All 99 broad region-period cells have received at least one targeted research pass.
- v0.5.0 audit: 57 Strong, 18 Provisional, 4 Disputed, 20 Researched-Inconclusive, 0 unresearched.
- Atlantic bulk ingestion was deliberately held back until this global first-pass baseline existed.
- v0.6.1 contains a controlled 8-voyage Atlantic seed used to test attribution and schema rules.
- Claim-level owner evidence, a source registry, normalized owner/entity records, and explicit many-to-many voyage-owner relationships are implemented in v0.6.1.
- The project is now in an **architecture-foundation phase** before further bulk ingestion.
- `schema_draft.yaml` draft-0.10 and `11_SYSTEM_ARCHITECTURE.md` describe the migration target; they do not retroactively alter v0.6.1.
- PostgreSQL + PostGIS is the target canonical database after a validated migration.
- DB Foundation v0.3 contains migrations 0001–0011, the v0.6.1 importer, and rollback-only non-Atlantic acceptance fixtures; all 18 workbook tabs are now raw-preserved by the importer; the four global evidence sheets still require reviewed semantic normalization before any canonical switch. Live PostgreSQL/PostGIS execution is also still pending, so the package remains a migration prototype rather than canonical data.

## Non-negotiable principles

1. Archive density is not prevalence.
2. Research coverage is not historical prevalence.
3. Unknown or inconclusive is not evidence of absence.
4. A voyage, owner, financier, port, flag, or company connection is external/network participation unless separate evidence supports territorial practice.
5. Vessel flag does not determine actor/owner nationality.
6. Nationality/political identity must be independently evidenced. Never infer it from flag, port, residence, business base, surname, or company jurisdiction.
7. Law and practice are separate. Abolition or prohibition does not prove disappearance of practice; recognition of slavery does not quantify prevalence.
8. Forced labour, penal labour, debt bondage, servitude, slavery/enslavement, captive-taking, and trafficking must remain distinguishable categories.
9. Primary sources and secondary scholarship have different roles; neither is automatically superior for every claim.
10. The neutral world land outline is always visible. Missing political or evidence data must never visually become ocean or imply absence.
11. Raw/source-native values must remain traceable when data are normalized.
12. Draft architecture/schema changes do not become canonical data until migration and QC are explicitly completed.

## Map layers that must stay separate

- Territorial practice intensity: P0–P4
- Legal/status layer
- External participation networks: voyages, actors, finance, ports, companies
- Research coverage / confidence
- Historical political/other geometry
- Neutral land base layer

## Practice levels

- P0 — unknown / no usable classification
- P1 — isolated direct attestation
- P2 — repeated independent attestations
- P3 — systemic or institutional practice strongly supported
- P4 — widespread or structurally major practice supported by scholarship

Source count never mechanically sets a P-level.

## Before changing data or schema

Read:

1. `01_PROJECT_STATUS.md`
2. `02_METHOD_AND_ONTOLOGY.md`
3. `03_SOURCE_POLICY.md`
4. `04_DATA_MODEL.md`
5. `05_GEOGRAPHY_AND_MAP.md`
6. `08_DECISIONS_LOG.md`
7. `11_SYSTEM_ARCHITECTURE.md`
8. `13_DATABASE_SCHEMA_IMPLEMENTATION.md`
9. `14_LOCAL_DATABASE_DEVELOPMENT.md`
10. `15_DEVELOPMENT_ENVIRONMENT.md`

Then record any schema or methodology change in the decision log and changelog before treating it as canonical.
