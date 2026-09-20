# Current Handoff — 2026-09-20

Use this file only as a **session handoff**. For durable methodology and architecture, follow the canonical docs and Decisions Log. GitHub `main` is the implementation source of truth.

## Where to start

Repository: `kaastumor/Slavery`

Read first:

- `BACKLOG.md` — canonical execution priority / risk register
- `docs/00_START_HERE.md`
- `docs/01_PROJECT_STATUS.md`
- `docs/02_METHOD_AND_ONTOLOGY.md`
- `docs/03_SOURCE_POLICY.md`
- `docs/04_DATA_MODEL.md`
- `docs/05_GEOGRAPHY_AND_MAP.md`
- `docs/08_DECISIONS_LOG.md`
- `docs/11_SYSTEM_ARCHITECTURE.md`
- `docs/19_PIPELINE_ARCHITECTURE.md`

Then inspect open GitHub issues and PRs before acting.

## Current product state

- Canonical historical data release remains **v0.6.1** and must not be overwritten.
- Public non-canonical preview remains **`mvp-preview-ancient-v2`**.
- Live Supabase project: `dilnayfllygkplsdymel`.
- Live DB is healthy at this handoff.
- Live migration history includes `0022_research_case_idempotency`.
- Live counts at handoff: 42 claims, 31 published claims, 68 geometries, 94 render-cache rows.
- Public API: `atlas-data`.
- Availability monitor + guarded project self-heal are active.
- Issue #35 availability incident is closed.

## Active P0: map quality — issue #27

The user explicitly wants the map/UI working correctly before more research expansion.

The successful direction is now established:

- historical extent source: Cliopatria or a better specialist source
- physical coastline/land: Natural Earth 1:10m
- offline preprocessing: QGIS/GEOS/GDAL standard algorithms
- browser renderer: MapLibre
- source geometry remains immutable
- production serves precomputed render geometry only

The old custom coastline buffer experiments are no longer the preferred direction.

### Accepted production pilot

Achaemenid ~500 BCE was processed with the QGIS + Natural Earth pipeline and the user explicitly said the live result **“looks great.”**

Two Achaemenid slices currently use live policy:

`cliopatria-qgis-natural-earth-v1`

The ~500 BCE slice:
- geometry id `34ff5048-242f-48a3-8fb2-5eca4dcd9a54`
- source points: 620
- render points: 6,125
- area delta: about +0.071%

Do not undo this without a regression reason.

### Representative validation

PR #41 merged and introduced representative tests for:

- Hittite central Anatolia
- New Kingdom Egypt
- Baekje
- Western Han
- Roman Empire
- Mauryan Empire
- Achaemenid benchmark

Tolerances tested: 10/15/20/25 km.

Important result: **Baekje is an outlier**. It loses roughly 8–9% of source area across the tested tolerance range. This means a single universal tolerance/recipe is unsafe. Treat it as a quarantine/fallback case and investigate separately. Do not lower global standards simply to force Baekje through.

Issue #27 stays P0 until representative visual and quantitative acceptance is complete.

## Pipeline architecture

PR #42 merged D-046 and `docs/19_PIPELINE_ARCHITECTURE.md`.

Four logical lanes:

1. research curation
2. cartography build
3. release/promotion
4. operations

Rules:
- CI/PR validation must not write to production.
- Build once and promote the exact immutable artifact.
- Automated validation is not historical/editorial approval.
- Generated geometry is not approved render geometry.
- Failed geometry candidates can fall back to the previous approved render.
- Production should eventually be behind explicit staging/production deployment boundaries.
- Repeated logic should be scripts/reusable workflows, not many permanent one-off workflows.

PR #45 has now consolidated the geometry experiments into one pinned, parameterized `geometry-build.yml`. PR #48 added exact-artifact scalable visual-review sheets. Both are merged; visual acceptance remains separate from automated QC.

## Research ingestion

Research ingestion is now retry-safe.

Migration `0022_research_case_idempotency.sql` is in repo and live.

`tools/add_research_case.py` supports stable `case_key` + canonical JSON SHA-256 content identity.

Expected behavior:
- first application → create unpublished claim
- exact retry → no-op
- same case key with changed content → reject
- changed historical interpretation → new explicit case/supersession path

This was added specifically so future automated research jobs cannot silently duplicate claims.

## Availability / operations

Two earlier map experiments caused production serving incidents. This must not recur.

Guardrails now active:
- no expensive GIS processing in request path
- browser API timeout ~12 sec
- external health monitor every 15 min
- incident automation
- guarded Supabase project restart through Management API
- 2 confirmed failures 120 sec apart before restart
- 2-hour restart cooldown
- post-restart API recovery check

The user manually created the GitHub secret `SUPABASE_MANAGEMENT_TOKEN`; do not expose or replace it.

Before any production DB/render operation, use a tiny health query first. Heavy spatial work belongs in CI/local/staging.

## Pipeline hardening — issue #43

Already completed under #43:

- consolidated `geometry-build.yml`
- pinned QGIS/Natural Earth inputs
- provenance/checksum manifests for geometry candidates
- explicit candidate quarantine
- exact-artifact visual-review packs

Still to do:

- protected staging/production promotion
- exact tested-artifact promotion rather than recomputation
- static/recoverable published release snapshot
- real staging environment

A Supabase development branch is possible, but branch creation has a current quoted cost of **0.01344 per hour** and the Supabase connector requires explicit user cost confirmation before creation. Do not create it without that confirmation.

## Geometry sources beyond Cliopatria

See `docs/18_GEOMETRY_SOURCE_SURVEY.md`.

Current approach:
- Cliopatria = open global deep-time backbone
- use stronger specialist HGIS where defensible
- evaluate CShapes 2.0 for modern historical borders
- evaluate CHGIS for China subject to license/version
- OpenHistoricalMap and Pleiades as supplementary/specialist resources
- evaluate CONFOEDERATIO / Naissance as a newer global comparator

Do not replace Cliopatria globally merely because another dataset is newer. Evaluate coverage, provenance, licensing and geometry quality.

## Immediate next action

Continue **issue #27**, not broad data gathering.

Recommended sequence:

1. inspect the final topology-correct 10 km visual-review artifact from the merged PR #48 run;
2. render the exact tested artifact in a disposable MapLibre review path at several zoom levels;
3. record visual acceptance/fallback per representative geometry;
4. keep Baekje quarantined and investigate its source/geometry separately;
5. select the source-family baseline recipe without regressing the accepted live Achaemenid result;
6. promote only the exact reviewed/checksummed artifacts through a controlled promotion path;
7. close #27 only when several regions/zoom levels are visually correct;
8. then resume balanced research expansion and unresolved geometry work.

## Communication preference

The user is action-oriented. Make progress directly, use GitHub as the current record, and report concise milestones. Clearly distinguish **proposed / merged / live / visually accepted**. Do not say something is fixed until it has actually been verified.
