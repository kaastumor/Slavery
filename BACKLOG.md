# Historical Slavery Atlas — Backlog

**Updated:** 2026-09-24  
**Role:** canonical execution queue only; assumptions/risks/value evidence live in `docs/25_PROJECT_HEALTH.md`  
**Canonical historical data release:** `v0.6.1` (unchanged)  
**Current public preview:** `mvp-preview-ancient-v2` (non-canonical legacy demonstration)  
**Published research candidate:** `exp06-candidate-v1` at `exp06-candidate.html` (non-canonical)

This file answers **what is justified to work on next**.

---

# DISC-06 INFERENCE-CHAIN STRESS TEST — FREEZE GATE

**Issue:** #240  
**Primary gate:** method / representation discovery  
**Current stage:** PROTOCOL + SIX-CASE REGRESSION SAMPLE FROZEN  
**Historical subject research:** **PAUSED / PROHIBITED IN THIS EXPERIMENT**

DISC-05 is complete and closed. It selected one bounded question: whether explicit
premise → reasoning → conclusion provenance materially improves the portable evidence
core over the current packet.

Frozen exposed regression cases:
- Teotihuacan — 500 CE;
- Shaolin — 1000 CE;
- Inuit frame — 1800 CE;
- Cahokia — 1200 CE;
- Lazica — 500 CE;
- Nālandā Mahāvihāra — 700 CE.

The experimental ledger is intentionally tiny: inference ID, target, conclusion,
premise references, one reasoning-rule label, result and review state. No RDF/graph
database/schema migration.

**Current exact action:** merge the DISC-06 freeze if CI is green. Only then construct
the ledger and compare it against the existing portable packet using the preregistered
threshold.

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
