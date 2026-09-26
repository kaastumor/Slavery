-- Migration 0031: add lossless research-target/result representation for reviewed v3 evidence.
-- Historical assertions remain normalized in atlas.claim; audit tables preserve research
-- outcomes (including HOLD/inconclusive) without inventing positive claims.

BEGIN;

ALTER TABLE atlas.claim
    ADD COLUMN temporal_applicability_mode text;

CREATE TABLE atlas.claim_asserted_interval (
    claim_asserted_interval_id uuid PRIMARY KEY DEFAULT gen_random_uuid(),
    claim_id uuid NOT NULL REFERENCES atlas.claim(claim_id) ON DELETE CASCADE,
    from_year integer,
    to_year integer,
    valid_years int4range GENERATED ALWAYS AS (atlas.make_year_range(from_year, to_year)) STORED,
    interval_role text,
    notes text,
    created_at timestamptz NOT NULL DEFAULT now(),
    CONSTRAINT claim_asserted_interval_year_order
        CHECK (from_year IS NULL OR to_year IS NULL OR from_year <= to_year)
);

CREATE INDEX claim_asserted_interval_claim_idx
    ON atlas.claim_asserted_interval(claim_id);
CREATE INDEX claim_asserted_interval_valid_years_gist
    ON atlas.claim_asserted_interval USING gist(valid_years);

CREATE TABLE atlas.claim_evidence_locus (
    claim_id uuid NOT NULL REFERENCES atlas.claim(claim_id) ON DELETE CASCADE,
    spatial_entity_id uuid NOT NULL REFERENCES atlas.spatial_entity(spatial_entity_id) ON DELETE RESTRICT,
    role_text text,
    notes text,
    PRIMARY KEY (claim_id, spatial_entity_id)
);

CREATE INDEX claim_evidence_locus_spatial_idx
    ON atlas.claim_evidence_locus(spatial_entity_id);

CREATE TABLE atlas.claim_inference_extent (
    claim_id uuid NOT NULL REFERENCES atlas.claim(claim_id) ON DELETE CASCADE,
    spatial_entity_id uuid NOT NULL REFERENCES atlas.spatial_entity(spatial_entity_id) ON DELETE RESTRICT,
    generalization_basis text,
    generalization_rationale text,
    PRIMARY KEY (claim_id, spatial_entity_id),
    CONSTRAINT broader_inference_requires_rationale
        CHECK (generalization_basis IS NULL OR generalization_rationale IS NOT NULL)
);

CREATE INDEX claim_inference_extent_spatial_idx
    ON atlas.claim_inference_extent(spatial_entity_id);

ALTER TABLE atlas.claim_source
    ADD COLUMN claim_fitness text;

ALTER TABLE atlas.territorial_practice_claim
    ALTER COLUMN practice_type_code DROP NOT NULL,
    ALTER COLUMN coverage_state_code DROP NOT NULL,
    ADD COLUMN assertion_form text,
    ADD COLUMN attestation_pattern text,
    ADD COLUMN interpretive_basis text,
    ADD COLUMN occurrence_pattern text,
    ADD COLUMN institutionalization text,
    ADD COLUMN prevalence_scope text,
    ADD COLUMN structural_significance text,
    ADD COLUMN research_stage text,
    ADD COLUMN classification_outcome text;

CREATE TABLE atlas.practice_facet_assertion (
    practice_facet_assertion_id uuid PRIMARY KEY DEFAULT gen_random_uuid(),
    claim_id uuid NOT NULL REFERENCES atlas.territorial_practice_claim(claim_id) ON DELETE CASCADE,
    facet_dimension text NOT NULL,
    concept_code text NOT NULL,
    notes text,
    created_at timestamptz NOT NULL DEFAULT now(),
    CONSTRAINT practice_facet_dimension_check
        CHECK (facet_dimension IN ('status','function','property_legal','transmission','process')),
    UNIQUE (claim_id, facet_dimension, concept_code)
);

COMMENT ON TABLE atlas.claim_asserted_interval IS
'Positive claim applicability intervals/dates. Outer claim ranges remain query envelopes and must not imply positive truth by themselves.';

COMMENT ON TABLE atlas.claim_evidence_locus IS
'Places where the underlying evidence or observation is anchored; separate from inference extent.';

COMMENT ON TABLE atlas.claim_inference_extent IS
'Places over which a reviewed claim is justified. Broader inference requires an explicit rationale.';

COMMENT ON COLUMN atlas.claim_source.claim_fitness IS
'Claim-specific source fitness/limitation assessment. Source quality is not global and does not mechanically determine prevalence.';

COMMENT ON COLUMN atlas.territorial_practice_claim.classification_outcome IS
'Epistemic historical result such as supported or researched_inconclusive; never infer absence or P0 from inconclusive.';

CREATE TABLE audit.research_target (
    target_key text PRIMARY KEY,
    target_label text NOT NULL,
    anchor_label text NOT NULL,
    anchor_year integer,
    frame_class text NOT NULL,
    spatial_entity_id uuid REFERENCES atlas.spatial_entity(spatial_entity_id) ON DELETE RESTRICT,
    origin text,
    review_status atlas.review_status NOT NULL DEFAULT 'draft',
    created_at timestamptz NOT NULL DEFAULT now()
);

COMMENT ON TABLE audit.research_target IS
'Stable research framing identity. A research target is not itself a historical claim and need not be a polity.';

CREATE TABLE audit.research_target_result (
    research_target_result_id uuid PRIMARY KEY DEFAULT gen_random_uuid(),
    target_key text NOT NULL REFERENCES audit.research_target(target_key) ON DELETE RESTRICT,
    research_stage text NOT NULL,
    research_outcome text NOT NULL,
    bounded_proposition text,
    required_abstention text,
    evidence_locus_summary text,
    inference_extent_summary text,
    temporal_state text,
    law_practice_note text,
    network_territorial_note text,
    historical_terms text,
    category_mapping_status text,
    category_mapping_note text,
    language_access_limitations text,
    coverage_confidence text,
    geometry_resolved_form text,
    geometry_claim_role text,
    geometry_unresolved_note text,
    source_path text,
    source_blob_ref text,
    content_sha256 text NOT NULL
        CHECK (content_sha256 ~ '^[0-9a-f]{64}$'),
    supersedes_result_id uuid REFERENCES audit.research_target_result(research_target_result_id) ON DELETE RESTRICT,
    review_status atlas.review_status NOT NULL DEFAULT 'draft',
    created_at timestamptz NOT NULL DEFAULT now(),
    UNIQUE (target_key, content_sha256),
    CONSTRAINT research_target_result_not_self_superseding
        CHECK (supersedes_result_id IS NULL OR supersedes_result_id <> research_target_result_id)
);

CREATE INDEX research_target_result_target_idx
    ON audit.research_target_result(target_key);

COMMENT ON TABLE audit.research_target_result IS
'Versioned research outcome for a target. HOLD and researched-inconclusive results are valid non-absence states and may exist without any positive historical claim.';

CREATE TABLE audit.research_target_review (
    research_target_review_id uuid PRIMARY KEY DEFAULT gen_random_uuid(),
    research_target_result_id uuid NOT NULL
        REFERENCES audit.research_target_result(research_target_result_id) ON DELETE CASCADE,
    candidate_id text,
    review_level text NOT NULL,
    review_disposition text NOT NULL,
    admitted boolean NOT NULL,
    review_reason text,
    failure_guards text[] NOT NULL DEFAULT '{}',
    dependency_or_scope_note text,
    reviewed_at timestamptz NOT NULL DEFAULT now(),
    notes text,
    CONSTRAINT research_target_review_level_check
        CHECK (review_level IN ('internal','independent')),
    UNIQUE (research_target_result_id, candidate_id, review_level)
);

COMMENT ON TABLE audit.research_target_review IS
'Review event for one research-target result. Internal and independent review remain distinct.';

CREATE TABLE audit.research_target_source (
    research_target_source_id uuid PRIMARY KEY DEFAULT gen_random_uuid(),
    research_target_result_id uuid NOT NULL
        REFERENCES audit.research_target_result(research_target_result_id) ON DELETE CASCADE,
    source_version_id uuid NOT NULL
        REFERENCES atlas.source_version(source_version_id) ON DELETE RESTRICT,
    source_relation_key text,
    source_version_ref_raw text NOT NULL,
    evidence_role text,
    independence_group text,
    claim_fitness text,
    direction_raw text,
    normalized_direction atlas.evidence_direction,
    locator text,
    notes text,
    created_at timestamptz NOT NULL DEFAULT now()
);

CREATE INDEX research_target_source_result_idx
    ON audit.research_target_source(research_target_result_id);
CREATE INDEX research_target_source_version_idx
    ON audit.research_target_source(source_version_id);
CREATE INDEX research_target_source_independence_idx
    ON audit.research_target_source(independence_group);

COMMENT ON TABLE audit.research_target_source IS
'Exact source-version relation reviewed for a research-target result. It need not imply a positive historical claim.';

CREATE TABLE audit.research_target_claim (
    research_target_result_id uuid NOT NULL
        REFERENCES audit.research_target_result(research_target_result_id) ON DELETE CASCADE,
    claim_id uuid NOT NULL REFERENCES atlas.claim(claim_id) ON DELETE RESTRICT,
    claim_role text NOT NULL DEFAULT 'primary',
    notes text,
    PRIMARY KEY (research_target_result_id, claim_id, claim_role)
);

CREATE INDEX research_target_claim_claim_idx
    ON audit.research_target_claim(claim_id);

COMMENT ON TABLE audit.research_target_claim IS
'Zero-to-many bridge from one reviewed research result to historical claims. Compound results must not be collapsed into one claim.';

COMMIT;
