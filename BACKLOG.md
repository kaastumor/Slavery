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
**Current gate:** Gate 1 — v0.6.1 DB reproduction / release-membership rebuild  
**Canonical historical data release:** `v0.6.1` unchanged  
**Reviewed successor input:** `post-r1-cumulative-review-v3-cross-frame` remains frozen/noncanonical  
**WIP:** #300 Gate 1 only

Gate 0 completed:
- migration 0030 applied exactly once;
- repository checksum ledger established with 30 verified rows;
- checksum mismatches = 0; extras = 0;
- known Supabase 0012–0014 gaps and 0016/0029 retries preserved as legacy audit evidence;
- release channel/membership counts unchanged;
- claim-kind integrity remains clean;
- internal schemas remain unavailable to anon/authenticated;
- Supabase security advisor currently reports 0 lints.

## Gate 1 finding already established

The old `0.6.1-db-migration-candidate` predates current reconstructible release
membership/artifact machinery.

Its embedded manifest contains:
- 18 claim IDs;
- 11 actor IDs;
- 8 voyage IDs;
- 18 source-version IDs;
- 99 coverage-assessment IDs.

But current exact membership tables contain **0 rows for that release**, and
`release_capture_status` remains
`pending_d054_release_bundle_rebuild`.

Therefore Gate 1 is not a re-import of historical evidence. It is a controlled
reconstruction/reconciliation task:

1. revalidate exact v0.6.1 workbook checksum/raw/crosswalk meaning;
2. rebuild exact release membership from the frozen candidate manifest/current DB;
3. generate/verify an immutable full-state bundle under the current release contract;
4. preserve the unresolved QC issue and draft/noncanonical status;
5. prove byte/digest reconstruction before any DB authority decision.

No v3 ingestion until Gate 1 passes.

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
