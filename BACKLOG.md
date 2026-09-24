# Historical Slavery Atlas — Backlog

**Updated:** 2026-09-24  
**Role:** canonical execution queue only; assumptions/risks/value evidence live in `docs/25_PROJECT_HEALTH.md`  
**Canonical historical data release:** `v0.6.1` (unchanged)  
**Current public preview:** `mvp-preview-ancient-v2` (non-canonical legacy demonstration)  
**Published research candidate:** `exp06-candidate-v1` at `exp06-candidate.html` (non-canonical)

This file answers **what is justified to work on next**.

---

# EXP-07 C0 QUALIFICATION — ACTIVE

**Issue:** #229  
**Current stage:** FROZEN IDENTITY / ANCHOR QUALIFICATION  
**Subject slavery/coercion research:** **NOT AUTHORIZED YET**

The next-horizon comparison is complete.

EXP-03/04/06 together leave exactly one untouched QA-ready C1 row in the frozen R1
registry: **Grand Duchy of Lithuania — 1300 CE**. Selecting it merely because it is
already ready would let C1 readiness/execution convenience bypass the specific C0
qualification question that this horizon is meant to test.

The project therefore opens one bounded C0 qualification horizon before new subject
research. The frozen sample is recorded in
`experiments/exp07-c0-qualification/01_SAMPLE_FREEZE.json`.

Frozen rows:
- Great Zimbabwe — 1400;
- Swahili maritime trade network — 1400;
- Māori communities in Aotearoa — 1700;
- Ifugao communities, northern Luzon — 1700;
- Nobatia — 500 CE;
- Kalabhra Dynasty — 500 CE;
- Qi — 500 BCE;
- Khanate of Kokand — 1800 CE.

**Current exact action:** validate only target identity, anchor chronology, frame class,
and defensible spatial scope. Do not inspect slavery/coercion evidence. Each row must
end as QUALIFIED_C1_READY, HOLD_IDENTITY_OR_TIME, REJECT_FRAME_INVALID, or
QUALIFICATION_INCONCLUSIVE.

Only after #229 closes may a later subject-research horizon be selected from qualified
rows. Do not silently mutate the R1 registry or promote C0 to historical research.

## Discovery execution

Use `docs/discovery/DISCOVERY_EXECUTION.md` and `docs/discovery/RUN_PROMPT.md`.
The sponsor-requested D-091 process repair changes execution guidance, not EXP-04's
frozen sample, historical conclusions or acceptance criteria. Resume #213 after it.

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
