# Historical Slavery Atlas — Backlog

**Updated:** 2026-09-24  
**Role:** canonical execution queue only; assumptions/risks/value evidence live in `docs/25_PROJECT_HEALTH.md`  
**Canonical historical data release:** `v0.6.1` (unchanged)  
**Current public preview:** `mvp-preview-ancient-v2` (non-canonical legacy demonstration)

This file answers **what is justified to work on next**.

---

# RESTING STATE — portable evidence core + replaceable Atlas views

**Decisions:** D-081, D-083, D-084, D-085, D-086, D-087  
**Current stage:** **PRESERVATION / IDLE — no active delivery or discovery successor**

The current best-supported project form is:

> **portable reviewed evidence core + replaceable Atlas/map/table/API views**

## What is complete

- R1 — **HOLD_NO_RELEASE**;
- EXP-02 — **PORTABLE CORE SURVIVES + SIMPLIFY CANDIDATE**;
- project-form reassessment #209 — **SIMPLIFY + PRESERVE ATLAS AS VIEW**.

## What this means

- PostgreSQL/PostGIS remains valid research/curation infrastructure;
- immutable evidence packages are the preferred release/interchange boundary;
- a map/web/API/table is a presentation adapter, not the owner of historical truth;
- the project remains the Historical Slavery Atlas;
- no canonical schema/data migration follows from EXP-02;
- v0.6.1 remains canonical;
- external-user value remains intentionally untested.

## No active successor

Do **not** automatically start:

- R2;
- global or tranche-based subject research;
- geometry completion;
- public-candidate publication;
- frontend redesign;
- portable-package productization;
- schema simplification/migration;
- new API/backend work;
- search/graph/timeline/comparison features;
- external recruitment or review;
- another internal discovery experiment.

## Reopen triggers

A bounded evaluation may be opened only when a concrete trigger appears, for example:

- an actual internal research/release task that the portable package cannot safely represent;
- mixed resolved/unresolved geometry that invalidates the frozen-set simplification;
- a real comparison/navigation task where an ordinary map/GIS view materially beats the table/register baseline;
- a scale/reconstruction failure of the portable package;
- explicit sponsor authorization for external/public-value testing;
- a new systematic-coverage objective whose methodological question was not already answered by COV/R1.

A trigger authorizes evaluation, not automatic implementation.

Durable project-form review: `docs/26_PROJECT_FORM_AFTER_EXP02.md`.

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
