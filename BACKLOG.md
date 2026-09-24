# Historical Slavery Atlas — Backlog

**Updated:** 2026-09-24  
**Role:** canonical execution queue only; assumptions/risks/value evidence live in `docs/25_PROJECT_HEALTH.md`  
**Canonical historical data release:** `v0.6.1` (unchanged)  
**Current public preview:** `mvp-preview-ancient-v2` (non-canonical legacy demonstration)

This file answers **what is justified to work on next**.

---

# ACTIVE R1.8 / POST-MVP — technical candidate ready; release decision pending

**Parent programme:** #159  
**MVP parent:** #174  
**Technical gate:** #182  
**Decision:** D-081  
**Current stage:** **R1.8 — sponsor usability + publish / hold / rework decision**

R1.7 has produced the intended small technical MVP candidate:

> **deterministic R1 candidate package + neutral world map + explicit geometry/research states + compact evidence register + discrete temporal guards**

## Technical MVP state

- 77 frozen targets preserved;
- 19 reviewed C1;
- 5 bounded-supported;
- 14 inconclusive;
- 15 planned/unresearched C1;
- 2 held;
- 41 C0-only;
- 45 source relations;
- 37 independence groups;
- no live evidence API required;
- no production database/backend migration;
- no new historical subject research;
- no P-level/intensity derivation.

Technical disposition: **TECHNICAL_MVP_CANDIDATE**.

Durable gate: `docs/mvp/v0.1-release-check.md`.

v0.6.1 remains canonical.

## Explicit limitations before R1.8

- all 77 target geometries remain unresolved rather than guessed;
- neutral Natural Earth land is still a runtime external static asset;
- no independent historical review;
- language/access coverage varies by row;
- sponsor/browser usability acceptance is still required;
- current public preview remains the legacy non-canonical demonstration until an explicit release decision.

## Next release action

Do **not** expand the MVP before review.

Next release sequence:
1. sponsor/browser usability review of the technical candidate;
2. record concrete defects only;
3. make explicit R1.8 **PUBLISH / HOLD / REWORK** decision;
4. canonical/public promotion remains separate from technical MVP completion.

## Discovery lane now eligible

Parent: #183.

Evidence-only order:
1. #184 — timeline interaction vs discrete-anchor baseline — **REJECTED**;
2. #185 — search/filter value — **NEXT**;
3. #186 — source-dependency visualization value;
4. #187 — cross-case comparison value.

DISC-01 found no material advantage for richer/continuous timeline interaction. The current discrete-anchor + temporal-precision baseline survives. Cross-anchor comparison friction is preserved for #187 rather than used to justify a timeline.

Discovery does not authorize production implementation. A later delivery issue is required for any feature that actually beats the boring MVP baseline.

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
