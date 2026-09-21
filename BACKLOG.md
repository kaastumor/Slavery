# Historical Slavery Atlas — Backlog

**Updated:** 2026-09-21  
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

All #27 acceptance steps are complete: exact-artifact browser review, explicit cartographic/semantic disposition, five controlled D-050 promotions, live public verification, and Baekje fallback/quarantine without weakened QC or invented geometry.

---

# P0 — Data API security / RLS audit

## DONE — Issue #62 private Data API boundary hardened and production-verified

Issue: **#62 — verify Data API exposure and secure atlas/cartography tables**

- [x] Verify effective client boundary and define D-051.
- [x] Apply migrations 0023/0024 and gate CI.
- [x] Re-verify production privileges and authoritative Supabase security advisors: zero security lints.

---

# P1 — Pipeline / release hardening

## BLOCKED — Finish issue #43

Issue: **#43 — pipeline hardening / protected release promotion**

Remaining blockers:

- [ ] Real staging -> production boundary. **BLOCKED:** Supabase development branch costs 0.01344/hour and requires explicit user approval.
- [ ] Protected GitHub deployment environments and scoped credentials. **BLOCKED:** connected GitHub integration cannot administer environments/secrets; no least-privilege DB-write credential is configured.

All code-side artifact, immutable snapshot, release-channel rollback, exact-bundle and reviewed-materialization gates are complete.

---

# P1 — Specialist geometry hierarchy

## DONE — Issue #40 source hierarchy established

Issue: **#40**. D-055 defines case-specific precedence/source isolation; Baekje remains quarantine/fallback pending a stronger period-appropriate specialist source.

---

# P1 — Resume globally balanced research

## DONE — Global Balance Batch 04 and external-participation lane

Globally balanced territorial research, unresolved geometry, external/network participation, unknown/inconclusive states, interpretive P-levels, and nationality-inference guardrails are implemented and CI-gated.

---

# P1/P2 — Exactly reconstructible published releases

## DONE — Issue #4 exact release reconstruction implemented

D-054 hybrid typed membership + immutable full-state bundles, migrations 0026/0027 and drift-rejecting bundle tooling are implemented. Canonical release v0.6.1 remains unchanged.

---

# P2 — Migration ledger reconciliation

## NOW — Issue #26 — reconcile live Supabase migration history

- [x] Inventory live migration ledger against repository migrations through 0027. Live platform history contains 0001–0011 and 0015–0027, but omits 0012–0014.
- [x] Document duplicate/retried entries without rewriting history casually. `0016_restore_fast_map_geometry` occurs three times; exact platform versions and the 0012–0014 gaps are recorded in `docs/20_MIGRATION_LEDGER_RECONCILIATION.md`.
- [ ] Reconcile non-destructively. **BLOCKED:** production writes are restricted to an already-reviewed explicit gate, and no reviewed metadata-only ledger repair path currently exists. Do not replay 0012–0014 merely to fill history; their schema effects are already present.
- [x] Add a divergence checker: `tools/check_migration_ledger.py` compares repository migrations with an exported Supabase history and fails on missing, duplicate, or unknown names; unit tests cover clean and irregular histories. Integration into a production deployment gate remains coupled to the blocked protected-environment/credential work in #43.

---

# P2 — Product/UI after cartographic correctness

## NEXT

- [ ] Timeline interaction and selected-year state.
- [ ] Clear visual distinction between territorial practice, legal status, external/network participation, research coverage/uncertainty and historical geometry.
- [ ] Evidence/source inspector.
- [ ] Geometry accuracy / proxy / unresolved indicator.
- [ ] Mobile and accessibility pass.
- [ ] Performance strategy as data volume grows.
- [ ] Move large stable layers toward vector tiles/PMTiles where justified; do not prematurely rewrite small layers.

---

# P3 — Tooling / integration evaluation

Issue: **#2 — evaluate end-to-end atlas tooling**. Evaluate only when there is a concrete workflow need.

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
| GitHub production promotion jobs lack a durable least-privilege DB-write credential | Exact artifact gates exist; unattended production apply remains blocked |
| No true staging environment yet | Local/CI testing; Supabase branch requires explicit cost approval |
| Historical migration ledger irregularities | Inventory/documentation/checker complete; metadata repair blocked pending reviewed production gate |
| Attractive geometry may be semantically overbroad | Separate scope review from visual/cartographic QC |
| Archive density could bias research priorities | Continue globally balanced/non-Atlantic-first research |

---

# Recently completed

- **DONE / closed:** issue #4 exact release reconstruction.
- **DONE:** external/network participation is separately CI-gated; nationality and absence inference are rejected.
- **DONE / closed:** issue #27 map/cartographic P0; Baekje remains fallback/quarantined.
- **DONE / closed:** issue #62 Data API security P0.
- **DONE / live:** D-052 static release fallback, D-053 reversible release-channel pointer, D-054 reconstructible release membership/bundles.
- **DONE:** issue #40 specialist geometry-source hierarchy and D-055 source-isolation rules.
