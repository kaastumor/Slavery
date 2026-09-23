# Historical Slavery Atlas — Backlog

**Updated:** 2026-09-23  
**Role:** canonical execution queue only; assumptions/risks/value evidence live in `docs/25_PROJECT_HEALTH.md`  
**Canonical historical data release:** `v0.6.1` (unchanged)  
**Current public preview:** `mvp-preview-ancient-v2` (non-canonical legacy demonstration)

This file answers **what is justified to work on next**.

---

# IDLE / PRESERVATION — H2 stop rule triggered

H2 / issue #146 completed the value-discrimination pilot authorized after HC-003.

Final disposition:

> **STOP ACTIVE ATLAS EXPANSION; PRESERVE METHOD/CORPUS/AUDIT ARTIFACTS**

Durable result:
- `experiments/h2-value-discrimination/09_FINAL_RESULT.md`
- HC-004 in `docs/25_PROJECT_HEALTH.md`
- D-063 in `docs/08_DECISIONS_LOG.md`

The pre-registered project-value threshold was not met:
- Atlas corpus/method materially beat the strongest baseline in **1/3** cases;
- the repaired thin query/visual arm materially beat the corpus/method in **0/3** cases.

Do **not** manufacture a successor horizon to escape the result.

## What is justified now

Routine preservation and bounded maintenance only:
- keep canonical/release artifacts reconstructible;
- repair security, link/source rot, CI breakage or repository decay when it threatens preserved artifacts;
- handle parked operational debt only when its existing trigger becomes real;
- retain the H2 negative result and M1/M2 adversarial evidence.

A new Atlas-development experiment requires a **new external trigger** showing a concrete failure of the strongest simpler workflow. Internal desire to add more data/features is not such a trigger.

## Explicitly not authorized

- H3 broad/global research expansion;
- M2 production schema migration;
- bulk Cliopatria source-row → atlas identity publication;
- another frontend/map redesign;
- PMTiles/vector-tile expansion;
- search/vector/RAG/graph/ontology infrastructure;
- new research platform/gazetteer/reconciliation services;
- contributor/peer-review platform;
- production-like monitoring/self-heal;
- autonomous build/research runway.

If no new external trigger exists, **idle is the correct state**.

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
