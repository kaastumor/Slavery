# Historical Slavery Atlas — Backlog

**Updated:** 2026-09-23  
**Role:** canonical execution queue only; assumptions/risks/value evidence live in `docs/25_PROJECT_HEALTH.md`  
**Canonical historical data release:** `v0.6.1` (unchanged)  
**Current public preview:** `mvp-preview-ancient-v2` (non-canonical legacy demonstration)

This file answers **what is justified to work on next**.

Detailed completed-work history belongs in GitHub issues/PRs, the Decisions Log and durable gate/audit records. It is intentionally not repeated here.

---

# ACTIVE — H2 value-discrimination pilot (#146)

Explicit sponsor authorization on 2026-09-23 activates one bounded experiment:

> **Does the corpus/method, and then the smallest thin atlas/query representation, materially improve difficult historical reasoning over the strongest competent boring baseline?**

Execution order is fixed:

1. pre-register protocol and cases;
2. adversarially attack the setup;
3. revise or reject the setup before historical execution;
4. run all three historical questions against the same-source three-arm comparison;
5. reconcile value evidence and choose **continue / simplify / redirect / stop**.

The issue is #146. Durable experiment artifacts live under `experiments/h2-value-discrimination/`.

This authorization does **not** reopen:
- M2 production migration;
- bulk/global research expansion;
- bulk Cliopatria publication;
- frontend/platform expansion;
- new infrastructure/monitoring;
- an automatic successor horizon.

After #146 is decided, the queue returns to IDLE unless a new horizon is explicitly authorized.

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
