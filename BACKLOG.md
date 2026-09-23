# Historical Slavery Atlas — Backlog

**Updated:** 2026-09-24  
**Role:** canonical execution queue only; assumptions/risks/value evidence live in `docs/25_PROJECT_HEALTH.md`  
**Canonical historical data release:** `v0.6.1` (unchanged)  
**Current public preview:** `mvp-preview-ancient-v2` (non-canonical legacy demonstration)

This file answers **what is justified to work on next**.

---

# ACTIVE R1 / MIDPOINT DECISION — one final three-row C1 closure tranche authorized

**Parent programme:** #159
**Midpoint review:** #168
**Decision:** D-078
**Current stage:** **R1 midpoint closure — freeze final 3-row subject tranche before research**

Midpoint disposition: **CONTINUE ONCE**, then stop subject expansion and enter release QC unless a new stop condition appears.

## Why exactly three rows

After tranches 01–02, 16 C1 rows are researched. The researched polity subset covers sectors A/C/D/F but not B/E.

Stopping now would require a narrower non-systematic scope. Adding only B+E would leave sector C above the 25% polity-sector balance ceiling.

The minimum neutral closure from the already frozen queue is:
- Tamna — 500 CE — sector F — first remaining validated new-polity row by queue order;
- Pandya Empire — 1300 CE — sector E — validated legacy promotion;
- Chimu Empire — 1300 CE — sector B — validated legacy promotion.

Projected researched polity balance after those rows:
A2 / B1 / C3 / D2 / E1 / F3 — maximum share **25%**.

Selection is based only on frozen target/QA/balance metadata, not subject evidence.

## Hard rules for the closing tranche

- freeze exact membership before subject research;
- no substitution;
- Core Contract v1 unchanged;
- 100% C1 adversarial replay under §19;
- 100% C2 replay;
- no schema/ontology/intensity change;
- no feature/platform work;
- v0.6.1 unchanged.

## After the closing tranche

Do **not** open another subject-research tranche merely because queue rows remain.

Move to R1.6 release-level QC, source-dependency/geometry/reconstructibility checks and candidate-release assembly unless the closing tranche creates a hold/rework condition.

R1 subject research should therefore stop at **19 C1 rows maximum**, not the 36-row ceiling.

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
