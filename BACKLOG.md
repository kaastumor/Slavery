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
**Current gate:** Gate 1 — v0.6.1 DB reproduction  
**Active execution slice:** #304 — repair incomplete live v0.6.1 semantic migration  
**Canonical historical data release:** `v0.6.1` unchanged  
**Reviewed successor input:** `post-r1-cumulative-review-v3-cross-frame` frozen/noncanonical  
**WIP:** #304 only under parent #300

Gate 0 is complete on `main`:
- forward migration 0030 applied exactly once;
- 30-row checksum ledger verified with zero mismatch/extras;
- known platform-history gaps/retries preserved as audit evidence;
- no historical migration replay.

## Gate 1 live revalidation — blocking finding

The old `0.6.1-db-migration-candidate` cannot currently be treated as reconciled.

Live execution of the unchanged
`db/tests/002_v061_reconciliation.sql` failed.

The test file is byte-identical to the version at the candidate's recorded
reconciliation commit, so this is not test drift.

Present and preserved:
- Atlantic voyage/owner/source core;
- 99 coverage assessments with expected state distribution;
- canonical workbook source/version/asset;
- canonical workbook SHA-256
  `0a38e4eb6f63c3bb4ce9543be379605d24dd9ff1c1cea1e0a49c0c3db7ba17d4`;
- existing public preview/channel state.

Missing live:
- `v061_workbook_row`: 0 / expected 288;
- v0.4.7–v0.5.0 global evidence mappings: 0 / expected 22 mappings over
  18 positive/disputed rows;
- evidence-sheet coverage-source links: 0 / expected 36;
- workbook external-participation claims: 0 / expected 3;
- workbook legal-event claims: 0 / expected 1.

A live blocking QC issue
`V061_LIVE_RECONCILIATION_INCOMPLETE`
is attached to the draft DB candidate.

## Repair contract

#304 restores **only** the missing phase:
- no full importer replay/reset;
- deterministic/idempotent identities;
- atomic transaction;
- exact source-version URLs;
- 288 raw workbook rows;
- 36 coverage-source links;
- explicit 22 global semantic targets;
- RI remains non-positive provenance;
- territorial P-level stays NULL;
- no geometry inference;
- repaired claims remain reviewed + unpublished;
- public release/channel membership is untouched.

A partial/conflicting repair state must fail closed.

## Gate 1 done gate

1. reviewed repair code passes repository CI;
2. live dry-run reports `READY_TO_REPAIR`;
3. one controlled atomic live apply;
4. unchanged `db/tests/002_v061_reconciliation.sql` passes;
5. schema/security/release-channel invariants still pass;
6. blocking QC issue is resolved only after those checks;
7. then rebuild exact v0.6.1 release membership/bundle under current contract;
8. record `V061_DB_RECONCILED`.

No v3 ingestion and no DB authority flip until Gate 1 passes.

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
