# Historical Slavery Atlas — Backlog

**Updated:** 2026-09-26  
**Role:** canonical execution queue only; assumptions/risks/value evidence live in `docs/25_PROJECT_HEALTH.md`  
**Canonical historical data release:** `v0.6.1` (unchanged)  
**Current public preview:** `mvp-preview-ancient-v2` (non-canonical legacy demonstration)  
**Published research candidate:** `exp06-candidate-v1` at `exp06-candidate.html` (non-canonical)

This file answers **what is justified to work on next**.

---

# CURRENT MODE — REVIEW / RELEASE + DATABASE CANONICALIZATION

**Parent gate:** #300 — canonical PostgreSQL + first DB-backed release gate  
**Gate 0:** **PASS — MIGRATION_HISTORY_RECONCILED**  
**Gate 1:** **PASS — V061_DB_RECONCILED**  
**Gate 2:** **PASS — V3_DB_RECONCILED**  
**Current gate:** Gate 3 — PostgreSQL canonical-research authority proof  
**Canonical historical data release:** `v0.6.1` unchanged  
**Frozen reviewed input:** `post-r1-cumulative-review-v3-cross-frame`  
**WIP:** #313 — full-state release reconstruction and DB authority proof

## Gate 2 closeout

Live PostgreSQL now contains the frozen v3 research package losslessly:

- 26 research targets/results;
- 21 internally admitted evidence states;
- 5 HOLD states;
- 166 target-source relations;
- 164 unique exact source versions;
- 0 target→historical-claim bridges from the Gate-2 import;
- 0 target spatial links invented;
- 0 independent reviews;
- exact frozen-payload round trip: PASS;
- representative idempotent rerun: PASS;
- v0.6.1 regression: PASS;
- private Data API boundary: PASS;
- claim-kind / Gate-2 schema / source-provenance regressions: PASS;
- Supabase security advisor: 0 lints.

Gate 2 changes research representation only. It does not publish or make the DB
canonical.

## Gate 3 exact question

Can the reconciled live database become the authoritative **research state** while
preserving immutable releases as the citable historical snapshots?

Required before authority flip:

1. deterministic/stable IDs and idempotent re-ingestion;
2. repository↔live schema/head agreement;
3. preservation-grade full-state release reconstruction, broader than the current
   territorial-preview bundle;
4. exact release membership and object digests;
5. draft/reviewed/published separation;
6. backup/rollback/recovery proof;
7. private Data API/security boundary;
8. no unresolved blocking QC issue;
9. reproducible successor package from DB state;
10. explicit decision recording the authority flip.

No UI/public cutover or canonical release follows until Gate 3 and Gate 4 separately
pass.

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

These remain trigger-bound and are not the default historical horizon.

## #43 — protected staging / release-promotion administration

Remaining protected environment / staging work matters only if production mutation or a new public release is again justified.

## #26 — live Supabase migration-history reconciliation

The documented live history mismatch remains real. Reconcile it only before a future production migration/change requires that boundary.

## Repository administration

- `main` currently reports unprotected;
- historical remote topic branches remain;
- current integration lacks some repository-admin capability.

Handle when it materially blocks evidence work; do not turn administration into the research horizon.

---

# Explicitly NOT the current horizon

Do not let renewed historical research become platform drift. The next historical horizon does **not** authorize:

- M2 production schema migration;
- frontend redesign;
- PMTiles/vector-tile infrastructure;
- new search service;
- graph database;
- vector store/RAG infrastructure;
- generic ontology/platform work;
- contributor/peer-review platform;
- new autonomous infrastructure for its own sake;
- external recruitment/review (still deferred by sponsor);
- automatic canonical/public release.

The project should stay active through **bounded evidence work**, not through feature or infrastructure accumulation.
