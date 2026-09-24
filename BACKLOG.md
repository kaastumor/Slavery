# Historical Slavery Atlas — Backlog

**Updated:** 2026-09-24  
**Role:** canonical execution queue only; assumptions/risks/value evidence live in `docs/25_PROJECT_HEALTH.md`  
**Canonical historical data release:** `v0.6.1` (unchanged)  
**Current public preview:** `mvp-preview-ancient-v2` (non-canonical legacy demonstration)  
**Published research candidate:** `exp06-candidate-v1` at `exp06-candidate.html` (non-canonical)

This file answers **what is justified to work on next**.

---

# EXP-08 CROSS-FRAME HISTORICAL EVIDENCE — ACTIVE

**Issue:** #232  
**Current stage:** SUBJECT RESEARCH — 3 / 4 FROZEN CASES COMPLETE / PAUSE AFTER NOBATIA  
**Subject slavery/coercion research:** **IN PROGRESS**

EXP-07 closed with seven QUALIFIED_C1_READY rows and one hold. The post-qualification
selection compared those seven plus deferred Grand Duchy of Lithuania by expected
methodological information gain using only frame, chronology, geography and prior
experiment coverage.

Frozen EXP-08 sample:
- Great Zimbabwe — 1400;
- Māori communities in Aotearoa — 1700;
- Nobatia — 500 CE;
- Qi — 500 BCE.

The tranche deliberately spans a node/site, a region/community and two widely
separated polity/source environments. It avoids selecting all available rows and avoids
repeating mobile-network/community mechanisms already exercised heavily in EXP-04/06.

Great Zimbabwe — 1400 is now **researched-inconclusive for slavery/enslavement and
Great-Zimbabwe-specific slave-trade participation**, while hierarchy, tribute/extraction,
dependency/reciprocity and organized collective labor are supported. Connected coastal
slavery remains contextual and directional only.

Māori communities in Aotearoa — 1700 is now **bounded-supported for pre-contact
war-captive unfreedom/slavery-category relations**, with exact 1700 distribution,
prevalence and local status rules across iwi/hapū explicitly unresolved.

Nobatia — 500 CE is now **bounded-supported for royal human/retainer sacrifice near
the anchor**, while slave status of the victims, polity-wide slaveholding prevalence and
external slave-trade participation remain unresolved.

Per sponsor priority, stop slavery-evidence expansion after this case. **Qi — 500 BCE
remains frozen and unstarted**; EXP-08 is paused rather than closed.

**Current exact action after this checkpoint merges:** switch WIP to a bounded
project-discovery research run focused on adjacent methods, comparable projects and
decision-relevant opportunities for the Atlas/evidence corpus. Do not resume Qi until
that discovery horizon is reconciled or the sponsor explicitly redirects back.

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
