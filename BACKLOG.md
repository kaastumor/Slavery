# Historical Slavery Atlas — Backlog

**Updated:** 2026-09-24  
**Role:** canonical execution queue only; assumptions/risks/value evidence live in `docs/25_PROJECT_HEALTH.md`  
**Canonical historical data release:** `v0.6.1` (unchanged)  
**Current public preview:** `mvp-preview-ancient-v2` (non-canonical legacy demonstration)

This file answers **what is justified to work on next**.

---

# EXP-06 RELEASE GATE — PUBLISH_CANDIDATE

**Issue:** #227  
**Current stage:** FINAL MERGE + STATIC DEPLOYMENT VERIFICATION

EXP-06 candidate v1 passed its bounded publish/hold/rework gate after one concrete
responsive-layout repair.

Disposition: **PUBLISH_CANDIDATE**.

Reviewed candidate evidence:
- historical source commit `16906affed159722cf940e6723401c7ab4e5d9f4`;
- successful browser run `36054132409`;
- browser job `107816768565`;
- browser artifact `10831472682`;
- zero page errors / zero semantic failures after rework.

Candidate semantics:
- 3 bounded internal;
- 1 researched inconclusive;
- 2 under review;
- 0 independently reviewed;
- no P-levels;
- no historical practice polygons;
- canonical v0.6.1 unchanged.

The candidate package includes manifest/checksums, QC, unresolved issues, exact
portable CSVs and `REVIEW_DECISION.md`.

**Next exact action:** merge PR #228 if ordinary checks remain green, verify Pages
deployment of `exp06-candidate.html`, close #227, then select the next bounded
historical evidence horizon by expected information gain.

Do not insert another application/product horizon. Candidate publication itself does
not authorize canonical promotion or new feature work.


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
