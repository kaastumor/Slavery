# Historical Slavery Atlas — Backlog

**Updated:** 2026-09-24  
**Role:** canonical execution queue only; assumptions/risks/value evidence live in `docs/25_PROJECT_HEALTH.md`  
**Canonical historical data release:** `v0.6.1` (unchanged)  
**Current public preview:** `mvp-preview-ancient-v2` (non-canonical legacy demonstration)

This file answers **what is justified to work on next**.

---

# ACTIVE EVIDENCE HORIZON — EXP-03 heterogeneous evidence stress test

**Active issue:** #211  
**Current stage:** **ACTIVE RESEARCH / DISCOVERY — WIP 1**

The current project form remains:

> **portable reviewed evidence core + replaceable Atlas/map/table/API views**

The execution policy has changed:

> **Do not optimize for returning to idle. Optimize for evidence quality, focus, information gain and bounded project complexity.**

Elapsed time is not treated as the scarce resource. A completed horizon should normally be followed by the highest-information bounded research/discovery question that can materially change belief about the evidence method, corpus or Atlas use.

Stopping, rejecting, simplifying and parking remain valid **results**. They are not the default scheduler.

## Active work — #211 / EXP-03

Question:

> Does the portable evidence core survive fresh, structurally heterogeneous historical research with non-polity targets, mixed geometry states, category-translation pressure, law/practice divergence and network/territorial overlap?

Frozen cases:
1. Classical Athens, c. 400 BCE
2. Mamluk Cairo, c. 1300 CE
3. Tenochtitlan, c. 1500 CE
4. Joseon Korea, c. 1700 CE
5. Zanzibar Town / port, c. 1850 CE
6. British India, 1843–1850 CE

Required outputs:
- one research packet per case;
- source/dependency register;
- geometry-state note per case;
- portability audit against EXP-02;
- adversarial result;
- explicit disposition.

No canonical release/schema migration follows automatically.

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

These are not eligible while #211 is active unless they block it.

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

Do not let proactive research become platform drift. #211 does **not** authorize:

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
