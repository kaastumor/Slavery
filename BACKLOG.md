# Historical Slavery Atlas — Backlog

**Updated:** 2026-09-25  
**Role:** canonical execution queue only; assumptions/risks/value evidence live in `docs/25_PROJECT_HEALTH.md`  
**Canonical historical data release:** `v0.6.1` (unchanged)  
**Current public preview:** `mvp-preview-ancient-v2` (non-canonical legacy demonstration)  
**Published research candidate:** `exp06-candidate-v1` at `exp06-candidate.html` (non-canonical)

This file answers **what is justified to work on next**.

---

# OVERNIGHT READY-QUEUE PROGRAMME — ACTIVE

**Issue:** #262  
**Mode:** execution → consolidation → review/release  
**Sponsor authorization:** 2026-09-25 overnight run  
**Historical intake:** authorized only for the four frozen/qualified targets below

**Morning goal:** research and internally review the currently ready historical queue,
then produce one cumulative non-canonical successor candidate or explicit HOLD.

Frozen overnight targets:
1. Qi — 500 BCE — `R1:P:-500:F:r2`
2. Swahili maritime trade network — 1400 — `R1:N:swahili_1400`
3. Ifugao communities — 1700 — `R1:N:ifugao_1700`
4. Khanate of Kokand — 1800 — `R1:P:1800:E:r1`

Execution order and run contracts are canonical in issue #262.

Eight-run sequence:
1. Qi subject research / close EXP-08;
2. Swahili subject research;
3. Ifugao subject research;
4. Kokand subject research;
5. four-case reconciliation/source dependency audit;
6. cumulative adversarial internal review;
7. integrate admitted rows into a new immutable non-canonical successor candidate;
8. final QC + adversarial morning gate + handoff.

WIP=1. Each run must finish/reconcile previous open WIP before advancing.
No fifth target, no P-level, no geometry promotion, no automatic public/canonical
release, and no threshold weakening to finish by morning.

Canonical v0.6.1 remains unchanged.

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
