# Historical Slavery Atlas — Backlog

**Updated:** 2026-09-24  
**Role:** canonical execution queue only; assumptions/risks/value evidence live in `docs/25_PROJECT_HEALTH.md`  
**Canonical historical data release:** `v0.6.1` (unchanged)  
**Current public preview:** `mvp-preview-ancient-v2` (non-canonical legacy demonstration)

This file answers **what is justified to work on next**.

---

# ACTIVE R1.7 / MVP — crystallize the surviving core

**Parent programme:** #159
**R1.6 QC:** #172
**Decision:** D-080
**Current stage:** **R1.7 — MVP v0.1 candidate release + boring Atlas surface**

R1.6 passes with explicit unresolved limitations.

The project is no longer expanding historical subject research.

The MVP is the smallest artifact that preserves the surviving value:

> **immutable R1 candidate package + neutral world map + explicit geometry/research states + compact evidence register**

## Frozen evidence core

- 77 frozen targets;
- 19 reviewed C1;
- 15 planned-C1 but intentionally unresearched;
- 2 held;
- 41 C0-only;
- 45 source relations;
- 37 independence groups;
- v0.6.1 remains canonical until R1.8.

## MVP rules

- read-only/static by default;
- no production database migration;
- no new backend/service/search stack;
- no target substitution or new subject research;
- neutral world land always visible;
- geometry may remain unresolved;
- unresearched/inconclusive/held != absence;
- review state and language/access limitations visible;
- temporal display uses R1.6 render guards;
- compact evidence register is the primary truth surface; map is navigation.

## Delivery order

Parent: **#174 — MVP v0.1**

Fixed serial MVP queue:

1. #175 — frontend reproducibility and build lock
2. #176 — deterministic static candidate bundle
3. #177 — explicit geometry representation manifest
4. #178 — static candidate as default web data path
5. #179 — research-state map / overview semantics
6. #180 — compact evidence register / target detail
7. #181 — temporal truth rendering guard
8. #182 — technical MVP gate / release-candidate handoff

The worker completes at most one atomic issue per run, WIP=1, with green CI before merge.

After #182 records **TECHNICAL_MVP_CANDIDATE**, discovery parent #183 opens the evidence-only queue:
#184 -> #185 -> #186 -> #187.

Discovery issues produce dispositions, not production features.

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
