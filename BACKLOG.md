# Historical Slavery Atlas — Backlog

**Updated:** 2026-09-23  
**Role:** canonical execution queue only; assumptions/risks/value evidence live in `docs/25_PROJECT_HEALTH.md`  
**Canonical historical data release:** `v0.6.1` (unchanged)  
**Current public preview:** `mvp-preview-ancient-v2` (non-canonical legacy demonstration)

This file answers **what is justified to work on next**.

---

# IDLE / PRESERVATION — COV-001 completed with NARROW SURVIVE

COV-001 / issue #148 tested a distinct post-H2 thesis:

> Does a systematically assembled global historical coverage corpus create reusable value even when the bespoke Atlas product does not?

Final result:

> **NARROW SURVIVE — COVERAGE CORPUS VALUE EXISTS; ATLAS PRODUCT EXPANSION REMAINS STOPPED**

Durable result:
- `experiments/coverage-value/11_FINAL_RESULT.md`
- HC-005 in `docs/25_PROJECT_HEALTH.md`
- D-065 in `docs/08_DECISIONS_LOG.md`

After adversarial downgrade, **4/6** fixed global tasks showed material value:
- law vs practice;
- network/participation vs territorial inference;
- global-handbook coverage visibility;
- unresolved/gap visibility.

The basic overview reached parity with a competent ordinary matrix, and the terminology query was not counted because one ordinary spreadsheet column could reproduce most of that gain.

Both negative controls behaved correctly:
- specialist narrative beat the index on deep Champa historiography;
- SlaveVoyages beat the index on voyage-level/quantitative work.

## What survives

A small, auditable, explicitly incomplete **coverage corpus** may be worth further investigation as a flat table/JSON/CSV:
- what can be said for a place/time target;
- what cannot be said;
- why research remains inconclusive/disputed;
- law/practice/network distinctions;
- source/provenance;
- whether global syntheses directly cover the target.

This is not authorization for the old Atlas application.

## Current execution state

**IDLE.**

COV-001 permits at most one future bounded **corpus-scale economics/reuse experiment**, but no such experiment is currently authorized.

The unresolved question is:

> Does corpus value grow faster than research/review/update cost at materially larger scale?

Do not answer that by simply researching more cells.

## Still explicitly not authorized

- H3 bulk/global evidence expansion;
- canonical release changes;
- M2 production migration;
- Atlas frontend/map/product expansion;
- new database/API/service infrastructure;
- autonomous bulk-research workers;
- search/vector/RAG/graph/ontology infrastructure;
- claims of literal historical completeness.

If a further scale test is authorized, it must test reuse/maintenance economics and strongest-baseline parity, not record-count growth.

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
