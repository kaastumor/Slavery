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
**Immediate prerequisite:** #26 — live migration-history reconciliation  
**Canonical historical data release:** `v0.6.1` remains unchanged  
**Reviewed successor input:** `post-r1-cumulative-review-v3-cross-frame`  
**WIP:** #300 parent gate; #26 is the current execution slice

## Sequencing decision

The project is now deliberately **database-first before the next canonical release**.

Target architecture:

> source evidence → canonical PostgreSQL/PostGIS research state → explicit release gate → immutable release package → replaceable UI/API/GIS views

This does **not** mean the live database is canonical yet.

The authority flip requires:
1. repository/live migration history reconciliation;
2. deterministic semantic reproduction of v0.6.1;
3. lossless ingestion/reconciliation of frozen v3 reviewed evidence;
4. release-membership/reconstruction proof;
5. security + draft/publish separation proof;
6. rollback/recovery verification.

Only then may the DB become canonical research state.

The first DB-backed canonical release is provisionally `v0.7.0` if the cutover does
not introduce a compatibility-breaking ontology change.

The UI/API cutover happens **after** the DB-backed immutable release passes QC. Public
services continue to consume published/release materializations, never unrestricted
draft research tables.

Independent historical review is not required for internal DB canonicalization.
Review provenance must remain explicit; current independent review count is 0.

## Immediate Gate 0 findings

Live Historical Slavery Atlas Supabase:
- PostgreSQL 17.6, ACTIVE_HEALTHY;
- repository schema head: 0029;
- live migration history missing 0012–0014;
- 0016 appears three times in live history;
- 0029 appears twice;
- required 0012–0014 schema effects are present;
- existing `0.6.1-db-migration-candidate` is draft/noncanonical;
- release membership/channel machinery already exists;
- public channel still points to `mvp-preview-ancient-v2`.

Security:
- Supabase advisor flags RLS-disabled internal tables;
- verified `anon` / `authenticated` have no USAGE on internal schemas and no table
  grants there;
- do not blindly enable RLS; recheck at canonical/public cutover.

## Next exact action

Complete #26 non-destructively:
- compare repository 0012–0029 intent with actual live definitions;
- build repository↔live migration matrix;
- repair only migration history required for safe future tooling;
- rerun schema/release/security regressions;
- record `MIGRATION_HISTORY_RECONCILED`.

Do **not** start new subject-history research while #300 is active.

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
