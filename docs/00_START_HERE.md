# Historical Slavery Atlas — Start Here

## Project purpose

Build an interactive global historical atlas of slavery, slavery-like systems, coerced labour, servile dependency, and participation in slave-trading networks from roughly 3000 BCE to the present.

The atlas is an **evidence-synthesis and data-curation project**. It collects, normalizes, reconciles and digests existing historical evidence and specialist scholarship into transparent spatial-temporal claims.

It is not intended to function as an independent historical research institute or to generate novel historical theories where specialist scholarship already exists.

The atlas must not reduce the question to a binary "slavery / no slavery" map. It must represent separate dimensions of evidence and keep uncertainty visible.

## Core interpretive model

The preferred evidentiary chain is:

```
primary / source-native evidence
        +
specialist historical scholarship
        ↓
best-supported atlas designation
        ↓
claim + provenance + uncertainty + contrary evidence
```

Primary evidence is especially valuable for bounded facts such as transactions, laws, inscriptions, terminology, dates, locations and recorded events.

Specialist scholarship is normally the interpretive backbone for classification, prevalence, continuity, structural significance and difficult historical terminology.

Conflicting sources do not automatically produce a blank or disputed designation. The atlas follows ordinary historical source criticism and the treatment of the problem in relevant specialist scholarship.

Use `disputed` only when a material disagreement remains genuinely unresolved in credible specialist historiography.

## Unknown is not absence

If no defensible territorial-practice claim exists for a place/time, the atlas state is **unknown**.

Unknown never means:

- slavery was absent
- coercion was absent
- the territory was free
- surviving evidence does not exist
- the project searched exhaustively

Research coverage separately records whether the area is unresearched, partly researched, reviewed, disputed, or researched-inconclusive.

A missing claim must never be rendered as a historical negative.

## Canonical current state

- Current canonical **data** release: `Historical_Slavery_Atlas_v0.6.1_Controlled_Atlantic_Ingestion.xlsx`
- Global research baseline: v0.5.0
- All 99 broad region-period cells received at least one targeted first-pass research review.
- Atlantic bulk ingestion was deliberately held back until this global first-pass baseline existed.
- PostgreSQL + PostGIS is now the working normalized research system, using repository migrations through `0011`.
- The canonical v0.6.1 workbook remains preserved and has not been overwritten.
- The repository contains a real MapLibre web MVP and a release-gated API.
- `mvp-preview-ancient-v1` is an explicitly **non-canonical** public preview used to validate the end-to-end product path.
- New manual research enters the normalized relational model directly and remains unpublished until it passes review and publication gates.
- Research batches may expand reviewed database content without automatically changing the public preview or canonical data release.

## Non-negotiable principles

1. The atlas synthesizes existing evidence and scholarship; it does not present itself as an original historical research center.
2. Archive density is not prevalence.
3. Research coverage is not historical prevalence.
4. Unknown or inconclusive is not evidence of absence.
5. If no defensible historical claim exists, leave the state unknown rather than inventing a negative.
6. Conflicting sources do not automatically mean `disputed`; use historical source criticism and specialist historiography to reach the best-supported designation.
7. Preserve contrary evidence even when the atlas reaches a working designation.
8. Use `disputed` only when a material historiographical disagreement remains unresolved after synthesis.
9. A voyage, owner, financier, port, flag, or company connection is external/network participation unless separate evidence supports territorial practice.
10. Vessel flag does not determine actor/owner nationality.
11. Nationality/political identity must be independently evidenced. Never infer it from flag, port, residence, business base, surname, or company jurisdiction.
12. Law and practice are separate. Legal recognition can establish a category or legal institution but does not by itself quantify prevalence. Abolition or prohibition does not prove disappearance of practice.
13. Forced labour, penal labour, debt bondage, servitude, slavery/enslavement, captive-taking, and trafficking must remain distinguishable categories.
14. Primary sources and secondary scholarship have different evidentiary roles; neither is automatically superior for every claim.
15. Broad claims about classification, prevalence and structural importance should normally follow specialist historical scholarship.
16. The neutral world land outline is always visible. Missing political or evidence data must never visually become ocean or imply absence.
17. Raw/source-native values must remain traceable when data are normalized.
18. Draft research, reviewed research, public previews and canonical releases are separate states.
19. Draft architecture/schema changes do not become canonical data until migration and QC are explicitly completed.

## Map layers that must stay separate

- Territorial practice intensity: P0–P4
- Legal/status layer
- External participation networks: voyages, actors, finance, ports, companies
- Research coverage / confidence
- Historical political/other geometry
- Neutral land base layer

## Practice levels

- P0 — explicit reviewed assessment that no usable P1–P4 classification is currently available; never absence
- P1 — isolated direct attestation
- P2 — recurrent/repeatedly evidenced practice
- P3 — systemic or institutional practice strongly supported
- P4 — widespread or structurally major practice supported by scholarship

Source count never mechanically sets a P-level.

No claim is different from P0: if no defensible territorial-practice claim exists, the atlas simply remains unknown for that place/time.

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
11. `17_SOURCE_EVIDENCE_LIFECYCLE.md`
12. `19_PIPELINE_ARCHITECTURE.md`

Then record any schema or methodology change in the decision log before treating it as canonical methodology.
