# Historical Slavery Atlas — Backlog

**Updated:** 2026-09-25  
**Role:** canonical execution queue only; assumptions/risks/value evidence live in `docs/25_PROJECT_HEALTH.md`  
**Canonical historical data release:** `v0.6.1` (unchanged)  
**Current public preview:** `mvp-preview-ancient-v2` (non-canonical legacy demonstration)  
**Published research candidate:** `exp06-candidate-v1` at `exp06-candidate.html` (non-canonical)

This file answers **what is justified to work on next**.

---

# POST-R1 CUMULATIVE INTERNAL REVIEW — RESULT READY

**Issue:** #259  
**Mode:** review / release  
**Current stage:** REPLAY COMPLETE / MERGE GATE  
**Disposition:** **CUMULATIVE_NONCANONICAL_CANDIDATE**  
**Historical/source research:** **NONE PERFORMED**

Frozen 17-row replay result:
- 12 `ACCEPT_INTERNAL_REVIEW`;
- 5 `HOLD_EXISTING_EVIDENCE`;
- 0 narrowed;
- 0 rejected.

HOLD rows:
- Indus Valley Civilization — 2000 BCE;
- Hadhramaut — 500 BCE;
- Cuzco — 1300 CE;
- Chámpa — 500 CE;
- Magadha–Haryanka — 500 BCE.

Source/reconstructibility gate:
- 113 source relations inspected;
- 0 missing source/version refs;
- 0 missing independence groups;
- 0 missing claim-fitness fields;
- 0 within-target duplicate exact source versions;
- 1 cross-target exact dependency family: `angkor-personnel-corpus` across Angkor
  1200 and Khmer 1300.

Candidate ID: `post-r1-cumulative-review-v1`.

This is an **internal non-canonical review candidate** only. Independent historical
review remains 0. No public/canonical publication is authorized.

**Next mode after merge: MAINTENANCE / TRIGGER-BOUND REVIEW.**

Do not resume Qi or other intake automatically. Reopen for sponsor-authorized historical
intake, independent review, a concrete publication/consumer need, a demonstrated defect,
or new evidence satisfying a HOLD trigger.

v0.6.1 remains canonical.

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

D-096 governs continuation.

At a boundary choose the next justified **mode**:
1. discovery;
2. execution;
3. consolidation;
4. review/release;
5. maintenance;
6. no justified work.

WIP = one active priority, not one mandatory experiment.

Choose by:
1. evidence quality;
2. decision importance / project goal;
3. focus;
4. review/reconciliation capacity;
5. whole-project complexity;
6. only then execution convenience.

Elapsed time alone is not a stop rule, and unused capacity is not a reason to invent
another experiment.

Accepted methods may be used within their declared operational scope without re-proving
their value. Reopen them only on a concrete trigger recorded in D-096.

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
