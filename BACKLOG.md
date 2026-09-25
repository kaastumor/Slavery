# Historical Slavery Atlas — Backlog

**Updated:** 2026-09-25  
**Role:** canonical execution queue only; assumptions/risks/value evidence live in `docs/25_PROJECT_HEALTH.md`  
**Canonical historical data release:** `v0.6.1` (unchanged)  
**Current public preview:** `mvp-preview-ancient-v2` (non-canonical legacy demonstration)  
**Published research candidate:** `exp06-candidate-v1` at `exp06-candidate.html` (non-canonical)

This file answers **what is justified to work on next**.

---

# CURRENT MODE — EXECUTION

**Active issue:** #276 — EXP-11 Karnak 1000 BCE bounded subject research  
**Target:** `R1:N:karnak_amun_m1000` — Temple of Amun at Karnak — 1000 BCE  
**Frame:** `institution_estate` (institutional locus qualified; estate extent unresolved)  
**Canonical historical data release:** `v0.6.1` unchanged  
**WIP:** 1

EXP-10 completed with four neutral `QUALIFIED_C1_READY` rows and no subject research.

Karnak is the next bounded subject horizon because:
- Nālandā 700 and Shaolin 1000 exposed a recurring institution-frame failure:
  generic monastic slavery/dependency evidence cannot be projected onto the target;
- Karnak tests that exact failure mode with an ancient institution-specific target;
- it also exercises the early chronology × non-polity interaction identified by
  DISC-07/D-094;
- Trans-Saharan and Sápmi would mostly replay already-exercised network/community
  inference guards.

Selection is for discrimination, not expected positive evidence or archive density.

Research question:
> What bounded slavery/coercion interpretation, if any, is supportable for the
> Temple/Precinct of Amun at Karnak around 1000 BCE?

Required controls:
- temple worker/dependent != slave by default;
- corvée, service, captives, dedicated persons, dependants and property status remain
  distinct unless specialist interpretation supports a mapping;
- generic Egyptian temple practice is contextual unless Karnak-specific;
- New Kingdom / Late Period evidence is not silently projected to 1000 BCE;
- Temple of Amun != whole Karnak complex != Thebes != an inferred estate territory;
- source-native terminology and translation uncertainty remain visible.

Allowed outcomes:
`BOUNDED_SUPPORTED`, `RESEARCHED_INCONCLUSIVE`, or
`HOLD_EVIDENCE_ACCESS_OR_SCOPE`.

Current branch result: **RESEARCHED_INCONCLUSIVE** for Temple-of-Amun slave/unfree
labour around 1000 BCE.

What is supported:
- earlier New Kingdom Amun/Karnak captive/enslaved labour;
- near-anchor continuity of the Amun institution;
- near-anchor subordinate/personnel/property context in the Amun priestly world,
  including alienable/perpetual services.

What remains unresolved:
- a human slave/unfree labour category tied specifically to the Temple of Amun at
  the selected anchor.

Internal adversarial replay rejected four tempting bridges:
New Kingdom continuity; `bꜣk.w = slave`; foreign/Asiatic = slave; and Amun-priestly
family property = Temple-of-Amun workforce.

Next exact action: one coherent PR + normal scoped CI → merge → close #276 → return to
the D-096 mode-selection boundary. No automatic cumulative-candidate integration.

No P-level, practice geometry, R1 reviewed-state mutation, schema/ontology change,
database/API/frontend work, canonical mutation, cumulative-candidate integration or
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
