# Historical Slavery Atlas — Backlog

**Updated:** 2026-09-25  
**Role:** canonical execution queue only; assumptions/risks/value evidence live in `docs/25_PROJECT_HEALTH.md`  
**Canonical historical data release:** `v0.6.1` (unchanged)  
**Current public preview:** `mvp-preview-ancient-v2` (non-canonical legacy demonstration)  
**Published research candidate:** `exp06-candidate-v1` at `exp06-candidate.html` (non-canonical)

This file answers **what is justified to work on next**.

---

# CURRENT MODE — EXECUTION

**Active issue:** #272 — EXP-09 Lithuania 1300 bounded subject research  
**Target:** `R1:P:1300:D:r1` — Grand Duchy of Lithuania — 1300 CE  
**Frame:** polity; identity already validated in R1  
**Canonical historical data release:** `v0.6.1` unchanged  
**WIP:** 1

Sponsor continuation authorization re-opened bounded historical intake after #262.

Why this target:
- every EXP-07 `QUALIFIED_C1_READY` row has now received subject research;
- Kalabhra remains an identity/time HOLD and is not eligible for subject research;
- Lithuania is the remaining previously qualified untouched C1 target;
- recent intake deliberately emphasized non-Western cases, so selecting Lithuania now
  no longer defeats the balancing intent that previously deferred it;
- using an existing qualified target avoids creating a new qualification batch first.

Research question:
> What bounded slavery/coercion interpretation, if any, is supportable for the Grand
> Duchy of Lithuania at or close to 1300 CE?

Required controls:
- no back-projection of later serfdom or sixteenth-century statutes;
- no neighboring Rus'/Polish/Prussian/Teutonic substitution;
- captivity != slave status without evidence;
- law/status, territorial practice and external participation remain separate;
- no source-count prevalence inference.

Allowed outcomes:
`BOUNDED_SUPPORTED`, `RESEARCHED_INCONCLUSIVE`, or
`HOLD_EVIDENCE_ACCESS_OR_SCOPE`.

No P-level, practice geometry, R1 reviewed-state mutation, schema/ontology change,
database/API/frontend work, canonical mutation or automatic publication.

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
