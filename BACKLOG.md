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
**WIP:** one fixed eight-slot campaign; no scheduled slot has run yet

## Scheduled execution architecture

Scheduled/autonomous executions are **READ-ONLY on GitHub** until the known scheduled
GitHub mutation limitation is demonstrably resolved.

GitHub remains canonical for:
- accepted project/governance state;
- BACKLOG/current WIP;
- campaign plan;
- issues/PRs;
- accepted checkpoints and review/release decisions.

A private persistent execution ledger outside Git/CI owns only temporary scheduled-run:
- claim status;
- crash recovery;
- terminal run status;
- compact result/artifact pointer;
- whether interactive GitHub reconciliation is pending.

Current ledger state: **Runs 1–8 all PENDING**.

Every scheduled invocation must:
1. read live GitHub canonical state;
2. read the private execution ledger;
3. resume any `IN_PROGRESS` slot, otherwise select the lowest `PENDING` slot;
4. durably mark exactly one slot `IN_PROGRESS` **before** substantive work;
5. stop before substantive work if the ledger cannot be written;
6. execute exactly one bounded slot;
7. never mutate GitHub;
8. save substantive artifacts privately;
9. mark the slot terminal as `DONE`, `REVISED`, `NO_VALUE`, or `BLOCKED`;
10. set `github_reconciliation_pending: true` when canonical GitHub does not yet
    reflect the result;
11. never repeat a terminal slot or begin a second slot in the same invocation;
12. never invent Run 9 or extend the fixed campaign.

The historical `NIGHT_STAGE_N_COMPLETE` comments on #291 are now **interactive
reconciliation markers only**, not scheduled claim/recovery state.

An interactive session must reconcile terminal ledger results into GitHub in order,
against current `main`, before writing markers, branches/commits, PRs, issue closures
or BACKLOG changes.

## Fixed eight-slot goal

1. EXP-14 Trans-Saharan 1300 research packet.
2. EXP-14 adversarial replay / merge-ready result for later interactive reconciliation.
3. EXP-10-derived programme closure retrospective.
4. Five-row post-v2 source/dependency reconciliation.
5. Five-row adversarial cumulative internal review.
6. D-099-compliant packaging gate.
7. Next-horizon allocation review.
8. Final QC + private morning handoff.

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
