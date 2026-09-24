# Historical Slavery Atlas — Backlog

**Updated:** 2026-09-24  
**Role:** canonical execution queue only; assumptions/risks/value evidence live in `docs/25_PROJECT_HEALTH.md`  
**Canonical historical data release:** `v0.6.1` (unchanged)  
**Current public preview:** `mvp-preview-ancient-v2` (non-canonical legacy demonstration)

This file answers **what is justified to work on next**.

---

# EXP-06 CLOSURE CANDIDATE — balanced evidence growth

**Active issue:** #225
**Current stage:** CLOSURE CANDIDATE — one coherent PR / scoped CI

All six frozen targets are researched and serialized in the portable package.

Observed:
- 6 target rows / 36 source-relation rows;
- 4 internally researched outcomes, including one researched-inconclusive;
- 2 under-review outcomes where exact target identity/chronology remains unresolved;
- no schema/ontology extension required;
- no P-level, geometry promotion, R1 reviewed-state or canonical-release mutation.

Key results:
- Chámpa: evidence exists, but the 500 CE polity frame is ambiguous;
- Magadha: slavery context is supported more strongly than exact Haryanka chronology;
- Mayapán: positive member-locus without aggregate-wide generalization;
- Mongol Yam: positive compulsory service without slave-status collapse;
- Yaghan: internal uncertainty preserved alongside external/intergroup coercion;
- Khmer 1300: independent 1296–1297 capital-core slavery evidence; no empire-wide fill.

Protocol: `experiments/exp06-balanced-evidence/00_PROTOCOL.md`
Result: `experiments/exp06-balanced-evidence/RESULT.md`
Checkpoint: `experiments/exp06-balanced-evidence/CHECKPOINT.md`

**Next after #225 merges/closes:** select one new bounded historical evidence horizon
from the remaining frozen/QA-ready queue by expected information gain. Do not insert
another application/product horizon unless a changed task meets EXP-05's reopening
conditions.

Canonical v0.6.1 remains unchanged.

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

These are not eligible while #225 is active unless they block the historical tranche.

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

Do not let evidence growth become platform drift. #225 does **not** authorize:

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
