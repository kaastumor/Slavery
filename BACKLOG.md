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
**Decisions:** D-081, D-083, D-084  
**Current stage:** **R1.8 REWORK — stale committed candidate artifact repair in progress (#203)**

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

## R1.8 internal adversary result

The internal static/reconstructibility review found one release-integrity defect: the committed MVP candidate bundle was stale because CI regenerated it before checking it.

Bounded REWORK only:
- refresh the committed generated candidate;
- make CI check committed freshness before generation;
- regression-test committed bytes against deterministic reconstruction.

No historical data or feature behavior changes are authorized.

## Next release action — #203 only

Do **not** expand the MVP before review.

Active sequence:
1. run the sponsor usability/release review in `docs/mvp/r1.8-sponsor-review.md`;
2. record concrete release-blocking defects only;
3. choose exactly one R1.8 disposition:
   - **PUBLISH_CANDIDATE**;
   - **HOLD_NO_RELEASE**;
   - **REWORK**;
4. if PUBLISH_CANDIDATE or HOLD_NO_RELEASE: close #159;
5. if REWORK: keep #159 open, fix only gate defects, rerun #203.

Canonical/public promotion remains separate. v0.6.1 remains canonical.

## Discovery lane — internal-only until sponsor explicitly reopens external involvement

Parent: #183.  
Method: D-082 / `docs/discovery/DISCOVERY_STANDARD_V2.md`.

Completed/parked:
- #184 richer timeline — **REJECT NOW**;
- #198 corrected wide-lens reassessment — **COMPLETE**;
- #185 search/filter — **PARK**;
- #186 dependency visualization — **PARK the visualization; audit problem retained**;
- #187 dedicated comparison view — **PARK**;
- #200 external expert audit — **DEFERRED BY SPONSOR**; protocol preserved, no recruitment/contact.

Prepared next internal experiment:
- **#205 — EXP-02 minimum sufficient evidence packet — protocol frozen; execution waits on #203 artifact freeze.**

EXP-02 is subtractive only. It tests field necessity, invariant preservation and portability into boring Markdown/table forms. It does **not** claim user demand or adoption.

No production feature implementation is authorized.


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
