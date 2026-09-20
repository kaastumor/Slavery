# Current Project Status

**Status date:** 2026-09-20  
**Canonical data version:** v0.6.1  
**Current public preview:** `mvp-preview-ancient-v2` (non-canonical)  
**Repository main head at status cut:** `2fb0cc0a7b60b08f1d0123a1f7a187addf405258`

## 1. Project position

The Historical Slavery Atlas now has a working end-to-end research, cartography, publication and web-serving stack.

The canonical historical data release remains the preserved `Historical_Slavery_Atlas_v0.6.1_Controlled_Atlantic_Ingestion.xlsx`. The live PostgreSQL/PostGIS database is the working normalized research system, and the public MVP consumes an explicitly non-canonical reviewed preview release. Database growth or newer schema work does not silently redefine the canonical historical release.

The project remains an evidence-synthesis and data-curation project. Historical claims, legal status, external/network participation, research coverage and geometry remain separate dimensions.

## 2. Live production state

Supabase project:

- project ref: `dilnayfllygkplsdymel`
- project name: Historical Slavery Atlas
- region: `eu-central-1`
- current control-plane state at this status cut: `ACTIVE_HEALTHY`
- PostgreSQL 17.6.1
- public edge function: `atlas-data`

Verified live data state:

- 42 territorial-practice claims
- 31 published claims
- 68 geometry records
- 94 render-cache rows
- latest published preview: `mvp-preview-ancient-v2`
- research-case idempotency ledger exists in production

The live migration ledger currently includes migrations through `0022_research_case_idempotency`. Historical ledger irregularities remain: repository-era objects corresponding to some earlier migrations existed before the ledger was fully reconciled, and `0016_restore_fast_map_geometry` appears three times in the Supabase migration history due retry/timeouts. Do not rewrite migration history casually; treat issue #26 as the reconciliation record.

## 3. Public availability and recovery

The second production outage during cartographic work is resolved. Issue #35 is closed.

Current safeguards:

- frontend API request abort after 12 seconds instead of infinite loading
- Retry UI on load failure
- external availability monitor every 15 minutes
- monitor also runs after main pushes
- API latency/shape and GitHub Pages health checks
- automatic incident issue creation/update/closure
- guarded Supabase project self-heal through the Management API
- restart requires two restart-eligible failures 120 seconds apart
- restart cooldown: one automatic restart per two hours
- no heavy spatial reconstruction or exploratory diagnostics in the production request path

The Supabase management credential is stored as the GitHub Actions secret `SUPABASE_MANAGEMENT_TOKEN`.

## 4. Cartography state — active P0

Issue #27, **P0 map alignment**, remains open and is the active product-quality blocker.

The important architectural reset is complete:

- Natural Earth 1:10m is the canonical physical land/coastline fabric.
- Cliopatria remains a historical-polity source, not the coastline authority.
- source historical geometry remains immutable.
- coastline/generalization work is performed offline with standard GIS tooling.
- QGIS/GEOS/GDAL are the preferred processing stack; Mapshaper may be used for topology-aware generalization where useful.
- MapLibre is the web renderer.
- bespoke adaptive coastline-buffer heuristics are no longer the preferred direction.

### Accepted live pilot

The Achaemenid ~500 BCE case was processed with the standard QGIS + Natural Earth pipeline and visually accepted by the user in the live MVP.

Production currently has two Achaemenid render-cache rows under:

`cliopatria-qgis-natural-earth-v1`

The -499 to -480 slice changed from 620 source vertices to 6,125 render vertices, with approximately +0.071% area change. The source geometry was not overwritten.

### Representative validation

PR #41 was merged as `ab88213e5bb9549d6336fdedfc2c48fc35201680`.

Representative QGIS validation now covers:

- Hittite central Anatolia
- New Kingdom Egypt
- Baekje
- Western Han China
- Roman Empire
- Mauryan Empire
- Achaemenid benchmark

CI evaluates 10/15/20/25 km snap tolerances with geometry validity, area change, symmetric difference and Hausdorff-style displacement diagnostics.

Important finding: Baekje behaves materially worse than the larger benchmark geometries and loses roughly 8–9% of area across the tested tolerance range. It must not be blindly promoted under a universal tolerance. The correct pipeline behavior is quarantine/fallback while the source/geometry case is reviewed separately.

Do not promote all representative candidates to production merely because CI is green.

## 5. Geometry-source strategy

Cliopatria remains the current open global deep-time baseline, but it is not assumed to be the best geometry source for every region/period.

`docs/18_GEOMETRY_SOURCE_SURVEY.md` records the current survey. Priority specialist sources to evaluate include:

- CShapes 2.0 for modern historical international borders in its covered period
- CHGIS for historical China, subject to exact version/license review
- OpenHistoricalMap as a supplementary geometry/source-discovery layer
- Pleiades for ancient place identity and local geography
- CONFOEDERATIO / Naissance HGIS as a newer global comparator requiring provenance/license/quality evaluation

Resolver rule remains: better specialist historical geometry may supersede Cliopatria where defensible and compatible.

## 6. Pipeline architecture

PR #42 was merged as `1301a98e59f070f75f47b08ea07570f452d5166c`.

Decision D-046 and `docs/19_PIPELINE_ARCHITECTURE.md` define four logical lanes:

1. research curation
2. cartography build
3. release/promotion
4. operations

Key rules:

- PR/ordinary CI is read-only toward production
- build once, promote the exact immutable artifact
- research validation is not historical/editorial approval
- generated geometry is not production geometry until approved
- failed candidates may be quarantined/fallback rather than blocking unrelated good candidates
- provenance/checksums are required for promoted derived artifacts
- staging and production should become explicit deployment boundaries
- operations monitoring/self-heal remains independent from research/build pipelines

Current new CI gates:

- `research-case-ci.yml`
- `release-candidate-ci.yml`
- foundation `ci.yml`
- current QGIS geometry experiment workflows
- `mvp-health.yml`
- `mvp-self-heal.yml`

The QGIS experiment workflows are temporary. After #27 is resolved they should be consolidated into one parameterized `geometry-build.yml` rather than retained as permanent workflow sprawl.

## 7. Research-ingestion hardening

Retry-safe research ingestion is now implemented and live.

Migration `0022_research_case_idempotency.sql` adds `audit.research_case_ingest`.

New research cases can carry a stable `case_key`; the loader computes a canonical JSON SHA-256 content hash.

Behavior:

- first application inserts the unpublished claim and ledger row
- exact retry is a no-op
- the same `case_key` with changed content is rejected
- historical claim changes must follow an explicit new case/supersession/review path rather than silent in-place mutation

This closes the most immediate duplicate-claim risk before automated research ingestion is expanded.

## 8. Current ancient research preview

`mvp-preview-ancient-v2` remains the public preview.

It contains 31 reviewed published claims across 27 released spatial targets. Several accepted claims intentionally remain geometry-unresolved rather than receiving false polygons.

Research expansion can continue independently of publication. Weak/deferred candidates remain unpublished until evidence improves.

The canonical v0.6.1 release remains unchanged.

## 9. Immediate priorities

### P0 — finish map/render quality

1. Finish multi-region acceptance criteria for #27.
2. Quarantine or separately diagnose Baekje rather than weakening global QC.
3. Determine whether the standard QGIS recipe can be promoted source-family-wide or requires bounded classes/recipes.
4. Preserve previous approved render/fallback for any failing geometry.
5. Once representative visual/QC acceptance is complete, materialize the approved render artifacts and close #27.

### P1 — pipeline hardening (#43)

1. Consolidate geometry experiment workflows into a parameterized geometry-build workflow.
2. Attach immutable provenance/checksum manifests to geometry candidates.
3. Configure real staging and production deployment boundaries.
4. Build release promotion from tested artifacts rather than recomputing.
5. Materialize static/recoverable published-release snapshots so a transient DB outage cannot take an already-published release offline.

### P1 — research/data growth

After #27 is visually resolved, resume globally balanced research, unresolved-geometry work and external-participation presentation. Do not let high-density Atlantic datasets mechanically dominate the next expansion.

## 10. Known unresolved items

- #27 P0 map alignment — open
- #26 migration-ledger reconciliation — nonblocking but unresolved
- #43 pipeline hardening / protected release promotion — open
- Baekje QGIS render candidate — quarantine/fallback case
- overbroad historical geometry audit, especially whole-imperial proxies used for narrower evidence targets
- several current preview claims intentionally geometry-unresolved
- static published-release fallback not yet implemented
- real staging environment not yet created

## 11. Operational rule for the next session

GitHub `kaastumor/Slavery` is the source of truth for current implementation status.

Before doing new work:

1. inspect `main` and open issues/PRs rather than relying only on chat history;
2. read `docs/00_START_HERE.md`, `01_PROJECT_STATUS.md`, `02_METHOD_AND_ONTOLOGY.md`, `03_SOURCE_POLICY.md`, `04_DATA_MODEL.md`, `05_GEOGRAPHY_AND_MAP.md`, `08_DECISIONS_LOG.md`, `11_SYSTEM_ARCHITECTURE.md`, and `19_PIPELINE_ARCHITECTURE.md`;
3. verify Supabase health with a cheap query before any production change;
4. keep heavy GIS work in CI/local/staging;
5. do not change the canonical v0.6.1 historical release unless explicitly creating and validating a new canonical version.
