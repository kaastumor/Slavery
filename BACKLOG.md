# Historical Slavery Atlas — Backlog

**Updated:** 2026-09-25  
**Role:** canonical execution queue only; assumptions/risks/value evidence live in `docs/25_PROJECT_HEALTH.md`  
**Canonical historical data release:** `v0.6.1` (unchanged)  
**Current public preview:** `mvp-preview-ancient-v2` (non-canonical legacy demonstration)  
**Published research candidate:** `exp06-candidate-v1` at `exp06-candidate.html` (non-canonical)

This file answers **what is justified to work on next**.

---

# CURRENT MODE — OVERNIGHT CONTROLLED EXECUTION

**Controller issue:** #291  
**Stages complete on main:** 1–2  
**Stages 3–6:** complete on branch `post-v2-five-row-cumulative`, pending one review PR  
**Latest candidate after merge:** `post-r1-cumulative-review-v3-cross-frame`  
**Canonical historical data release:** `v0.6.1` unchanged  
**WIP:** one cumulative review/package branch

## Current programme result

EXP-14 Trans-Saharan 1300 is complete and merged.

The EXP-10-derived cross-frame programme is now closed:
- Karnak 1000 BCE — researched-inconclusive;
- Tōdai-ji 800 — bounded-supported near-anchor non-free status;
- Sápmi 1600 — bounded-supported state coercion, internal slavery unresolved;
- Trans-Saharan 1300 — bounded-supported network participation.

Five post-v2 rows (including Lithuania 1300) passed cumulative internal review.

Source reconciliation:
- v2 source relations: 133;
- post-v2 additions: 33;
- integrated lineage: 166;
- missing version/group/claim-fitness metadata: 0;
- new exact source-version overlap with v2: 0;
- new cross-target exact overlaps: 0.

D-099 packaging gate: **BUILD_SUCCESSOR_CANDIDATE**.

The successor `post-r1-cumulative-review-v3-cross-frame` is internal/noncanonical:
26 members, 21 accepted bounded evidence states, 5 HOLDs, 166 source relations,
2 preserved candidate-wide exact cross-target dependencies, 0 independent historical
reviews.

Next exact action:
1. merge the Stages 3–6 review/package PR after cheap CI;
2. record `NIGHT_STAGE_3_COMPLETE` through `NIGHT_STAGE_6_COMPLETE`;
3. perform Stage 7 next-horizon allocation from fresh main;
4. perform Stage 8 final QC/handoff and close #291.

No automatic canonical/public release, P-level, practice geometry, R1 mutation,
schema/ontology/database/API/frontend change or independent-review claim follows.

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
