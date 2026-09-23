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


## D-053 — Public serving uses an explicit release-channel pointer, not “latest published”
**Date:** 2026-09-20  
**Decision:** Public serving must select the active non-canonical preview through an explicit release-channel pointer rather than implicitly choosing the most recently created published manifest.

The initial channel is `public_mvp_preview`. A channel row points to one existing published `audit.release_manifest.release_version`. Promotion and rollback are atomic pointer moves between already-published releases; they do not mutate historical release manifests, claim membership, geometry membership, or canonical data.

Channel updates must:
- verify the target release exists and is `published`;
- verify the target release manifest `purpose` matches the channel;
- support compare-and-set against an expected current release so concurrent/stale promotion attempts fail safely;
- preserve the previous release as an immutable rollback target;
- run public health verification after a production pointer move.

The `atlas-data` Edge Function must resolve the public preview through this pointer. Absence or invalidity of the pointer is a serving error, not permission to silently fall back to “latest published”.

This release-channel pointer is a serving/promotion control, not full exact historical release membership. Issue #4 still governs reconstructible release-object membership and immutable release bundles.

**Reason:** selecting `order by created_at desc limit 1` makes publication order an implicit deployment mechanism. A newly published manifest can silently become public, and rollback requires changing release state. An explicit pointer makes promotion intentional, auditable, reversible, and separable from immutable release contents while preserving D-046’s staged promotion model.

## D-054 — Published releases use typed membership plus an immutable full-state bundle
**Date:** 2026-09-20  
**Decision:** Exact release reconstruction uses a hybrid model.

1. Typed `audit.release_*` membership tables record which claims, actors, spatial entities, geometries, voyages, coverage assessments and source versions belong to a release.
2. New captured-at-release membership rows carry an object SHA-256 for the exact serialized object state used to build the release.
3. A release also carries one or more checksummed immutable artifacts; the preservation-grade full-state bundle is the authority for reconstructing historical row values after canonical rows change.
4. Membership and artifact digests use canonical UTF-8 JSON: keys sorted, compact separators, JSON null preserved, identifiers normalized as strings, and arrays explicitly sorted where their semantics are set-like. Geometry state is represented in the bundle by SRID plus hexadecimal EWKB rather than by a presentation-oriented GeoJSON serialization.
5. `captured_at_release` means the object digest was produced from the immutable bundle before publication. `legacy_membership_backfill` means only historical membership could be reconstructed from an older manifest; it must not be presented as proof of exact historical row bytes.
6. Once a release is `published`, its typed membership is immutable. A revised release gets a new release version; it does not mutate the old membership.
7. Current serving may use the explicit D-053 release channel plus typed membership. A future exact historical-release API must serve the immutable bundle (or data verified byte-equivalent to it), not mutable current publish views.
8. Future release promotion must build and test the bundle/membership first, then apply that exact artifact to production without recomputing membership.

Existing `mvp-preview-ancient-v1` and `mvp-preview-ancient-v2` are backfilled from their stored manifest ID arrays with `legacy_membership_backfill` status. They remain useful historical membership records, but the project does not claim exact pre-existing row-state reconstruction for them unless a contemporaneous preserved bundle is independently available.

**Reason:** Typed membership alone answers “which IDs belonged to release X” but cannot reconstruct a historical row after that row is edited. An export bundle alone preserves bytes but lacks relational integrity/queryability. The hybrid model provides both while keeping legacy evidence limits explicit and supports D-046 build-once/promote-unchanged semantics.


## D-055 — Historical geometry precedence is case-specific; accepted specialist geometry may supersede the global baseline
**Date:** 2026-09-20  
**Decision:** The atlas separates a **global fallback baseline** from **case-specific source precedence**.

For a target spatial entity and year/interval, the resolver order is:

1. an exact or period-matched specialist historical geometry that has been explicitly accepted for that bounded case;
2. the exact Cliopatria polygon valid for the target year as the open global baseline;
3. another defensible historical geometry, clearly marked `approximate_historical`;
4. a defensible modern geographic proxy, clearly marked `modern_proxy`;
5. unresolved geometry, with neutral world land still visible.

This supersedes D-010 only in the ordering of the first two choices. The rest of the five-step fallback principle remains unchanged.

“Specialist” is not a permanent label applied to an entire dataset. Precedence belongs to a specific source version, feature/geometry, target identity and temporal interval. Before a specialist candidate can replace the baseline it must pass a bounded review covering:

- identity and semantic scope: the geometry represents the same historical target the atlas intends to map;
- temporal fit and uncertainty: the source is valid for the target year/interval without unsupported interpolation;
- source provenance: exact source version, native identifier, relevant citations/lineage and raw values are retained;
- redistribution/license compatibility for the intended published use;
- geometric validity and topology;
- explicit source-vs-source comparison showing a defensible improvement for the bounded case;
- historical/semantic review plus the normal cartographic QC/visual acceptance required for any promoted render artifact.

Greater vertex count, apparent smoothness, archive density, popularity, newer publication date or broader temporal resolution do not establish precedence by themselves.

Each canonical `GEOMETRY` record has one historical geometry source lineage. Do not silently splice coordinates from multiple historical source families into a record attributed to only one source. If a genuinely composite historical geometry is ever necessary, it must be registered as a new derived source/version with all contributing sources, transformation methodology, uncertainty and license compatibility preserved explicitly.

Natural Earth coastline/land-fabric operations are not historical-source mixing: they remain a render-only physical-topology transformation under D-037/D-038/D-044 and do not alter or replace the historical source record.

Accepted/live geometry is not retroactively replaced merely because a new candidate source exists. Replacement requires a new bounded acceptance decision; quarantine/fallback is a valid result.

**Current source-family guidance:** Cliopatria remains the global deep-time baseline. AWMC may generate preferred candidates for its explicit Greco-Roman snapshots. CHGIS V6 and CShapes 2.0 are strong internal comparators but currently have public-redistribution constraints under the atlas distribution model. OpenHistoricalMap is feature/version-specific supplementary evidence rather than a globally preferred family. Confoederatio Atlas/Naissance remains an experimental comparator until feature/keyframe provenance is strong enough for claim-specific review. These examples are guidance from the current source survey, not hard-coded permanent routing rules.

**Reason:** The previous D-010 wording placed an exact Cliopatria polygon before a better specialist geometry, which made specialist replacement logically unreachable whenever Cliopatria had coverage. The completed source survey also shows why a simple region-to-dataset lookup is unsafe: specialist datasets differ in date coverage, entity semantics, licensing, feature-level provenance and temporal uncertainty. Case-specific precedence preserves a stable global fallback while allowing demonstrably better historical geometry without silently trading reproducibility for visual detail.


## D-056 — Repository operating model is canonical; autonomous work is issue-driven and gate-bound
**Date:** 2026-09-22  
**Decision:** GitHub repository `kaastumor/Slavery` is the canonical source for current project implementation and operating state. The repository-root `BACKLOG.md` remains the single execution queue; GitHub issues hold durable task evidence; this Decisions Log remains the durable decision record. A small operating layer defines the charter, way of working, assumptions/risks/value/health state, and the scheduled-worker runbook.

Scheduled autonomous work is serial. It resumes an unfinished `auto/*` PR before selecting new work, otherwise chooses exactly one highest-priority eligible `AUTO READY —` issue. It may not skip gates or create a next gate merely because the current queue is empty. Gate-boundary adversarial and Project Health Check issues are dependency-gated.

**Alternatives considered:** a separate project board/roadmap/risk system; a free-running worker that interprets the backlog broadly; keeping operational behavior only inside the scheduled-task prompt.

**Reason:** the repository already has adequate backlog, decision, QC and issue structures. Duplicating them would create drift. Versioning the worker contract beside the project makes automation behavior auditable and lets newer repository decisions override stale scheduled prompts.

**Consequences:** governance should remain deliberately small and may be deleted/simplified when it stops preventing real failure. Green CI is necessary but not evidence that an idea or analysis is correct.

## D-057 — M1 methodology hardening precedes the next large-scale evidence expansion
**Date:** 2026-09-22  
**Decision:** After the working cartography/release/UI foundation and the 2026-09-22 adversarial review, the next substantive gate is M1 (#100): pressure-test the semantics that can create false equivalence or false temporal/spatial precision before another large-scale evidence expansion.

M1 does not invalidate the canonical v0.6.1 release or the working public preview. Current P0–P4 remains backward-compatible until a replacement/compatibility model survives the gate. The gate must use both synthetic adversarial fixtures and real atlas cases. The complete Cliopatria baseline may be profiled as raw geography infrastructure, but raw ingestion does not promote geometry or historical claims.

The gate ends with an integrated adversarial review followed by a Project Health Check that explicitly chooses continue, redirect or stop.

**Alternatives considered:** immediately resume broad research ingestion; immediately replace P0–P4; freeze the working project for a wholesale ontology rewrite.

**Reason:** the current stack already demonstrates real operational value. The strongest unresolved risk is analytical overclaiming at scale, so the smallest useful next step is discriminating semantic tests rather than more infrastructure or more records.


## D-058 — Post-M1 territorial-practice semantics become the canonical target model
**Date:** 2026-09-23  
**Status:** accepted target semantics; relational implementation and release migration remain M2 work

**Decision:** The corrected M1 v2 semantic structure is promoted from experiment to the canonical **target methodology/data model** for new integration work. This does not mutate canonical historical release v0.6.1, the current public preview, or the live PostgreSQL schema.

The target model keeps the existing universal CLAIM/provenance/release architecture and introduces only the separations demonstrated necessary by M1:

1. **Evidence package**
   - attestation pattern is separate from interpretive basis;
   - source/document count does not prove independence.

2. **Historical characterization**
   - occurrence pattern, institutionalization, prevalence scope and structural significance are independent dimensions;
   - one dimension must not be mechanically inferred from another.

3. **Research/epistemic state**
   - research stage is workflow progress;
   - classification outcome is the result of synthesis;
   - review_complete may coexist with disputed or inconclusive.

4. **Assertion form and practice concepts**
   - bounded event/process assertions are distinct from enduring practice/status assertions;
   - practice concepts are faceted and may coexist across status, function, property/legal, transmission and process dimensions;
   - M1 does not establish an exhaustive final controlled vocabulary.

5. **Time**
   - outer query/legacy bounds are not sufficient selected-year truth;
   - applicability semantics are separate from temporal precision/certainty;
   - approximation or broad dating does not itself imply continuity.

6. **Space**
   - evidence locus is separate from reviewed inference extent;
   - a broader inference extent requires an explicit reviewed basis/rationale;
   - geometry availability or containment cannot create historical generalization.

7. **Legacy compatibility**
   - P0–P4 and legacy coverage_state remain available to reproduce and interpret historical releases;
   - they are not the target universal comparative ontology;
   - no post-M1 dimension may be backfilled from legacy P-level alone;
   - no new P-level may be mechanically derived from the post-M1 dimensions;
   - inconclusive does not imply P0.

**Alternatives considered:**
- keep P0–P4/coverage_state as the primary model and improve wording only — rejected by M1 because wording cannot fix query truth or simultaneous categories;
- replace the entire claim/provenance architecture — rejected because it survived the adversarial gate;
- immediately implement a large final ontology/schema — rejected as premature; only the proven structural separations are promoted;
- probabilistic temporal/spatial modeling — parked; the evidence does not justify probability distributions.

**Consequences:** docs/02_METHOD_AND_ONTOLOGY.md, docs/04_DATA_MODEL.md and docs/schema_draft.yaml define the post-M1 target. The schema draft advances to draft-0.11 and remains a target contract, not proof of live implementation. M2 must test the relational form in disposable PostGIS before any production apply or new canonical historical release. Existing v0.6.1/P-level semantics remain immutable historical release meaning.


## D-059 — Cliopatria source-time and composite semantics are preserved before atlas resolution
**Date:** 2026-09-23  
**Status:** accepted source-normalization/resolver rule for pinned Cliopatria v0.2.0; implementation remains M2 work

**Decision:** The complete pinned Cliopatria corpus is a raw global geography baseline, but its source timeline and composite hierarchy are not flattened into atlas polity geometry.

### Time

Upstream defines `FromYear` / `ToYear` as inclusive, negative integers as BCE and positive integers as CE. The exact pinned corpus contains six POLITY rows ending at source integer `0`, each followed by the same polity beginning at `1`. The pinned original-map sequence near the era boundary jumps from `B105-14.PNG` to `C001-1.PNG`; upstream prose does not assign source `0` a historical BCE/CE label.

Atlas selected-year lookup therefore translates its astronomical internal year `y` to the Cliopatria source query year as:

- `y <= 0` → `y - 1`
- `y >= 1` → `y`

This maps atlas 1 BCE (0) to source -1 and atlas 1 CE (1) to source 1. Source integer 0 is preserved exactly in raw data but receives no independent atlas historical-year meaning and is never selected directly by a historical-year query.

This is an atlas normalization rule derived from upstream's explicit BCE/CE labels plus the observed boundary structure; it is not a claim that Cliopatria itself explicitly defines year zero as a particular historical year.

Source-native ranges remain intact in raw/staging storage. Same-name gaps remain gaps and are not automatically interpolated.

### Composite hierarchy and RELATION

Cliopatria `MemberOf` and `Components` are preserved raw and may additionally be parsed as semicolon-delimited lists. The pinned corpus contains nested composites and multiple memberships; the hierarchy must not be reduced to one parent.

`RELATION` remains a distinct source type. v0.2.0 introduced it for a subset of Seshat-based supra-polity relations such as personal unions, vassalages, alliances and allegiances. RELATION composite geometry duplicates component geometry and must not be coerced into a normal atlas POLITY.

For the default atlas Cliopatria polity baseline:

1. select source rows active under the translated source year;
2. treat active `Type=POLITY` rows as polity candidates;
3. resolve active `MemberOf` parent composites;
4. suppress a constituent POLITY only when an active parent composite resolves to `Type=POLITY`;
5. membership in `Type=RELATION` does not suppress the constituent polity;
6. nested POLITY composites resolve recursively to the highest active POLITY composite;
7. RELATION rows remain separate relationship/composite evidence or an optional relation layer;
8. unresolved parent identity/type is flagged rather than guessed.

Accepted specialist geometry still takes precedence over this baseline under D-055.

**Alternatives considered:**
- map source integer 0 directly to atlas astronomical 0 — rejected because upstream explicitly labels negative magnitudes as BCE and this would create an off-by-one BCE interpretation;
- shift all source years by one — rejected because positive CE labels are already direct;
- rewrite raw source years during ingestion — rejected because it destroys source-native lineage and obscures the special zero;
- use Cliopatria's top-level display rule unchanged — rejected for the atlas default because RELATION composites can replace constituent polities and imply a stronger political unity than the source type warrants;
- drop all composites — rejected because POLITY composites are legitimate source representations and nested composites occur in the corpus;
- flatten hierarchy to one parent — rejected because the pinned corpus contains rows with multiple memberships and nested composites;
- interpolate gaps between same-name rows — rejected because upstream explicitly documents temporary incorporation/gaps and the pinned corpus contains hundreds of gaps.

**Evidence:** pinned commit `ad28a691b7c07c1fca89d0e0636d324667d2a258`; exact source blob SHA-1 `cefab0f4b622e2e7fb3daf68d4f461f83991204c`; SHA-256 `d01ae3a20d358cc5d54f69d9d725d390767d9c8759ac89ad6f90c58d106f3370`; upstream README and `notebooks/map_functions.py`; exact-corpus diagnostic recorded in `validation/cliopatria_v0.2.0_semantics.json`; Bennett et al. (2025), DOI 10.1038/s41597-025-04516-9.

**Consequences:** #119 must preserve the raw source timeline/hierarchy and #121 must implement this type-aware selected-year resolution. No raw source row becomes reviewed/published atlas geometry merely through ingestion.

## D-060 — Claim kind is structural and must match typed claim relations
**Date:** 2026-09-23  
**Status:** accepted integrity rule for the existing live claim architecture; does not replace D-058 target semantics

**Decision:** A universal `atlas.claim` row and any typed subtype or claim-bearing relationship row must agree on the claim's semantic kind. The database must reject a typed row when its `claim_id` points to a claim with a different `claim_kind_code`.

For the current live architecture this applies to:
- territorial-practice claims;
- legal events;
- actor-attribute claims;
- external/network-participation claims;
- spatial relations carrying claims;
- voyage-owner, voyage-finance and voyage-stop claim relations.

Once a claim exists, `claim_kind_code` is immutable. A correction that changes the semantic kind must create/supersede with a new claim rather than retyping an existing claim underneath already-linked subtype, provenance or release-history rows.

This rule is semantic integrity only. It does not infer claim kind from source density, geography, P0–P4, actor attributes or other evidence. It does not promote the legacy P0–P4 model, and it does not pre-empt the post-M1 relational implementation still required under D-058/M2.

**Evidence:** Before production hardening, all 42 existing live territorial-practice subtype rows were checked against their universal claims and had zero kind mismatches. Migration `0028_claim_kind_integrity` was then applied to production with negative controls proving that a wrong-kind legal-event insert and a claim-kind mutation are rejected. The v0.6.1 reconciliation and non-Atlantic acceptance suites continued to pass after the change.

**Reason:** The universal claim table is intentionally shared across heterogeneous historical assertion types. Without an explicit compatibility guard, a foreign key proves only that a claim exists, not that a typed row preserves the claim's stated semantics. Silent retyping would make claim-specific provenance and release history internally contradictory.

**Consequences:** Migrations `0028_claim_kind_integrity.sql` and `0029_claim_kind_function_privileges.sql`, plus the rollback-only regression test, are part of the canonical schema history. The follow-up 0029 explicitly revokes PostgreSQL's default PUBLIC EXECUTE grant on the new guard functions so D-051 remains true for future schema-exposure changes. Future typed claim relations must either use the same structural guard or provide an equivalent integrity mechanism. Any later M2 schema replacement must preserve this invariant even if claim-kind vocabulary or subtype tables evolve.



## D-061 — Open termini constrain candidate time; they do not create indefinite positive applicability
**Date:** 2026-09-23  
**Status:** accepted M2 clarification of D-058 / M1 temporal semantics

**Decision:** `terminus_after` and `terminus_before` are temporal **constraints on an uncertain historical date/window**, not assertions that a condition held continuously from the bound to infinity.

This restores the surviving M1 invariant `open_terminus_does_not_imply_indefinite_continuity`.

For the post-M1 prototype:

- `terminus_after` requires an open-upper outer query window: `from_year IS NOT NULL`, `to_year IS NULL`;
- `terminus_before` requires an open-lower outer query window: `from_year IS NULL`, `to_year IS NOT NULL`;
- neither mode creates a positive `claim_asserted_interval` merely from the terminus;
- selected-year truth therefore remains false from the terminus alone;
- if evidence separately supports positive applicability, represent that support explicitly with the appropriate claim/applicability semantics rather than treating the terminus as continuity.

The outer `CLAIM.valid_years` range remains useful for candidate retrieval. It is not sufficient positive historical truth.

**Reason:** #135 made open termini structurally representable, but its first implementation encoded them as half-infinite asserted intervals and thereby made `terminus_after` true arbitrarily far into the future and `terminus_before` true arbitrarily far into the past. That contradicted M1's accepted temporal invariant and silently changed methodology during an integrity correction.

**Alternatives considered:**
- retain half-infinite asserted intervals — rejected because a terminus post/ante quem constrains an unknown date and does not itself prove indefinite continuity;
- remove terminus modes entirely — rejected because the distinction remains useful for source-faithful temporal uncertainty and candidate retrieval;
- introduce probabilistic time surfaces — parked under D-058; the evidence does not justify probability distributions.

**Consequences:** M2 validators must reject positive asserted intervals for terminus modes, while preserving open outer query bounds. The correction remains disposable prototype work; no production schema, canonical v0.6.1 release or public preview is changed.


## D-062 — After M2, preserve the evidence core and simplify the product/operations boundary
**Date:** 2026-09-23  
**Status:** accepted project-direction decision from HC-003; no new horizon authorized

**Decision:** The Historical Slavery Atlas continues, but the default project identity is narrowed to an **auditable global/deep-time evidence corpus + comparison method + thin atlas/query surface**.

The current full application/platform footprint is not the contribution and does not receive automatic further investment.

Preserve as the durable core:
- claim-specific source/version/evidence provenance;
- post-M1 semantic separations and adversarial fixtures;
- raw/reviewed/published/canonical state boundaries;
- historical geography resolution and selected-year logic;
- PostgreSQL/PostGIS where it materially supports research integrity and query behavior;
- reproducible release artifacts and reconstruction;
- a minimal map/query/evidence surface when it demonstrates comparative value.

Treat as contingent/derived:
- the current MapLibre/API public preview;
- always-on cloud operations;
- richer application UI;
- production migration of experimental M2 structures.

**Evidence:**
- M1/M2 repeatedly found real semantic/integrity defects and justify the research-method core.
- A bounded Silla/Hittite challenge found parity on core fact discovery using ordinary targeted research + a strong general-purpose model; the plausible Atlas advantage is durable comparative semantics rather than discovery itself.
- External precedent review found generic DH research-platform functionality already well served by nodegoat and adjacent standards/projects.
- The current public preview is non-canonical and has no demonstrated user-critical availability requirement.
- The project can remove operational machinery without losing its strongest research contribution.

**Alternatives considered:**
- continue full-platform expansion by default — rejected until user/research value is demonstrated;
- redirect into a generic digital-history platform — rejected because strong precedents already cover that category and no cross-domain need is evidenced;
- stop immediately — rejected because the domain-specific corpus/method and adversarial evidence have not yet been tested against the strongest baseline in the form most likely to preserve their value;
- collapse immediately to methodology-only — parked as the explicit fallback if the thin atlas/query layer fails a value-discrimination pilot.

**Consequences:**
- v0.6.1 remains canonical;
- the current preview remains a frozen/non-canonical demonstration;
- M2 production migration remains parked;
- broad H2 evidence expansion is no longer the automatic next horizon;
- production-like preview operations are reduced;
- future generic platform features require a demonstrated need not met by existing tools;
- the project execution queue may remain intentionally idle;
- a bounded value-discrimination pilot is the only currently justified candidate next experiment, but HC-003 does not authorize starting it;
- if corpus/method value survives but the thin atlas does not, the project should shrink to methodology/corpus;
- if neither materially outperforms the strongest baseline, further Atlas expansion should stop.


## D-063 — H2 value-discrimination does not earn another Atlas expansion horizon
**Date:** 2026-09-23  
**Status:** accepted project-direction decision from H2 / issue #146

**Decision:** The H2 value-discrimination pilot did not meet the pre-registered threshold for a repeatable practical advantage over the strongest competent baseline. Active Historical Slavery Atlas expansion therefore stops. Preserve the methodology, adversarial fixtures, provenance conventions, existing corpus/release artifacts, historical-geography/query work, and audit trail; do not create a successor research/product/infrastructure horizon from project momentum alone.

**Evidence:**
- the setup was adversarially revised before research because the original case set gave the Atlas a home-field advantage;
- three frozen evidence packets were compared through (A) a strong conventional research artifact, (B) the Atlas corpus/method representation, and (C) a repaired dependency-free thin query/visual artifact;
- B showed a material advantage over A only in the Mexica category/terminology negative-control case, not in the India 1843 or Genoese Black Sea cases;
- C made selected temporal/spatial inference errors more salient in the India and Genoese cases, but did not meet the two-probe/two-case material-advantage rule over B;
- a result adversary repaired C's avoidable provenance loss before the final disposition, and the threshold still failed.

**Interpretation:** This does not erase the value of M1/M2. Their strongest surviving contribution is methodological: claim-specific provenance, uncertainty/abstention, evidence-locus/inference-extent discipline, law/practice/participation separation, adversarial fixtures, and reproducible audit/release practices. The pilot shows that a competent ordinary notes/table/GIS/model workflow can carry most of those distinctions in the tested cases without requiring an actively expanding bespoke Atlas system.

**Consequences:**
- v0.6.1 remains the immutable canonical historical data release;
- H2 experiment cases remain non-canonical experiment evidence;
- no H3/H4 research/product horizon is authorized;
- M2 production migration remains parked;
- bulk/global evidence expansion remains parked;
- richer frontend/platform, serving, search, ontology and infrastructure work remain parked;
- the current preview remains a frozen non-canonical legacy demonstration;
- the repository enters an **IDLE / preservation** state rather than a new development phase;
- future Atlas development requires genuinely new external evidence: e.g. a real repeated user/research task or scale failure that the strongest simpler workflow cannot handle without losing provenance, uncertainty or correct cross-place/time reasoning;
- such a trigger authorizes a new evaluation, not automatic platform expansion.

**Durable experiment record:** `experiments/h2-value-discrimination/` and issue #146.


## D-064 — COV-001 may test corpus coverage value without reopening Atlas expansion
**Date:** 2026-09-23  
**Status:** accepted bounded experiment authorization; no successor horizon authorized

**Decision:** Authorize COV-001 / issue #148 as a bounded **coverage-value experiment** distinct from the Atlas product hypothesis rejected for active expansion by D-063.

COV-001 may test whether a small, systematically assembled global place/time evidence corpus provides material value because it makes:
- research coverage and gaps inspectable;
- bounded propositions and abstentions reusable;
- provenance recoverable;
- cross-place/time coverage questions answerable without repeated reconstruction.

This does **not** authorize:
- H3 bulk/global evidence expansion;
- production migration of M2 structures;
- a new Atlas release;
- frontend/map work;
- database/API/service expansion;
- automated bulk research.

**Experimental form:** use a deterministic sample from the already pinned Cliopatria corpus plus four fixed non-polity challenge contexts. The experimental index must remain plain CSV/JSON/Markdown and must be compared against Cambridge/Palgrave, relevant specialist structured resources, ordinary specialist research and a plain ordinary matrix.

**Reason:** H2 established that bespoke Atlas representation/UI did not earn continued development, but it did not test the separate possibility that accumulated global coverage itself is useful. Testing that narrower thesis with a small plain artifact does not contradict the D-063 stop rule.

**Guardrail:** The deterministic sample must be frozen before slavery/coercion research. Missing/weak coverage never becomes historical absence. A positive result may authorize at most one further bounded corpus-scale test and cannot automatically revive the Atlas platform.

**Durable setup:** `experiments/coverage-value/` and issue #148.
