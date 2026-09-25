# Historical Slavery Atlas — Backlog

**Updated:** 2026-09-25  
**Role:** canonical execution queue only; assumptions/risks/value evidence live in `docs/25_PROJECT_HEALTH.md`  
**Canonical historical data release:** `v0.6.1` (unchanged)  
**Current public preview:** `mvp-preview-ancient-v2` (non-canonical legacy demonstration)  
**Published research candidate:** `exp06-candidate-v1` at `exp06-candidate.html` (non-canonical)

This file answers **what is justified to work on next**.

---

# CURRENT MODE — EXECUTION

**Active issue:** #282 — EXP-12 Tōdai-ji 800 bounded subject research  
**Target:** `R1:N:todaiji_800` — Tōdai-ji — 800 CE  
**Frame:** `institution_estate` (institutional locus qualified; estate extent unresolved)  
**Canonical historical data release:** `v0.6.1` unchanged  
**WIP:** 1

The review-only CI cost leak is fixed by #280 / PR #281. Text review artifacts now
stay on cheap sanitation/Python checks while executable/non-text/unknown review paths
remain database-gated.

Tōdai-ji is the next bounded subject horizon because it gives a controlled replication
of the institution-specific inference problem in a different source tradition:
- Nālandā 700 and Shaolin 1000 remained target-specific inconclusive despite broader
  monastic slavery/dependency context;
- Karnak 1000 BCE remained selected-anchor inconclusive despite strong earlier
  target-specific captive labour;
- Tōdai-ji tests whether a Nara-period temple with a distinct legal/estate documentary
  tradition supplies a stronger or equally bounded target-specific answer.

Research question:
> What bounded slavery/coercion interpretation, if any, is supportable for Tōdai-ji at
> or around 800 CE?

Required controls:
- temple worker / tenant / dependent / corvée worker != slave by default;
- preserve `nuhi` / 奴婢 and other source-native status distinctions;
- generic Nara/Heian slavery is contextual unless linked to Tōdai-ji;
- later shōen/estate evidence is not back-projected;
- temple identity != estate boundary or practice polygon;
- law/status and actual practice remain separate.

Allowed outcomes:
`BOUNDED_SUPPORTED`, `RESEARCHED_INCONCLUSIVE`, or
`HOLD_EVIDENCE_ACCESS_OR_SCOPE`.

No P-level, practice geometry, R1 reviewed-state mutation, schema/ontology,
database/API/frontend change, canonical mutation, cumulative-candidate integration or
automatic publication.

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
