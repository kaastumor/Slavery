# Historical Slavery Atlas — Backlog

**Updated:** 2026-09-25  
**Role:** canonical execution queue only; assumptions/risks/value evidence live in `docs/25_PROJECT_HEALTH.md`  
**Canonical historical data release:** `v0.6.1` (unchanged)  
**Current public preview:** `mvp-preview-ancient-v2` (non-canonical legacy demonstration)  
**Published research candidate:** `exp06-candidate-v1` at `exp06-candidate.html` (non-canonical)

This file answers **what is justified to work on next**.

---

# CURRENT MODE — MAINTENANCE / TRIGGER-BOUND REVIEW

**Latest completed programme:** #262 — overnight ready historical queue  
**Latest internal candidate:** `post-r1-cumulative-review-v2-overnight`  
**Canonical historical data release:** `v0.6.1` unchanged  
**Historical intake:** no new tranche is currently authorized

The sponsor-authorized four-target queue is complete:
1. Qi — 500 BCE — internally reviewed bounded evidence state; exact Qi territorial
   slavery/servitude remains researched-inconclusive.
2. Swahili maritime trade network — 1400 — medieval slave-trade participation is
   supported at the network dimension; coast-wide territorial prevalence and exact
   volume remain unresolved.
3. Ifugao communities — 1700 — exact-anchor slavery/status remains
   researched-inconclusive; later traditional child sale, debt bondage, captivity and
   slaveholding remain bounded contextual evidence.
4. Khanate of Kokand — 1800 — exact-anchor slavery/slave-trade practice remains
   researched-inconclusive; later early-nineteenth-century Kokand slavery/captive
   enslavement remains bounded contextual evidence.

The successor candidate contains:
- 21 total members;
- 16 internally accepted bounded evidence states;
- 5 explicit HOLD rows;
- 133 source relations by pinned lineage;
- 2 explicit cross-target exact source-version dependencies;
- 0 independent historical reviews.

Under D-096/D-098, the next justified mode is **maintenance / trigger-bound review**.
This does not authorize another historical intake tranche automatically.

Reopen active work only for a concrete trigger such as:
- new sponsor authorization for bounded historical intake;
- independent/external historical review;
- a concrete consumer/publication need for the cumulative candidate;
- a demonstrated defect in an accepted row;
- new evidence satisfying a recorded HOLD/reopen condition;
- a production/release need that activates one of the parked operational items.

The completed programme creates no P-level, historical-practice geometry, canonical
release, public release, R1 reviewed-state, schema, database/API or frontend change.

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
