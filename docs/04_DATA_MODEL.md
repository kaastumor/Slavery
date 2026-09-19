# Data Model

## 1. Design rule

Normalize identities, claims, relationships, sources, time and geometry. Do not build the atlas around one wide row in which a polity, law, ship, owner, port, source and practice classification become one object.

The current canonical workbook is v0.6.1. This document defines the migration target; it does not retroactively rewrite the workbook.

Database entity identities use internal UUIDs. Source-native IDs remain separate, preserved attributes/crosswalks. Missing/unknown values are statuses, not fictional entities.

## 2. Historical-time convention

Use signed astronomical integer years internally:

- 1 CE = `1`
- 1 BCE = `0`
- 2 BCE = `-1`

The UI converts internal values to normal BCE/CE labels.

Time-bounded records should retain:

- `from_year`
- `to_year`
- derived/queryable `valid_years` integer range
- `temporal_precision`
- `temporal_certainty` where needed
- `date_text_original` where useful

Do not convert a broad or uncertain period into false exactness.

## 3. Core identity entities

### ACTOR

A person or organization. Roles are relationships and claims rather than separate identities.

Suggested fields:

- `actor_id`
- `actor_type` = person / organization / partnership / state_institution / other
- `canonical_name`
- `display_name`
- `from_year` / `to_year` where meaningful
- `notes`
- `review_status`

Names/aliases from individual datasets should be preserved separately from the canonical label.

Database primary keys are internal UUIDs. Legacy/source identifiers such as `OWN-0006` are preserved in migration crosswalks rather than becoming the permanent actor key.

### ACTOR_NAME

Preserves aliases and source-native/raw name strings without overwriting the normalized actor label.

Suggested fields:

- `actor_name_id`
- `actor_id`
- `name_text`
- `name_type` = canonical / alias / source_raw / variant / other
- `source_version_id` where the name came from a source
- language / notes where relevant

### SPATIAL_ENTITY

A named or bounded geographical/historical unit that may receive claims or geometry.

Suggested fields:

- `spatial_entity_id`
- `entity_type` = polity / province / region / city / port / site / estate / other
- `canonical_name`
- `display_name`
- `from_year`
- `to_year`
- external identifiers where applicable
- `notes`
- `review_status`

### POLITY

A specialization of `SPATIAL_ENTITY` for historical political/social units.

Suggested fields:

- `spatial_entity_id` PK/FK
- `polity_type`
- `source_polity_id`
- `wikidata_id`
- `seshat_id`
- `notes`

Do not make every geography target a polity.

### SPATIAL_RELATION

Time-bounded relation between spatial entities.

Examples:

- port within polity
- province controlled by polity
- site within region

Suggested fields:

- `spatial_relation_id`
- `subject_spatial_entity_id`
- `object_spatial_entity_id`
- `relation_type`
- `from_year`
- `to_year`
- `valid_years`
- `claim_id` where the relationship itself requires evidence
- `notes`

A port must not carry one timeless `polity_id`.

### GEOMETRY

Time-bounded representation of a spatial entity.

Suggested fields:

- `geometry_id`
- `spatial_entity_id`
- `from_year`
- `to_year`
- `valid_years`
- `geometry_source_version_id`
- `geometry_source_id` / source-native identifier
- `resolution_method`
- `accuracy_status` = exact / specialist / approximate_historical / modern_proxy / unresolved
- `geom`
- `notes`

## 4. Universal claim model

### CLAIM

Every substantive historical assertion that needs provenance receives a stable claim identity.

Suggested fields:

- `claim_id`
- `claim_kind`
- `from_year`
- `to_year`
- `valid_years`
- `date_text_original`
- `temporal_precision`
- `temporal_certainty`
- `spatial_precision`
- `summary`
- `confidence`
- `review_status`
- `publication_status`
- `supersedes_claim_id`
- `notes`

A claim may be supported, challenged or qualified by multiple sources.

### TERRITORIAL_PRACTICE_CLAIM

Subtype of `CLAIM` about practice physically occurring in a spatial entity.

- `claim_id` PK/FK -> CLAIM
- `spatial_entity_id`
- `practice_type`
- `practice_level` P0–P4, nullable until an explicit P-level assessment is made
- `coverage_state`
- `classification_status`

P-level is interpreted from the evidence package and is never mechanically calculated from row counts.

`practice_level = NULL` means no P-level assessment has yet been recorded for that claim. It is not equivalent to P0. P0 is an explicit assessment of unknown/no usable classification and still does not mean absence. This distinction allows disputed or reviewed evidence to be stored without inventing an intensity classification.

### LEGAL_EVENT

Subtype of `CLAIM` describing a legal/state event or regime change.

- `claim_id` PK/FK -> CLAIM
- `jurisdiction_spatial_entity_id`
- `event_type`
- `legal_status_after`
- `instrument_name`
- `scope`
- `effective_date_text` where useful

Law and actual practice remain separate.

### EXTERNAL_PARTICIPATION_CLAIM

Subtype of `CLAIM` for participation in enslavement, slave-trading, captive-movement, market, finance or related networks when that evidence must remain separate from territorial practice intensity.

Suggested fields:

- `claim_id` PK/FK -> CLAIM
- `spatial_entity_id` and/or `actor_id`
- `participation_type`
- `role_text`
- `notes`

Use this for non-voyage network evidence such as a region documented as an origin/export node in an enslavement network when the source does not justify a territorial-practice prevalence claim. Voyage-specific ownership/finance/stop relationships remain in their specialized tables.

### ACTOR_ATTRIBUTE_CLAIM

Subtype of `CLAIM` for historically time-bounded actor attributes.

Examples:

- nationality / political identity
- residence
- business base
- corporate jurisdiction/context
- political/legal affiliation

Suggested fields:

- `claim_id` PK/FK -> CLAIM
- `actor_id`
- `attribute_type`
- `value_text`
- normalized reference where appropriate

This replaces the long-term need for a special `OWNER_EVIDENCE` evidence model while preserving all v0.6.1 owner-evidence meaning during migration.

## 5. Source and provenance model

### SOURCE

Conceptual source/publication/dataset/archive collection.

Suggested fields:

- `source_id`
- `title`
- `author_or_institution`
- `source_type`
- `source_classification` = primary / secondary / methodology / dataset / other
- `language`
- `geographic_scope`
- `temporal_scope`
- `independence_notes`
- `reliability_limitations`

### SOURCE_VERSION

Exact edition/release/snapshot/item used.

Suggested fields:

- `source_version_id`
- `source_id`
- `version_label`
- `publication_or_creation_date`
- `accessed_at`
- `url_or_identifier`
- `license_status`
- `redistribution_status`
- `notes`

Never silently merge source versions.

### SOURCE_ASSET

Optional locally stored asset when legally/permissibly available.

Suggested fields:

- `source_asset_id`
- `source_version_id`
- `filename_or_object_key`
- `media_type`
- `checksum_sha256`
- `storage_location`
- `redistribution_status`
- `notes`

### CLAIM_SOURCE

Many-to-many bridge from claims to exact source versions.

Suggested fields:

- `claim_source_id`
- `claim_id`
- `source_version_id`
- `evidence_role`
- `independence_group`
- `directness`
- `supports_or_challenges`
- `locator`
- `notes`

This is a real foreign-key relationship; do not use a polymorphic `claim_type + claim_id` reference.

## 6. Import provenance

### INGEST_RUN

Records a reproducible import/transformation run.

Suggested fields:

- `ingest_run_id`
- `source_version_id`
- `started_at`
- `completed_at`
- `code_version`
- `status`
- `notes`

### RAW_RECORD

Optional source-native row/object preservation for bulk datasets.

- `raw_record_id`
- `ingest_run_id`
- `source_native_id`
- `raw_payload` or external raw-asset locator
- `checksum` where useful

Raw values are not silently overwritten by normalized interpretations.

## 7. Voyage / participation network

### VOYAGE

Voyage facts and source-native identifiers. Documented versus imputed carrier fields remain separate.

### VOYAGE_OWNER

Explicit ownership relation between a voyage and an `ACTOR`.

Suggested fields:

- `voyage_owner_id`
- `voyage_id`
- `actor_id`
- `relationship_role`
- `ownership_share`
- `share_status`
- `claim_id` / provenance linkage as implemented
- `notes`

Ownership share remains unknown unless explicitly documented.

`VOYAGE_OWNER` is a claimable relationship and carries a `claim_id` so ownership evidence attaches through the same `CLAIM_SOURCE` model. `actor_id` may be NULL only for an explicit missing-owner/status row. Do not create an `ACTOR` representing “unknown owner”.

### VOYAGE_FINANCE

Explicit finance/insurance/credit/investment relation between a voyage and an `ACTOR`.

Suggested fields:

- `voyage_finance_id`
- `voyage_id`
- `actor_id`
- `finance_role`
- `amount_or_share` where documented
- `claim_id` / provenance linkage as implemented
- `notes`

Financing never implies ownership unless separately evidenced.

### VOYAGE_STOP

Links voyages to `SPATIAL_ENTITY` places.

Suggested fields:

- `voyage_stop_id`
- `voyage_id`
- `spatial_entity_id`
- `stop_role` = origin / embarkation / landing / call / other
- `sequence`
- `documented_or_imputed`
- `from_year` / `to_year` or event date where known
- `notes`

A historical port is represented as a `SPATIAL_ENTITY` with type `port`; its political context is resolved through time-bounded spatial relations rather than a permanent `polity_id`.

## 8. Publication and audit state

Canonical research records and public map records are not automatically identical.

Preferred lifecycle:

- `draft`
- `reviewed`
- `published`
- `superseded`
- `rejected_or_withdrawn` where required

Public services should consume reviewed/published views or release materializations rather than unrestricted research tables.

## 9. Research coverage metadata

### RESEARCH_COVERAGE_ASSESSMENT

Project research coverage is separate from historical practice. Broad audit states such as S/P/D/RI belong to a project/audit table, not `TERRITORIAL_PRACTICE_CLAIM`.

Suggested fields:

- `coverage_assessment_id`
- `spatial_entity_id` where a normalized region exists
- raw region label
- raw period label
- `from_year` / `to_year` / `valid_years`
- legacy coverage code S / P / D / RI / —
- normalized coverage state where applicable
- project-management coverage points where retained
- release/batch identifier
- review/publication state when exposed publicly
- notes

These fields may power a transparency/coverage layer but must never set P0–P4.

### RESEARCH_COVERAGE_SOURCE

Links a research-coverage assessment to exact source versions reviewed for that assessment. This is project/research provenance, not evidence that a territorial practice existed. Suggested fields:

- `coverage_assessment_id`
- `source_version_id`
- `source_role`
- `locator`
- `notes`

Do not reuse `CLAIM_SOURCE` for this purpose unless there is an actual historical claim.

## 10. Legacy migration mappings

The v0.6.1 workbook remains unchanged. During migration:

- `OWNER` -> `ACTOR`
- `OWNER_EVIDENCE` -> semantic migration: actor attributes become `ACTOR_ATTRIBUTE_CLAIM`; ownership/missing-owner evidence supports the claim carried by `VOYAGE_OWNER`; one legacy row may split into multiple claims; all provenance uses `CLAIM_SOURCE`
- planned `FINANCIER` -> `ACTOR` + `VOYAGE_FINANCE`
- planned `VOYAGE_FINANCIER` -> `VOYAGE_FINANCE`
- planned `PORT` -> `SPATIAL_ENTITY(entity_type=port)`
- existing/new `POLITY` -> `SPATIAL_ENTITY` + `POLITY`
- `GEOMETRY.polity_id` -> `GEOMETRY.spatial_entity_id`
- `TERRITORIAL_PRACTICE_CLAIM.polity_id` -> `spatial_entity_id`

No information may be discarded simply because the target model is more normalized.

## 11. Attributes/concepts that must never be collapsed

- vessel documented flag
- imputed carrier category
- actor nationality / political identity
- actor residence
- actor business base
- organization corporate jurisdiction
- ownership relation
- financing/insurance relation
- departure/origin place
- registration place
- territorial practice
- legal/state status
- research coverage
- geometry accuracy

Unknown remains unknown.
