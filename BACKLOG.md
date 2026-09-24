# Historical Slavery Atlas — Backlog

**Updated:** 2026-09-24  
**Role:** canonical execution queue only; assumptions/risks/value evidence live in `docs/25_PROJECT_HEALTH.md`  
**Canonical historical data release:** `v0.6.1` (unchanged)  
**Current public preview:** `mvp-preview-ancient-v2` (non-canonical legacy demonstration)

This file answers **what is justified to work on next**.

---

# ACTIVE PRESENTATION HORIZON — EXP-04 Research Preview

**Active issue:** #221  
**Current stage:** IMPLEMENTATION / PRESENTATION TEST — WIP 1

EXP-04 (#213, merged #220) completed its eight-case method/representation test with
**SUCCESS — PORTABLE CONTRACT SURVIVES EXP-04**. Five targets are
`researched_internal`, three remain `under_review / unassessed`, and zero EXP-04
targets are independently historically reviewed.

Canonical v0.6.1 is unchanged.

Current horizon: make that experimental package inspectable without promoting it to
canonical/public historical data.

Implementation boundary:
- deterministic EXP-04 preview JSON generated from the checked-in target/source tables;
- separate static `web/research-preview.html` page;
- reuse existing Vite + MapLibre stack;
- neutral land always visible;
- navigation/reference markers only; no practice polygons;
- map marker state reflects research stage only, never historical intensity;
- table/detail view exposes bounded proposition, abstention, temporal state,
  evidence-locus/inference-extent distinction, category notes, access limits and
  source-family dependencies.

The preview must keep Indus, Hadhramaut and Cuzco visibly under review and must preserve
Andaman's external-colonial-positive / indigenous-internal-unassessed split.

**Next:** finish deterministic bundle/build checks, run one scoped PR CI cycle, deploy
through the existing GitHub Pages path, then inspect the live preview for misleading
compression. Any visual failure is a presentation/representation finding, not permission
to strengthen the historical rows.

Project form remains: portable reviewed evidence core + replaceable Atlas/map/table/API
views. No production API/database mutation, schema migration or platform expansion is
authorized by #221.

## Sponsor-visible milestone

The current WIP **is** the sponsor-visible milestone: a non-canonical EXP-04
**map + table** research preview.

Acceptance:
- all eight frozen targets visible;
- 5 internal / 3 under-review / 0 independently-reviewed counts remain explicit;
- reference points are labeled navigation-only;
- under-review is never styled as absence;
- source counts never determine marker size/intensity;
- canonical v0.6.1 and existing R1 candidate stay untouched;
- page is reproducibly built and viewable from the ordinary static deployment path.


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

These are not eligible while #221 is active unless they block the preview.

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

Do not let the presentation test become platform drift. #221 does **not** authorize:

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
