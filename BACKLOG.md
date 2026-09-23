# Historical Slavery Atlas — Backlog

**Updated:** 2026-09-23  
**Role:** canonical execution queue only; assumptions/risks/value evidence live in `docs/25_PROJECT_HEALTH.md`  
**Canonical historical data release:** `v0.6.1` (unchanged)  
**Current public preview:** `mvp-preview-ancient-v2` (non-canonical legacy demonstration)

This file answers **what is justified to work on next**.

---

# ACTIVE — COV-002 scale/reuse economics (#151)

COV-001 survived narrowly as a flat coverage-corpus thesis. The sponsor has now explicitly authorized the one further bounded experiment permitted by D-065:

> **Does coverage-corpus value grow faster than research, review and update burden when the corpus becomes materially larger?**

This does **not** reopen Atlas product expansion.

## Current state

**PROTOCOL + SETUP ADVERSARY COMPLETE; SAMPLE NOT YET FROZEN; HISTORICAL RESEARCH NOT STARTED.**

Durable setup:
- `experiments/coverage-scale/00_PROTOCOL_PREREGISTERED.md`
- `experiments/coverage-scale/01_SETUP_ADVERSARY.md`
- `experiments/coverage-scale/02_PROTOCOL_REVISED.md`
- `experiments/coverage-scale/select_expansion.py`
- `tests/test_cov002_expansion_selector.py`

The experiment compares:
- F — full COV-001 row;
- R — compact coverage register containing only demonstrated-value fields;
- M — strongest ordinary research matrix.

It tests:
- reuse at N=25, 31 and 37;
- review-surface growth;
- information loss F→R;
- six deterministic maintenance shocks;
- specialist/specialized-data/single-cell negative controls.

## Only justified next action

1. generate the exact deterministic 12-cell rank-2 cohort from the pinned Cliopatria asset;
2. freeze `expansion_sample.json`;
3. remove the one-off networked freeze probe;
4. **only then** research those 12 cells.

No cell may be substituted after slavery/coercion evidence is inspected.

## Hard boundary

Still not authorized:
- H3 bulk/global research;
- comprehensive ingestion;
- canonical release change;
- Postgres/API/frontend/map work;
- automated bulk research;
- Atlas product revival.

COV-002 ends with STOP, REDIRECT, or NARROW SUSTAIN. It does not create its own successor horizon.

---

# PARKED / trigger-bound operational debt

These are not eligible autonomous work.

## #43 — protected staging / release-promotion administration

Remaining protected environment / staging work matters only if production mutation or a new public release is again justified.

Current controls intentionally reduce mutation:
- production geometry promotion is manual/explicit;
- current preview has static fallback;
- no new production migration is authorized.

Do not create paid staging or new credentials merely to close this issue.

## #26 — live Supabase migration-history reconciliation

The documented live history mismatch remains real.

Do not rewrite migration history casually. Reconcile it only before a future production migration/change actually requires that boundary.

## Repository administration

Not represented as a new issue/queue:
- `main` currently reports unprotected;
- approximately 100 historical remote topic branches remain;
- current integration lacks the repository-admin capability needed for branch protection/bulk pruning.

Handle when an admin-capable maintenance opportunity exists. Do not let it create a development horizon.

## Frontend reproducibility

A real `web/package-lock.json` is still absent.

Generate and commit the genuine lockfile in a networked environment before the next substantive frontend change. Do not invent one offline and do not add package-management infrastructure merely for this.

---

# Explicitly NOT next

Do not next start:

- M2 production schema migration;
- bulk/global H2 evidence expansion;
- bulk Cliopatria source-row → atlas identity publication;
- another frontend redesign;
- PMTiles/vector-tile infrastructure;
- new search service;
- graph database;
- vector store/RAG infrastructure;
- generic ontology/platform work;
- generic digital-humanities research UI;
- custom gazetteer/reconciliation service;
- RDF/CIDOC/PROV infrastructure without a real consumer;
- contributor/peer-review platform;
- new monitoring/self-healing machinery;
- new autonomous execution runway.

If the repository has no explicitly authorized issue after HC-003, **idle is the correct state**.
