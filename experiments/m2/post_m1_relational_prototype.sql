-- M2 #120 disposable relational prototype for D-058 post-M1 semantics.
-- This file is deliberately NOT a production migration. It is applied only to
-- disposable/local PostGIS until the M2 integrated adversary and health gate
-- decide whether the shape is fit for canonical implementation.

ALTER TABLE atlas.claim
    ADD COLUMN temporal_applicability_mode text;

ALTER TABLE atlas.claim
    ADD CONSTRAINT claim_temporal_applicability_mode_allowed
    CHECK (
        temporal_applicability_mode IS NULL
        OR temporal_applicability_mode IN (
            'continuous_interval',
            'bounded_occurrence',
            'alternative_dates',
            'terminus_after',
            'terminus_before',
            'unknown'
        )
    );

ALTER TABLE atlas.territorial_practice_claim
    ADD COLUMN assertion_form text,
    ADD COLUMN attestation_pattern text,
    ADD COLUMN interpretive_basis text,
    ADD COLUMN occurrence_pattern text,
    ADD COLUMN institutionalization text,
    ADD COLUMN prevalence_scope text,
    ADD COLUMN structural_significance text,
    ADD COLUMN research_stage text,
    ADD COLUMN classification_outcome text;

ALTER TABLE atlas.territorial_practice_claim
    ADD CONSTRAINT territorial_practice_assertion_form_allowed
        CHECK (
            assertion_form IS NULL
            OR assertion_form IN ('practice_or_status', 'event_or_process')
        ),
    ADD CONSTRAINT territorial_practice_attestation_pattern_allowed
        CHECK (
            attestation_pattern IS NULL
            OR attestation_pattern IN (
                'unassessed',
                'single_bounded_attestation',
                'recurrent_attestation',
                'multiple_independent_attestations',
                'mixed_or_unclear'
            )
        ),
    ADD CONSTRAINT territorial_practice_interpretive_basis_allowed
        CHECK (
            interpretive_basis IS NULL
            OR interpretive_basis IN (
                'unassessed',
                'primary_or_source_native',
                'specialist_synthesis',
                'mixed_primary_and_specialist'
            )
        ),
    ADD CONSTRAINT territorial_practice_occurrence_pattern_allowed
        CHECK (
            occurrence_pattern IS NULL
            OR occurrence_pattern IN (
                'unassessed',
                'bounded_occurrence',
                'recurrent',
                'continuous_period'
            )
        ),
    ADD CONSTRAINT territorial_practice_institutionalization_allowed
        CHECK (
            institutionalization IS NULL
            OR institutionalization IN (
                'unassessed',
                'institutional_features_supported'
            )
        ),
    ADD CONSTRAINT territorial_practice_prevalence_scope_allowed
        CHECK (
            prevalence_scope IS NULL
            OR prevalence_scope IN (
                'unassessed',
                'localized',
                'broader',
                'widespread'
            )
        ),
    ADD CONSTRAINT territorial_practice_structural_significance_allowed
        CHECK (
            structural_significance IS NULL
            OR structural_significance IN (
                'unassessed',
                'structurally_major_supported'
            )
        ),
    ADD CONSTRAINT territorial_practice_research_stage_allowed
        CHECK (
            research_stage IS NULL
            OR research_stage IN (
                'not_researched',
                'source_identified',
                'under_review',
                'review_complete'
            )
        ),
    ADD CONSTRAINT territorial_practice_classification_outcome_allowed
        CHECK (
            classification_outcome IS NULL
            OR classification_outcome IN (
                'unassessed',
                'classified',
                'disputed',
                'inconclusive'
            )
        ),
    ADD CONSTRAINT territorial_practice_post_m1_dimensions_explicit
        CHECK (
            (
                assertion_form IS NULL
                AND attestation_pattern IS NULL
                AND interpretive_basis IS NULL
                AND occurrence_pattern IS NULL
                AND institutionalization IS NULL
                AND prevalence_scope IS NULL
                AND structural_significance IS NULL
                AND research_stage IS NULL
                AND classification_outcome IS NULL
            )
            OR
            (
                assertion_form IS NOT NULL
                AND attestation_pattern IS NOT NULL
                AND interpretive_basis IS NOT NULL
                AND occurrence_pattern IS NOT NULL
                AND institutionalization IS NOT NULL
                AND prevalence_scope IS NOT NULL
                AND structural_significance IS NOT NULL
                AND research_stage IS NOT NULL
                AND classification_outcome IS NOT NULL
            )
        );

CREATE TABLE atlas.claim_asserted_interval (
    claim_asserted_interval_id uuid PRIMARY KEY DEFAULT gen_random_uuid(),
    claim_id uuid NOT NULL
        REFERENCES atlas.claim(claim_id) ON DELETE CASCADE,
    from_year integer NOT NULL,
    to_year integer NOT NULL,
    valid_years int4range GENERATED ALWAYS AS (
        atlas.make_year_range(from_year, to_year)
    ) STORED,
    interval_role text NOT NULL DEFAULT 'asserted_applicability'
        CHECK (interval_role IN ('asserted_applicability', 'alternative')),
    notes text,
    CONSTRAINT claim_asserted_interval_year_order
        CHECK (from_year <= to_year)
);

CREATE INDEX claim_asserted_interval_claim_idx
    ON atlas.claim_asserted_interval(claim_id);
CREATE INDEX claim_asserted_interval_years_gist
    ON atlas.claim_asserted_interval USING gist(valid_years);

CREATE TABLE atlas.practice_facet_assertion (
    practice_facet_assertion_id uuid PRIMARY KEY DEFAULT gen_random_uuid(),
    claim_id uuid NOT NULL
        REFERENCES atlas.territorial_practice_claim(claim_id) ON DELETE CASCADE,
    facet_dimension text NOT NULL
        CHECK (
            facet_dimension IN (
                'status',
                'function',
                'property_legal',
                'transmission',
                'process'
            )
        ),
    concept_code text NOT NULL
        CHECK (btrim(concept_code) <> ''),
    notes text,
    UNIQUE (claim_id, facet_dimension, concept_code)
);

CREATE INDEX practice_facet_assertion_claim_idx
    ON atlas.practice_facet_assertion(claim_id);

CREATE TABLE atlas.claim_evidence_locus (
    claim_id uuid NOT NULL
        REFERENCES atlas.claim(claim_id) ON DELETE CASCADE,
    spatial_entity_id uuid NOT NULL
        REFERENCES atlas.spatial_entity(spatial_entity_id) ON DELETE RESTRICT,
    role_text text,
    notes text,
    PRIMARY KEY (claim_id, spatial_entity_id)
);

CREATE INDEX claim_evidence_locus_spatial_idx
    ON atlas.claim_evidence_locus(spatial_entity_id);

CREATE TABLE atlas.claim_inference_extent (
    claim_id uuid NOT NULL
        REFERENCES atlas.claim(claim_id) ON DELETE CASCADE,
    spatial_entity_id uuid NOT NULL
        REFERENCES atlas.spatial_entity(spatial_entity_id) ON DELETE RESTRICT,
    generalization_basis text NOT NULL
        CHECK (
            generalization_basis IN (
                'same_as_locus',
                'specialist_polity_synthesis',
                'explicit_source_jurisdiction',
                'multi_locus_synthesis',
                'other_reviewed'
            )
        ),
    generalization_rationale text,
    notes text,
    PRIMARY KEY (claim_id, spatial_entity_id)
);

CREATE INDEX claim_inference_extent_spatial_idx
    ON atlas.claim_inference_extent(spatial_entity_id);

CREATE OR REPLACE FUNCTION atlas.validate_asserted_interval_row()
RETURNS trigger
LANGUAGE plpgsql
SET search_path = pg_catalog, atlas
AS $$
DECLARE
    v_query_from integer;
    v_query_to integer;
    v_mode text;
BEGIN
    SELECT c.from_year, c.to_year, c.temporal_applicability_mode
      INTO v_query_from, v_query_to, v_mode
      FROM atlas.claim c
     WHERE c.claim_id = NEW.claim_id;

    IF NOT FOUND THEN
        RAISE EXCEPTION 'claim % does not exist', NEW.claim_id;
    END IF;

    IF v_mode IS NULL OR v_mode = 'unknown' THEN
        RAISE EXCEPTION
            'claim % cannot have positive asserted intervals with applicability mode %',
            NEW.claim_id, coalesce(v_mode, '<legacy/null>');
    END IF;

    IF v_query_from IS NOT NULL AND NEW.from_year < v_query_from THEN
        RAISE EXCEPTION
            'asserted interval starts before claim query window for claim %',
            NEW.claim_id;
    END IF;

    IF v_query_to IS NOT NULL AND NEW.to_year > v_query_to THEN
        RAISE EXCEPTION
            'asserted interval ends after claim query window for claim %',
            NEW.claim_id;
    END IF;

    IF v_mode = 'alternative_dates' AND NEW.interval_role <> 'alternative' THEN
        RAISE EXCEPTION
            'alternative_dates claim % requires interval_role=alternative',
            NEW.claim_id;
    END IF;

    IF v_mode <> 'alternative_dates' AND NEW.interval_role = 'alternative' THEN
        RAISE EXCEPTION
            'claim % uses alternative interval role without alternative_dates mode',
            NEW.claim_id;
    END IF;

    RETURN NEW;
END;
$$;

CREATE TRIGGER claim_asserted_interval_row_guard
BEFORE INSERT OR UPDATE ON atlas.claim_asserted_interval
FOR EACH ROW EXECUTE FUNCTION atlas.validate_asserted_interval_row();

CREATE OR REPLACE FUNCTION atlas.validate_claim_temporal_semantics(p_claim_id uuid)
RETURNS void
LANGUAGE plpgsql
SET search_path = pg_catalog, atlas
AS $$
DECLARE
    v_mode text;
    v_interval_count integer;
    v_post_m1_territorial boolean;
BEGIN
    SELECT c.temporal_applicability_mode
      INTO v_mode
      FROM atlas.claim c
     WHERE c.claim_id = p_claim_id;

    IF NOT FOUND THEN
        RETURN;
    END IF;

    SELECT count(*)
      INTO v_interval_count
      FROM atlas.claim_asserted_interval i
     WHERE i.claim_id = p_claim_id;

    SELECT EXISTS (
        SELECT 1
          FROM atlas.territorial_practice_claim t
         WHERE t.claim_id = p_claim_id
           AND t.assertion_form IS NOT NULL
    )
      INTO v_post_m1_territorial;

    IF v_post_m1_territorial AND v_mode IS NULL THEN
        RAISE EXCEPTION
            'post-M1 territorial claim % requires explicit temporal_applicability_mode',
            p_claim_id;
    END IF;

    IF v_mode IS NULL AND v_interval_count > 0 THEN
        RAISE EXCEPTION
            'legacy/null temporal mode claim % cannot carry asserted intervals',
            p_claim_id;
    END IF;

    IF v_mode = 'unknown' AND v_interval_count > 0 THEN
        RAISE EXCEPTION
            'unknown applicability claim % cannot carry positive asserted intervals',
            p_claim_id;
    END IF;

    IF v_mode IN (
        'continuous_interval',
        'bounded_occurrence',
        'alternative_dates'
    ) AND v_interval_count = 0 THEN
        RAISE EXCEPTION
            'applicability mode % requires at least one asserted interval for claim %',
            v_mode, p_claim_id;
    END IF;
END;
$$;

CREATE OR REPLACE FUNCTION atlas.check_claim_temporal_semantics()
RETURNS trigger
LANGUAGE plpgsql
SET search_path = pg_catalog, atlas
AS $$
DECLARE
    v_claim_id uuid;
BEGIN
    v_claim_id := CASE
        WHEN TG_OP = 'DELETE' THEN OLD.claim_id
        ELSE NEW.claim_id
    END;
    PERFORM atlas.validate_claim_temporal_semantics(v_claim_id);
    RETURN NULL;
END;
$$;

CREATE CONSTRAINT TRIGGER claim_temporal_semantics_complete
AFTER INSERT OR UPDATE ON atlas.claim
DEFERRABLE INITIALLY DEFERRED
FOR EACH ROW EXECUTE FUNCTION atlas.check_claim_temporal_semantics();

CREATE CONSTRAINT TRIGGER territorial_post_m1_temporal_semantics_complete
AFTER INSERT OR UPDATE ON atlas.territorial_practice_claim
DEFERRABLE INITIALLY DEFERRED
FOR EACH ROW EXECUTE FUNCTION atlas.check_claim_temporal_semantics();

CREATE CONSTRAINT TRIGGER asserted_interval_temporal_semantics_complete
AFTER INSERT OR UPDATE OR DELETE ON atlas.claim_asserted_interval
DEFERRABLE INITIALLY DEFERRED
FOR EACH ROW EXECUTE FUNCTION atlas.check_claim_temporal_semantics();

CREATE OR REPLACE FUNCTION atlas.post_m1_claim_active_at(
    p_claim_id uuid,
    p_selected_year integer
)
RETURNS boolean
LANGUAGE sql
STABLE
SET search_path = pg_catalog, atlas
AS $$
    SELECT coalesce((
        SELECT CASE
            WHEN c.temporal_applicability_mode IS NULL
                 OR c.temporal_applicability_mode = 'unknown'
                THEN false
            WHEN c.valid_years IS NOT NULL
                 AND NOT (c.valid_years @> p_selected_year)
                THEN false
            ELSE EXISTS (
                SELECT 1
                  FROM atlas.claim_asserted_interval i
                 WHERE i.claim_id = c.claim_id
                   AND i.valid_years @> p_selected_year
            )
        END
          FROM atlas.claim c
         WHERE c.claim_id = p_claim_id
    ), false);
$$;

COMMENT ON FUNCTION atlas.post_m1_claim_active_at(uuid, integer) IS
'Prototype selected-year predicate: outer query bounds retrieve candidates, but only explicit asserted intervals create positive post-M1 applicability. Temporal precision is intentionally not part of the truth predicate.';

CREATE OR REPLACE FUNCTION atlas.validate_claim_spatial_scope(p_claim_id uuid)
RETURNS void
LANGUAGE plpgsql
SET search_path = pg_catalog, atlas
AS $$
DECLARE
    v_extent record;
    v_same_as_locus boolean;
BEGIN
    FOR v_extent IN
        SELECT i.spatial_entity_id,
               i.generalization_basis,
               i.generalization_rationale
          FROM atlas.claim_inference_extent i
         WHERE i.claim_id = p_claim_id
    LOOP
        SELECT EXISTS (
            SELECT 1
              FROM atlas.claim_evidence_locus l
             WHERE l.claim_id = p_claim_id
               AND l.spatial_entity_id = v_extent.spatial_entity_id
        )
          INTO v_same_as_locus;

        IF v_same_as_locus THEN
            IF v_extent.generalization_basis <> 'same_as_locus' THEN
                RAISE EXCEPTION
                    'claim % inference extent matching its evidence locus must use same_as_locus',
                    p_claim_id;
            END IF;
        ELSE
            IF v_extent.generalization_basis = 'same_as_locus' THEN
                RAISE EXCEPTION
                    'claim % cannot label a broader/different inference extent as same_as_locus',
                    p_claim_id;
            END IF;

            IF btrim(coalesce(v_extent.generalization_rationale, '')) = '' THEN
                RAISE EXCEPTION
                    'claim % broader/different inference extent requires reviewed rationale',
                    p_claim_id;
            END IF;
        END IF;
    END LOOP;
END;
$$;

CREATE OR REPLACE FUNCTION atlas.check_claim_spatial_scope()
RETURNS trigger
LANGUAGE plpgsql
SET search_path = pg_catalog, atlas
AS $$
DECLARE
    v_claim_id uuid;
BEGIN
    v_claim_id := CASE
        WHEN TG_OP = 'DELETE' THEN OLD.claim_id
        ELSE NEW.claim_id
    END;
    PERFORM atlas.validate_claim_spatial_scope(v_claim_id);
    RETURN NULL;
END;
$$;

CREATE CONSTRAINT TRIGGER claim_evidence_locus_scope_complete
AFTER INSERT OR UPDATE OR DELETE ON atlas.claim_evidence_locus
DEFERRABLE INITIALLY DEFERRED
FOR EACH ROW EXECUTE FUNCTION atlas.check_claim_spatial_scope();

CREATE CONSTRAINT TRIGGER claim_inference_extent_scope_complete
AFTER INSERT OR UPDATE OR DELETE ON atlas.claim_inference_extent
DEFERRABLE INITIALLY DEFERRED
FOR EACH ROW EXECUTE FUNCTION atlas.check_claim_spatial_scope();

COMMENT ON TABLE atlas.claim_asserted_interval IS
'M2 disposable prototype: positively asserted applicability intervals/dates. Outer CLAIM.valid_years remains only a retrieval/query envelope.';
COMMENT ON TABLE atlas.claim_evidence_locus IS
'M2 disposable prototype: places where underlying evidence/observation is anchored.';
COMMENT ON TABLE atlas.claim_inference_extent IS
'M2 disposable prototype: reviewed spatial extent of a claim; a broader/different extent requires explicit reviewed basis and rationale.';
COMMENT ON TABLE atlas.practice_facet_assertion IS
'M2 disposable prototype: simultaneous typed practice concepts; this does not establish a final exhaustive controlled vocabulary.';

-- D-051 defense in depth: PostgreSQL grants EXECUTE on new functions to
-- PUBLIC by default in some execution paths. The disposable prototype must not
-- weaken the existing internal-schema boundary merely because it adds helpers.
REVOKE ALL PRIVILEGES ON
    atlas.claim_asserted_interval,
    atlas.practice_facet_assertion,
    atlas.claim_evidence_locus,
    atlas.claim_inference_extent
FROM PUBLIC;

REVOKE EXECUTE ON FUNCTION atlas.validate_asserted_interval_row() FROM PUBLIC;
REVOKE EXECUTE ON FUNCTION atlas.validate_claim_temporal_semantics(uuid) FROM PUBLIC;
REVOKE EXECUTE ON FUNCTION atlas.check_claim_temporal_semantics() FROM PUBLIC;
REVOKE EXECUTE ON FUNCTION atlas.post_m1_claim_active_at(uuid, integer) FROM PUBLIC;
REVOKE EXECUTE ON FUNCTION atlas.validate_claim_spatial_scope(uuid) FROM PUBLIC;
REVOKE EXECUTE ON FUNCTION atlas.check_claim_spatial_scope() FROM PUBLIC;

