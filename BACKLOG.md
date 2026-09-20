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

## NOW — Close issue #27 without regressing the accepted Achaemenid result

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
- Final 10 km CI artifact passes automated QC for:
  - Hittite central Anatolia
  - New Kingdom Egypt
  - Western Han
  - Roman Empire
  - Mauryan Empire
  - Achaemenid benchmark
- Baekje remains correctly **quarantined** at approximately -8.43% area change / 10.39% symmetric difference.

### Remaining acceptance steps

- [x] Inspect the final topology-correct **10 km** review artifact at full extent and representative boundary/coast views; Baekje remains quarantined.
- [x] Build a local-only MapLibre review path that verifies and renders the **exact tested artifact**, not a recomputation. Merged in PR #51.
- [x] Use that review path to validate representative candidates at several browser zoom levels/continents against the same Natural Earth fabric. Boundary-focused CI review run `35526192586` passed with exact-artifact SHA verification and no browser page errors.
- [x] Record explicit cartographic visual disposition per candidate: Achaemenid (both slices), Hittite central Anatolia, New Kingdom Egypt, Western Han, Roman Empire and Mauryan Empire are `visually_accepted_candidate`; Baekje is `quarantined/fallback`. This is cartographic acceptance, not historical-semantic scope approval.
- [x] Keep Baekje on fallback; do not weaken global QC.
- [ ] Investigate Baekje's source/geometry separately under the specialist-geometry track (#40).
- [x] Use 10 km as the conservative generic Cliopatria candidate baseline under D-049; do not auto-escalate tolerance, and do not replace the already accepted live Achaemenid render merely for uniformity.
- [ ] Promote only the exact reviewed/checksummed artifact through a controlled promotion path.
- [ ] Re-check the public browser after promotion.
- [ ] Close #27 only when multiple representative regions and zoom levels are genuinely correct.

### Specific risk: semantic overbreadth

A cartographically attractive polygon can still be historically wrong for a claim if the geometry represents a whole polity while the evidence target is narrower.

- [ ] Audit overbroad whole-polity proxies during geometry promotion.
- [ ] Prefer unresolved/narrower defensible geometry over attractive false precision.

---

# P1 — Pipeline / release hardening

## NEXT — Finish issue #43

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

- [ ] Define a real staging -> production promotion boundary.
- [ ] Make promotion consume the exact tested geometry/release artifact instead of recomputing it.
- [ ] Add protected GitHub deployment environments and appropriately scoped credentials.
- [ ] Materialize a static/recoverable published-release snapshot so a transient database outage cannot remove an already-published atlas state.
- [ ] Add post-promotion verification and rollback/fallback semantics.
- [ ] Ensure public services consume reviewed/published materializations only.

### BLOCKED — Supabase development branch

A Supabase development branch would provide a useful staging target.

- Current quoted cost: **0.01344/hour**
- Creation requires explicit user cost confirmation.
- Do **not** create it without that confirmation.

A local/CI disposable environment remains acceptable for testing in the meantime.

---

# P1 — Specialist geometry hierarchy

## NEXT after #27 — Issue #40

Issue: **#40 — specialist regional geometry sources over Cliopatria where superior**

- [ ] Investigate Baekje/Korean historical geometry first because it is an observed generic-pipeline failure.
- [ ] Evaluate CHGIS exact version/license/export suitability for historical China.
- [ ] Evaluate CShapes 2.0 for its modern historical coverage.
- [ ] Evaluate Ancient World Mapping Center / other specialist ancient datasets for bounded Greco-Roman cases.
- [ ] Evaluate OpenHistoricalMap as supplementary material, not automatic authority.
- [ ] Evaluate CONFOEDERATIO / Naissance as a comparator with provenance/license scrutiny.
- [ ] Define explicit region/time/source precedence rules.
- [ ] Never silently mix geometry source families within one geometry record.
- [ ] Replace Cliopatria only where a bounded comparison shows a defensible improvement.

---

# P1 — Resume globally balanced research

## NEXT after map P0

The user explicitly wants the UI/map working properly before broad data gathering resumes.

When #27 is closed:

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

This is part of the broader release-hardening architecture and should be solved on current `main`, not by reviving stale migration prototypes.

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

Current production objects and migration history are not perfectly aligned because of earlier manual/retried deployment history.

- [ ] Inventory live migration ledger against repository migrations through 0022.
- [ ] Document duplicate/retried entries without rewriting history casually.
- [ ] Reconcile non-destructively.
- [ ] Add a deployment check that flags future ledger/repository divergence early.

This is important housekeeping but is not currently blocking the public preview.

---

# P2 — Product/UI after cartographic correctness

Once #27 is closed and promotion is safe:

- [ ] Timeline interaction and selected-year state.
- [ ] Clear visual distinction between:
  - territorial practice
  - legal status
  - external/network participation
  - research coverage/uncertainty
  - historical geometry
- [ ] Evidence/source inspector.
- [ ] Geometry accuracy / proxy / unresolved indicator.
- [ ] Mobile and accessibility pass.
- [ ] Performance strategy as data volume grows.
- [ ] Move large stable layers toward vector tiles/PMTiles where justified; do not prematurely rewrite small layers.

---

# P3 — Tooling / integration evaluation

Issue: **#2 — evaluate end-to-end atlas tooling**

Evaluate only when there is a concrete workflow need. Do not add infrastructure for novelty.

Candidates already worth revisiting when relevant:

- Zotero / OpenAlex / Crossref / Scite for research discovery and bibliography
- IIIF / GROBID / Transkribus for source handling
- OpenRefine / WHG for reconciliation
- QGIS LTR for geometry QA
- DVC/object storage for large immutable artifacts
- Martin / PMTiles for publication
- FastAPI only if the existing API boundary becomes limiting
- Storybook / Playwright / axe when UI complexity justifies them

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
| No true staging environment yet | Local/CI testing; Supabase branch requires user cost approval |
| Published release depends heavily on live DB | #43 static/recoverable snapshot work |
| Historical migration ledger irregularities | #26 non-destructive reconciliation |
| Attractive geometry may be semantically overbroad | Separate scope review from visual/cartographic QC |
| Archive density could bias research priorities | Resume globally balanced/non-Atlantic-first research after #27 |

---

# Recently completed

- **DONE / merged:** PR #41 representative QGIS validation.
- **DONE / merged:** PR #42 pipeline architecture / D-046.
- **DONE / live:** migration 0022 research-case idempotency.
- **DONE / merged:** PR #45 consolidated geometry build/QC/quarantine pipeline / D-048.
- **DONE / merged:** PR #48 exact-artifact scalable visual-review sheets with MultiPolygon regression coverage.
- **DONE / visually accepted + live:** Achaemenid ~500 BCE QGIS/Natural Earth pilot.
- **DONE:** stale PR #37 closed because its migration/cartography path was superseded.
- **DONE:** stale PR #5 closed because its migration sequence no longer matched current `main`; the underlying release-reconstruction requirement remains issue #4.

---

# Session-start checklist

Before starting substantial work:

1. Read this `BACKLOG.md`.
2. Inspect current `main`, open issues, and open PRs.
3. Read the linked issue for the active backlog item.
4. Read the canonical methodology/architecture docs relevant to the change.
5. For schema/methodology/ontology changes, update the Decisions Log before treating the change as canonical.
6. Keep the backlog updated when the task state or priority changes.
