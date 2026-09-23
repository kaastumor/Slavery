# Historical Slavery Atlas — Backlog

**Updated:** 2026-09-23  
**Role:** canonical execution queue only; assumptions/risks/value evidence live in `docs/25_PROJECT_HEALTH.md`  
**Canonical historical data release:** `v0.6.1` (unchanged)  
**Current public preview:** `mvp-preview-ancient-v2` (non-canonical legacy demonstration)

This file answers **what is justified to work on next**.

---

# ACTIVE R1 — Core Hardening + First Systematic Coverage Release

**Issue:** #159  
**Decision:** D-073  
**Current stage:** **R1.3 — construct C0 release register and run identity/time QA before C1 subject research**

R1 is the first real research/release programme after COV-001→004.

## Completed inside R1

- programme charter frozen;
- setup adversary: **PROCEED** after tightening;
- Core Contract v1 frozen;
- Core Contract adversary: **SURVIVES AFTER SMALL CORRECTIONS**;
- dependency-free release-row validator + regression tests added.

## Current task

Build the release-facing C0 register from the frozen frame and validate identity/time state for every planned C1 target before subject research.

Target frame is frozen in:
- `programmes/r1/target_frame.json`
- `programmes/r1/05_TARGET_FRAME_FREEZE.md`
- D-074

No target substitution is permitted after subject evidence is inspected.

## R1 ceilings — not quotas

- MAX 120 C0;
- MAX 36 C1;
- MAX 12 C2.

Release may stop smaller.

## Hard rules

- v0.6.1 remains canonical until an explicit release decision;
- candidate research release != independently reviewed/public release;
- at least 50% of C1 gets adversarial replay;
- all C2 gets adversarial replay;
- no bulk automated research;
- no bespoke Atlas/platform work;
- features arise only from real R1 friction tickets;
- C0 never means absence;
- source/language/access limits remain visible.

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
