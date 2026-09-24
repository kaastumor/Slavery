# Historical Slavery Atlas — Backlog

**Updated:** 2026-09-24  
**Role:** canonical execution queue only; assumptions/risks/value evidence live in `docs/25_PROJECT_HEALTH.md`  
**Canonical historical data release:** `v0.6.1` (unchanged)  
**Current public preview:** `mvp-preview-ancient-v2` (non-canonical legacy demonstration)

This file answers **what is justified to work on next**.

---

# ACTIVE EVIDENCE HORIZON — EXP-04 blind frontier tranche

**Active issue:** #213
**Current stage:** ACTIVE RESEARCH / DISCOVERY — WIP 1

EXP-03 (#211, merged #212) completed with CORE REQUIRES EXTENSION; D-089 accepted
historical terminology/category mapping and source role/claim fitness in the portable contract.

EXP-04 tests that contract on the eight previously registered targets frozen in #213.
Protocol and pinned selection: `experiments/exp04-blind-frontier/00_PROTOCOL.md`
and `sample.json`.

Current checkpoint: **Indus packet under review; seven cases not started**.
A positive secondary slavery interpretation and a Mesopotamian textual lead are
preserved; no completed inconclusive or territorial-practice designation is asserted.

**Next:** reconcile recovered CDLI P453801 / Nisaba 15 371 with the full Laursen–Steinkeller 2017 pp.83–84 discussion; verify
status, date and acquisition geography; finish the Indus synthesis. Then research
Sumerian City-States, preserving any shared-source dependency. See `CHECKPOINT.md`.

Project form: portable reviewed evidence core + replaceable Atlas/map/table/API views.
Canonical v0.6.1, frozen R1 registry and public preview remain unchanged.

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

These are not eligible while #213 is active unless they block it.

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

Do not let proactive research become platform drift. #213 does **not** authorize:

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
