Warning: truncated output (original token count: 32415)
Total output lines: 1704

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

## D-050 — Promote external render geometry only …12415 tokens truncated…tion/inference metadata.

4. **immutable/as-of releases + review ledger**
   - do not silently rewrite historical experiment states.

5. **source-to-row dependency tracking**
   - shared-source corrections propagate review state to dependent rows.

**Evidence:**
- 24 C0 targets were represented while only 12 required C1 research;
- 6 identity/time probes surfaced one mismatch and one ambiguity without forcing subject conclusions;
- C1 produced 4 bounded-supported and 8 researched-inconclusive outcomes;
- source-reuse factor increased from 1.00 in the COV-002 row-centric cohort to 2.20 in COV-003;
- two of three batches had shared specialist sources materially informing all four C1 targets;
- all 12 C1 targets nevertheless needed target-specific follow-up, so the strong batch-economy gate failed;
- C2 materially improved 2 of 3 escalated targets, supporting selective rather than universal deep packets;
- the deterministic maintenance searches produced no positive new-source shock, so lower long-run update cost remains unproven;
- a real C2 correction exposed correlated shared-source review risk across four early-China rows, demonstrating the need for dependency tracking;
- none of the 12 C1 targets had direct Cambridge/Palgrave coverage, yet systematic selection recovered both supported results and meaningful abstentions.

**Consequences:**
- COV-003 receives **TIERED SURVIVE**, not STRONG SURVIVE;
- tiering is a methodological architecture, not authorization for bulk research;
- v0.6.1 remains canonical;
- COV-003 remains experimental/non-canonical;
- D-063 remains in force for Atlas product/platform work;
- no global C1/C2 completion is authorized;
- no automated mass research or successor experiment is authorized;
- record count remains an invalid success metric;
- source-quality state and source-dependency review propagation are required in any future tiered validation;
- future testing requires explicit sponsor authorization and should address non-polity frames, coherent batching, independent review and a real positive update event.

**Durable result:** `experiments/coverage-tiered/13_FINAL_RESULT.md`.


## D-071 — Authorize COV-004 as the final architecture-falsification gate
**Date:** 2026-09-23  
**Status:** accepted bounded experiment authorization

**Decision:** Authorize COV-004 / issue #157 to attack the COV-003 tiered method before any real systematic coverage programme is started.

The sponsor explicitly required:
- adversarial setup review before historical research;
- do not abandon the Atlas concept prematurely.

COV-004 therefore tests four independent arms:
- C1/C2 escalation calibration;
- non-polity target frames;
- 2015→2016–2026 publication-time updates;
- Atlas re-entry against a competent ordinary map/register baseline.

No arm may compensate for failure of another, and no result automatically authorizes comprehensive ingestion or a production Atlas.

**Durable setup:** `experiments/falsification-atlas/00_PROTOCOL_PREREGISTERED.md` and `01_SETUP_ADVERSARY.md`.


## D-072 — COV-004 preserves the tiered method and a boring Atlas surface, not bespoke Atlas machinery
**Date:** 2026-09-23  
**Status:** accepted direction decision from COV-004 / issue #157

**Decision:** Accept the formal COV-004 result **METHOD SURVIVE**.

Preserve:
1. C0 target/research-state coverage;
2. C1 compact bounded research;
3. selective C2 escalation;
4. source-quality failure as an explicit escalation/review trigger;
5. source-to-claim dependency tracking;
6. immutable/as-of releases with explicit review/update state;
7. ordinary map/GIS navigation over the evidence register.

Do not reopen bespoke Atlas application/platform work.

**Evidence:**
- Arm A: 1/6 material false negatives among non-escalated C1 rows; 2/3 prior escalations remain useful; source-quality trigger added;
- Arm B: all 12 non-polity targets represented without false territorialization and all 8 researched cases fit the claim model;
- Arm C: 3/6 real post-2015 evidence events survived the immutable-release/update model;
- Arm D: bespoke Atlas semantics produced 0/4 material gains over a strong conventional map + register with the same data/geometry; D5 reached parity and no misleading Atlas inference was introduced.

**Interpretation:** The map is still useful, but as a navigation/inspection surface. The strongest boring baseline is itself a viable thin Historical Slavery Atlas. Custom interaction/serving infrastructure is not the research contribution.

**Consequences:**
- v0.6.1 remains canonical and immutable;
- COV-004 remains experimental/non-canonical;
- no global C1/C2 completion is authorized;
- no automated mass research;
- no production DB/API/frontend migration;
- non-polity frame classes remain experimental rather than canonical ontology;
- future public C1 requires stronger source-quality state and independent/multi-reviewer calibration;
- no COV-005 architecture experiment is created automatically;
- the next substantive horizon, if explicitly authorized, should be an actual lean research/release programme rather than another architecture prototype.

**Durable result:** `experiments/falsification-atlas/27_FINAL_RESULT.md`.


## D-073 — Authorize R1 and freeze Core Contract v1 as the first real release-method profile
**Date:** 2026-09-23  
**Status:** accepted programme decision from explicit sponsor authorization / issue #159

**Decision:** Graduate the Historical Slavery Atlas from the COV architecture-experiment sequence into **R1 — Core Hardening + First Systematic Coverage Release**.

R1 is a real research/release programme, not COV-005.

Freeze `programmes/r1/03_CORE_CONTRACT_V1.md` as the binding R1 release-method profile.

Core Contract v1:
- consolidates existing methodology, source policy, geography rules, release/version rules and demonstrated COV failure modes;
- does not replace the PostgreSQL/PostGIS target data model;
- does not change canonical v0.6.1;
- introduces C0/C1/C2 only as research/release tiers;
- introduces claim-fitness/source-quality state as a release-review control;
- requires source-quality failure to trigger deeper review where it makes a positive proposition unsafe;
- requires language/access limitations and research coverage confidence to remain separate from historical classification;
- requires at least 50% C1 adversarial replay for the R1 candidate release, 100% C2 replay, and 100% replay for single-decisive-source or limited-source positive claims;
- preserves immutable/as-of release history and source-to-claim dependencies;
- keeps the default Atlas surface deliberately simple.

**R1 ceilings, not quotas:**
- at most 120 C0 targets;
- at most 36 C1 researched targets;
- at most 12 C2 deep packets.

**Scope correction from setup adversary:**
- R1 is pre-1900 by default;
- contemporary person-level forced-labour data are outside R1;
- no progress metric may use percentage of row ceiling;
- candidate research release and independently/publicly reviewed release remain distinct;
- no new backend/platform work follows from programme authorization.

**Hard sequence:** no new R1 historical subject research before the exact R1.2 target frame and C1 selection are frozen.

**Durable programme setup:**
- `programmes/r1/00_PROGRAMME_CHARTER.md`
- `programmes/r1/01_SETUP_ADVERSARY.md`
- `programmes/r1/03_CORE_CONTRACT_V1.md`
- `programmes/r1/04_CORE_CONTRACT_ADVERSARY.md`
- `programmes/r1/core_contract_fixtures.json`

A successful R1 does not automatically authorize R2.


## D-074 — Freeze the R1 target frame before subject research
**Date:** 2026-09-23  
**Status:** accepted R1 release-frame decision

**Decision:** Freeze `programmes/r1/target_frame.json` as the exact R1 target frame before any new R1 slavery/coercion subject research.

**Frame:**
- 41 new polity C0 targets from the exact pinned Cliopatria source;
- 24 new non-polity C0 targets from the previously frozen neutral COV-004 candidate universe;
- 65 new C0 registrations total;
- 16 new polity C1 research targets;
- 8 new non-polity C1 research targets;
- 24 genuinely new C1 targets total;
- 12 deterministic legacy C1 rows selected for Core Contract v1 re-review;
- 36 planned C1 rows total.

These are frozen members, not completion quotas. Rows may fail identity/time review, remain inconclusive/disputed, or be held from release.

**Source controls:**
- Cliopatria commit `ad28a691b7c07c1fca89d0e0636d324667d2a258`;
- asset SHA-256 `d01ae3a20d358cc5d54f69d9d725d390767d9c8759ac89ad6f90c58d106f3370`;
- previously sampled COV-001/002/003 source rows excluded from the new polity lane;
- no target selected using slavery/coercion evidence.

**Calendar correction:** negative Cliopatria source years remain source-native. R1 separately records Atlas astronomical internal years: source `-500` = 500 BCE = Atlas internal `-499`.

**Sector-B gap:** no eligible unused new Cliopatria polity candidate exists in sector B at the frozen R1 polity anchors after prior sampled rows are excluded. The gap remains explicit; no substitute is manufactured. The full planned C1 frame still covers all six neutral polity sectors through deterministic legacy re-review (including Chimú/Cuzco in sector B), while Yaghan/Tierra del Fuego independently appears in the new non-polity C1 cohort.

**Balance gates passed:**
- all five frozen polity anchor bands represented;
- all six neutral polity sampling sectors represented across the complete planned C1 release;
- at least three target-frame classes represented;
- no polity sampling sector exceeds 25% of planned C1 membership.

**Consequence:** R1 subject research may now begin only against this frozen frame. No post-evidence target substitution is allowed.

**Durable artifact:** `programmes/r1/05_TARGET_FRAME_FREEZE.md`.


## D-075 — Freeze the R1 subject-research queue after identity/time QA
**Date:** 2026-09-23  
**Status:** accepted R1 operational decision

**Decision:** Freeze `programmes/r1/subject_research_queue.json` as the only R1.4 subject-research queue derived from the D-074 target frame.

R1.3 performed identity/time/frame QA only; no slavery/coercion subject research occurred.

**QA result across 36 planned C1 members:**
- 18 `validated`;
- 16 `validated_with_frame_limitation`;
- 1 `ambiguous_requires_C2_or_hold`;
- 1 `invalid_or_mismatched_hold`.

**Held without replacement:**
1. **French Louisiana, 1800** — annual target cannot safely collapse 1800 treaty/title retrocession into effective French possession/administration, which remained Spanish until formal 1803 delivery;
2. **Duchy of Bavaria, 1800** — the source-native label is wrong for the anchor; Bavaria was an Electorate from 1623 to 1806.

No replacement target is introduced.

The resulting R1.4 queue contains **34** C1 research/re-review rows.

**Frame-limit examples retained rather than normalized away:**
- Sumerian City-States — polity aggregate;
- Indus Valley Civilization — civilization/archaeological-cultural frame rather than one sovereign polity;
- Teotihuacan — urban polity/site with uncertain territorial extent;
- Later Mayan City-States — multi-polity aggregate;
- Ethiopian Empire 1800 — imperial identity with fragmented effective sovereignty during Zemene Mesafint;
- Incense Route / Mongol Yam — mobile networks;
- Inuit / Yaghan — broad community-region frames;
- Portuguese Colonies — aggregate of multiple jurisdictions;
- Cuzco 1300 — site/incipient polity, not mature Inca Empire.

**Consequence:** R1.4 may research only the 34 frozen queue members. Identity/time/frame failure remains part of the release evidence package; no post-evidence substitution is permitted.

**Durable artifacts:**
- `programmes/r1/c0_register.json`
- `programmes/r1/identity_qa.json`
- `programmes/r1/06_IDENTITY_QA.md`
- `programmes/r1/subject_research_queue.json`


## D-076 — Accept R1.4 tranche 01 after material correction; retain Core v1 review controls
**Date:** 2026-09-24  
**Status:** accepted R1 programme checkpoint decision

**Decision:** Accept the final internally adversarially reviewed result of R1.4 tranche 01 as evidence that Core Contract v1 survives first real subject-research use **after material correction**.

Do not infer a methodology success rate from the tranche.

**Evidence:**
- 10 frozen C1 rows researched and replayed;
- 10/10 internal adversarial replay;
- 2/2 earned C2 packets completed;
- replay found and corrected four material overreach risks involving selected-year time, target/context evidence, external-versus-territorial inference and slave-status interpretation;
- Portuguese Colonies C2 refused one aggregate territorial-practice classification;
- Cahokia C2 changed preliminary `disputed` to `inconclusive` and removed selected-year 1200 implication.

**Decision consequences:**
- retain Core Contract v1;
- retain the R1 minimum 50% C1 adversarial-replay floor;
- retain 100% C2 replay;
- do not relax selected-year temporal truth checks;
- do not relax evidence-locus/inference-extent or dimension separation;
- do not create a new schema/ontology from this tranche;
- do not generalize the stress-set correction rate to the remaining queue;
- no target substitution;
- v0.6.1 remains canonical.

**Execution boundary:** issue #163 does not authorize tranche 02 automatically. The next R1 research tranche, if authorized, should preferentially test ordinary operational repeatability and review burden rather than intentionally selecting another stress set.

**Durable artifacts:**
- `programmes/r1/c1_tranche_01_final.json`
- `programmes/r1/12_C1_TRANCHE_01_ADVERSARIAL_REPLAY.md`


## D-077 — Accept R1.5 tranche 02; apply Core v1 §19 full-replay trigger and enter midpoint review
**Date:** 2026-09-24  
**Status:** accepted R1 programme checkpoint decision

**Decision:** Accept the final internally adversarially reviewed R1.5 ordinary operational tranche 02 and move R1 to its mandatory midpoint stop review.

Apply the already-frozen Core Contract v1 §19 trigger conservatively: tranche 01 produced material release-safety corrections in 4/10 replayed C1 rows, above the 10% threshold. Remaining R1 candidate C1 work therefore receives **100% adversarial replay** unless a later explicit decision supersedes this.

This is execution of Core Contract v1, not a new historical classification rule or ontology change.

**Evidence:**
- 6 frozen tranche-02 rows researched;
- 6/6 internally adversarially replayed;
- 1/1 earned C2 packet completed;
- final outcome: 1 classified, 5 inconclusive, 0 disputed;
- no target substitution;
- no post-synthesis semantic release correction;
- replay still corrected two source-dependency/provenance groupings (Lazica and Nālandā);
- Mali C2 resolved Sākūra's status to an explicit possible servile/client-origin question rather than a secure slave-status or territorial-practice claim.

**Decision consequences:**
- Core Contract v1 remains frozen;
- 100% C1 replay is the active R1 setting under §19;
- 100% C2 replay remains required;
- no schema/ontology/intensity-scale change;
- no new Atlas/platform feature is earned by this tranche;
- no target substitution;
- v0.6.1 remains canonical;
- tranche 03 is not authorized automatically;
- the next R1 action is the mandatory midpoint stop review after 16 researched C1 rows.

**Durable artifacts:**
- `programmes/r1/c1_tranche_02_final.json`;
- `programmes/r1/15_C1_TRANCHE_02_ADVERSARIAL_REPLAY.md`;
- `tests/test_r1_c1_tranche02.py`.


## D-078 — Midpoint: authorize one minimal three-row balance-closing tranche, then stop subject expansion
**Date:** 2026-09-24
**Status:** accepted R1 midpoint programme decision

**Decision:** After 16 researched C1 rows, choose **CONTINUE ONCE** rather than stop immediately or expand toward the 36-row ceiling.

The only additional C1 subject research authorized is a three-row tranche frozen from the existing D-075 queue:
- Tamna — 500 CE — sector F;
- Pandya Empire — 1300 CE — sector E;
- Chimu Empire — 1300 CE — sector B.

**Reason:** The current researched polity subset lacks sectors B and E. Adding only one B and one E row would leave sector C at 3/11 = 27.3%, above the R1 25% balance ceiling. Adding the earliest remaining neutral-QA validated polity by frozen queue order (Tamna, sector F) yields 12 researched polity rows with counts A2/B1/C3/D2/E1/F3, so the maximum sector share is exactly 25%.

This selection is based on the frozen sampling/QA frame, not slavery/coercion evidence.

**Midpoint findings:**
- bounded claims survive real use only with active temporal/inference/source controls;
- language/access limitations are material but do not dominate all results;
- source/version recovery is working, while source-family dependency normalization remains necessary;
- recurring cross-history value lies in safe temporal/inference/abstention/provenance structure;
- 100% replay remains active under Core v1 §19;
- research/review burden supports one small closure tranche, not quota-filling to 36;
- no repeated friction has earned a software/Atlas feature test.

**Consequences:**
- tranche membership must be frozen before subject research;
- no target substitution;
- 100% C1 replay and 100% C2 replay;
- after the three-row tranche, no further C1 research tranche is authorized by default;
- move next to R1.6 release QC unless the closing tranche creates a hold/rework condition;
- v0.6.1 remains canonical.

**Durable review:** programmes/r1/16_MIDPOINT_STOP_REVIEW.md.


## D-079 — Accept final R1 C1 closure tranche and stop subject-research expansion
**Date:** 2026-09-24
**Status:** accepted R1 programme checkpoint decision

**Decision:** Accept the final internally adversarially reviewed three-row midpoint closure tranche and end R1 C1 subject-research expansion at **19 researched C1 rows**.

Move next to R1.6 release-level QC and candidate-release assembly.

**Evidence:**
- 3/3 closure rows internally adversarially replayed;
- 1/1 earned C2 packet completed;
- final closure outcome: 1 classified, 2 inconclusive;
- no target substitution;
- no post-synthesis semantic release correction;
- Pandya legacy `bounded_supported` did not survive fresh Core-v1 target-fit review and resolved to inconclusive after C2;
- Chimú legacy `researched_inconclusive` became a narrower bounded-supported state-labor/corvée claim;
- Tamna remained target-specific inconclusive rather than inheriting peninsula-wide Korean slavery evidence.

**R1 subject-research totals:**
- 19 C1 researched;
- 5 classified;
- 14 inconclusive;
- 0 final disputed;
- 4 C2 packets completed;
- 19/19 internally replayed.

**Balance consequence:**
researched polity sectors are A2/B1/C3/D2/E1/F3. With 12 polity rows, the maximum sector share is 25%, satisfying the frozen R1 balance ceiling that motivated D-078.

**Decision consequences:**
- no tranche 04;
- remaining frozen queue rows stay research-state/planned, not absence;
- Core Contract v1 remains frozen;
- 100% replay remains part of the R1 candidate provenance;
- no schema/ontology/intensity-scale change;
- no new Atlas/platform feature is earned;
- v0.6.1 remains canonical;
- next work is release QC, source/dependency/geometry/reconstructibility checks and candidate-release assembly.

**Durable artifacts:**
- `programmes/r1/c1_tranche_03_final.json`;
- `programmes/r1/19_C1_TRANCHE_03_ADVERSARIAL_REPLAY.md`;
- `tests/test_r1_c1_tranche03.py`.


## D-080 — Pass R1.6 release QC with explicit limitations and define R1.7 as the MVP
**Date:** 2026-09-24
**Status:** accepted R1 release-gate decision

**Decision:** R1.6 passes release-level QC **with explicit unresolved limitations**.

Proceed to R1.7 as a deliberately small MVP:

> **immutable R1 candidate package + neutral world map + explicit geometry/research states + compact evidence register**

This is the crystallized surviving core of the Historical Slavery Atlas.

**QC evidence:**
- 19 unique reviewed C1 rows;
- 5 classified / bounded-supported;
- 14 inconclusive;
- 4 completed C2 packets;
- 19/19 internally adversarially replayed;
- 77 frozen targets preserved in the candidate research-state registry;
- 45 source relations / 45 source-version references / 37 independence groups;
- all six polity sectors represented with a maximum 25% share;
- deterministic release-QC validator reports no blocking errors.

**Explicit unresolved limitations:**
- concrete geometry materialization remains an R1.7 task;
- no independent historical review has occurred;
- language/access coverage varies by row;
- some positives are period-level or near-anchor rather than exact-year observations;
- the simple Atlas surface has not yet been materialized;
- v0.6.1 remains canonical.

**MVP constraints:**
- static/read-only by default;
- no production migration;
- no new backend/database/service;
- no bespoke graph/search infrastructure;
- neutral world land always visible;
- unresearched/held/geometry-unresolved states remain visible and never imply absence;
- exact source/version and review labels remain inspectable;
- temporal rendering must use the R1.6 guard artifact rather than inventing annual precision.

**After MVP:** feature work returns to discovery mode. A candidate feature must first beat the strongest boring baseline in a bounded experiment. Discovery does not authorize implementation.

**Durable artifacts:**
- `programmes/r1/20_RELEASE_QC.md`
- `programmes/r1/r1_release_qc_manifest.json`
- `programmes/r1/r1_candidate_target_registry.json`
- `programmes/r1/r1_source_dependencies.json`
- `programmes/r1/r1_temporal_render_annotations.json`
- `programmes/r1/r1_release_qc_unresolved.json`
- `programmes/r1/validate_r1_release_qc.py`


## D-081 — Accept technical MVP candidate; open discovery lane; keep R1.8 publication explicit
**Date:** 2026-09-24  
**Status:** accepted product/release checkpoint decision

**Decision:** Accept R1.7 / MVP v0.1 as **TECHNICAL_MVP_CANDIDATE**.

The candidate is:
> deterministic R1 evidence bundle + neutral world map + explicit research/geometry states + compact evidence register + discrete temporal guards.

This decision closes technical MVP delivery but does **not** canonicalize or publicly publish the R1 candidate.

**Evidence:**
- #175–#181 merged through green Web MVP + foundation CI gates;
- locked frontend dependency graph;
- deterministic 77-target / 19-reviewed static candidate;
- no live evidence API or database needed for core historical evidence;
- all target geometry explicit, currently 77/77 unresolved rather than guessed;
- research-state semantics preserve inconclusive/unresearched/held/C0 != absence;
- reviewed details expose proposition, abstention, locus/extent, source/version/dependency, review and access limits;
- discrete temporal anchors consume R1.6 render guards;
- source-native BCE and Atlas astronomical internal years are separated correctly;
- technical gate regression suite covers static boundary, accessibility semantics and deterministic reconstruction.

**Explicit limitations:**
- all historical target geometry unresolved;
- external neutral-land asset remains a runtime static dependency;
- no independent historical review;
- uneven language/access coverage;
- sponsor/browser usability acceptance pending;
- current public preview remains legacy/non-canonical;
- v0.6.1 remains canonical.

**Consequences:**
- MVP delivery queue #175–#182 is complete;
- subject-research stop remains in force;
- post-MVP discovery #184–#187 may run as evidence-only experiments;
- discovery cannot directly authorize implementation;
- next release decision is R1.8 **PUBLISH / HOLD / REWORK** after sponsor usability review;
- no backend/platform expansion is earned.

**Durable gate:** `docs/mvp/v0.1-release-check.md`.


## D-082 — Discovery v2 separates novelty from value and pauses feature-first discovery
**Date:** 2026-09-24  
**Status:** accepted

**Decision:** Adopt a corrected post-MVP discovery standard that treats competitor existence and novelty as evidence inputs, not decision shortcuts.

Governing principle:

> **EXISTING ≠ USELESS. DIFFERENT ≠ VALUABLE. NOVEL ≠ DEMANDED. COMPETITION ≠ VALIDATION. EVIDENCE DECIDES.**

**Why:** The prior wide-angle review already used baseline/value evidence, but some conclusions gave competitor/standards overlap too much argumentative weight. The post-MVP queue also became feature-first before reconstructing user jobs and realistic alternatives.

**Required discovery sequence:**
1. user/circumstance/job;
2. real current alternative, including manual work/non-consumption;
3. novelty status separated from strategic relevance;
4. relative advantage against that alternative;
5. difference / importance / behavioural consequence kept distinct;
6. adoption/switching friction where relevant;
7. system-level complementarity with the existing core;
8. OBSERVED / SUPPORTED INFERENCE / HYPOTHESIS / UNKNOWN evidence labels;
9. adversarial attack;
10. smallest falsifiable experiment with high information gain.

**Calibration:** “proven core” means technically/methodologically validated within this project. External-user demand, adoption and willingness to switch are not proven.

**Consequences:**
- #198 becomes the active discovery reset;
- #185–#187 are blocked until #198 decides whether to keep/rewrite, park or reject them;
- desk/competitor research alone cannot produce PROMOTION CANDIDATE;
- commercial/pricing/business-model analysis is conditional rather than ceremonial;
- no production implementation is authorized by this method change;
- v0.6.1 remains canonical and R1.8 publication remains separate.

**Durable method:** `docs/discovery/DISCOVERY_STANDARD_V2.md`.


## D-083 — Finish R1 release/no-release gate before external participant execution
**Date:** 2026-09-24  
**Status:** accepted sequencing decision

**Decision:** Make #203 the single active project boundary.

The #200 external expert audit protocol is frozen and may remain prepared, but participant case execution waits until R1.8 identifies the exact frozen artifact/packet to carry forward.

**Red-team rationale:**
- sponsor usability is not external-user validation;
- #200 preparation should not be discarded or repeatedly redesigned;
- recruitment feasibility may proceed in parallel;
- participant execution against a potentially superseded R1 packet would contaminate the experiment;
- “publish” must not imply canonical promotion;
- closing R1 on REWORK would hide unfinished release work;
- freezing a permanent “method/package” identity before external evidence would bias discovery.

**R1.8 dispositions:**
- **PUBLISH_CANDIDATE** — close R1; non-canonical candidate/research preview only unless separately promoted;
- **HOLD_NO_RELEASE** — close R1 with no publication;
- **REWORK** — keep R1 open; fix only release-blocking defects and rerun #203.

**Consequences:**
- #159 closes only on PUBLISH_CANDIDATE or HOLD_NO_RELEASE;
- #200 remains the highest-information post-R1 experiment;
- no participant case task runs before #203;
- recruitment feasibility may proceed;
- v0.6.1 remains canonical;
- no R2 or feature-delivery queue is authorized.

**Durable gate:** `docs/mvp/r1.8-sponsor-review.md`.


## D-084 — Defer external involvement and use internal subtractive discovery
**Date:** 2026-09-24  
**Status:** accepted sequencing decision

**Decision:** Do not involve external participants at this stage.

Preserve #200 and its protocol, but defer all recruitment/contact/participant execution until the sponsor explicitly reopens external involvement.

Use the internal runway only for questions that can be answered honestly without external-user evidence.

**Red-team result:**
- model/sponsor review cannot substitute for external validation;
- internal work must not claim demand, adoption, preference or product-market value;
- the highest-value internal-only uncertainty is now subtractive: determine the minimum evidence packet that preserves R1 safety/reconstructibility and whether the core survives in boring portable formats;
- EXP-02 (#205) is therefore prepared but waits for the R1.8 artifact freeze.

**R1.8 finding:** the internal release adversary discovered a stale committed MVP candidate file. CI regenerated the artifact before checking freshness, so a stale committed artifact could pass.

**Consequences:**
- #203 enters bounded REWORK;
- refresh the committed candidate artifact;
- CI must check freshness before regeneration;
- add committed-byte reconstruction regression;
- no historical data/ontology/geometry/feature expansion;
- #205 may execute only after #203 freezes R1;
- #200 is deferred, not falsified;
- v0.6.1 remains canonical.

**Durable artifacts:**
- `docs/mvp/r1.8-internal-adversary.md`
- `docs/discovery/EXP_02_MINIMUM_SUFFICIENT_PACKET.md`


## D-085 — Close R1 with HOLD_NO_RELEASE
**Date:** 2026-09-24  
**Status:** accepted R1 final-gate decision

**Decision:** Close R1 with **HOLD_NO_RELEASE**.

The frozen R1 candidate at `a6987d3f14369c6ea2d7b2b3db74ac65faa8ec57` is internally coherent and reconstructible after the bounded stale-artifact repair.

No public/canonical promotion occurs.

**Why not publish now:**
- 77/77 historical target geometries remain unresolved;
- no independent historical review exists;
- external involvement is intentionally deferred;
- public promotion would not reduce the project’s current highest-value uncertainty;
- v0.6.1 already remains the canonical historical release.

**What this means:**
- R1 is a completed bounded research/release programme;
- HOLD_NO_RELEASE is a valid programme result, not a failed technical gate;
- the candidate remains preserved as the frozen reference artifact;
- #159 and #203 may close;
- #205 becomes the active internal discovery item;
- #200 remains deferred;
- no R2, feature queue, geometry programme or new subject-research tranche is authorized.

**Canonical release:** v0.6.1 unchanged.


## D-086 — Accept EXP-02 portable-core result without canonical schema change
**Date:** 2026-09-24  
**Status:** accepted internal discovery decision

**Decision:** Accept EXP-02 disposition:

> **PORTABLE CORE SURVIVES + SIMPLIFY CANDIDATE**

The frozen R1 evidence contract can be represented as:
- package-level manifest/state definitions;
- flat target table;
- flat source-relation table;
- human-readable Markdown packets;

without requiring bespoke application structure for the fixed internal invariants.

**Preserve as core:**
- bounded proposition + required abstention;
- evidence locus + inference extent;
- per-target temporal state + display rule;
- source version + locator + independence group;
- language/access limitation;
- coverage confidence;
- explicit research-state / non-absence semantics;
- law/practice and network/territorial notes when present.

**Simplification candidates in this frozen set:**
- hoist uniform per-row review state to package level;
- hoist uniform unresolved geometry state to package default with overrides;
- treat Atlas astronomical internal year as application-specific rather than evidence-packet core;
- treat detailed unresolved-geometry provenance and some source-relation enrichment as outside the minimum portable packet.

**Limits:**
- no canonical ontology/schema change follows automatically;
- no historical classification changes;
- no claim is made about external user value, preference or adoption;
- this result does not prove the Atlas UI is useless.

**Evidence:** flat tables + manifest are about 19% of the uncompressed current candidate JSON size while preserving the fixed internal invariants; compact experiment JSON is about 35%.

**Consequence:** strengthen the working hypothesis that the demonstrated core is a portable evidence method/package rather than application-dependent structure.

Stop after EXP-02 and reassess project form before authorizing a successor.


## D-087 — Simplify project form: portable evidence core, Atlas as view
**Date:** 2026-09-24  
**Status:** accepted project-form / architecture decision

**Decision:** Adopt the following resting project form:

> **portable reviewed evidence core + replaceable Atlas/map/table/API views**

The project remains the **Historical Slavery Atlas**.

“Atlas” is a geographic/time-aware inspection and publication mode. It is not the architectural owner of historical truth.

**Evidence:**
- H2: corpus/method beat the strongest baseline materially in only 1/3 tasks; thin view added 0/3 material gains;
- COV-004: bespoke Atlas inspector did not materially beat a competent conventional map/register on the frozen map tasks;
- COV-003/COV-004/R1: tiered evidence method, abstention, temporal/spatial guards, source dependency and research-state semantics survived;
- R1: deterministic static candidate did not require a live evidence API;
- EXP-02: fixed R1 safety/reconstructibility invariants survived in a manifest + flat target/source tables + Markdown packets.

**Red-team result:**
- do **not** infer that maps are useless;
- do **not** rename the project away from Atlas;
- do **not** delete PostgreSQL/PostGIS or the web implementation;
- do **not** generalize frozen-set geometry simplification to future mixed-geometry releases;
- do **not** treat the EXP-02 minimum packet as a canonical replacement schema;
- do **not** infer user value from structural portability.

**Architecture consequence:**
- PostgreSQL/PostGIS remains valid research/curation infrastructure;
- the preferred release/interchange boundary is reviewed research state → immutable portable evidence package;
- maps, tables, Markdown, notebooks, APIs and web applications are presentation adapters;
- no adapter may silently strengthen the reviewed evidence claim;
- the research system may remain richer than the release package;
- the release package may remain richer than any individual presentation view.

**Execution consequence:**
- current state becomes **PRESERVATION / IDLE**;
- no R2, geometry-completion programme, feature queue, schema migration, portable-package productization or new discovery experiment is authorized automatically;
- #200 external review remains deferred by sponsor;
- reopen only on a concrete trigger defined in `docs/26_PROJECT_FORM_AFTER_EXP02.md`.

**Canonical data:** v0.6.1 remains unchanged.

**Durable reassessment:** `docs/26_PROJECT_FORM_AFTER_EXP02.md`.


## D-088 — Active evidence continuity; idle is not the default successor
**Date:** 2026-09-24  
**Status:** accepted execution/governance decision  
**Sponsor direction:** explicit

**Decision:** Supersede only the **PRESERVATION / IDLE execution consequence** of D-087.

The project form from D-087 remains accepted:

> **portable reviewed evidence core + replaceable Atlas/map/table/API views**

The project now operates under this continuation rule:

> **After a bounded horizon completes, reconcile the evidence and select one next bounded research/discovery experiment by expected information gain. Do not optimize for returning to idle.**

**Resource policy:**
1. evidence quality is scarce;
2. focus is scarce;
3. project complexity is scarce;
4. elapsed time is not treated as the scarce resource.

Time/research-labour alone is therefore not a stop rule.

**Controls:**
- WIP remains 1;
- each successor needs a discriminating question, falsifier, evidence contract and complexity boundary;
- prefer real historical/source research over meta-work when both can resolve the uncertainty;
- archive density still does not determine prevalence;
- stopping, simplifying, rejecting and parking remain valid **experiment results**;
- a no-work state is reserved for genuine blockers, constraint conflicts, or the absence of any bounded experiment capable of materially changing belief.

**Still trigger-gated:**
- canonical data/schema migration;
- public/canonical release;
- major infrastructure expansion;
- external participant recruitment/review;
- sensitive modern-person coverage.

**Immediate consequence:** authorize **#211 / EXP-03 heterogeneous evidence stress test** as the active WIP-1 research horizon.

**Canonical data:** v0.6.1 unchanged.


## D-089 — Extend portable evidence contract after heterogeneous stress test
**Date:** 2026-09-24
**Status:** accepted architecture/release-contract decision

**Evidence:** EXP-03 / #211.

**Decision:** Preserve the D-087 portable-core project form, but extend the minimum portable evidence contract.

For reviewed targets/claims, preserve where material:
- historical term(s);
- category-mapping status;
- category-mapping note.

For source relations, preserve:
- evidence role;
- claim fitness / inference scope.

When geometry states are mixed, do not hoist one package-level geometry state across the release. Preserve per-target geometry state/role and unresolved/proxy warnings.

**Reason:** Fresh Athens, Cairo, Tenochtitlan, Joseon, Zanzibar and British-India cases showed that a source may be decisive for one proposition but unfit for another, and that historically specific status terms cannot always be safely collapsed into one comparative category. The six cases still fit flat portable artifacts; platform expansion is not required.

**Dependency rule:** source-version identity, locator and independence group remain mandatory. Claim fitness does not replace dependency tracking.

**Complexity rule:** Do not respond by creating a universal taxonomy engine. Start with transparent term + mapping status/note and free-text claim-fitness semantics; normalize further only if repeated evidence warrants it.

**Canonical effect:** none. v0.6.1 remains canonical; no database/schema migration or public release is authorized by this decision.

## D-090 — Scope Actions to relevant verification
**Date:** 2026-09-24
**Status:** accepted operational decision; sponsor requested cost reduction

All PRs retain sanitation and Python regression checks. PostGIS is skipped only for
diffs consisting entirely of known documentation/research text paths; unknown paths,
code, SQL, workflow and dependency changes fail closed to the full gate. Manual
dispatch always runs the full gate. Remove duplicate foundation-on-main-push and
preview-health-on-every-push; preserve weekly/manual preview monitoring. Superseded
PR runs cancel automatically. Main changes continue through reviewed PRs.

Relevant verification is not waived. Green checks remain implementation evidence,
not historical review. No ontology, canonical data or public-release effect.

## D-091 — Compact discovery execution with distinct evidence gates
**Date:** 2026-09-24
**Status:** accepted operating decision; sponsor requested implementation and 5.6-ready discovery

Use `discovery/DISCOVERY_EXECUTION.md` as the execution guide and
`discovery/RUN_PROMPT.md` as the shared continuation prompt. Keep v2's novelty/value
principle as a product-value reference. It does not impose customer-demand gates
on historical research. Historical evidence, method/representation tests and
product/workflow value require distinct conclusions and acceptance evidence.

Resume from the backlog plus active protocol/checkpoint; load historical context
when needed. WIP is one experiment across workers. At selection boundaries compare
mechanism-based adjacencies and strong simpler/negative alternatives, then freeze
one discriminating test. No candidate quota or automatic feature backlog.

Preregistration, before/after adversarial passes, internal-versus-independent review,
access limits, search sufficiency and concrete resumable actions must remain explicit.
A partial checkpoint does not close its issue; successful research does not promote
public/canonical data. D-088 continuity and D-090 CI cost controls remain.

Validation: `discovery/EXECUTION_REVIEW_2026-09-24.md` records internal scenario replay
and its limitations. No measured 5.6 performance or external-user validation claimed.
No historical ontology, frozen sample, schema or release change.
