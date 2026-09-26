# Historical Slavery Atlas — Backlog

**Updated:** 2026-09-25  
**Role:** canonical execution queue only; assumptions/risks/value evidence live in `docs/25_PROJECT_HEALTH.md`  
**Canonical historical data release:** `v0.6.1` (unchanged)  
**Current public preview:** `mvp-preview-ancient-v2` (non-canonical legacy demonstration)  
**Published research candidate:** `exp06-candidate-v1` at `exp06-candidate.html` (non-canonical)

This file answers **what is justified to work on next**.

---

# CURRENT MODE — OVERNIGHT CONTROLLED EXECUTION

**Controller issue:** #291 — close EXP-10 programme and reconcile post-v2 evidence  
**Immediate dependency:** #290 — EXP-14 Trans-Saharan 1300 bounded subject research  
**Canonical historical data release:** `v0.6.1` unchanged  
**WIP:** one overnight controller programme; stages are serialized by exact issue markers

The programme has eight goal-linked stages and is designed for one scheduled controller
task running eight hourly occurrences.

Progress is determined only by the lowest missing exact marker on issue #291:
`NIGHT_STAGE_1_COMPLETE` through `NIGHT_STAGE_8_COMPLETE`.

Recovery rules:
- every run re-reads GitHub `main`, #291 comments, open PRs/issues and relevant branches;
- resume unfinished work rather than creating duplicate branches/PRs;
- a run may complete multiple contiguous stages to recover from a missed occurrence;
- do not skip a stage merely to match the nominal run number;
- final occurrence must leave a truthful handoff even if programme completion fails.

Actions budget:
- normally <=3 coherent PR/CI cycles for the whole programme;
- research/review text must use the cheap CI path and must not trigger PostGIS;
- inspect pending CI once plus at most one bounded follow-up;
- never rerun unchanged successful jobs.

Programme goal:
1. finish EXP-14 Trans-Saharan 1300;
2. close the EXP-10-derived cross-frame programme;
3. reconcile/review the five post-v2 subject rows;
4. apply D-099 packaging discipline;
5. select/freeze the next justified D-096 horizon;
6. leave a final QC + morning handoff.

No automatic canonical/public release, P-level, historical-practice geometry, R1 state,
schema/ontology/database/API/frontend mutation or independent-review claim.

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
