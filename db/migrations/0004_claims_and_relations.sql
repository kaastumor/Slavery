-- Migration 0004: universal claims, specialized claims, claim-specific evidence, spatial relations.

BEGIN;

CREATE TABLE atlas.claim (
    claim_id uuid PRIMARY KEY DEFAULT gen_random_uuid(),
    claim_kind_code text NOT NULL REFERENCES atlas.claim_kind(code),
    from_year integer,
    to_year integer,
    valid_years int4range GENERATED ALWAYS AS (atlas.make_year_range(from_year, to_year)) STORED,
    date_text_original text,
    temporal_precision text,
    temporal_certainty text,
    spatial_precision text,
    summary text NOT NULL,
    confidence text,
    review_status atlas.review_status NOT NULL DEFAULT 'draft',
    publication_status atlas.publication_status NOT NULL DEFAULT 'unpublished',
    supersedes_claim_id uuid REFERENCES atlas.claim(claim_id) ON DELETE RESTRICT,
    notes text,
    created_at timestamptz NOT NULL DEFAULT now(),
    CONSTRAINT claim_year_order CHECK (from_year IS NULL OR to_year IS NULL OR from_year <= to_year),
    CONSTRAINT claim_not_self_superseding CHECK (supersedes_claim_id IS NULL OR supersedes_claim_id <> claim_id),
    CONSTRAINT published_claim_must_be_reviewed CHECK (publication_status <> 'published' OR review_status = 'reviewed')
);

CREATE INDEX claim_valid_years_gist ON atlas.claim USING gist(valid_years);
CREATE INDEX claim_kind_idx ON atlas.claim(claim_kind_code);
CREATE INDEX claim_publication_idx ON atlas.claim(publication_status, review_status);

CREATE TABLE atlas.territorial_practice_claim (
    claim_id uuid PRIMARY KEY REFERENCES atlas.claim(claim_id) ON DELETE CASCADE,
    spatial_entity_id uuid NOT NULL REFERENCES atlas.spatial_entity(spatial_entity_id) ON DELETE RESTRICT,
    practice_type_code text NOT NULL REFERENCES atlas.practice_type(code),
    practice_level atlas.practice_level NOT NULL,
    coverage_state_code text NOT NULL REFERENCES atlas.coverage_state(code),
    classification_status text,
    notes text
);

CREATE INDEX territorial_practice_spatial_idx ON atlas.territorial_practice_claim(spatial_entity_id);
CREATE INDEX territorial_practice_type_idx ON atlas.territorial_practice_claim(practice_type_code);
CREATE INDEX territorial_practice_level_idx ON atlas.territorial_practice_claim(practice_level);

CREATE TABLE atlas.legal_event (
    claim_id uuid PRIMARY KEY REFERENCES atlas.claim(claim_id) ON DELETE CASCADE,
    jurisdiction_spatial_entity_id uuid NOT NULL REFERENCES atlas.spatial_entity(spatial_entity_id) ON DELETE RESTRICT,
    event_type text NOT NULL,
    legal_status_after text,
    instrument_name text,
    scope text,
    effective_date_text text,
    notes text
);

CREATE INDEX legal_event_jurisdiction_idx ON atlas.legal_event(jurisdiction_spatial_entity_id);

CREATE TABLE atlas.actor_attribute_claim (
    claim_id uuid PRIMARY KEY REFERENCES atlas.claim(claim_id) ON DELETE CASCADE,
    actor_id uuid NOT NULL REFERENCES atlas.actor(actor_id) ON DELETE RESTRICT,
    attribute_type_code text NOT NULL REFERENCES atlas.actor_attribute_type(code),
    value_text text,
    value_actor_id uuid REFERENCES atlas.actor(actor_id) ON DELETE RESTRICT,
    value_spatial_entity_id uuid REFERENCES atlas.spatial_entity(spatial_entity_id) ON DELETE RESTRICT,
    notes text,
    CONSTRAINT actor_attribute_has_value CHECK (
        value_text IS NOT NULL OR value_actor_id IS NOT NULL OR value_spatial_entity_id IS NOT NULL
    )
);

CREATE INDEX actor_attribute_actor_idx ON atlas.actor_attribute_claim(actor_id);
CREATE INDEX actor_attribute_type_idx ON atlas.actor_attribute_claim(attribute_type_code);

CREATE TABLE atlas.claim_source (
    claim_source_id uuid PRIMARY KEY DEFAULT gen_random_uuid(),
    claim_id uuid NOT NULL REFERENCES atlas.claim(claim_id) ON DELETE CASCADE,
    source_version_id uuid NOT NULL REFERENCES atlas.source_version(source_version_id) ON DELETE RESTRICT,
    evidence_role text,
    independence_group text,
    directness text,
    direction atlas.evidence_direction NOT NULL DEFAULT 'supports',
    locator text,
    notes text,
    created_at timestamptz NOT NULL DEFAULT now()
);

CREATE INDEX claim_source_claim_idx ON atlas.claim_source(claim_id);
CREATE INDEX claim_source_version_idx ON atlas.claim_source(source_version_id);
CREATE INDEX claim_source_independence_idx ON atlas.claim_source(independence_group);

CREATE TABLE atlas.spatial_relation (
    spatial_relation_id uuid PRIMARY KEY DEFAULT gen_random_uuid(),
    subject_spatial_entity_id uuid NOT NULL REFERENCES atlas.spatial_entity(spatial_entity_id) ON DELETE CASCADE,
    object_spatial_entity_id uuid NOT NULL REFERENCES atlas.spatial_entity(spatial_entity_id) ON DELETE CASCADE,
    relation_type_code text NOT NULL REFERENCES atlas.spatial_relation_type(code),
    from_year integer,
    to_year integer,
    valid_years int4range GENERATED ALWAYS AS (atlas.make_year_range(from_year, to_year)) STORED,
    claim_id uuid REFERENCES atlas.claim(claim_id) ON DELETE RESTRICT,
    notes text,
    review_status atlas.review_status NOT NULL DEFAULT 'draft',
    created_at timestamptz NOT NULL DEFAULT now(),
    CONSTRAINT spatial_relation_distinct_entities CHECK (subject_spatial_entity_id <> object_spatial_entity_id),
    CONSTRAINT spatial_relation_year_order CHECK (from_year IS NULL OR to_year IS NULL OR from_year <= to_year)
);

CREATE INDEX spatial_relation_subject_idx ON atlas.spatial_relation(subject_spatial_entity_id);
CREATE INDEX spatial_relation_object_idx ON atlas.spatial_relation(object_spatial_entity_id);
CREATE INDEX spatial_relation_valid_years_gist ON atlas.spatial_relation USING gist(valid_years);

COMMIT;
