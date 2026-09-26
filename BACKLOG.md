# Historical Slavery Atlas — Backlog

**Updated:** 2026-09-26  
**Role:** canonical execution queue only; assumptions/risks/value evidence live in `docs/25_PROJECT_HEALTH.md`  
**Canonical historical data release:** `v0.6.1` (unchanged)  
**Current public preview:** `mvp-preview-ancient-v2` (non-canonical legacy demonstration)  
**Published research candidate:** `exp06-candidate-v1` at `exp06-candidate.html` (non-canonical)

This file answers **what is justified to work on next**.

---

# CURRENT MODE — REVIEW / RELEASE + DATABASE CANONICALIZATION

**Parent gate:** #300 — canonical PostgreSQL + first DB-backed release gate  
**Gate 0:** **PASS — MIGRATION_HISTORY_RECONCILED**  
**Gate 1:** **PASS — V061_DB_RECONCILED**  
**Current gate:** Gate 2 — v3 reviewed-evidence DB reconciliation  
**Canonical historical data release:** `v0.6.1` unchanged  
**Frozen reviewed input:** `post-r1-cumulative-review-v3-cross-frame`  
**WIP:** Gate 2 mapping/ingestion design only under #300

## Gate 1 closeout

The guarded v0.6.1 repair was applied once atomically to production.

Restored:
- 288 raw workbook rows;
- 36 evidence-sheet coverage-source links;
- 22 global semantic mappings over 18 positive/disputed workbook rows;
- 18 territorial-practice claims;
- 3 external-participation claims;
- 1 legal-event claim;
- 29 exact global source versions.

Preserved:
- 8 voyages;
- 11 actors;
- 12 voyage-owner rows;
- Atlantic crosswalks and owner semantics;
- canonical workbook source/version/asset + checksum lineage;
- 99 coverage assessments;
- public release membership and `public_mvp_preview` channel;
- zero auto-assigned P-levels;
- no new practice geometry.

Live regression after repair:
- unchanged `db/tests/002_v061_reconciliation.sql`: PASS;
- `db/tests/001_schema_smoke.sql`: PASS;
- `db/tests/009_claim_kind_integrity.sql`: PASS;
- Supabase security advisor: 0 lints;
- anon/authenticated internal-schema grants: none.

Blocking QC `V061_LIVE_RECONCILIATION_INCOMPLETE` is resolved with live evidence.

The old draft `0.6.1-db-migration-candidate` manifest is not promoted and the public
channel does not move. The current D-054 full-state bundle contract is intentionally
territorial-preview-only and therefore is **not** used to represent the broader
canonical v0.6.1 database state. A canonical full-state release contract remains a
Gate 3/4 requirement.

## Gate 2 exact question

Can frozen v3 reviewed evidence be represented in the existing database without
semantic loss?

Must preserve:
- target/frame/anchor identity;
- bounded proposition + required abstention;
- temporal precision and uncertainty;
- evidence locus vs inference extent;
- territorial vs external/network vs legal dimensions;
- HOLD and researched-inconclusive as non-absence;
- source/version identity;
- dependency/independence groups;
- claim fitness;
- internal-review provenance;
- unresolved geometry;
- P-level null unless independently justified.

Prefer the existing schema. Any material representational loss is a schema-decision gate,
not a reason to bury semantics in generic notes.

No DB authority flip, canonical release, public-channel move or UI cutover follows until
Gate 2 and later gates pass.

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
