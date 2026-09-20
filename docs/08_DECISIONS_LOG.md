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
