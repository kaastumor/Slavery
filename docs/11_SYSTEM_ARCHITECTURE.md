# System Architecture

**Architecture status:** approved research/curation target; presentation/release boundary simplified after EXP-02; not yet the canonical data implementation  
**Canonical data remains:** `Historical_Slavery_Atlas_v0.6.1_Controlled_Atlantic_Ingestion.xlsx`

## 1. Architectural goal

Build a research-grade historical evidence system whose reviewed output can be reconstructed and consumed independently of any one application.

The system may power an interactive historical Atlas, ordinary GIS, tables, Markdown packets, notebooks or APIs, but no presentation surface is the source of historical truth.

After EXP-02, the preferred release boundary is:

> **reviewed research state → immutable portable evidence package → replaceable presentation adapters**

PostgreSQL/PostGIS remains the working research/curation target. The portable package is a release/interchange boundary, not a replacement canonical schema.

The architecture must support:

- time-bounded historical claims from roughly 3000 BCE to the present
- historical polygons, points, routes and unresolved geometry
- claim-level provenance and disagreement
- multiple roles for the same person or organization
- separate territorial practice, legal status, network participation, research coverage and geometry
- reproducible imports from external datasets
- review before publication
- reconstruction of historical data releases
- efficient map delivery at global scale

## 2. Logical architecture

```text
External sources / archives / datasets / scholarship
                     |
                     v
              RAW SOURCE LAYER
        immutable source values/snapshots
                     |
                     v
             STAGING / INGESTION
       parsing, normalization, validation
                     |
                     v
        RESEARCH / CURATION SYSTEM
             PostgreSQL + PostGIS
                     |
                     v
           REVIEW / RELEASE GATE
                     |
                     v
       IMMUTABLE EVIDENCE PACKAGE
 manifest + target rows + source relations
                     |
        +------------+-------------+-------------+
        |                          |             |
        v                          v             v
  MAP / GIS VIEW             TABLE / MD      API / WEB
 geographic adapter          inspection       adapter
```

The exact hosting provider, backend framework and frontend framework are implementation choices.

The architectural requirement is the separation of:
- source-native evidence;
- research/curation state;
- reviewed release state;
- portable evidence package;
- presentation adapters.

A presentation adapter may omit information for a bounded task only if the omitted information cannot change the represented historical meaning. It may never strengthen a claim beyond the reviewed package.

## 2A. Project-form boundary after EXP-02

EXP-02 demonstrated, on the frozen R1 set, that the fixed safety/reconstructibility contract survives outside the application-shaped candidate JSON.

This supports the following architecture policy:

- the research database may remain richer than the portable package;
- the portable package may remain richer than any single presentation view;
- no view owns canonical truth;
- uniform release-level facts may be hoisted to a package manifest when doing so is lossless for that release;
- release-specific simplification must not be generalized silently to future mixed-state releases;
- source/version identity and the distinctions that prevent false absence, false precision and false territorial inference remain explicit.

The EXP-02 artifact is evidence for this boundary, not a canonical replacement data model.

## 3. Canonical database target

The migration target is PostgreSQL with PostGIS.

Reasons:

- relational foreign-key integrity for claims, sources, actors and relationships
- native integer range types suitable for historical intervals
- PostGIS geometry types and spatial indexes
- spatial joins between evidence targets and historical geometry
- support for views/materialized views for publication
- mature tooling for migrations, backups and read-only publication access

The workbook remains canonical until a database migration has passed reconciliation and QC.

## 4. Historical time model

Historical time is a first-class data concept.

### Internal year convention

Use astronomical integer year numbering internally:

- 1 CE = `1`
- 1 BCE = `0`
- 2 BCE = `-1`
- 3000 BCE = `-2999`

The public UI must convert these values back to conventional BCE/CE labels and must never display year zero as a historical BCE/CE label.

### Interval convention

Store explicit bounded fields as well as a database range:

- `from_year`
- `to_year`
- derived/queryable `valid_years` integer range
- `temporal_precision`
- `temporal_certainty` where needed
- `date_text_original` where the source wording matters

Conceptually, database ranges are half-open: `[from_year, to_year + 1)` when both bounds are known and inclusive at the research level.

Open-ended ranges are allowed when the evidence only establishes a terminus before/after.

A broad research period must not be silently treated as an exact start/end date. Precision metadata remains visible.

## 5. Identity model

### Internal identity rule

Use generated UUIDs for canonical database identities. Preserve source-native identifiers and legacy workbook IDs separately. Do not use a dataset's row ID as the atlas-wide primary key.

Missingness is not identity: a documented unknown owner/place does not become a fictional actor/spatial entity merely to make a foreign key non-null.

### ACTOR

A person or organization exists once as an identity. Historical roles are relationships, not separate identities.

An ACTOR may therefore be, at different times or simultaneously:

- vessel/voyage owner
- financier
- insurer
- lender
- operator
- shareholder
- company director
- official
- other documented role

`OWNER` and `FINANCIER` from the workbook are therefore migration-era role concepts, not separate long-term identity tables.

### SPATIAL_ENTITY

Use a generic spatial identity for anything that can be the target of a claim or geometry:

- polity/state/empire
- province or subnational unit
- city
- port
- region
- archaeological site
- plantation/estate where appropriate
- other bounded or named spatial unit

`POLITY` remains a subtype/specialization, not the only possible geography target.

Historical relationships between spatial entities are time-bounded. A port must not have one timeless `polity_id`; control/jurisdiction can change over time.

## 6. Claim and evidence model

Use a universal `CLAIM` identity.

Specialized claim tables may include:

- `TERRITORIAL_PRACTICE_CLAIM`
- `LEGAL_EVENT`
- `ACTOR_ATTRIBUTE_CLAIM`
- `EXTERNAL_PARTICIPATION_CLAIM`
- later specialized claim types as required

Each specialized record uses `claim_id` as its primary/foreign key to `CLAIM`.

This allows one enforceable `CLAIM_SOURCE` relationship instead of a polymorphic `claim_type + claim_id` pseudo-foreign-key.

Each claim records its own:

- temporal scope and precision
- spatial scope/target
- summary
- coverage/classification state where relevant
- confidence or uncertainty metadata where relevant
- review/publication state
- supersession relationship where relevant

Evidence supports or challenges a specific claim. It does not automatically validate all attributes of an entity.

Non-voyage network evidence is represented through `EXTERNAL_PARTICIPATION_CLAIM` rather than being forced into territorial practice. It may target a spatial entity, actor, or both, while remaining independent of P0–P4.

`practice_level` remains a nullable **legacy P0–P4 compatibility field** for historical releases. NULL is distinct from legacy P0, and disputed/inconclusive research states must not be coerced to P0. The post-M1 target model uses separate evidence, historical-characterization, temporal and spatial dimensions; no new P-level or post-M1 dimension is mechanically derived from the other.

## 7. Source provenance model

Separate conceptual sources from exact versions and archived assets.

### SOURCE

The conceptual publication, archive series, dataset or source collection.

### SOURCE_VERSION

The exact edition, database release, snapshot, archival item/version or retrieved web state used for evidence.

At minimum track where applicable:

- version/edition label
- publication/creation date
- retrieval/access date
- stable identifier or URL
- license/terms status
- language
- source classification
- limitations/independence notes

### SOURCE_ASSET

Optional local/raw file when storage is permitted.

Track where applicable:

- filename/object key
- checksum
- media type
- storage location
- redistribution status

A source does not require a locally archived asset if copyright, licensing, access restrictions or practicality prevent it.

### INGEST_RUN / RAW_RECORD

Bulk datasets should preserve source-native records and import lineage so normalized values can always be traced back to the original value and the ingestion run that produced them.
For canonical-workbook migration, every non-empty workbook row is preserved in raw ingest lineage as well as in the checksummed workbook asset. Raw preservation does not substitute for semantic normalization of substantive evidence sheets before canonical cut-over.

## 8. Research coverage layer

Research coverage is project metadata distinct from historical practice. The S/P/D/RI broad matrix is stored in a separate coverage-assessment structure and may be exposed as a transparency layer. It never sets P0–P4.
Coverage assessments may cite exact reviewed `SOURCE_VERSION` rows through a separate coverage-provenance bridge. Those links document the research process and do not automatically become evidence for a historical practice claim.

## 9. Data layers

The target database should logically separate:

- `raw` — immutable imported/source-native data when locally stored
- `staging` — parsed and normalized candidate data
- `atlas` — canonical researched entities, claims and relationships
- `publish` — reviewed/released views used by public services
- `audit` — ingest runs, QC findings, reconciliation metadata

These PostgreSQL schema names are the preferred implementation, but the logical separation matters more than the literal names.

## 10. Publication boundary and releases

Draft research must not automatically appear on the public atlas.

Records/claims need a controlled lifecycle such as:

- draft
- reviewed
- published
- superseded
- rejected/withdrawn where necessary

The public application reads only from approved publish views or release materializations.

Published releases must remain reconstructible. This can be achieved through immutable release snapshots/manifests plus auditable history; an append-only claim history is preferred for substantive interpretation changes.

An Excel workbook is optional as a human-readable export. It is not part of the core web architecture.

## 11. Web-map delivery

### Client

MapLibre GL JS is the preferred map-rendering client because it supports interactive browser maps and vector-tile sources.

The application framework around it is not yet fixed.

### Geometry/data delivery

Do not impose one format on every layer.

Use:

- GeoJSON for genuinely small/simple/static datasets where appropriate
- vector tiles for larger or highly detailed historical geometry and dense network layers
- regular JSON API responses for evidence panels, sources and claim details

The neutral land outline can be static and independent of historical evidence.

Public map geometry may be a publication/render transformation of reviewed historical geometry. In particular, coarse polygonal coastlines may be intersected with a versioned neutral land mask in a dedicated publish view. The underlying `atlas.geometry` and reviewed `publish.geometry` source geometry remain unchanged and auditable.

### Tile server

Martin is the preferred prototype/initial tile server because it can expose PostGIS tables/functions and can also serve MBTiles/PMTiles. It is not a permanent architectural dependency; it may be replaced if later requirements justify it.

PMTiles is an optional later publication optimization for stable/read-heavy layers or release snapshots. It is not required for the database foundation.

## 12. API boundary

Map tiles should contain only properties needed for display, filtering, selection and linking back to canonical IDs.

Detailed evidence should be loaded from an API by stable identifiers.

Example separation:

```text
map feature:
  spatial_entity_id
  claim_id / aggregate display id
  practice_level
  coverage/classification indicator
  geometry_accuracy

claim API:
  full claim
  supporting/challenging evidence
  source versions
  review state
  uncertainty
  related legal/network information
```

This keeps map payloads small without sacrificing evidence depth.

## 13. What is deliberately not locked yet

Do not treat the following as canonical architecture decisions yet:

- Next.js versus another web framework
- React versus another UI framework beyond MapLibre integration needs
- FastAPI versus another API framework
- cloud provider
- managed versus self-hosted PostgreSQL
- S3 versus another object store
- Martin as the permanent tile server
- PMTiles for every layer
- Excel exports
- CDN strategy

These can be selected after the database and query patterns are proven.

## 14. Migration rule

No current workbook table is deleted or reinterpreted in place.

Migration mappings are explicit:

- legacy `OWNER` -> `ACTOR`
- planned `FINANCIER` -> `ACTOR` plus finance relationship
- legacy `OWNER_EVIDENCE` -> semantic claim migration: actor attributes become `ACTOR_ATTRIBUTE_CLAIM`; ownership/missing-owner evidence supports claimable relationship rows; one legacy evidence row may split into multiple claims
- legacy/planned `PORT` -> `SPATIAL_ENTITY` with place type `port`
- `POLITY` -> `SPATIAL_ENTITY` subtype/specialization
- `VOYAGE_OWNER` remains an explicit ownership relationship using `actor_id`

Canonical v0.6.1 stays unchanged until the migrated database reproduces its meaning and passes QC.

## 15. Immediate architecture milestone

Before further bulk ingestion:

1. finalize the relational schema from `schema_draft.yaml`
2. create PostgreSQL/PostGIS migrations
3. execute migrations 0001–0011 and migrate the v0.6.1 controlled seed
4. reconcile every migrated value against the workbook
5. execute the rollback-only non-Atlantic acceptance fixtures so the schema is not accidentally optimized only for SlaveVoyages
6. build one thin technical map slice: neutral land + selected-year geometry + one practice claim + evidence click-through
7. only then resume financier/port expansion and larger data ingestion

## 16. Development and deployment environments

Local Docker Compose is the reproducible development boundary, not production infrastructure. Database/Python tooling is containerized so workstation-specific Python/PostgreSQL installs are not required. SQL migrations are tracked by checksum in `atlas_meta.schema_migration`.

Environment separation:

- local development — disposable schema/import/map/API work;
- CI — clean reproducibility and acceptance tests;
- staging — future production-like integration/release-candidate environment;
- production — future reviewed/published serving environment with separate credentials, backups/recovery and read-only public access.

The hosting provider remains deliberately undecided. Provider-specific infrastructure-as-code will be added only after that deployment decision.

## 17. Implementation references

Technology choices above were checked against official documentation:

- PostgreSQL range types: https://www.postgresql.org/docs/current/rangetypes.html
- PostGIS spatial indexes: https://postgis.net/documentation/faq/spatial-indexes/
- MapLibre GL JS: https://maplibre.org/maplibre-gl-js/docs/
- Martin PostgreSQL function sources: https://maplibre.org/martin/sources-pg-functions/
- Martin MBTiles/PMTiles sources: https://maplibre.org/martin/sources-files/

## Cartography fabric boundary

Physical land/coastline geometry is a first-class shared dependency rather than a frontend-owned asset.

`cartography.land_fabric` stores the active versioned physical land geometry and its upstream provenance/checksums. Public map delivery uses that same fabric in two places:

1. the API returns the active immutable source URL for the MapLibre neutral-land source;
2. `publish.map_geometry` uses the active PostGIS copy as the coastline constraint for historical polygon fills.

This keeps basemap and overlay coastlines structurally identical. Historical inland boundaries remain independent source geometry and are never replaced by the modern physical land fabric.

## Public MVP availability and production-change gates

The public serving path is part of release correctness.

Operational rules:

- public API requests may read precomputed/cache geometry but must not perform heavy smoothing, buffering, bulk unions or equivalent expensive spatial reconstruction;
- large spatial diagnostics belong in local Docker/CI or staging, not the live database;
- render-cache population is a bounded precomputation job and is never coupled to a user request;
- before a production schema/render change, verify the current public API and site are healthy;
- after the change, verify HTTP availability, payload sanity and latency before treating the change as complete;
- the frontend aborts an API load after 12 seconds and exposes a retry action rather than showing an infinite loading state;
- GitHub Actions runs a **weekly** external public health check for the non-canonical preview, validating API HTTP status, latency, release metadata, non-empty place data, cartography metadata and GitHub Pages availability;
- monitor failures create/update a GitHub incident issue and successful recovery closes it automatically.

D-052 already materializes the published preview as a deployment-bound static API snapshot/fallback, so a transient database outage does not erase the already-published demonstration.

## Recovery and availability posture

HC-003 / D-062 retires automatic Supabase project restart.

The current public preview is non-canonical and has no demonstrated user-critical availability requirement. Availability therefore uses:

1. weekly liveness monitoring;
2. the checksummed static fallback for already-published preview state;
3. explicit/manual investigation for persistent live API or database failure;
4. no automatic cloud-project restart from GitHub Actions.

A future user-critical service may reintroduce stronger recovery automation only after the service-level need and credential/protection boundary are demonstrated.

## Pipeline separation and artifact promotion

D-046 defines four logical operational lanes: research curation, cartography build, release/promotion and runtime operations.

Implementation rules:

- PR/CI jobs validate and build artifacts but do not write to production;
- research cases remain unpublished until review and release gating;
- render geometry is generated offline and promoted as an immutable derived artifact with provenance/QC;
- releases compose reviewed claims and approved geometry rather than regenerating them;
- staging verifies the same immutable release/render artifacts intended for production;
- production receives only bounded migrations and approved artifacts/materializations;
- availability monitoring stays independent from build/research workflows;
- repeated deterministic pipeline logic should live in scripts or reusable workflows rather than duplicated top-level workflow files.

The target GitHub workflow surface is intentionally small: foundation CI, research-case CI, bounded geometry build/review/promotion, release validation/deployment, web validation/deployment and low-cadence availability monitoring. Completed experiments and recovery machinery without a current need should be retired rather than retained.

GitHub protected deployment environments remain the preferred credential/protection boundary if a future approved production-mutation horizon requires them. Until then, production geometry promotion is explicit/manual and #43 remains parked. A workflow run passing CI is not itself sufficient to mark historical research as reviewed or geometry as visually accepted.


## Client Data API security boundary

D-051 makes the public serving boundary explicit:

- `atlas`, `audit`, `cartography` and `publish` are internal schemas, not direct browser PostgREST APIs;
- the public browser currently consumes the `atlas-data` Edge Function;
- the Edge Function reads the release manifest, reviewed publish views and approved cartography server-side;
- `anon` and `authenticated` must not receive direct schema/table privileges on internal research schemas;
- a future direct PostgREST contract must use a deliberately exposed API surface with explicit grants and RLS/policies;
- internal tables may remain non-RLS when they are genuinely private, but explicit revokes/default privileges must prevent accidental future exposure.

See `docs/21_DATA_API_SECURITY.md` for the production verification and hardening plan.

## Explicit public release channel

D-053 replaces implicit "latest published release" serving with an explicit `audit.release_channel` pointer.

- `public_mvp_preview` points to exactly one already-published release manifest.
- `atlas-data` resolves the public preview through that pointer and does not silently fall back to creation-time ordering.
- pointer targets must be published and their manifest `purpose` must match the channel;
- promotion/rollback moves the pointer only; it does not mutate historical release manifests, claim membership, geometry membership, or canonical v0.6.1;
- compare-and-set semantics protect against stale/concurrent promotion attempts;
- external health verification follows production pointer moves.

The pointer is a serving/deployment control. Exact historical release-object membership and immutable release bundles remain governed by issue #4.
