# Historical Slavery Atlas — Backlog

**Updated:** 2026-09-23  
**Role:** canonical execution queue only; assumptions/risks/value evidence live in `docs/25_PROJECT_HEALTH.md`  
**Canonical historical data release:** `v0.6.1` (unchanged)  
**Current public preview:** `mvp-preview-ancient-v2` (non-canonical legacy demonstration)

This file answers **what is justified to work on next**.

---

# ACTIVE — COV-001 coverage-value experiment setup (#148)

H2 / D-063 still controls the product boundary:

> **STOP ACTIVE ATLAS EXPANSION; PRESERVE METHOD/CORPUS/AUDIT ARTIFACTS**

COV-001 does **not** reverse that decision. It tests a different unresolved thesis:

> Does a small, systematically assembled global historical coverage corpus provide value because knowledge, uncertainty and research gaps are preassembled across place/time?

## Current state

**SETUP COMPLETE; HISTORICAL RESEARCH NOT STARTED.**

Durable setup:
- `experiments/coverage-value/00_PROTOCOL_PREREGISTERED.md`
- `experiments/coverage-value/01_BASELINE_LANDSCAPE.md`
- `experiments/coverage-value/02_SETUP_ADVERSARY.md`
- `experiments/coverage-value/03_PROTOCOL_REVISED.md`
- `experiments/coverage-value/04_EXECUTION_PACKET.md`
- `experiments/coverage-value/select_sample.py`
- `experiments/coverage-value/coverage_row_template.json`

The setup adversary returned **REVISE** and corrected:
- polity-only sampling bias by adding four fixed non-polity challenge contexts;
- index-shaped/task tautology by adding a plain ordinary-matrix baseline;
- architecture creep by requiring plain CSV/JSON/Markdown only;
- same-model contamination through preferred isolated evaluation runs;
- global-handbook coverage coding and language/access limitations.

## Only justified next action

1. obtain the exact pinned Cliopatria asset;
2. run `select_sample.py`;
3. verify >=18/24 deterministic polity-year cells are valid;
4. commit the generated `sample.json`;
5. **only then** begin bounded research for the frozen cells plus NP-01..NP-04.

If the sampler yields fewer than 18 valid cells, revise the sampling frame **before** any slavery/coercion research.

## Still explicitly not authorized

- H3 bulk/global research expansion;
- canonical release changes;
- M2 production migration;
- Atlas frontend/map/product expansion;
- new database/API/service infrastructure;
- autonomous bulk-research workers;
- treating missing evidence as historical absence.

A positive COV-001 result could authorize at most one further bounded **corpus-scale** value test. It cannot restart the old Atlas roadmap.

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
