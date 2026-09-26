# Historical Slavery Atlas — Backlog

**Updated:** 2026-09-26  
**Role:** canonical execution queue only; assumptions/risks/value evidence live in `docs/25_PROJECT_HEALTH.md`  
**Canonical research authority:** PostgreSQL/PostGIS, explicit governed membership under D-109  
**Canonical historical data release:** `v0.7.0`  
**Current public preview:** `mvp-preview-ancient-v2` (non-canonical legacy demonstration)  
**Published research candidate:** `exp06-candidate-v1` at `exp06-candidate.html` (non-canonical)

This file answers **what is justified to work on next**.

---

# CURRENT MODE — REVIEW / RELEASE + PUBLIC CUTOVER

**Parent gate:** #300 — canonical PostgreSQL + first DB-backed release gate  
**Gate 0:** **PASS — MIGRATION_HISTORY_RECONCILED**  
**Gate 1:** **PASS — V061_DB_RECONCILED**  
**Gate 2:** **PASS — V3_DB_RECONCILED**  
**Gate 3:** **PASS — PROMOTE_DB_CANONICAL_RESEARCH_STATE**  
**Gate 4:** **PASS — PUBLISH_DB_BACKED_CANONICAL_RELEASE**  
**Current gate:** Gate 5 — public UI/API cutover to canonical v0.7.0  
**Canonical historical data release:** `v0.7.0`  
**Current public preview/channel:** `mvp-preview-ancient-v2` until Gate 5 passes  
**Frozen reviewed input:** `post-r1-cumulative-review-v3-cross-frame`  
**WIP:** #323 — cut public UI/API to canonical v0.7.0 release

## Gate 4 closeout

D-110 makes `v0.7.0` the first canonical historical release generated from the
D-109 PostgreSQL/PostGIS research-authority closure.

Frozen release membership:

- 40 claims;
- 11 actors;
- 18 spatial entities;
- 0 reviewed historical evidence geometries;
- 8 voyages;
- 99 coverage assessments;
- 211 exact source versions;
- 26 research-target results;
- membership SHA-256
  `ebc9d32f09857744841a0cf92699c41739b624ac4bd94c43798eb1f61e3b0dd3`;
- D-109 production database-state SHA-256
  `31b7a7b675445e5758ffd68d64ff0f0cde83df1b0ea65f29835246deb2ae26ff`;
- deterministic package/rebuild: PASS;
- exact typed release membership/digests: PASS;
- D-108 portable cartography artifact included: PASS;
- published membership/artifact immutability: PASS;
- Supabase security advisor: 0 lints;
- independent historical review: 0.

The v0.6.1 workbook remains the immutable predecessor and source-native lineage anchor;
it was not overwritten or silently normalized.

Gate 4 deliberately left every authority claim's `publication_status` unchanged and
left `public_mvp_preview` pointing to `mvp-preview-ancient-v2`. Canonical release
publication and public serving remain separate gates.

## Gate 5 exact question

Can the public UI/API be cut over to an exact v0.7.0-derived serving materialization
without exposing draft/unrestricted research state or weakening the release's
provenance, uncertainty, temporal/spatial or non-absence semantics?

Required before channel move:

1. derive serving state strictly from v0.7.0 release membership/materialization;
2. never select public content by broad `review_status` alone;
3. preserve territorial practice, law, external/network participation and coverage as
   separate dimensions;
4. preserve under-review, HOLD, researched-inconclusive and unresolved as non-absence;
5. keep 0 reviewed historical evidence geometries truthful and retain neutral world
   land independently;
6. preserve exact source/source-version and source-native lineage;
7. preserve D-108 cartography behavior;
8. stage the exact API/browser artifact intended for production;
9. run reconstruction, API/browser and security regression against that exact state;
10. prove rollback to the previous serving pointer before promotion;
11. move `public_mvp_preview` only as the final controlled step;
12. verify post-cutover channel identity and no draft leakage.

Allowed Gate-5 disposition:

- `CUTOVER_PUBLIC_CHANNEL_TO_V070`;
- `HOLD_PUBLIC_CUTOVER`;
- `REWORK_PUBLIC_MATERIALIZATION`.

No UI redesign, new historical research, P-level inference or historical geometry
promotion is authorized by Gate 5.

## Discovery execution

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
