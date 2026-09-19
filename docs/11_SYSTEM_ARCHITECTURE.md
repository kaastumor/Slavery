# System Architecture

**Architecture status:** approved migration target; not yet the canonical data implementation  
**Canonical data remains:** `Historical_Slavery_Atlas_v0.6.1_Controlled_Atlantic_Ingestion.xlsx`

## 1. Architectural goal

Build a research-grade historical evidence system that can power a fully interactive web map without making the web application itself the source of historical truth.

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
        CANONICAL RESEARCH DATABASE
             PostgreSQL + PostGIS
                     |
          +----------+-----------+
          |                      |
          v                      v
   PUBLISH / MAP VIEWS      RESEARCH API
 reviewed/released data     claims/evidence
          |                      |
          +----------+-----------+
                     v
               WEB APPLICATION
                  MapLibre
```

The exact hosting provider, backend framework and frontend framework are implementation choices. The separation of layers is the architectural requirement.

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

For territorial-practice claims, `practice_level` may remain NULL until an explicit P0–P4 assessment is made. NULL is not P0: it means the assessment has not been recorded. P0 is an explicit unknown/no-usable-classification assessment. Disputed/RI coverage must not be coerced to P0.

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
