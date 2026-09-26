# Historical Slavery Atlas — Backlog

**Updated:** 2026-09-25  
**Role:** canonical execution queue only; assumptions/risks/value evidence live in `docs/25_PROJECT_HEALTH.md`  
**Canonical historical data release:** `v0.6.1` (unchanged)  
**Current public preview:** `mvp-preview-ancient-v2` (non-canonical legacy demonstration)  
**Published research candidate:** `exp06-candidate-v1` at `exp06-candidate.html` (non-canonical)

This file answers **what is justified to work on next**.

---

# CURRENT MODE — REVIEW / RELEASE

**Active issue:** #288 — post-D099 Sápmi/Tōdai delta review  
**Reviewed delta:** EXP-12 Sápmi 1600 + EXP-13 Tōdai-ji 800  
**Immutable base candidate:** `post-r1-cumulative-review-v2-overnight`  
**Earlier reviewed delta:** Lithuania 1300 + Karnak 1000 BCE (D-099; separate)  
**Canonical historical data release:** `v0.6.1` unchanged  
**WIP:** 1

No new historical/source research is authorized inside this review.

Current branch review result:
- Sápmi 1600 — `ACCEPT_INTERNAL_REVIEW`;
- Tōdai-ji 800 — `ACCEPT_INTERNAL_REVIEW`;
- source reconciliation — `RECONCILIATION_PASS`;
- 15 new source relations;
- 0 missing source-version / independence-group / claim-fitness fields;
- 0 exact source-version overlap with v2;
- 0 exact overlap with the Lithuania/Karnak reviewed delta;
- 0 exact Sápmi ↔ Tōdai source-version overlap.

Packaging gate:
**`KEEP_REVIEWED_DELTA_SEPARATE`**.

This is a positive internal-review result, not a canonical/public release.

D-099 remains sufficient: no successor candidate is created merely because another
pair of rows passed review. v2 and the earlier reviewed delta remain immutable.

Next exact action: structural sanitation → one coherent PR → cheap scoped CI → merge →
close #288 → return to D-096 mode selection.

After closure, the Trans-Saharan trade network — 1300 is the only EXP-10-qualified row
without subject research. That fact is a state description, not an automatic execution
instruction.

No P-level, practice geometry, R1 state mutation, schema/ontology/database/API/frontend
change, canonical/public release or independent-review claim.

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
