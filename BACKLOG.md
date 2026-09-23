# Historical Slavery Atlas — Backlog

**Updated:** 2026-09-23  
**Role:** canonical execution queue; standing assumptions/risks live in `docs/25_PROJECT_HEALTH.md`  
**Canonical historical data release:** `v0.6.1` (unchanged)  
**Current public preview:** `mvp-preview-ancient-v2` (non-canonical)

This file answers **what should be worked on next**.

It does **not** override methodology, ontology, source policy, architecture decisions, release rules, or historical evidence judgments. Those remain governed by the canonical documentation and `docs/08_DECISIONS_LOG.md`.

GitHub issues hold detailed discussion and acceptance history. This backlog holds the current ordering and execution state.

## Working rules

- Update this file when priorities materially change, a blocker appears, or a milestone is completed.
- Keep active work near the top. Do not let completed work obscure the execution queue.
- A green CI run is not historical/editorial approval and is not automatically visual acceptance.
- Never promote failed geometry merely to clear the queue. Quarantine/fallback is an acceptable outcome.
- Never overwrite historical releases. A new canonical release requires its own validated release process.
- Heavy GIS/research experiments stay out of production request paths.
- If this backlog conflicts with a durable methodology/architecture decision, the durable decision wins and the backlog must be corrected.

### Priority scale

| Priority | Meaning |
| --- | --- |
| **P0** | User-visible correctness, data-integrity, or availability blocker. Work before normal expansion. |
| **P1** | Next major capability or structural hardening needed after P0. |
| **P2** | Important non-blocking correctness/maintenance work. |
| **P3** | Useful later work, evaluation, or optimization. |

### Status vocabulary

- **NOW** — current focus
- **NEXT** — ready after current focus
- **BLOCKED** — cannot proceed without an explicit dependency/decision
- **PARKED** — intentionally deferred
- **DONE** — completed/merged; retained briefly for context

---

# DONE — Gate M1 methodology hardening

Parent: **#100**

M1 completed with one deliberate revise/correct/re-attack cycle. The integrated gate rejected P0–P4 as the target universal comparative ordinal, retained it only for legacy compatibility, and accepted the corrected experimental semantic/temporal/spatial prototype for integration testing. Canonical release v0.6.1 and the public preview remain unchanged.

---

# NOW — Gate M2 semantic integration + complete geography backbone

Parent: **#116 — Integrate hardened semantics with complete geography backbone**

Current integrated evidence:
- #117 / D-058: post-M1 semantics are now the canonical **target** model, with draft-0.11 explicitly not yet live implementation.
- #118 / D-059: Cliopatria v0.2.0 calendar and POLITY/RELATION/composite rules are resolved sufficiently for raw integration; source-native year zero and hierarchy remain preserved.
- #119: the complete pinned 13,765-feature Cliopatria corpus now survives a clean disposable PostGIS raw/staging load plus exact retry/no-op. Source-native years, POLITY/RELATION, hierarchy fields, full raw payloads and geometry remain distinct from atlas identities and publication.

**Execution order / eligibility:**

1. **DONE — #117 — Canonicalize M1 target semantics for M2**
2. **DONE — #118 — Resolve Cliopatria calendar and relation semantics**
3. **DONE — #119 — Ingest complete pinned Cliopatria corpus into raw staging** (full-corpus disposable PostGIS load + exact retry passed; no production apply)
4. **DONE — #120 — Prototype post-M1 claim semantics in disposable PostGIS** (legacy compatibility + explicit target dimensions + temporal/spatial prototype passed; no production apply)
5. **DONE — #121 — Build complete Cliopatria selected-year resolver prototype** (synthetic adversary + exact 13,765-feature full-corpus acceptance passed; no production apply)
6. **NOW — #135 AUTO READY — Correct post-M1 cross-table integrity gaps** (#122 REVISE finding; smallest bounded correction)
7. **GATE / REVISE — #122 — M2 integrated adversarial gate** (first attack found reverse-direction temporal/spatial integrity and open-terminus representation gaps; re-attack after #135)
8. **GATE — #123 AUTO READY — M2 Project Health Check and reconciliation** (depends on successful #122 re-attack)

M2 rules:

- do not resume bulk evidence expansion merely because M1 passed;
- preserve v0.6.1 and the current preview exactly;
- raw Cliopatria ingestion is infrastructure, not geometry approval;
- no automatic P0–P4 conversion;
- no production apply until disposable/local integration survives;
- #123 must explicitly choose continue / redirect / stop before the next gate exists.

Blocked #43 and #26 remain documented but are not eligible autonomous work while their external/admin blockers remain.

# P0 — Map/cartographic quality

## DONE — Issue #27 closed without regressing the accepted Achaemenid result

Issue: **#27 — map alignment / render quality**

Established architecture:

- historical extent: Cliopatria or stronger specialist historical GIS
- physical coastline/land: Natural Earth 1:10m
- preprocessing: offline QGIS / GEOS / GDAL
- browser: MapLibre
- historical source geometry remains immutable
- production consumes precomputed approved render geometry only
- failed candidates quarantine/fallback instead of changing unrelated good cases

### Current evidence

- Achaemenid ~500 BCE live pilot is **visually accepted**.
- PR #45 consolidated geometry generation/QC into `geometry-build.yml`.
- D-048 hard-gates render candidates at valid/non-empty geometry, <= 2% absolute area change, <= 5% source-normalized symmetric difference; Hausdorff remains diagnostic.
- PR #48 added scalable visual-review sheets tied to the exact immutable CI artifact.
- Final 10 km CI artifact passes automated QC for Hittite central Anatolia, New Kingdom Egypt, Western Han, Roman Empire, Mauryan Empire and the Achaemenid benchmark.
- Baekje remains correctly quarantined at approximately -8.43% area change / 10.39% symmetric difference.

All #27 acceptance steps are complete: exact-artifact browser review, explicit cartographic/semantic disposition, five controlled D-050 promotions, live public verification, and Baekje fallback/quarantine without weakened QC or invented geometry.

---

# P0 — Data API security / RLS audit

## DONE — Issue #62 private Data API boundary hardened and production-verified

Issue: **#62 — verify Data API exposure and secure atlas/cartography tables**

- [x] Verify effective client boundary: `anon`/`authenticated` have no schema `USAGE` on `atlas`, `audit`, `cartography`, `publish` and no table read/write privileges.
- [x] Define D-051: browser uses `atlas-data`; internal schemas are not a direct client Data API.
- [x] Apply migration 0023: explicit `PUBLIC`/client-role revokes plus restrictive default privileges for internal schemas/tables/sequences/functions.
- [x] Gate CI on the private-schema boundary; main foundation CI passed at commit `cc5c670` and production availability monitor passed.
- [x] Re-verify production after migration: both client roles still have no internal-schema usage and 0 SELECT/INSERT/UPDATE/DELETE privileges.
- [x] Resolve the remaining advisor warning with migration 0024 by pinning `atlas.make_year_range` to `search_path = pg_catalog`.
- [x] Rerun authoritative Supabase security advisors after 0024: zero security lints.

No indiscriminate RLS policies were added because these schemas are intentionally non-client surfaces. Any future direct PostgREST contract must use an explicitly exposed API schema with reviewed grants and RLS/policies.

---

# P1 — Pipeline / release hardening

## BLOCKED — Finish issue #43

Issue: **#43 — pipeline hardening / protected release promotion**

Already complete:

- [x] research-case idempotency / stable `case_key`
- [x] canonical JSON content hashes
- [x] exact-retry no-op / changed-content rejection
- [x] consolidated `geometry-build.yml`
- [x] pinned QGIS container
- [x] pinned/checksummed Natural Earth input
- [x] immutable geometry candidate manifests
- [x] explicit QC quarantine policy
- [x] exact-artifact visual-review pack

Remaining:

- [ ] Define a real staging -> production promotion boundary. **BLOCKED:** the concrete Supabase staging target is a development branch costing 0.01344/hour and requires explicit user approval before creation.
- [x] Make promotion consume the exact tested geometry/release artifact instead of recomputing it. Geometry uses D-050 immutable acceptance artifacts. Releases now use D-054 typed membership + preservation-grade full-state bundles: `tools/release_bundle.py` freezes exact membership, API-relevant object/render digests, candidate/Git provenance and active land-fabric identity before promotion; verify/apply hard-block on drift, populate `captured_at_release` typed membership, register the exact bundle, and never move the D-053 serving channel implicitly. Disposable PostGIS CI passed build → verify → deliberate-drift rejection → exact apply → post-apply verify. Migration 0027 is live and makes published `audit.release_artifact` provenance immutable.
- [ ] Add protected GitHub deployment environments and appropriately scoped credentials. **BLOCKED:** the connected GitHub integration cannot administer repository environments/secrets, and the existing scoped Supabase Management API token cannot execute database queries. Code-side artifact/promotion gates are ready; repository-admin environment protection plus a least-privilege DB-write credential must be configured externally.
- [x] Materialize a static/recoverable published-release snapshot so a transient database outage cannot remove an already-published atlas state. D-052 is live: Pages deploy `873abc1c` captured `mvp-preview-ancient-v2` as a canonicalized 4.87 MB static payload (27 places / 31 claims / 57 geometry records), retained it as an Actions artifact, embedded it in the deployed site, and verified SHA-256 `53b64f65ae7fead65e2f9274cf4d9b87e4868a5a98f38eb0d97fea23e2d29d21` after deployment. Adversarial browser run `35531531089` then blocked the live Supabase API and verified all six representative cases from the deployed snapshot with no page/map errors; live-vs-fallback screenshots differ only in the `static fallback` badge. The browser remains API-first.
- [x] Add post-promotion verification and rollback/fallback semantics. D-052 provides deployment-bound static fallback plus adversarial forced-outage verification. D-053 + migration 0025 add an explicit `public_mvp_preview` release-channel pointer with guarded published/purpose validation and compare-and-set moves. Production rollback drill on 2026-09-20 proved v2 → v1 → v2 without mutating release contents: health run `35533535121` served v2 at 27 places / 31 claims, rollback served v1 at 8 places / 11 claims, and restore served v2 again at 27 places / 31 claims, all HTTP/API/site healthy.
- [x] Ensure public services consume reviewed/published materializations only. The browser consumes `atlas-data`; that Edge Function resolves the current public preview through `audit.release_manifest` plus `publish` views and approved render materializations, while D-051 blocks direct client access to internal research schemas.

### BLOCKED — Supabase development branch

A Supabase development branch would provide a useful staging target.

- Current quoted cost: **0.01344/hour**
- Creation requires explicit user cost confirmation.
- Do **not** create it without that confirmation.

A local/CI disposable environment remains acceptable for testing in the meantime.

---

# P1 — Specialist geometry hierarchy

## DONE — Issue #40 source hierarchy established

Issue: **#40 — specialist regional geometry sources over Cliopatria where superior**

- [x] Investigate Baekje/Korean historical geometry first. NIKH HGIS provides authoritative Korean historical GIS but its documented polygon coverage is modern (1910+); no period-appropriate open vector replacement for 347–391 CE was identified. Baekje remains quarantine/fallback pending a stronger specialist source.
- [x] Evaluate CHGIS exact version/license/export suitability for historical China. Version 6 is technically strong for internal specialist comparison but its dataset-specific license prohibits redistribution. Do not publish CHGIS geometry without explicit permission.
- [x] Evaluate CShapes 2.0 for modern historical coverage; use internally pending an explicit distribution-license decision.
- [x] Evaluate Ancient World Mapping Center / other specialist ancient datasets for bounded Greco-Roman cases; AWMC may be preferred when date/entity semantics match.
- [x] Evaluate OpenHistoricalMap as supplementary material, not automatic authority.
- [x] Evaluate CONFOEDERATIO / Naissance as an experimental comparator with provenance/license scrutiny.
- [x] Define explicit region/time/source precedence rules in D-055.
- [x] Never silently mix geometry source families within one geometry record.
- [x] Replace Cliopatria only where a bounded comparison shows a defensible improvement.

---

# P1 — Resume globally balanced research

## DONE — Global Balance Batch 04 and external-participation lane

- [x] Resume globally balanced territorial-practice research. Global Balance Batch 04 stages four new unpublished weak-region territorial cases across Southeast Asia, the Americas, Oceania/Pacific and East/Southern Africa, with claim-specific evidence and deliberately unresolved geometry where appropriate.
- [x] Prioritize weak/non-Atlantic cells before dense Atlantic bulk ingestion.
- [x] Continue unresolved-geometry work alongside evidence research.
- [x] Expand external/network participation separately from territorial practice. PR #87 makes this a separately validated research lane: staged external cases are CI-gated against the ontology, territorial-practice/P-level leakage is rejected, and explicit guardrails reject nationality/absence inference. The first Zaghāwa captive-export case remains unpublished and separate from territorial prevalence.
- [x] Preserve unknown / researched-inconclusive states rather than manufacturing negatives.
- [x] Keep P0-P4 interpretive; never derive it mechanically from document/voyage counts.
- [x] Keep owner/actor nationality unknown unless independently evidenced. The external-participation validator requires `nationality_inferred=false`; the standing ontology rule remains claim-specific evidence only.

---

# P1/P2 — Exactly reconstructible published releases

## DONE — Issue #4 exact release reconstruction implemented

Issue: **#4 — make published database releases exactly reconstructible**

- [x] Decide typed release membership vs hybrid membership + immutable bundle: D-054 adopts the hybrid model.
- [x] Define row/object digest rules: canonical UTF-8 JSON with deterministic ordering; geometry uses SRID + hexadecimal EWKB in the preservation bundle.
- [x] Define historical-release API semantics versus current-reviewed state: exact historical state comes from the immutable bundle or byte-equivalent verified data, not mutable current publish views.
- [x] Prevent reviewed-but-not-release-member leakage into historical release reconstruction through explicit typed membership and bundle verification.
- [x] Add SQL acceptance tests first: release-membership and bundle fixture/drift/apply tests cover the contract.
- [x] Record the durable decision in `docs/08_DECISIONS_LOG.md` before schema implementation as D-054.
- [x] Implement as migrations 0026 and 0027 plus `tools/release_bundle.py`; legacy v1/v2 memberships are explicitly marked `legacy_membership_backfill` rather than overstating exact historical row-state preservation.

Issue #4 was closed 2026-09-21 after verifying the implementation and acceptance history. Canonical release v0.6.1 remains unchanged.

---

# P2 — Migration ledger reconciliation

Issue: **#26 — reconcile live Supabase migration history**

- [x] Inventory live migration ledger against repository migrations through the current head. The 2026-09-21 read-only inventory through 0027 is recorded in `docs/20_MIGRATION_LEDGER_RECONCILIATION.md`.
- [x] Document duplicate/retried entries without rewriting history casually. The three live 0016 retry entries are preserved and documented.
- [ ] Reconcile non-destructively. **BLOCKED for mutation:** repository 0012–0014 effects are already live, but the platform ledger lacks those names; replaying them would be unsafe and no reviewed metadata-only repair gate currently exists. Keep the discrepancy explicit rather than rewriting or replaying production history.
- [x] Add a deployment check that flags future ledger/repository divergence early. `tools/check_migration_ledger.py` reports missing, duplicate and unknown remote names and fails non-zero; unit coverage is merged.

---

# P2 — Product/UI after cartographic correctness

- [x] Timeline interaction and selected-year state. PR #92 persists selected year as shareable `?year=` URL state, restores/clamps it against the published release range, and supports browser history navigation without changing release/data semantics.
- [x] Clear visual distinction between territorial practice, legal status, external/network participation, research coverage/uncertainty and historical geometry. PR #93 makes P-level shading explicitly territorial-practice-only and presents the other evidence dimensions as independent, preserving unknown as the default rather than implying unavailable data.
- [x] Evidence/source inspector. The existing claim panel is the inspector: for each active published claim it exposes the claim summary and date, evidence direction (`supports`/`challenges`/`qualifies`/`context`), source title/link, author or institution, and locator. Verified against the current `atlas-data` response model; evidence remains claim-specific rather than aggregated into a misleading source-count score.
- [x] Geometry accuracy / proxy / unresolved indicator. The existing place panel exposes the active geometry's explicit `accuracy_status` (`exact`, `specialist`, `approximate_historical`, `modern_proxy`, or `unresolved`) as a visible Geometry tag; unresolved records remain visible even without drawable geometry, and the Historical geometry disclosure exposes resolution method, source, and any bounded render transform while stating that source historical geometry is preserved unchanged. The year overview separately labels unmapped active cases. No accuracy is inferred from render appearance.
- [x] Mobile and accessibility pass. PR #96 adds keyboard-operable map-feature selection, focus-visible navigation, screen-reader live status for year/data changes, larger touch targets, responsive narrow-screen controls, and reduced-motion handling. Main foundation/build/deploy and post-merge availability checks passed at `4c9d3ec`.
- [x] Performance strategy as data volume grows. `docs/21_PERFORMANCE_STRATEGY.md` defines release-bound measurement, a staged API/GeoJSON → split-payload → immutable vector-tile/PMTiles escalation path, conservative investigation triggers, tile provenance/QC requirements, and an explicit ban on live-production load testing or premature rewrites.
- [ ] **PARKED — trigger not met.** Move large stable layers toward vector tiles/PMTiles only when `docs/21_PERFORMANCE_STRATEGY.md` Stage C investigation triggers are repeatedly observed. The current preview remains below the adoption gate; do not implement a tile rewrite merely to clear the queue.

---

# P3 — Tooling / integration evaluation

## CLOSED — Issue #2 trigger-driven evaluation register

Issue: **#2 — evaluate end-to-end atlas tooling**

PR #99 replaced technology-shopping with a trigger/acceptance matrix. No candidate currently has a demonstrated workflow trigger that justifies a new infrastructure commitment: existing QGIS/GEOS/GDAL, PostgreSQL/PostGIS + `atlas-data`, current release artifacts, and the present frontend/toolchain cover the demonstrated needs.

Issue #2 is closed as not planned. If a concrete trigger fires, create a new bounded child issue with a real sample, baseline, measurable acceptance criteria, licensing/cost constraints, and an exit path. Do not adopt infrastructure merely to clear the queue.

---

# PARKED deliberately

- Full Atlantic bulk ingestion before global/map/release foundations are ready.
- Automatic P-level assignment.
- Actor nationality inference from vessel flag, surname, residence, port, or corporate jurisdiction.
- Per-polity hand-edited coastline fixes.
- New custom coastline buffer heuristics unless standard GIS methods are proven insufficient.
- Replacing Cliopatria globally merely because another dataset is newer.
- Permanent cloud/framework commitments before the relevant requirements are demonstrated.
