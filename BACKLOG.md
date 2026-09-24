# Historical Slavery Atlas — Backlog

**Updated:** 2026-09-24  
**Role:** canonical execution queue only; assumptions/risks/value evidence live in `docs/25_PROJECT_HEALTH.md`  
**Canonical historical data release:** `v0.6.1` (unchanged)  
**Current public preview:** `mvp-preview-ancient-v2` (non-canonical legacy demonstration)

This file answers **what is justified to work on next**.

---

# ACTIVE VALUE HORIZON — EXP-05 thin-view discrimination

**Active issue:** #223  
**Current stage:** EXECUTION — WIP 1

#221 / the EXP-04 Research Preview is live and received sponsor first-look browser
acceptance. That acceptance is lightweight usability evidence, not external demand or
independent historical validation.

The current decision-relevant uncertainty is whether the **thin Atlas view materially
improves difficult comparative work** over:
- A: ordinary case packets + source notes;
- B: the portable evidence package without the map;
- C: the live map + table preview.

Frozen protocol: `experiments/exp05-thin-view-value/00_PROTOCOL.md`.

Three tasks are preregistered:
1. temporal + spatial truth;
2. external/network versus territorial practice;
3. category + dependency negative control.

Lane A has been executed first. Lane B has been executed second. Lane C will be
captured once through the existing Playwright pattern against the live preview; no UI
change is allowed before that run.

Decision rule:
- C material advantage on >=2/3 tasks → thin Atlas earns continued derived-view
  investment;
- B improves but C does not → preserve corpus/method; stop app expansion beyond
  maintenance;
- neither B nor C improves A → stop further Atlas expansion and preserve the
  method/corpus/audit artifacts;
- any dangerous UI-induced overclaim can force REVISE.

This remains an **internal workflow/value experiment**. It cannot establish external
demand, adoption, researcher preference or independent historical validity.

Canonical v0.6.1 remains unchanged. No historical research tranche, schema/API/database
change, geometry programme or frontend change is authorized by #223.

## Sponsor-visible state

The EXP-04 preview remains live at
`https://kaastumor.github.io/Slavery/research-preview.html`.

#223 may inspect that existing view, but it must not modify the interface before all
frozen lane-C tasks are captured.


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

These are not eligible while #223 is active unless they block the value experiment.

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

Do not let the value test become platform drift. #223 does **not** authorize:

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
