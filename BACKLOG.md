# Historical Slavery Atlas — Backlog

**Updated:** 2026-09-24  
**Role:** canonical execution queue only; assumptions/risks/value evidence live in `docs/25_PROJECT_HEALTH.md`  
**Canonical historical data release:** `v0.6.1` (unchanged)  
**Current public preview:** `mvp-preview-ancient-v2` (non-canonical legacy demonstration)  
**Published research candidate:** `exp06-candidate-v1` at `exp06-candidate.html` (non-canonical)

This file answers **what is justified to work on next**.

---

# DISC-07 CROSS-DIMENSIONAL COVERAGE AUDIT — RESULT READY

**Issue:** #245  
**Primary gate:** method / research-design discovery  
**Disposition:** **SURVIVES NARROWLY**  
**Historical subject research:** **NONE**

The 77-target R1.6 registry was audited with three non-visual cross-tabs.

Material result:
- anchor-band coverage and frame diversity both pass separately;
- their **interaction is concentrated**, especially in early chronology;
- current marginal gates do not explicitly state that limitation.

Future target-frame programmes that claim cross-chronology structural diversity should
therefore add a chronology × **broad selection-frame family** QA check before subject
research.

Boundaries:
- sparse cells are research-design states, never historical absence;
- do not fill cells by quota;
- polity sector-B gaps were already known and are not a new finding;
- `effective_frame_class` is too granular for naïve balance counting;
- immutable R1.6 research state is not a live post-R1 dashboard.

**Current exact action:** merge DISC-07 if CI is green, close #245, then freeze the next
discovery candidate: benchmark the existing portable candidate package against
**Frictionless Data Package** first, with RO-Crate only as a richer comparator if it
adds material reconstructibility/interoperability.

EXP-08 remains open/paused after 3/4. **Qi — 500 BCE remains frozen/unstarted.**

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

After the active bounded horizon closes:

1. reconcile the evidence;
2. identify the most decision-relevant unresolved uncertainty;
3. compare plausible next experiments by expected information gain;
4. select **one** bounded successor (WIP 1);
5. preregister its question, falsifier, evidence contract and complexity boundary;
6. continue.

Prefer real historical/source research over meta-work when both can answer the uncertainty.

A no-work state is justified only when the next useful step is genuinely blocked by unavailable evidence/permissions, would violate project constraints, or no bounded experiment can materially change belief. “The previous horizon completed” is not itself a reason to idle.

## Resource priority

Optimize in this order:
1. evidence quality;
2. focus / question discipline;
3. project complexity;
4. only then execution convenience.

Do **not** use elapsed research time alone as a stop criterion.

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
