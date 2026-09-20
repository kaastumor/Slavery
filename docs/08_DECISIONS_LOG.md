# Decisions Log

This file records durable methodological choices. Add a dated entry whenever a future change affects ontology, classification, geography, attribution or source policy.

## D-001 — Neutral world outline
**Decision:** Always show neutral land even when historical geometry or evidence is missing.  
**Reason:** Missing data must not visually imply absence or ocean.

## D-002 — Non-Atlantic-first balancing
**Decision:** Build broad global coverage before bulk Atlantic ingestion.  
**Reason:** Atlantic/Western archives are unusually dense and digitized; ingesting them first would create archive-density bias.

## D-003 — P-level is not a source-count score
**Decision:** P0–P4 reflects interpreted historical evidence, not document or voyage counts.  
**Reason:** record survival differs radically across regions and periods.

## D-004 — Multiple attestations matter
**Decision:** Repeated independent attestations can move a practice beyond an isolated instance even without explicit state legislation.  
**Reason:** law is only one dimension of practice.

## D-005 — Law and practice separate
**Decision:** legal status is a separate layer from territorial practice.  
**Reason:** law can recognize, regulate, prohibit or abolish a practice without matching actual social practice.

## D-006 — External participation separate
**Decision:** voyages, ports, merchants, owners, financiers and companies represent participation networks and do not directly set territorial practice intensity.  
**Reason:** participation elsewhere is not the same as practice within a territory.

## D-007 — Owner nationality requires independent evidence
**Decision:** never infer owner nationality from vessel flag, registration, departure port, residence, business base, surname or company jurisdiction.  
**Reason:** these attributes can differ historically and analytically.

## D-008 — Company and person identity separate
**Decision:** corporate jurisdiction does not determine every partner/director/shareholder's nationality.  
**Reason:** firms and persons require separate entity models.

## D-009 — Seshat dataset identity
**Decision:** detailed slavery variables previously used are retained as legacy/Equinox data; do not silently relabel them as current Polaris data.  
**Reason:** version provenance matters.

## D-010 — Historical geometry resolver
**Decision:** use the five-step historical geometry hierarchy defined in `05_GEOGRAPHY_AND_MAP.md`.  
**Reason:** prevents anachronistic boundaries and makes approximation visible.

## D-011 — Database migration target
**Date:** 2026-09-19  
**Decision:** PostgreSQL + PostGIS is the target canonical research database after a validated migration. The v0.6.1 workbook remains canonical until reconciliation and QC succeed.  
**Reason:** the atlas requires relational integrity, temporal querying, historical geometry, spatial indexing, provenance and publishable views in one durable system.

## D-012 — Universal claim identity
**Date:** 2026-09-19  
**Decision:** introduce a base `CLAIM` identity and attach evidence through a true `CLAIM_SOURCE` foreign-key relationship. Specialized claim tables extend `CLAIM`.  
**Reason:** evidence is claim-specific; the previous polymorphic `claim_type + claim_id` bridge is difficult to enforce relationally.

## D-013 — Actor identity separated from roles
**Date:** 2026-09-19  
**Decision:** people and organizations are normalized as `ACTOR`. Owner, financier, insurer, lender, operator and similar functions are separate relationships/claims, not separate identities.  
**Reason:** one historical actor may hold multiple roles, while the analytical distinction between those roles must remain visible.

## D-014 — Generic spatial identity and time-bounded spatial relations
**Date:** 2026-09-19  
**Decision:** introduce `SPATIAL_ENTITY`; `POLITY` is a specialization. Ports, cities, regions and sites may be claim/geometry targets without pretending they are polities. Political containment/control is time-bounded.  
**Reason:** historical places change jurisdiction and many evidence targets are not states.

## D-015 — Historical internal year convention
**Date:** 2026-09-19  
**Decision:** use astronomical signed integer years internally (`1 BCE = 0`, `2 BCE = -1`, `1 CE = 1`) and convert to conventional BCE/CE in the UI. Preserve explicit bounds plus temporal precision and a queryable integer range.  
**Reason:** a continuous integer chronology simplifies interval overlap, containment and BCE/CE calculations while preserving user-facing historical notation.

## D-016 — Source, version and asset separation
**Date:** 2026-09-19  
**Decision:** separate conceptual `SOURCE`, exact `SOURCE_VERSION`, and optional locally archived `SOURCE_ASSET`; preserve bulk-import lineage and source-native values.  
**Reason:** editions/snapshots may differ, raw values must remain auditable, and not every source can legally or practically be mirrored.

## D-017 — Research/publication boundary
**Date:** 2026-09-19  
**Decision:** draft research and public map data are separate logical layers. Public services consume reviewed/published views or release materializations. Published releases must remain reconstructible.  
**Reason:** ongoing research, disputes and corrections must not silently alter the public atlas or erase the history of prior releases.

## D-018 — Web-map delivery strategy
**Date:** 2026-09-19  
**Decision:** MapLibre GL JS is the preferred map client. GeoJSON remains acceptable for small/simple layers; vector tiles are preferred for large/dense layers. Martin is the preferred initial tile server but is replaceable; PMTiles is optional for stable release layers.  
**Reason:** this keeps the map scalable without prematurely locking the project to one server or encoding every small layer as tiles.

## D-019 — Internal identities versus source-native identifiers
**Date:** 2026-09-19  
**Decision:** canonical database entities use generated UUID primary keys. Source-native identifiers and legacy project identifiers are preserved separately and connected through explicit fields/crosswalks.  
**Reason:** IDs from different datasets can collide, change version semantics, or refer to source records rather than stable historical entities. The atlas must retain source identity without making it the global database identity.

## D-020 — Missingness is not an entity
**Date:** 2026-09-19  
**Decision:** documented missing or unknown values are represented as missing/status facts, not as invented historical actors or places. The v0.6.1 `Unknown owner — Orestes` placeholder therefore migrates to a missing-owner relation/status with `actor_id = NULL`, not to an `ACTOR`.  
**Reason:** queryable missingness is useful, but turning “unknown” into an entity creates false identity and corrupts network analysis.

## D-021 — Claimable relationships
**Date:** 2026-09-19  
**Decision:** historically substantive relationship rows such as `VOYAGE_OWNER`, `VOYAGE_FINANCE`, `VOYAGE_STOP`, and evidenced `SPATIAL_RELATION` may carry a `claim_id`. Evidence attaches to that claim through `CLAIM_SOURCE`. Legacy evidence may map one-to-many when a workbook row bundles distinct assertions.  
**Reason:** ownership, financing and jurisdiction are assertions requiring provenance just as actor attributes and territorial-practice classifications do.

## D-022 — Evolving vocabularies use lookup tables
**Date:** 2026-09-19  
**Decision:** research vocabularies expected to grow (practice types, actor/spatial types, relation roles, attribute types) are stored as reference tables rather than hard PostgreSQL enum types. Stable technical lifecycle states may use constrained domains/checks.  
**Reason:** legitimate ontology growth should not require replacing database enum types or weakening referential integrity.

## D-023 — Research coverage has its own data structure
**Date:** 2026-09-19  
**Decision:** research-coverage assessments such as the v0.5.0/v0.6.1 S/P/D/RI region-period matrix are stored separately from territorial-practice claims, initially under the audit/project-metadata layer.  
**Reason:** coverage describes what the project has researched; it is neither historical prevalence nor a P0–P4 practice classification, but it may still be published as a transparency layer.

## D-024 — Unassigned P-level is distinct from P0
**Date:** 2026-09-19  
**Decision:** `TERRITORIAL_PRACTICE_CLAIM.practice_level` may be NULL until an explicit P0–P4 assessment is made. NULL means no P-level assessment has yet been recorded; P0 remains an explicit assessment that no usable practice classification is currently available and never means absence. Legacy S/P/D/RI coverage codes are never converted mechanically to P0–P4.  
**Reason:** forcing a non-null P-level would make disputed, researched-inconclusive, or merely reviewed evidence acquire an unsupported intensity classification and would collapse research coverage into territorial practice.

## D-025 — Research-coverage provenance is separate from claim evidence
**Date:** 2026-09-19  
**Decision:** research-coverage assessments may link to exact reviewed source versions through `RESEARCH_COVERAGE_SOURCE`. This link records what was consulted for the coverage/RI/dispute assessment and does not itself support a territorial-practice claim.  
**Reason:** researched-inconclusive and disputed cells need auditable provenance even when no positive historical claim is justified; reusing `CLAIM_SOURCE` would falsely imply that the source supports a practice claim.

## D-026 — Full canonical workbook preservation precedes canonical switch
**Date:** 2026-09-19  
**Decision:** the v0.6.1 importer must preserve every non-empty row from every workbook tab in raw ingest lineage, in addition to the original workbook asset/checksum. A successful migration of only the Atlantic seed and coverage matrix cannot qualify as a canonical database migration. The global evidence sheets must be semantically normalized and reviewed before canonical cut-over.  
**Reason:** v0.6.1 contains substantive global evidence sheets as well as Atlantic/network sheets. Omitting them would silently discard canonical project content even if Atlantic reconciliation passed.

## D-027 — Generic external participation claims
**Date:** 2026-09-19  
**Decision:** add `EXTERNAL_PARTICIPATION_CLAIM` for non-voyage evidence of participation in enslavement, slave-trading, captive movement, markets, finance or related networks. Such evidence remains separate from `TERRITORIAL_PRACTICE_CLAIM` and does not set P0–P4.  
**Reason:** global evidence includes network participation that cannot be represented honestly as territorial practice and is not always tied to a specific voyage. The Anshan/Elam c. 2130–2110 BCE case is an explicit test: the workbook supports enslavement/export/purchase-network participation while cautioning against a territorial prevalence classification.

## D-028 — Reproducible development environment and migration ledger
**Date:** 2026-09-19  
**Decision:** use Docker Compose as the reproducible local development boundary for PostgreSQL/PostGIS and Python migration tooling. SQL migrations are applied through a checksum ledger (`atlas_meta.schema_migration`) that records each applied filename and SHA-256 and rejects later checksum changes. Local development, CI, staging and production remain distinct environments; local Docker volumes are never canonical release storage.  
**Reason:** repeated development and CI must be deterministic and must not depend on a manually configured workstation. A migration ledger prevents accidental reapplication or silent editing of already-applied schema changes while keeping the production hosting provider undecided.

## D-029 — Canonical workbook releases are checksum-identified
**Date:** 2026-09-19  
**Decision:** the v0.6.1 importer verifies the exact SHA-256 of the canonical workbook in addition to semantic/count invariants. A byte-different workbook is not accepted as v0.6.1; it must be treated as a new release/version even if its visible contents appear equivalent.  
**Reason:** immutable release identity requires detecting accidental re-saves, edits or substitutions. Semantic invariants protect meaning, while the checksum protects exact release provenance.


## D-030 — Direct research entry uses the canonical relational model
**Date:** 2026-09-19  
**Decision:** New hand-researched historical cases should be entered directly into PostgreSQL/PostGIS through the normalized `SOURCE → SOURCE_VERSION → SPATIAL_ENTITY → CLAIM → specialized claim → CLAIM_SOURCE → GEOMETRY` path. A new Excel workbook is not an intermediate authoring requirement. New claims default to unpublished and must pass review/publication gates separately.  
**Reason:** the atlas now has a working relational research store; routing new manual research through spreadsheets would duplicate work and recreate migration overhead while weakening claim-level provenance.

## D-031 — Public MVP previews do not imply a canonical data switch
**Date:** 2026-09-19  
**Decision:** The project may publish explicitly non-canonical preview releases for end-to-end product validation. Every such preview must have immutable release membership, QC summary, changelog and unresolved-issues metadata, and public services must resolve data through the release manifest plus publish boundary. The canonical v0.6.1 release remains unchanged until the documented canonical-switch criteria are met.  
**Reason:** the web product needs real public slices before the historical workbook migration is complete, but a functioning preview must not silently redefine the canonical research release.

## D-032 — The atlas is an evidence-synthesis project, not an original research center
**Date:** 2026-09-19  
**Decision:** The Historical Slavery Atlas collects, normalizes, reconciles and digests existing historical evidence and specialist scholarship into transparent claims. It does not present its own ad hoc interpretation of difficult historical controversies as new scholarship when relevant specialist historiography already exists. Primary/source-native evidence anchors bounded facts; specialist historical scholarship is normally the interpretive backbone for classification, prevalence, continuity and structural significance.  
**Reason:** The atlas's value lies in structured global synthesis, provenance and comparability. Attempting to function as an independent research institute would exceed the project's role, encourage inconsistent interpretation across regions and duplicate specialist scholarship.

## D-033 — Source conflict does not automatically create a disputed atlas designation
**Date:** 2026-09-19  
**Decision:** When evidence conflicts, preserve the conflict at claim-source level and synthesize it using ordinary historical source criticism together with the treatment found in relevant specialist historiography. Record the best-supported working designation when historians provide a defensible interpretation. Use `disputed` only when credible specialist scholarship remains materially divided over the historical classification after synthesis. A source marked `challenges` or `qualifies` does not automatically nullify the claim or force `practice_level = NULL`.  
**Reason:** Historical sources frequently contradict one another because of chronology, genre, transmission, terminology, observer perspective or scope. Treating every contradiction as unresolved would hide rather than represent historical knowledge.

## D-034 — No usable claim means unknown; missingness never becomes historical absence
**Date:** 2026-09-19  
**Decision:** If no defensible territorial-practice claim exists for a place/time, the atlas displays the historical condition as unknown. Research coverage records whether the project has researched the target and with what result. No claim is distinct from P0: P0 is an explicit reviewed assessment that the evidence package does not currently support a usable P1–P4 classification. Neither no claim, P0, researched-inconclusive status, nor unresolved geometry implies historical absence.  
**Reason:** The atlas must distinguish what is historically known from what the project has not established. Otherwise unequal source survival and research coverage would become false negative historical assertions.

## D-035 — Broad atlas designations follow the evidence package, not isolated source wording
**Date:** 2026-09-19  
**Decision:** Broad territorial classifications and P-levels must be based on the interpreted evidence package. A primary text, law, inscription, transaction, external observer or individual specialist work is recorded for what it can support, but its wording is not mechanically promoted to the atlas designation. For broad questions, relevant specialist historical synthesis normally determines how bounded evidence should be understood. Contrary evidence remains visible through provenance and evidence direction.  
**Reason:** Source types answer different historical questions. This preserves both primary evidence and scholarly interpretation while preventing one exceptional document or observer from controlling a territory-wide classification.

## D-036 — Published polygon fills are clipped to the neutral land mask
**Date:** 2026-09-20  
**Decision:** Preserve historical/source polygons unchanged in `atlas.geometry` and `publish.geometry`. For public map rendering, polygonal geometry is delivered through a separate render view that intersects it with the versioned neutral world land mask. Points and other non-polygon geometry are unchanged. The render transformation must be exposed in metadata.  
**Reason:** historical boundary datasets such as Cliopatria can contain coarse reconstructed coastlines that visibly extend into the neutral ocean layer. Clipping the display fill to the same neutral land mask removes this cartographic artifact without silently rewriting the source geometry or claiming improved historical inland boundaries.

## D-037 — Basemap and historical overlays share one canonical 1:10m land fabric
**Date:** 2026-09-20  
**Decision:** Register a single versioned physical-land fabric in `cartography.land_fabric`. The public basemap and the coastline clipping performed by `publish.map_geometry` must derive from that same active fabric. The initial master is Natural Earth `ne_10m_land` v5.1.1 pinned to upstream commit `ca96624a56bd078437bca8184e78163e5039ad19` and blob `2d76878175b8054acd9c5a52917ee9ea59a36fc5`. The prior 1:110m static land asset is removed from normal frontend use. Historical source geometry remains unchanged.  
**Reason:** every Cliopatria-derived polity can inherit the same raster-derived coastline/alignment problem. Per-polity clipping against a separately maintained basemap is not structurally sufficient. One physical geometry source guarantees that neutral land and rendered historical coastlines use identical coordinates while keeping inland historical boundaries independent and provenance-faithful.

## D-038 — Physical coastline replacement is a render-topology operation
**Date:** 2026-09-20  
**Decision:** One-sided intersection with the canonical land fabric is not sufficient for coarse historical polygon sources. When a reviewed historical polygon is intended to reach a physical coastline, public render geometry must treat the historical source as evidence for the landward political footprint while deriving the physical shoreline from the canonical cartographic land fabric. Source geometry in `atlas.geometry` / `publish.geometry` remains unchanged. Coastal normalization is a publication/render transformation, must be auditable in render metadata, and must be implemented by reproducible source-family/render policy rather than per-entity hand editing. Inland historical boundaries must remain source-derived. Where the system cannot distinguish a coarse source coastline from a genuine inland frontier safely, the geometry must remain unresolved or be rendered in a less committal form rather than inventing precision.  
**Reason:** Cliopatria polygons can be raster/coarse enough that their source boundary alternates between seaward overshoot and landward underreach. `ST_Intersection(source, land)` removes ocean overshoot but leaves the landward underreach untouched, producing a zipper/stair-step coastline even though the basemap and clipping mask use the same Natural Earth 1:10m fabric. The defect therefore exists in the render topology, not in individual historical entities.

## D-039 — Raster-derived historical boundaries use bounded render generalization and precomputation
**Date:** 2026-09-20  
**Decision:** Coarse raster-derived historical polygons may receive a bounded, source-family-specific **render-only boundary generalization** before public display. The canonical/source geometry remains unchanged. For the initial Cliopatria policy, one Chaikin smoothing iteration is permitted for polygonal display geometry, subject to QC limits on smoothing displacement, area change and geometry validity. Physical coastline recovery then follows D-038 and the result is clipped to the canonical Natural Earth 1:10m land fabric. Normalized display geometry must be precomputed/materialized outside the public request path; the API must read cached render geometry and fall back to the proven land-clip view when no valid cache row exists.  
**Reason:** The visible staircase artifacts occur on inland frontiers as well as coastlines because the source polygons themselves encode coarse raster/grid boundaries. Coastline replacement alone cannot remove inland stair-stepping. A bounded cartographic generalization is more faithful than displaying grid artifacts as if they were historically meaningful precision, but it must remain explicitly separate from source geometry. Live testing also showed that computing geography buffers/unions dynamically inside `publish.map_geometry` can stall the MVP, so expensive normalization must never run per request.

**Initial QC basis:** across the 39 Cliopatria polygon geometries in `mvp-preview-ancient-v2`, one Chaikin iteration produced zero invalid geometries, mean area change of approximately -0.039%, maximum absolute area change of 0.775%, mean source-to-smoothed Hausdorff distance of about 17.5 km and maximum of about 30.3 km (Web Mercator diagnostic). These values justify a conservative initial policy ceiling of 35 km smoothing displacement and 1% absolute area change. The metrics are render-QC diagnostics, not historical confidence estimates.

## D-040 — Cliopatria live render policy uses two bounded smoothing iterations
**Date:** 2026-09-20  
**Decision:** After live browser review of the first precomputed generalized geometry, the active Cliopatria render policy uses **two** Chaikin smoothing iterations rather than one. The D-039 QC ceilings remain unchanged: no invalid geometry, no more than 35 km source-to-smoothed Hausdorff displacement and no more than 1% absolute area change. Approximate historical polygons should also use a visually softer outline than exact/specialist geometry so residual source uncertainty is not presented as a falsely crisp frontier.  
**Reason:** One iteration removed the dominant raster/grid staircase but left a visible residual angular signature on some inland/desert frontiers. Across all 39 Cliopatria polygons in the current MVP, two iterations still produced zero invalid geometries, maximum absolute area change of 0.968% and maximum Hausdorff displacement of about 30.3 km. A third iteration crossed the 1% area-change ceiling for one geometry, so two iterations are the conservative live-reviewed maximum under the present policy.

## D-041 — Coastal completion is adaptive and area-bounded
**Date:** 2026-09-20  
**Decision:** For approved coarse historical polygon source families, physical-coastline recovery may expand beyond the base recovery corridor only through a precomputed adaptive tier. The initial Cliopatria policy keeps a 25 km baseline, tests larger recovery corridors up to 50 km, and accepts the largest tier whose added land versus the 25 km baseline is no more than 2% of the baseline display area. Failed/unsafe candidates fall back automatically to a smaller tier or the 25 km baseline. The chosen recovery distance and added-area percentage are stored in render-cache metadata. Source geometry remains immutable and inland smoothing remains governed separately by D-039/D-040.  
**Reason:** Live review after D-040 showed remaining coastal land gaps where the source polygon under-reaches the physical shoreline by more than 25 km. A single globally larger corridor is unsafe for smaller coastal polities: tests showed 50 km would add only about 0.37% to the 500 BCE Achaemenid display but about 7.28% to Baekje. An adaptive, area-bounded policy fixes the same source-family artifact without introducing entity-specific hand tuning or large uncontrolled territorial expansion.

## D-042 — Public MVP availability is a release-quality invariant
**Date:** 2026-09-20  
**Decision:** The public atlas must never depend on unbounded or computationally heavy spatial work in the request path. Expensive geometry normalization, cache generation and bulk spatial diagnostics run in CI, staging/local infrastructure or bounded precomputation jobs, not synchronously during public API requests. Production changes that touch public map/data delivery require an availability gate: pre-change health check, bounded migration, post-change API/data sanity check and latency check. The browser must fail visibly after a bounded timeout rather than remain indefinitely in a loading state. An automated external monitor checks the public API and GitHub Pages regularly and records an incident when either is unavailable, structurally invalid or too slow.
**Reason:** Two separate live iterations of boundary-normalization work caused the MVP to remain stuck in a loading state because expensive production spatial work saturated or blocked the serving path. Availability must therefore be tested as part of release correctness rather than treated as an operational afterthought.

**Initial operational thresholds:** browser API timeout 12 seconds; automated API availability threshold 10 seconds; monitor cadence 15 minutes. These are operational guardrails and may be tightened as the serving path matures.

## D-043 — Automatic project restart is a guarded self-healing action
**Date:** 2026-09-20  
**Decision:** The public MVP monitor may trigger an automatic Supabase **project restart** only after two restart-eligible public API failures separated by 120 seconds, while Supabase still reports the project `ACTIVE_HEALTHY`. Automatic restart is limited to once per two hours per open availability incident. Client/payload errors that indicate application defects rather than service unavailability do not qualify. After restart, the workflow waits up to ten minutes for the public API to recover and records the outcome in the incident issue.  
**Reason:** the 2026-09-20 outage recovered only after a full project restart, while Supabase's control plane had reported the project healthy despite the database refusing usable connections. Restart is a valid temporary recovery mechanism for overloaded/stuck projects, but unguarded restart loops could hide underlying defects or amplify an external platform outage.

**Credential boundary:** automated restart uses a dedicated scoped Supabase Management API personal access token stored only as the GitHub Actions secret `SUPABASE_MANAGEMENT_TOKEN`. It should be limited to this project and the minimum Project Settings read-write permission required for restart. The token must never be committed to the repository.

## D-044 — Stop bespoke coastal heuristics; use standard GIS preprocessing for Cliopatria render geometry
**Date:** 2026-09-20  
**Decision:** The atlas will not continue inventing source-specific coastline buffers or increasingly complex PostGIS recovery heuristics for Cliopatria. The published Cliopatria methodology itself documents that the polygons were vectorized from 2400×4800 raster map images, that coarse raster resolution can leave polygons misaligned with coast/land datasets, and that the source authors already applied smoothing to reduce raster border artifacts. This is therefore a known source-generalization problem, not an atlas-specific historical-geometry problem.

The next render pipeline must be built from established GIS operations executed **offline/pre-publication**, with immutable source geometry preserved:
1. cartographic smoothing/generalization using a standard GIS implementation (initial evaluation: QGIS `native:smoothgeometry` / Mapshaper `-smooth`);
2. snap the generalized historical polygon to the canonical Natural Earth 1:10m physical-land boundary using a standard reference-layer snapping operation (initial evaluation: QGIS `native:snapgeometries`, behavior “prefer closest point, insert extra vertices where required”);
3. clean/validate topology with standard GIS tools;
4. clip the final display polygon to the same canonical Natural Earth land fabric;
5. materialize the result as render geometry and serve it without geometry processing in the public request path.

The custom adaptive coastal-completion policy from D-041 is retained in migration history for reproducibility but is **not** the active production policy while this standard pipeline is evaluated. The fully populated v3 render cache remains the public fallback until the standard GIS result passes multi-region visual and quantitative QC.

**Reason:** continuing to tune custom buffer distances reproduces a solved GIS workflow badly and risks source-family distortions, operational instability and non-generalizable code. Standard snapping algorithms are explicitly designed to align one geometry layer to a reference layer within a tolerance and can insert/remove vertices so boundaries follow the reference geometry exactly. Standard smoothing/generalization tools also expose controls for preserving sharp corners rather than rounding every historical frontier indiscriminately.

## D-045 — Use a mainstream, scale-aware cartographic stack
**Date:** 2026-09-20  
**Decision:** The atlas standardizes on a mainstream open GIS/cartography stack rather than bespoke map geometry logic.

1. **Canonical physical fabric:** Natural Earth physical land/coastline remains the authoritative physical reference. The 1:10m dataset is the canonical master because the product supports country/region zooms and because it is the highest-detail Natural Earth global physical product. Lower-zoom display may use generalized derivatives or Natural Earth's 1:50m/1:110m products, but historical overlays and the visible physical shoreline at any given zoom must be produced from the same scale/topology so they cannot diverge.
2. **Historical source:** Cliopatria remains a historical polity source, not the physical coastline authority. Raw/source polygons stay immutable.
3. **Conflation/preprocessing:** alignment to the physical fabric is performed offline with established GIS algorithms (QGIS/GEOS/GDAL; Mapshaper where appropriate for cartographic smoothing/topology), including reference-layer snapping, geometry repair and clipping. Custom distance-buffer heuristics are not the preferred solution.
4. **Rendering/delivery:** MapLibre remains the web renderer. As geometry volume grows, move from full GeoJSON payloads toward standard vector-tile delivery (Tippecanoe/Martin or equivalent) rather than adding client-side geometry complexity.
5. **Scale discipline:** do not display more physical or historical precision than the underlying source supports. A more detailed coastline may improve visual fit, but it must not imply that uncertain historical inland frontiers are equally precise.

**Reason:** this maximizes reuse of established GIS behavior, documentation, tooling and operational experience. Natural Earth is widely used as a global physical map source, including by Cartopy; QGIS provides standard geometry snapping that inserts/removes vertices to make geometries follow a reference layer within tolerance; Mapshaper provides topology-aware cleaning/generalization; and MapLibre's own guidance recommends vector tiling as datasets grow. This makes future problems more likely to have known solutions and community experience rather than requiring atlas-specific geometry inventions.

## D-046 — Separate curation, cartography build, release promotion and operations; promote immutable artifacts
**Date:** 2026-09-20  
**Decision:** The atlas adopts four **logical** pipeline lanes with explicit state boundaries:

1. **Research curation:** source acquisition/registration → claim construction → automated validation → draft ingestion → editorial/research review → release eligibility.
2. **Cartography build:** immutable historical source geometry → offline render candidate → topology/quantitative QC → representative visual QC → approved render artifact.
3. **Release/promotion:** assemble only reviewed claims and approved geometry → release manifest/QC → immutable release artifact → staging verification → production promotion → post-deploy health.
4. **Operations:** independent availability monitoring, incident handling, guarded recovery and escalation.

These are logical lanes, not a requirement to create one GitHub Actions file per individual step. Repeated deterministic logic should be implemented as scripts/reusable workflows; top-level workflows should remain few and purpose-specific.

**Build/promotion rule:** expensive or interpretive outputs are built once from pinned inputs, assigned provenance/checksums, and promoted unchanged. Production must not regenerate a geometry candidate, research interpretation or release payload that was tested elsewhere.

**Write boundary:** pull-request CI is read-only with respect to production. Research CI may validate case files but must not publish them. Geometry CI may create candidate artifacts but must not alter canonical source geometry or production render caches. Only an explicit release/promotion job may change published state or production-serving materializations.

**Review boundary:** automated QC can establish structural validity, schema conformance and quantitative thresholds, but it cannot substitute for historical/editorial review or the representative visual review required for cartographic transformations that can change apparent extent.

**Provenance boundary:** every promoted derived artifact must retain enough metadata to identify source versions, code revision, tool/runtime versions, processing parameters, QC results and file/content hashes.

**Reason:** this matches established scientific-data and CI/CD practice more closely than a proliferation of ad-hoc workflows. USGS guidance recommends scripted, modular, standardized and reproducible processing with provenance recorded throughout the data lifecycle; FAIR requires detailed provenance and domain-relevant standards; GitHub Actions supports reusable workflows and protected deployment environments; and mainstream continuous-delivery guidance recommends build-once/promote-many immutable artifacts rather than rebuilding in each environment. The separation also prevents experimental cartography or unfinished research from affecting the public atlas.

## D-048 — Geometry candidates are quarantined by explicit render-QC policy before visual acceptance
**Date:** 2026-09-20  
**Decision:** The consolidated geometry build pipeline classifies each derived render geometry against a versioned QC policy before any promotion. The initial policy requires valid/non-empty geometry, no more than 2% absolute source-area change, and no more than 5% source-normalized symmetric-difference area. Candidates that exceed a hard gate are marked `quarantined`; the previous approved render/fallback remains in use.

Hausdorff distance is retained as a diagnostic rather than a universal hard gate. In representative testing, Western Han and Mauryan candidates showed large maximum Hausdorff distances while changing less than ~1.2% of source area by symmetric difference, demonstrating that a single extreme boundary point can dominate the metric for very large polygons. Visual review remains mandatory before promotion because automated geometry metrics do not determine historical/cartographic acceptability.

The policy is stored as data/configuration rather than hidden in workflow code. Build artifacts record the QGIS container digest, Natural Earth checksum, transformation parameters, source inputs, QC reports and artifact hashes.

**Reason:** automated map QC should catch large distortions consistently without turning one fragile metric into a proxy for cartographic correctness. Explicit quarantine/fallback makes outliers such as Baekje visible and reviewable while allowing unrelated geometries to progress safely.

## D-047 — Research-case ingestion is immutable and idempotent
**Date:** 2026-09-20  
**Decision:** Every new claim-centric research package must carry a stable `case_key`. The loader computes a SHA-256 hash from canonical JSON serialization and records `case_key -> content hash -> claim_id` in `audit.research_case_ingest`.

Reapplying the same case key with the same content is a no-op. Reapplying the same key with different content is rejected. A materially revised historical interpretation must therefore use a new case key and the explicit review/supersession model instead of silently changing an already-ingested package.

This ledger applies prospectively to research packages ingested through the claim-centric loader. Historical claims and stored research fixtures created before this mechanism are not retroactively assigned synthetic case identities merely for completeness.

**Reason:** research ingestion will increasingly run through repeatable automation. Retry-safe writes are necessary to prevent workflow retries, operator reruns or transient failures from creating duplicate claims. Immutable case identities also improve provenance by making a substantive change visible as a new reviewed research package rather than an invisible mutation.

## D-049 — Prefer the least-distorting tested QGIS snap tolerance; do not auto-upgrade tolerance
**Date:** 2026-09-20  
**Decision:** For new generic Cliopatria render candidates under the standard QGIS + Natural Earth policy, 10 km is the preferred baseline snap tolerance among the currently evaluated 10/15/20/25 km matrix. Larger tested tolerances remain alternate candidates for diagnosis or explicit visual override; they are not automatically preferred merely because they pass the same hard QC gates.

If the preferred 10 km candidate fails a hard gate, the geometry is quarantined and the previous approved render/fallback remains in use. The pipeline must not silently escalate to a larger tolerance to force a candidate through. Every QC-passing candidate still requires visual review before promotion.

Existing explicitly approved/published render artifacts, including the visually accepted Achaemenid pilot, are not invalidated or regenerated solely because 10 km becomes the default candidate baseline.

**Reason:** Representative testing found 10 km to be the least-distorting tested tolerance overall, while larger tolerances did not produce monotonic improvement. Baekje also demonstrates that changing tolerance does not rescue every source geometry: it remains a material outlier across the tested matrix. A conservative fixed baseline plus quarantine/fallback is more reproducible than selecting whichever tolerance happens to make an individual geometry look acceptable.

## D-050 — Promote external render geometry only from an immutable acceptance registry
**Date:** 2026-09-20  
**Decision:** Promotion of externally generated render geometry is a separate, explicit step from candidate generation. A promotion must consume the **exact immutable artifact that passed automated QC and visual review**; production must not recompute the geometry.

Each promotion batch is represented by a checked-in acceptance registry that records:

- geometry-build run/artifact identity and Git SHA;
- artifact-manifest and candidate/QC file SHA-256 values;
- canonical land-fabric identity/checksum and render parameters;
- the browser-review run used for cartographic acceptance;
- per-geometry automated-QC state;
- per-geometry cartographic visual disposition;
- per-geometry semantic-scope disposition;
- the requested action: `promote`, `quarantine`, or `preserve_existing_live`.

The promotion tool must verify all recorded checksums before it can produce a database-ready plan. `promote` is allowed only when automated QC passed, cartographic review is accepted, semantic scope is explicitly accepted, the source geometry exists in reviewed state, the active land fabric matches, and the target render-cache slot is not already occupied unexpectedly. Quarantined candidates are never inserted. Existing explicitly accepted live renders are preserved unless a later registry deliberately supersedes them.

The registry, together with the immutable build artifact and Git history, is the provenance record for the promoted derived geometry. The database render cache is a serving materialization, not the sole provenance store. This avoids adding premature per-row provenance columns while the broader release/provenance model under #43/#4 is still being designed.

**Reason:** issue #27 needs a safe route from reviewed CI geometry to production without violating D-046's build-once/promote-unchanged rule. A versioned acceptance registry makes the human cartographic and semantic decisions explicit, prevents a green CI run from becoming an implicit publication decision, and allows the serving cache to remain replaceable/reconstructible from immutable inputs.



## D-051 — Internal research schemas are not a client Data API
**Date:** 2026-09-20  
**Decision:** The `atlas`, `audit`, `cartography` and `publish` PostgreSQL schemas are internal database boundaries, not direct browser/client Data API surfaces. Anonymous and authenticated client roles must not receive schema `USAGE` or table mutation/read privileges on those schemas merely to serve the public atlas. The current public browser consumes reviewed/released data through the `atlas-data` Edge Function, which queries the publication boundary server-side. If direct PostgREST access is introduced later, it must use a deliberately exposed API schema or other explicitly reviewed surface with least-privilege grants and RLS/policies appropriate to that public contract.

RLS-disabled tables in an internal schema are therefore not, by themselves, evidence that those tables are publicly reachable. Security review must evaluate both PostgREST exposure and PostgreSQL grants. Defense in depth still requires explicit revokes/default-privilege controls so future migrations cannot accidentally make internal schemas client-accessible.

**Reason:** Supabase's Data API security model has two gates: schema/object grants determine whether client roles can reach an object, and RLS controls which rows they may access once reachable. Production verification on 2026-09-20 found `anon` and `authenticated` have no `USAGE` on `atlas`, `audit`, `cartography` or `publish`, and no SELECT/INSERT/UPDATE/DELETE privileges across the 54 checked internal tables/views. The authoritative Supabase security advisor did not report an RLS-disabled-table exposure finding; its only current security lint was a mutable `search_path` on `atlas.make_year_range`. Keeping the public contract behind the Edge Function preserves the project's reviewed/published boundary and reduces accidental draft-data exposure.


## D-052 — Every public deployment carries a checksummed static release snapshot fallback
**Date:** 2026-09-20  
**Decision:** Until the full staging/build-once release pipeline in #43/#4 is complete, every successful public web deployment must materialize the exact currently published `atlas-data` API payload as a checksummed static snapshot inside the same GitHub Pages deployment artifact. The browser remains API-first, but if the live API is unavailable, times out, or returns an unusable response, it may load that deployment-bound snapshot and must label the session as a static fallback.

The snapshot build must:
- fail closed if the current published API payload is unavailable or structurally invalid;
- canonicalize the JSON payload before hashing/writing;
- record release version, schema version, source Git revision, counts and SHA-256 in a snapshot manifest;
- upload the snapshot as a retained CI artifact as well as embedding it in the Pages deployment;
- never change the canonical historical data release or publish draft/unreviewed data;
- never allow a failed snapshot build to replace the last known-good Pages deployment.

This is an availability/recovery materialization, not yet the final release-promotion architecture. Future #43/#4 work must move snapshot creation earlier so the immutable release artifact is built once from approved release inputs and promoted unchanged through staging and production, rather than deriving the fallback from an already-live API.

**Reason:** the public preview currently depends on a live database-backed Edge Function. A transient database/API outage should not make an already-published atlas state disappear. Embedding a validated static copy in the web deployment provides an immediate recoverable state while preserving the stronger build-once/promote-many target as a separate remaining requirement.
