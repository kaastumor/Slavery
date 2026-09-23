# Historical Slavery Atlas — Backlog

**Updated:** 2026-09-23  
**Role:** canonical execution queue only; assumptions/risks/value evidence live in `docs/25_PROJECT_HEALTH.md`  
**Canonical historical data release:** `v0.6.1` (unchanged)  
**Current public preview:** `mvp-preview-ancient-v2` (non-canonical legacy demonstration)

This file answers **what is justified to work on next**.

---

# ACTIVE — COV-003 tiered systematic coverage (#155)

ADV-001 / D-068 reopened one narrow methodological hypothesis:

> Can a tiered, versioned, batch-curated coverage architecture preserve the demonstrated cross-history value without reproducing COV-002's row-by-row research/maintenance model?

The sponsor explicitly authorized COV-003.

## Frozen architecture

- **C0:** target/research-state register; no slavery conclusion required.
- **C1:** compact evidence/coverage record for a preregistered subset.
- **C2:** selective deep packet only when a frozen escalation rule justifies it.
- flat JSON/CSV/Markdown only;
- immutable/as-of experiment releases;
- no Atlas product/database/API/frontend work.

## Frozen sample

Pinned Cliopatria source unchanged.

Three deterministic batches:
- `-500:F`
- `1300:E`
- `-500:E`

Total:
- 24 new C0 targets;
- 12 preregistered C1 research targets;
- 12 C0-only targets that cannot be promoted after evidence inspection;
- 6 deterministic identity-validation probes;
- at most 3 C2 escalations after C1 freeze.

Durable setup:
- `experiments/coverage-tiered/00_PROTOCOL_PREREGISTERED.md`
- `experiments/coverage-tiered/01_SETUP_ADVERSARY.md`
- `experiments/coverage-tiered/02_SAMPLE_FREEZE.md`
- `experiments/coverage-tiered/sample.json`

## Current execution state

**C1 BATCH RESEARCH ACTIVE; C1 NOT YET FROZEN.**

The next justified work is only:
1. freeze six C0 identity-validation results;
2. freeze the three shared-source packets;
3. freeze the twelve C1 outcomes;
4. evaluate source reuse against the COV-002 row-centric baseline;
5. apply the preregistered C2 escalation rule;
6. test versioned maintenance, coverage/bias function and emergent queries;
7. adversarially disposition the result.

## Hard boundary

COV-003 is not comprehensive ingestion.

Still not authorized:
- research beyond the 12 frozen C1 targets except the <=3 frozen C2 escalations and 3 maintenance searches;
- promotion of C0-only targets because an interesting source appears;
- canonical release changes;
- M2 production migration;
- Atlas/frontend/map/platform work;
- autonomous successor experiment;
- literal “all known history” claims.

COV-003 ends at its own gate.

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
