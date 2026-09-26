# Historical Slavery Atlas — Backlog

**Updated:** 2026-09-26  
**Role:** canonical execution queue only; assumptions/risks/value evidence live in `docs/25_PROJECT_HEALTH.md`  
**Canonical research authority:** PostgreSQL/PostGIS, explicit governed membership under D-109  
**Canonical historical data release:** `v0.7.0`  
**Current public serving adapter:** `v0.7.0-public-mvp-v1` → canonical source `v0.7.0`  
**Public Atlas:** `https://kaastumor.github.io/Slavery/`  
**Preserved R1 technical candidate:** `r1-candidate.html` (non-canonical historical project artifact)

This file answers **what is justified to work on next**.

---

# CURRENT MODE — CONSOLIDATION / POST-CUTOVER REVIEW

**Parent canonicalization gate:** #300  
**Gate 0:** **PASS — MIGRATION_HISTORY_RECONCILED**  
**Gate 1:** **PASS — V061_DB_RECONCILED**  
**Gate 2:** **PASS — V3_DB_RECONCILED**  
**Gate 3:** **PASS — PROMOTE_DB_CANONICAL_RESEARCH_STATE**  
**Gate 4:** **PASS — PUBLISH_DB_BACKED_CANONICAL_RELEASE**  
**Gate 5:** **PASS — CUTOVER_PUBLIC_CHANNEL_TO_V070** under D-113  
**Live schema head:** `0034`  
**Canonical release package schema:** `0033` (immutable v0.7.0 historical artifact)  
**Independent historical review:** 0

The DB-canonicalization / first DB-backed release programme is complete. No new
historical subject-research tranche is automatically authorized by that success.

## Gate 5 closeout

Public serving now uses the immutable release-derived adapter
`v0.7.0-public-mvp-v1`.

Verified production invariants:

- public payload SHA-256
  `2a04787a2ee0e42a97f273621eebbf32ddc6a1b2e903239a626eb41d72c29786`;
- 16 displayed spatial entities / 18 territorial-practice claims;
- 0 reviewed historical evidence geometries;
- 21 `researched_internal` + 5 `under_review` target states;
- 6 researched-inconclusive outcomes remain non-absence;
- independent historical review remains 0;
- exact source-version provenance survives the serving adapter;
- territorial practice remains distinct from law, external/network participation,
  research coverage and geometry;
- neutral Natural Earth land remains independent cartographic context;
- live API and deployed static fallback use the same frozen payload bytes;
- D-053 compare-and-set rollback to `mvp-preview-ancient-v2` was proved before cutover;
- D-112 / migration 0034 freezes published release-manifest metadata;
- Supabase security advisor: 0 lints after 0034;
- Pages deployment of commit
  `5675186303b30c43cdfaff9c41c72b64df1b153b`: PASS.

The frozen R1 technical candidate remains available as a historical project artifact at
`r1-candidate.html`; it is no longer the default public root.

## Immediate consolidation task

After the Gate-5 closeout PR merges:

1. close #323 with disposition `CUTOVER_PUBLIC_CHANNEL_TO_V070`;
2. close parent #300 as the completed Gate-0→Gate-5 canonicalization programme;
3. perform one project-wide backlog / health review under D-096;
4. choose the next justified mode from discovery, execution, consolidation,
   review/release, maintenance, or no justified work;
5. do **not** reopen subject research merely because the release pipeline is now stable.

No UI redesign, automatic P-level inference, inferred historical geometry, archive-count
prevalence inference or false independent-review claim is authorized by this closeout.

# Discovery execution

Use `docs/discovery/DISCOVERY_EXECUTION.md` and `docs/discovery/RUN_PROMPT.md`.
D-091/D-092 govern execution discipline; neither changes EXP-08's frozen sample,
historical acceptance criteria or release boundary.

## Actions budget

Batch one coherent checkpoint per PR. Run Python tests/sanitation locally first.
Normal PR checks run sanitation and Python regressions; PostGIS runs for changes
outside known documentation/research text paths, or on manual dispatch. No duplicate
foundation run on merge. Legacy preview health remains weekly/manual, not every push.
Do not skip required relevant checks or rerun unchanged successful jobs.

## Continuation rule

D-096 governs continuation.

At a boundary choose the next justified **mode**:
1. discovery;
2. execution;
3. consolidation;
4. review/release;
5. maintenance;
6. no justified work.

WIP = one active priority, not one mandatory experiment.

Choose by:
1. evidence quality;
2. decision importance / project goal;
3. focus;
4. review/reconciliation capacity;
5. whole-project complexity;
6. only then execution convenience.

Elapsed time alone is not a stop rule, and unused capacity is not a reason to invent
another experiment.

Accepted methods may be used within their declared operational scope without re-proving
their value. Reopen them only on a concrete trigger recorded in D-096.

---

# PARKED / trigger-bound operational debt

These remain trigger-bound and are not the default horizon.

## #43 — protected staging / release-promotion administration

Remaining protected environment / staging work matters only when Gate 5/public
promotion actually requires it.

## #26 — migration-history reconciliation

**Closed / historical.** Gate 0 passed `MIGRATION_HISTORY_RECONCILED`. Do not reopen the
old mismatch as active work unless a new concrete migration-history inconsistency is
observed.

## Managed backup/PITR

Current Supabase Free-plan recovery evidence is logical/preservation-grade rather than
physical managed backup/PITR. Revisit if plan/capabilities change or operational
durability becomes a release requirement; do not require a paid temporary branch merely
for process ceremony.

## Repository administration

- `main` currently reports unprotected;
- historical remote topic branches remain;
- current integration lacks some repository-admin capability.

Handle when it materially blocks evidence/release work; do not turn administration into
the project horizon.

---

# Explicitly NOT the current horizon

Gate 4 does **not** authorize:

- new historical subject research;
- UI/API cutover;
- frontend redesign;
- PMTiles/vector-tile infrastructure expansion;
- new search service;
- graph database;
- vector store/RAG infrastructure;
- generic ontology/platform work;
- contributor/peer-review platform;
- new autonomous infrastructure for its own sake;
- external recruitment/review;
- automatic public-channel movement.

The current priority is one bounded release task: prove or reject the first DB-backed
canonical historical release.
