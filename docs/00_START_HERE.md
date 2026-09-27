# Historical Slavery Atlas — Start Here

## Project purpose

Build an interactive global historical atlas of slavery, slavery-like systems, coerced labour, servile dependency, and participation in slave-trading networks from roughly 3000 BCE to the present.

The atlas is an **evidence-synthesis and data-curation project**. It collects, normalizes, reconciles and digests existing historical evidence and specialist scholarship into transparent spatial-temporal claims.

After R1 and EXP-02, the best-supported project form is a **portable reviewed evidence core with replaceable Atlas/map/table views**. The Atlas remains the project identity and a valid geographic inspection surface, but the web application does not own historical truth.

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

- Current canonical historical data release: **v0.8.1**, preserved immutably in
  `data/releases/v0.8.1/`.
- Current public serving materialization: **v0.8.1-public-mvp-v1**, selected through
  `audit.release_channel.public_mvp_preview`.
- Canonical current research authority remains governed PostgreSQL/PostGIS state;
  release membership is explicit and never inferred from all reviewed rows.
- Repository/live schema head remains `0034`.
- v0.8.1 contains 75 claims, 11 actors, 50 spatial entities, 46 reviewed/resolved
  historical geometries, 8 voyages, 99 coverage assessments, 294 exact source versions
  and 26 research-target results.
- The public territorial-practice adapter renders 53 claims across 48 places. Missing
  geometry remains an explicit unresolved state and never means historical absence.
- D-116 separates raw/source historical geometry from public render geometry. Public
  polygon assets use the canonical Natural Earth land fabric; raw geometry is preserved.
- D-117 replaces only the Roman 14–22 CE slice with the reviewed AWMC-derived A.D. 14
  specialist geometry. Earlier Roman slices are not silently changed.
- D-118 completes the v0.8.1 serving cutover. Payload SHA-256:
  `56cb29dfd8fcb968d08ae3a7fa0bd8b11af44e15c03facc7ee2c6b27cae49347`.
- Independent historical review remains **0**.
- The v0.6.1 workbook and all later canonical releases remain immutable lineage.
- Current expansion priority is owned by root `BACKLOG.md` / issue #332.

## Active-continuity rule

Elapsed time is not treated as the scarce resource. The scarce resources are evidence quality, focus and project complexity.

A completed horizon should not automatically return the project to idle. Unless genuinely blocked, select one next bounded experiment by expected information gain, preregister it, and continue. Stopping/simplifying/rejecting remain valid evidence outcomes, not default scheduling policy.

Current active priority/mode: see root `BACKLOG.md`.

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

## Analytical layers that must stay separate

- Territorial-practice claims, represented through the post-M1 multidimensional model
- Legal/status layer
- External participation networks: voyages, actors, finance, ports, companies
- Research stage / classification outcome
- Historical political/other geometry
- Neutral land base layer

Territorial practice must not be reduced to one universal intensity score. The target model keeps evidence pattern, interpretive basis, occurrence pattern, institutionalization, prevalence scope, structural significance, temporal applicability/precision and spatial locus/inference extent separable where supported.

## Legacy P0–P4 compatibility

P0–P4 remains only for reproducing and interpreting historical releases that already use it.

- P0 — explicit reviewed legacy assessment that no usable P1–P4 classification was assigned; never absence
- P1–P4 — retain their historical release meanings
- NULL/no claim — remains distinct from P0

Do not infer new post-M1 dimensions mechanically from a legacy P-level, and do not derive a new P-level mechanically from the post-M1 dimensions.

Source count never mechanically sets a P-level.

If no defensible territorial-practice claim exists, the atlas remains unknown for that place/time.

## Before starting work

Read:
1. `23_PROJECT_CHARTER.md`
2. repository-root `BACKLOG.md`
3. `24_WAY_OF_WORKING.md`
4. `25_PROJECT_HEALTH.md`

Then inspect current `main`, open issues/PRs and current CI. For scheduled autonomous work, `automation/hourly-worker.md` is binding.

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
13. `20_CURRENT_HANDOFF.md` — pointer to canonical live repository state; it is deliberately not a second mutable execution narrative

Then record any schema or methodology change in the decision log before treating it as canonical methodology.
