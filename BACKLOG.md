# Historical Slavery Atlas — Backlog

**Updated:** 2026-09-23  
**Role:** canonical execution queue only; assumptions/risks/value evidence live in `docs/25_PROJECT_HEALTH.md`  
**Canonical historical data release:** `v0.6.1` (unchanged)  
**Current public preview:** `mvp-preview-ancient-v2` (non-canonical legacy demonstration)

This file answers **what is justified to work on next**.

---

# IDLE / SPONSOR DECISION BOUNDARY — COV-004 completed with METHOD SURVIVE

COV-004 / issue #157 was the final architecture-falsification gate in the COV-001→004 sequence.

Formal disposition:

> **METHOD SURVIVE.**

Product interpretation:

> **A boring map/register Atlas survives; bespoke Atlas-specific semantic machinery still does not beat the strongest ordinary map + register baseline.**

Durable result:
- `experiments/falsification-atlas/27_FINAL_RESULT.md`
- HC-009 in `docs/25_PROJECT_HEALTH.md`
- D-072 in `docs/08_DECISIONS_LOG.md`

## What survived

### Research method
- C0 broad target/research-state registration;
- C1 compact bounded research;
- selective C2 depth;
- source-quality failure as an explicit escalation/review trigger;
- source-to-claim dependency tracking;
- immutable/as-of releases and explicit later review events.

### Non-polity coverage
The experimental claim model successfully represented:
- sites/nodes;
- institutions/estates;
- mobile/trading networks;
- fuzzy community/region frames;

without forcing them into polity polygons.

### Real update mechanics
A frozen 2015-as-of test produced **3/6 genuine 2016–2026 evidence events**. Old snapshots remained auditable while later evidence could be represented as release-bound review/update state.

### Atlas presentation
A conventional world map + evidence register remains useful and compatible with:
- points;
- routes;
- fuzzy/unresolved regions;
- visible C0/unresearched targets;
- citations and bounded claims.

That is still a legitimate **Historical Slavery Atlas** presentation.

## What did not survive

### C1 safety without stronger QC
Masked replay found **1/6** material false negatives among supposedly non-escalated C1 rows: Chandela's positive event proposition exceeded the quality of its decisive citation.

Therefore production/public C1 requires source-quality escalation/review.

### Bespoke Atlas UI
The project-specific Atlas inspector materially beat the strong conventional map+register baseline on **0/4** frozen spatial/temporal tasks.

The map survives. Extra custom semantic UI does not currently earn separate infrastructure.

## Current execution state

**IDLE.**

COV-004 deliberately creates no fifth architecture experiment.

The next project-level choice is now sponsor-level:

1. preserve the project at the current evidence/method state; or
2. explicitly authorize the first **real lean systematic coverage programme** using C0/C1/selective-C2 plus an ordinary map/register atlas surface.

If option 2 is authorized, it must be operated as a research/release programme with QC and changelogs, not another architecture experiment and not a bulk automated ingestion.

## Still not authorized

- comprehensive world-history C1 completion;
- global C2 completion;
- automated mass research;
- production database/schema migration from these experimental rows;
- bespoke Atlas application/platform rebuild;
- claims of literal completeness;
- replacing specialist scholarship or specialist datasets.

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
