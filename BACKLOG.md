# Historical Slavery Atlas — Backlog

**Updated:** 2026-09-20  
**Role:** canonical execution queue / risk register  
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
- D-048 hard-gates render candidates at:
  - valid/non-empty geometry
  - <= 2% absolute area change
  - <= 5% source-normalized symmetric difference
  - Hausdorff retained as diagnostic, not a universal hard gate
- PR #48 added scalable visual-review sheets tied to the exact immutable CI artifact.
- Final 10 km CI artifact passes automated QC for Hittite central Anatolia, New Kingdom Egypt, Western Han, Roman Empire, Mauryan Empire and the Achaemenid benchmark.
- Baekje remains correctly **quarantined** at approximately -8.43% area change / 10.39% symmetric difference.

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
- [x] Rerun authoritative Supabase security advisors after 0024: **zero security lints**.

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

## NOW — Issue #40

Issue: **#40 — specialist regional geometry sources over Cliopatria where superior**

- [x] Investigate Baekje/Korean historical geometry first. NIKH HGIS provides authoritative Korean historical GIS but its documented polygon coverage is modern (1910+); no period-appropriate open vector replacement for 347–391 CE was identified. Baekje remains quarantine/fallback pending a stronger specialist source.
- [x] Evaluate CHGIS exact version/license/export suitability for historical China. Version 6 (Dec 2016) is technically strong for internal specialist comparison (221 BCE–1911; year-granular time series; prefecture/higher historical polygons; QGIS-compatible downloads), but its dataset-specific license prohibits redistribution. Do not publish CHGIS geometry without explicit permission; use it as an internal comparator/source-discovery aid meanwhile. See docs/18_GEOMETRY_SOURCE_SURVEY.md.
- [x] Evaluate CShapes 2.0 for its modern historical coverage. CShapes is a strong specialist comparator for independent states and dependencies globally from 1886–2019 (CShapes-Europe extends Europe to 1816), with standard GIS exports and scholarly border-change provenance. The dataset is CC BY-NC-SA 4.0, so do not directly ingest its geometry into the public canonical layer without an explicit distribution-license decision or permission. Use it internally for bounded modern comparisons meanwhile. See docs/18_GEOMETRY_SOURCE_SURVEY.md.
- [x] Evaluate Ancient World Mapping Center / other specialist ancient datasets for bounded Greco-Roman cases. Current AWMC GeoJSON is ODbL-1.0 and provides discrete specialist political snapshots (including Roman 60 BCE, 117 CE, 200 CE and 200 CE provinces), making it a preferred bounded candidate when date/entity semantics match—but not a continuous timeline source and never a basis for interpolation. Harvard MAPS/DARMC is a useful dated CC BY-NC-SA comparator; the inspected DARE province file lacks explicit historical validity dates and remains supplementary pending provenance. See docs/18_GEOMETRY_SOURCE_SURVEY.md.
- [x] Evaluate OpenHistoricalMap as supplementary material, not automatic authority. OHM has a useful temporal OSM-style boundary model and is CC0 by default, but administrative-boundary coverage and scholarly provenance are uneven and feature-level; some elements also carry source-specific licenses. Use OHM for source discovery/local comparison and accept only pinned relation versions after explicit source/date/license/geometry review. Missing OHM data never implies historical absence. See docs/18_GEOMETRY_SOURCE_SURVEY.md.
- [x] Evaluate CONFOEDERATIO / Naissance as a comparator with provenance/license scrutiny. The public Atlas is an ambitious global/sub-yearly beta and accessible CRD datasets are stated MIT-licensed, but public 0.5b/0.51b scope/version descriptions differ, public files may be simplified/compressed, de-jure CShapes content retains upstream licensing, and no adequate public per-polity/keyframe citation mapping was identified. Keep it as an experimental second-global-baseline comparator/source-discovery aid; no automatic precedence or promotion. See docs/18_GEOMETRY_SOURCE_SURVEY.md.
- [ ] Define explicit region/time/source precedence rules.
- [ ] Never silently mix geometry source families within one geometry record.
- [ ] Replace Cliopatria only where a bounded comparison shows a defensible improvement.

---

# P1 — Resume globally balanced research

## NEXT

- [ ] Resume globally balanced territorial-practice research.
- [ ] Prioritize weak/non-Atlantic cells before dense Atlantic bulk ingestion.
- [ ] Continue unresolved-geometry work alongside evidence research.
- [ ] Expand external/network participation separately from territorial practice.
- [ ] Preserve unknown / researched-inconclusive states rather than manufacturing negatives.
- [ ] Keep P0-P4 interpretive; never derive it mechanically from document/voyage counts.
- [ ] Keep owner/actor nationality unknown unless independently evidenced.

---

# P1/P2 — Exactly reconstructible published releases

Issue: **#4 — make published database releases exactly reconstructible**

- [ ] Decide typed release membership vs hybrid membership + immutable bundle.
- [ ] Define row/object digest rules.
- [ ] Define historical-release API semantics versus current-reviewed state.
- [ ] Prevent reviewed-but-not-release-member leakage into historical release reconstruction.
- [ ] Add SQL acceptance tests first.
- [ ] Record the durable decision in `docs/08_DECISIONS_LOG.md` before schema implementation.
- [ ] Implement as fresh migrations after the current migration head.

---

# P2 — Migration ledger reconciliation

Issue: **#26 — reconcile live Supabase migration history**

- [ ] Inventory live migration ledger against repository migrations through the current head.
- [ ] Document duplicate/retried entries without rewriting history casually.
- [ ] Reconcile non-destructively.
- [ ] Add a deployment check that flags future ledger/repository divergence early.

---

# P2 — Product/UI after cartographic correctness

- [ ] Timeline interaction and selected-year state.
- [ ] Clear visual distinction between territorial practice, legal status, external/network participation, research coverage/uncertainty and historical geometry.
- [ ] Evidence/source inspector.
- [ ] Geometry accuracy / proxy / unresolved indicator.
- [ ] Mobile and accessibility pass.
- [ ] Performance strategy as data volume grows.
- [ ] Move large stable layers toward vector tiles/PMTiles where justified; do not prematurely rewrite small layers.

---

# P3 — Tooling / integration evaluation

Issue: **#2 — evaluate end-to-end atlas tooling**

Evaluate only when there is a concrete workflow need. Do not add infrastructure for novelty.

---

# PARKED deliberately

- Full Atlantic bulk ingestion before global/map/release foundations are ready.
- Automatic P-level assignment.
- Actor nationality inference from vessel flag, surname, residence, port, or corporate jurisdiction.
- Per-polity hand-edited coastline fixes.
- New custom coastline buffer heuristics unless standard GIS methods are proven insufficient.
- Replacing Cliopatria globally merely because another dataset is newer.
- Permanent cloud/framework commitments before the relevant requirements are demonstrated.

---

# Current blockers / risks

| Risk | Current handling |
| --- | --- |
| Baekje loses ~8–9% area in generic QGIS pipeline | Quarantine/fallback; investigate source/specialist geometry |
| Production GIS experimentation can cause outages | Offline/CI/staging only; public path serves precomputed geometry |
| GitHub production promotion jobs still lack a durable least-privilege database-write credential | Existing scoped Management API token cannot use `/database/query`; exact geometry/release artifact gates exist, but unattended production apply remains blocked until an appropriately scoped credential/environment is configured |
| No true staging environment yet | Local/CI testing; Supabase branch requires explicit cost approval |
| Live API/database outage could hide an already-published atlas state | D-052 deployed snapshot fallback is live and adversarially verified; D-053 provides explicit reversible release-channel repointing |
| Historical migration ledger irregularities | #26 non-destructive reconciliation |
| Attractive geometry may be semantically overbroad | Separate scope review from visual/cartographic QC |
| Archive density could bias research priorities | Resume globally balanced/non-Atlantic-first research after release hardening |

---

# Recently completed

- **DONE / closed:** issue #27 map/cartographic P0 after exact-artifact promotion and multi-region live browser verification; Baekje remains fallback/quarantined.
- **DONE / live:** five D-050-approved 10 km representative render geometries promoted from immutable artifact `7644ea348ec43093219d964069a7b88ec088a331`.
- **DONE / closed:** issue #62 Data API security P0: D-051 private boundary, migration 0023 defense-in-depth revokes/default privileges, migration 0024 immutable helper search path, production privilege recheck, public health green, and zero remaining Supabase security-advisor lints.
- **DONE / live:** D-052 deployment-bound static release fallback for `mvp-preview-ancient-v2`; exact deployed snapshot retained and checksummed, with API-first browser fallback semantics.
- **DONE / live:** D-053 explicit `public_mvp_preview` release-channel pointer (migration 0025 + `atlas-data` v8), with compare-and-set rollback drill v2 → v1 → v2 externally verified healthy.
- **DONE / live:** D-054 reconstructible typed release membership (migration 0026) plus preservation-grade full-state bundle build/verify/apply tooling and migration 0027 artifact immutability. CI proves exact bundle promotion and drift rejection; production 0027 guard is verified.
