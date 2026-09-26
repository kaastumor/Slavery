# Historical Slavery Atlas — Backlog

**Updated:** 2026-09-26  
**Role:** canonical execution queue only; assumptions/risks/value evidence live in `docs/25_PROJECT_HEALTH.md`  
**Canonical historical data release:** `v0.6.1` (unchanged)  
**Current public preview:** `mvp-preview-ancient-v2` (non-canonical legacy demonstration)  
**Published research candidate:** `exp06-candidate-v1` at `exp06-candidate.html` (non-canonical)

This file answers **what is justified to work on next**.

---

# CURRENT MODE — EXECUTION

**Active issue:** #297 — EXP-15 neutral node-site C0 qualification tranche  
**Mode:** neutral identity / chronology / frame / spatial-scope qualification  
**Canonical historical data release:** `v0.6.1` unchanged  
**WIP:** #297 only

Branch result: **PASS — THREE QUALIFIED**.

- Samarkand 1400 — `QUALIFIED_C1_READY`
  - Timurid city/node;
  - ancient Afrasiab, surrounding oasis and Timurid realm excluded.
- Timbuktu 1500 — `QUALIFIED_C1_READY`
  - urban/commercial/intellectual node;
  - Songhai territory and the whole trans-Saharan network excluded.
- Tenochtitlan 1500 — `QUALIFIED_C1_READY`
  - pre-conquest island capital/city;
  - Triple Alliance/Aztec territory and modern Mexico City excluded;
  - Tlatelolco-linked evidence must remain explicit.

No slavery/coercion subject research was performed.

Next exact action:
1. merge #297 after cheap research-text CI;
2. close #297;
3. return to D-096 mode selection;
4. prefer **review/release** next: evaluate
   `post-r1-cumulative-review-v3-cross-frame` for explicit canonical promotion before
   opening another subject-research tranche.

EXP-15 itself does not authorize canonical/public release.

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
