# Current Project Status

For execution order, use repository-root `BACKLOG.md`. GitHub `main`, open issues/PRs and current CI override this snapshot.

**Status date:** 2026-09-23  
**Canonical historical data release:** v0.6.1 (unchanged)  
**Current public preview:** `mvp-preview-ancient-v2` (non-canonical)

## Current position

The atlas has a working end-to-end research, PostgreSQL/PostGIS, cartography, release, API and MapLibre path. The database is the working normalized research system; it has not silently replaced the immutable canonical v0.6.1 historical release.

Repository migrations currently run through `0029_claim_kind_function_privileges.sql`.

M1 methodology hardening and the M2 semantic/geography integration gate are complete. M2 survived an integrated adversarial process only after corrections for:

- reverse cross-table semantic integrity;
- chosen specialist-geometry provenance;
- open-terminus semantics.

The durable final M2 gate record is `docs/33_M2_INTEGRATED_ADVERSARIAL_GATE.md`.

## Current boundary

**#123 — M2 Project Health Check and reconciliation.**

This is intentionally a stopping point, not permission to keep building.

The health check must reconsider:

- the north star;
- demonstrated value **for and against** the project thesis;
- the strongest boring baseline;
- competing project identities;
- whether the artifact can shrink materially while preserving its contribution;
- architecture/governance complexity;
- assumptions, risks, privacy and reproducibility;
- whether H2 globally balanced evidence expansion is actually the best next horizon.

It must end with an explicit disposition: **continue / simplify / redirect / stop**.

Until #123 is complete, do not create a new broad execution runway, resume bulk evidence expansion, productionize the M2 experimental schema/resolver, promote the raw global geography baseline, or supersede canonical v0.6.1.

## M2 evidence now established

- D-058: post-M1 target semantics separate evidence, historical structure, workflow/outcome, temporal applicability/precision and spatial locus/inference extent.
- D-059: pinned Cliopatria calendar and POLITY/RELATION/composite behavior are explicit.
- #119: all 13,765 pinned Cliopatria features survived exact raw/staging ingestion and retry/no-op.
- #120/#135/#140: post-M1 relational semantics survived bounded and reverse-mutation adversaries, including restoration of non-positive open termini.
- #121/#136: complete selected-year resolution survived synthetic and exact full-corpus checks; specialist provenance remains distinct from baseline provenance.
- #122: integrated adversarial gate passed after two revise/correct/re-attack cycles.
- post-merge foundation CI, release reconstruction/security checks and public availability remained green.
- production/public release pointers remained unchanged throughout M2.

## Existing blockers

- **#43** — remaining protected staging/production boundary work requires sponsor/admin/credential action. Do not manufacture a workaround.
- **#26** — live migration-ledger metadata mismatch remains documented. Do not replay already-live schema migrations or rewrite production history casually.

These blockers do not decide #123.

## Canonical operating documents

- `docs/23_PROJECT_CHARTER.md`
- repository-root `BACKLOG.md`
- `docs/24_WAY_OF_WORKING.md`
- `docs/25_PROJECT_HEALTH.md`
- `docs/automation/hourly-worker.md`
- `docs/08_DECISIONS_LOG.md`

This file is only a subordinate status snapshot. It must never become a second execution queue.

## Important invariants

The atlas remains an evidence-synthesis/data-curation project. Territorial practice, legal regime, external participation, research coverage and geometry stay separate. Unknown is not absence. Raw/source-native values remain recoverable. Draft/reviewed/published/canonical are different states. Canonical releases are immutable.
