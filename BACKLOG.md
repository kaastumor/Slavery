# Historical Slavery Atlas — Backlog

**Updated:** 2026-09-26  
**Role:** canonical execution queue only; assumptions/risks/value evidence live in `docs/25_PROJECT_HEALTH.md`  
**Canonical research authority:** PostgreSQL/PostGIS, explicit governed membership under D-109  
**Canonical historical data release:** `v0.6.1` (unchanged)  
**Current public preview:** `mvp-preview-ancient-v2` (non-canonical legacy demonstration)  
**Published research candidate:** `exp06-candidate-v1` at `exp06-candidate.html` (non-canonical)

This file answers **what is justified to work on next**.

---

# CURRENT MODE — REVIEW / RELEASE + DATABASE CANONICALIZATION

**Parent gate:** #300 — canonical PostgreSQL + first DB-backed release gate  
**Gate 0:** **PASS — MIGRATION_HISTORY_RECONCILED**  
**Gate 1:** **PASS — V061_DB_RECONCILED**  
**Gate 2:** **PASS — V3_DB_RECONCILED**  
**Gate 3:** **PASS — PROMOTE_DB_CANONICAL_RESEARCH_STATE**  
**Current gate:** Gate 4 — first DB-backed canonical historical release  
**Canonical historical data release:** `v0.6.1` unchanged  
**Frozen reviewed input:** `post-r1-cumulative-review-v3-cross-frame`  
**WIP:** #319 — first DB-backed canonical release

## Gate 3 closeout

D-109 makes PostgreSQL/PostGIS authoritative for the project's explicitly governed
current research closure.

Frozen authority baseline `gate3-db-authority-proof-v1`:

- schema head 0033;
- 40 claims;
- 11 actors;
- 18 spatial entities;
- 0 reviewed historical geometries;
- 8 voyages;
- 99 coverage assessments;
- 211 exact source versions;
- 26 research-target results;
- membership SHA-256
  `ebc9d32f09857744841a0cf92699c41739b624ac4bd94c43798eb1f61e3b0dd3`;
- production database-state SHA-256
  `31b7a7b675445e5758ffd68d64ff0f0cde83df1b0ea65f29835246deb2ae26ff`;
- fresh-database logical recovery: PASS;
- exact research-object digest reconstruction: PASS;
- D-108 portable cartography fingerprint: PASS;
- private Data API boundary: PASS;
- Supabase security advisor: 0 lints;
- independent historical review: 0.

Authority is defined by explicit governed membership, not physical row presence or
`review_status` alone. Legacy preview/prototype rows remain outside the Gate-3 authority
closure unless explicitly admitted later.

The Supabase Free plan does not provide verified managed backup/PITR evidence to the
project's current management probe. Gate 3 proves preservation-grade logical recovery,
not physical cluster backup or arbitrary draft-row recovery.

No canonical historical release or public channel moved in Gate 3.

## Gate 4 exact question

Can the project produce the first immutable DB-backed canonical historical release from
the D-109 authority closure without weakening provenance, uncertainty, review state or
release immutability?

Provisional release version: **v0.7.0**, unless Gate-4 work discovers a
compatibility-breaking ontology change.

Required before publication:

1. exact release membership derived from the governed DB authority boundary;
2. predecessor v0.6.1 identity/checksum retained;
3. reviewed v3 evidence and HOLD/inconclusive states preserved losslessly;
4. schema/methodology/release-contract versions recorded;
5. exact source/source-version information retained;
6. changelog, QC summary and unresolved-issues list included;
7. migration/reconciliation report included;
8. deterministic manifest/checksums and independent rebuild verification;
9. immutable published release artifacts;
10. explicit review/publication states and truthful independent-review count;
11. no legacy preview/prototype leakage through broad `review_status` selection;
12. public release channel remains unchanged until Gate 5.

Allowed Gate-4 disposition:

- `PUBLISH_DB_BACKED_CANONICAL_RELEASE`;
- `HOLD_RELEASE_CANDIDATE`;
- `REWORK_RELEASE_BUILDER`.

No UI/API cutover follows until Gate 4 separately passes.

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

These remain trigger-bound and are not the default horizon.

## #43 — protected staging / release-promotion administration

Remaining protected environment / staging work matters only when Gate 5/public
promotion actually requires it.

## #26 — migration-history reconciliation

**Closed / historical.** Gate 0 passed `MIGRATION_HISTORY_RECONCILED`. Do not reopen the
old mismatch as active work unless a new concrete migration-history inconsistency is
observed.

## Managed backup/PITR

Current Supabase Free-plan recovery evidence is logical/preservation-grade rather than
physical managed backup/PITR. Revisit if plan/capabilities change or operational
durability becomes a release requirement; do not require a paid temporary branch merely
for process ceremony.

## Repository administration

- `main` currently reports unprotected;
- historical remote topic branches remain;
- current integration lacks some repository-admin capability.

Handle when it materially blocks evidence/release work; do not turn administration into
the project horizon.

---

# Explicitly NOT the current horizon

Gate 4 does **not** authorize:

- new historical subject research;
- UI/API cutover;
- frontend redesign;
- PMTiles/vector-tile infrastructure expansion;
- new search service;
- graph database;
- vector store/RAG infrastructure;
- generic ontology/platform work;
- contributor/peer-review platform;
- new autonomous infrastructure for its own sake;
- external recruitment/review;
- automatic public-channel movement.

The current priority is one bounded release task: prove or reject the first DB-backed
canonical historical release.
