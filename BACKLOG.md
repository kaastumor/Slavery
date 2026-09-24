# Historical Slavery Atlas — Backlog

**Updated:** 2026-09-25  
**Role:** canonical execution queue only; assumptions/risks/value evidence live in `docs/25_PROJECT_HEALTH.md`  
**Canonical historical data release:** `v0.6.1` (unchanged)  
**Current public preview:** `mvp-preview-ancient-v2` (non-canonical legacy demonstration)  
**Published research candidate:** `exp06-candidate-v1` at `exp06-candidate.html` (non-canonical)

This file answers **what is justified to work on next**.

---

# CROSS-BATCH RESEARCH CONSOLIDATION — RESULT READY

**Issue:** #257  
**Mode:** consolidation  
**Current stage:** RECONCILIATION COMPLETE / MERGE GATE  
**Disposition:** **REVIEW_RELEASE_CANDIDATE**  
**Historical subject research:** **NONE PERFORMED**

R1 + EXP-04 + EXP-06 + EXP-07 + completed EXP-08 state are now reconciled into a
single **non-canonical research inventory**.

Key facts:
- 41 unique targets;
- 19 R1 rows internally adversarially reviewed;
- 12 post-R1 rows researched internally;
- 5 post-R1 rows remain under review;
- 3 qualification-ready targets remain unresearched;
- Kalabhra remains on identity/time hold;
- Qi remains frozen/unstarted;
- 0 independent historical reviews.

Across 173 inspected source relations, one exact cross-experiment dependency overlap
was found: Lustig & Lustig 2013 / `angkor-personnel-corpus`, shared by Angkor 1200
and Khmer Empire 1300. The claims remain separately scoped but are not independent
evidence streams.

No R1 reviewed target ID conflicts with later subject experiments. EXP-07 → EXP-08
target overlaps are deliberate qualification-to-research progressions, not competing
claims.

**Next mode after merge: REVIEW / RELEASE.**

Freeze the 17 post-R1 subject-research target IDs as one cumulative internal review
tranche. Review existing evidence only; do **not** admit new targets or resume Qi.
Goal: one cumulative non-canonical review candidate or explicit HOLD decision.

Do not canonicalize or publish automatically. v0.6.1 remains canonical.

EXP-08 stays paused after 3/4.

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
