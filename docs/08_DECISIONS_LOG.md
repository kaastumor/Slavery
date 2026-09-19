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
