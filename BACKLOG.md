# Historical Slavery Atlas — Backlog

**Updated:** 2026-09-24  
**Role:** canonical execution queue only; assumptions/risks/value evidence live in `docs/25_PROJECT_HEALTH.md`  
**Canonical historical data release:** `v0.6.1` (unchanged)  
**Current public preview:** `mvp-preview-ancient-v2` (non-canonical legacy demonstration)

This file answers **what is justified to work on next**.

---

# ACTIVE RELEASE GATE — EXP-06 non-canonical candidate

**Active issue:** #227  
**Current stage:** CANDIDATE PACKAGE + BROWSER REVIEW — WIP 1

EXP-06 is complete and merged. Before another historical tranche begins, package the
six-case evidence output as an exact **non-canonical candidate** and return exactly one:

- **PUBLISH_CANDIDATE**
- **HOLD_NO_RELEASE**
- **REWORK**

Canonical historical release **v0.6.1 remains unchanged**.

Candidate boundary:
- exact frozen EXP-06 target/source rows;
- manifest/checksums;
- QC summary;
- unresolved-issues list;
- thin human-facing map + evidence register;
- navigation/reference geometry only;
- explicit 3 bounded / 1 researched-inconclusive / 2 under-review states;
- 0 independent historical reviews.

Review must use the actual candidate artifact. Under-review and inconclusive must never
render as absence. Chámpa/Magadha frame/chronology limits, Yaghan internal uncertainty,
Mayapán aggregate limits, Mongol coerced-service/slavery separation and Khmer
capital/core-vs-polity extent must remain visible.

No new subject research, P-level, practice polygon, schema/API/database work, feature
discovery or next research tranche is authorized while #227 is active.

**Next exact action:** run the bounded browser review on the exact candidate, inspect
the browser evidence, and record PUBLISH_CANDIDATE / HOLD_NO_RELEASE / REWORK. If
REWORK, fix only concrete release-blocking defects and rerun the gate.


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

These are not eligible while #227 is active unless they block the candidate gate.

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

Do not let candidate review become platform drift. #227 does **not** authorize:

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
