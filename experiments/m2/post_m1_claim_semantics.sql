-- M2 #120 disposable prototype: post-M1 claim semantics in the real relational model.
-- Intentionally NOT a production migration. Apply only to disposable/local PostGIS.
-- Legacy rows opt out by leaving semantic_model_version NULL.

ALTER TABLE atlas.claim
    ADD COLUMN IF NOT EXISTS semantic_model_version text,
    ADD COLUMN IF NOT EXISTS temporal_applicability_mode text;

ALTER TABLE atlas.claim
    DROP CONSTRAINT IF EXISTS claim_semantic_model_version_allowed,
    ADD CONSTRAINT claim_semantic_model_version_allowed CHECK (
        semantic_model_version IS NULL OR semantic_model_version = 'post_m1_v2'
    ),
    DROP CONSTRAINT IF EXISTS claim_temporal_applicability_mode_allowed,
    ADD CONSTRAINT claim_temporal_applicability_mode_allowed CHECK (
        temporal_applicability_mode IS NULL OR temporal_applicability_mode IN (
            'continuous_interval',
            'bounded_occurrence',
            'alternative_dates',
            'terminus_after',
            'terminus_before',
            'unknown'
        )
    ),
    DROP CONSTRAINT IF EXISTS claim_post_m1_temporal_mode_required,
    ADD CONSTRAINT claim_post_m1_temporal_mode_required CHECK (
        (semantic_model_version IS NULL AND temporal_applicability_mode IS NULL)
        OR
        (semantic_model_version = 'post_m1_v2' AND temporal_applicability_mode IS NOT NULL)
    );

ALTER TABLE atlas.territorial_practice_claim
    ADD COLUMN IF NOT EXISTS assertion_form text,
    ADD COLUMN IF NOT EXISTS attestation_pattern text,
    ADD COLUMN IF NOT EXISTS interpretive_basis text,
    ADD COLUMN IF NOT EXISTS occurrence_pattern text,
    ADD COLUMN IF NOT EXISTS institutionalization text,
    ADD COLUMN IF NOT EXISTS prevalence_scope text,
    ADD COLUMN IF NOT EXISTS structural_significance text,
    ADD COLUMN IF NOT EXISTS research_stage text,
    ADD COLUMN IF NOT EXISTS classification_outcome text;

ALTER TABLE atlas.territorial_practice_claim
    DROP CONSTRAINT IF EXISTS tpc_assertion_form_allowed,
    ADD CONSTRAINT tpc_assertion_form_allowed CHECK (
        assertion_form IS NULL OR assertion_form IN ('practice_or_status','event_or_process')
    ),
    DROP CONSTRAINT IF EXISTS tpc_attestation_pattern_allowed,
    ADD CONSTRAINT tpc_attestation_pattern_allowed CHECK (
        attestation_pattern IS NULL OR attestation_pattern IN (
            'unassessed','single_bounded_attestation','recurrent_attestation',
            'multiple_independent_attestations','mixed_or_unclear'
        )
    ),
    DROP CONSTRAINT IF EXISTS tpc_interpretive_basis_allowed,
    ADD CONSTRAINT tpc_interpretive_basis_allowed CHECK (
        interpretive_basis IS NULL OR interpretive_basis IN (
            'unassessed','primary_or_source_native','specialist_synthesis',
            'mixed_primary_and_specialist'
        )
    ),
    DROP CONSTRAINT IF EXISTS tpc_occurrence_pattern_allowed,
    ADD CONSTRAINT tpc_occurrence_pattern_allowed CHECK (
        occurrence_pattern IS NULL OR occurrence_pattern IN (
            'unassessed','bounded_occurrence','recurrent','continuous_period'
        )
    ),
    DROP CONSTRAINT IF EXISTS tpc_institutionalization_allowed,
    ADD CONSTRAINT tpc_institutionalization_allowed CHECK (
        institutionalization IS NULL OR institutionalization IN (
            'unassessed','institutional_features_supported'
        )
    ),
    DROP CONSTRAINT IF EXISTS tpc_prevalence_scope_allowed,
    ADD CONSTRAINT tpc_prevalence_scope_allowed CHECK (
        prevalence_scope IS NULL OR prevalence_scope IN (
            'unassessed','localized','broader','widespread'
        )
    ),
    DROP CONSTRAINT IF EXISTS tpc_structural_significance_allowed,
    ADD CONSTRAINT tpc_structural_significance_allowed CHECK (
        structural_significance IS NULL OR structural_significance IN (
            'unassessed','structurally_major_supported'
        )
    ),
    DROP CONSTRAINT IF EXISTS tpc_research_stage_allowed,
    ADD CONSTRAINT tpc_research_stage_allowed CHECK (
        research_stage IS NULL OR research_stage IN (
            'not_researched','source_identified','under_review','review_complete'
        )
    ),
    DROP CONSTRAINT IF EXISTS tpc_classification_outcome_allowed,
    ADD CONSTRAINT tpc_classification_outcome_allowed CHECK (
        classification_outcome IS NULL OR classification_outcome IN (
            'unassessed','classified','disputed','inconclusive'
        )
    );

CREATE TABLE IF NOT EXISTS atlas.claim_asserted_interval (
    claim_asserted_interval_id uuid PRIMARY KEY DEFAULT gen_random_uuid(),
    claim_id uuid NOT NULL REFERENCES atlas.claim(claim_id) ON DELETE CASCADE,
    from_year integer NOT NULL,
    to_year integer NOT NULL,
    valid_years int4range GENERATED ALWAYS AS (atlas.make_year_range(from_year, to_year)) STORED,
    interval_role text NOT NULL DEFAULT 'asserted'
        CHECK (interval_role IN ('asserted','alternative')),
    notes text,
    CONSTRAINT claim_asserted_interval_year_order CHECK (from_year <= to_year),
    UNIQUE (claim_id, from_year, to_year, interval_role)
);

CREATE INDEX IF NOT EXISTS claim_asserted_interval_claim_idx
    ON atlas.claim_asserted_interval(claim_id);
CREATE INDEX IF NOT EXISTS claim_asserted_interval_years_gist
    ON atlas.claim_asserted_interval USING gist(valid_years);

CREATE TABLE IF NOT EXISTS atlas.claim_evidence_locus (
    claim_id uuid NOT NULL REFERENCES atlas.claim(claim_id) ON DELETE CASCADE,
    spatial_entity_id uuid NOT NULL REFERENCES atlas.spatial_entity(spatial_entity_id) ON DELETE RESTRICT,
    role_text text,
    notes text,
    PRIMARY KEY (claim_id, spatial_entity_id)
);

CREATE TABLE IF NOT EXISTS atlas.claim_inference_extent (
    claim_id uuid NOT NULL REFERENCES atlas.claim(claim_id) ON DELETE CASCADE,
    spatial_entity_id uuid NOT NULL REFERENCES atlas.spatial_entity(spatial_entity_id) ON DELETE RESTRICT,
    generalization_basis text NOT NULL CHECK (
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
    PRIMARY KEY (claim_id, spatial_entity_id),
    CONSTRAINT inference_broader_basis_requires_rationale CHECK (
        generalization_basis = 'same_as_locus'
        OR nullif(btrim(generalization_rationale),'') IS NOT NULL
    )
);

CREATE TABLE IF NOT EXISTS atlas.practice_facet_assertion (
    practice_facet_assertion_id uuid PRIMARY KEY DEFAULT gen_random_uuid(),
    claim_id uuid NOT NULL REFERENCES atlas.territorial_practice_claim(claim_id) ON DELETE CASCADE,
    facet_dimension text NOT NULL CHECK (
        facet_dimension IN ('status','function','property_legal','transmission','process')
    ),
    concept_code text NOT NULL CHECK (nullif(btrim(concept_code),'') IS NOT NULL),
    notes text,
    UNIQUE (claim_id, facet_dimension, concept_code)
);

CREATE OR REPLACE FUNCTION atlas.enforce_post_m1_territorial_semantics()
RETURNS trigger
LANGUAGE plpgsql
SET search_path = ''
AS $$
DECLARE
    model_version text;
    any_target_value boolean;
BEGIN
    SELECT semantic_model_version INTO model_version
    FROM atlas.claim
    WHERE claim_id = NEW.claim_id;

    any_target_value :=
        NEW.assertion_form IS NOT NULL
        OR NEW.attestation_pattern IS NOT NULL
        OR NEW.interpretive_basis IS NOT NULL
        OR NEW.occurrence_pattern IS NOT NULL
        OR NEW.institutionalization IS NOT NULL
        OR NEW.prevalence_scope IS NOT NULL
        OR NEW.structural_significance IS NOT NULL
        OR NEW.research_stage IS NOT NULL
        OR NEW.classification_outcome IS NOT NULL;

    IF model_version IS NULL THEN
        IF any_target_value THEN
            RAISE EXCEPTION
                'post-M1 territorial dimensions require claim semantic_model_version=post_m1_v2';
        END IF;
        RETURN NEW;
    END IF;

    IF model_version <> 'post_m1_v2' THEN
        RAISE EXCEPTION 'unsupported semantic model version %', model_version;
    END IF;

    IF NEW.assertion_form IS NULL
       OR NEW.attestation_pattern IS NULL
       OR NEW.interpretive_basis IS NULL
       OR NEW.occurrence_pattern IS NULL
       OR NEW.institutionalization IS NULL
       OR NEW.prevalence_scope IS NULL
       OR NEW.structural_significance IS NULL
       OR NEW.research_stage IS NULL
       OR NEW.classification_outcome IS NULL THEN
        RAISE EXCEPTION
            'post-M1 territorial claim % must state every target dimension explicitly; use unassessed where appropriate',
            NEW.claim_id;
    END IF;

    RETURN NEW;
END;
$$;

DROP TRIGGER IF EXISTS territorial_post_m1_semantics_check
    ON atlas.territorial_practice_claim;
CREATE TRIGGER territorial_post_m1_semantics_check
BEFORE INSERT OR UPDATE ON atlas.territorial_practice_claim
FOR EACH ROW EXECUTE FUNCTION atlas.enforce_post_m1_territorial_semantics();

CREATE OR REPLACE FUNCTION atlas.enforce_asserted_interval_within_query_window()
RETURNS trigger
LANGUAGE plpgsql
SET search_path = ''
AS $$
DECLARE
    outer_from integer;
    outer_to integer;
    model_version text;
BEGIN
    SELECT from_year, to_year, semantic_model_version
      INTO outer_from, outer_to, model_version
    FROM atlas.claim
    WHERE claim_id = NEW.claim_id;

    IF model_version IS DISTINCT FROM 'post_m1_v2' THEN
        RAISE EXCEPTION
            'asserted intervals are post-M1 semantics and require claim semantic_model_version=post_m1_v2';
    END IF;

    IF outer_from IS NOT NULL AND NEW.from_year < outer_from THEN
        RAISE EXCEPTION
            'asserted interval starts before claim outer query window';
    END IF;
    IF outer_to IS NOT NULL AND NEW.to_year > outer_to THEN
        RAISE EXCEPTION
            'asserted interval ends after claim outer query window';
    END IF;

    RETURN NEW;
END;
$$;

DROP TRIGGER IF EXISTS claim_asserted_interval_query_window_check
    ON atlas.claim_asserted_interval;
CREATE TRIGGER claim_asserted_interval_query_window_check
BEFORE INSERT OR UPDATE ON atlas.claim_asserted_interval
FOR EACH ROW EXECUTE FUNCTION atlas.enforce_asserted_interval_within_query_window();

CREATE OR REPLACE FUNCTION atlas.enforce_same_as_locus_inference()
RETURNS trigger
LANGUAGE plpgsql
SET search_path = ''
AS $$
BEGIN
    IF NEW.generalization_basis = 'same_as_locus'
       AND NOT EXISTS (
           SELECT 1
           FROM atlas.claim_evidence_locus l
           WHERE l.claim_id = NEW.claim_id
             AND l.spatial_entity_id = NEW.spatial_entity_id
       ) THEN
        RAISE EXCEPTION
            'same_as_locus inference extent requires the same spatial entity to be an evidence locus';
    END IF;
    RETURN NEW;
END;
$$;

DROP TRIGGER IF EXISTS claim_inference_same_as_locus_check
    ON atlas.claim_inference_extent;
CREATE TRIGGER claim_inference_same_as_locus_check
BEFORE INSERT OR UPDATE ON atlas.claim_inference_extent
FOR EACH ROW EXECUTE FUNCTION atlas.enforce_same_as_locus_inference();

CREATE OR REPLACE FUNCTION atlas.claim_applies_at_year(
    p_claim_id uuid,
    p_year integer
)
RETURNS boolean
LANGUAGE sql
STABLE
SET search_path = ''
AS $$
    SELECT EXISTS (
        SELECT 1
        FROM atlas.claim c
        JOIN atlas.claim_asserted_interval i ON i.claim_id = c.claim_id
        WHERE c.claim_id = p_claim_id
          AND c.semantic_model_version = 'post_m1_v2'
          AND c.temporal_applicability_mode <> 'unknown'
          AND i.valid_years @> p_year
    );
$$;

COMMENT ON FUNCTION atlas.claim_applies_at_year(uuid, integer) IS
'Experimental M2 selected-year truth predicate. It intentionally ignores the outer claim.valid_years envelope and returns true only for explicit asserted intervals.';

CREATE OR REPLACE FUNCTION atlas.validate_post_m1_claim_parent_state()
RETURNS trigger
LANGUAGE plpgsql
SET search_path = ''
AS $
BEGIN
    IF NEW.semantic_model_version IS NULL THEN
        IF EXISTS (
            SELECT 1
            FROM atlas.territorial_practice_claim t
            WHERE t.claim_id = NEW.claim_id
              AND (
                  t.assertion_form IS NOT NULL
                  OR t.attestation_pattern IS NOT NULL
                  OR t.interpretive_basis IS NOT NULL
                  OR t.occurrence_pattern IS NOT NULL
                  OR t.institutionalization IS NOT NULL
                  OR t.prevalence_scope IS NOT NULL
                  OR t.structural_significance IS NOT NULL
                  OR t.research_stage IS NOT NULL
                  OR t.classification_outcome IS NOT NULL
              )
        ) THEN
            RAISE EXCEPTION
                'legacy/null semantic model cannot retain post-M1 territorial dimensions for claim %',
                NEW.claim_id;
        END IF;

        IF EXISTS (
            SELECT 1
            FROM atlas.claim_asserted_interval i
            WHERE i.claim_id = NEW.claim_id
        ) THEN
            RAISE EXCEPTION
                'legacy/null semantic model cannot retain post-M1 asserted intervals for claim %',
                NEW.claim_id;
        END IF;
    ELSIF NEW.semantic_model_version = 'post_m1_v2' THEN
        IF EXISTS (
            SELECT 1
            FROM atlas.territorial_practice_claim t
            WHERE t.claim_id = NEW.claim_id
              AND (
                  t.assertion_form IS NULL
                  OR t.attestation_pattern IS NULL
                  OR t.interpretive_basis IS NULL
                  OR t.occurrence_pattern IS NULL
                  OR t.institutionalization IS NULL
                  OR t.prevalence_scope IS NULL
                  OR t.structural_significance IS NULL
                  OR t.research_stage IS NULL
                  OR t.classification_outcome IS NULL
              )
        ) THEN
            RAISE EXCEPTION
                'post-M1 parent claim % has an incomplete territorial semantic subtype',
                NEW.claim_id;
        END IF;

        IF EXISTS (
            SELECT 1
            FROM atlas.claim_asserted_interval i
            WHERE i.claim_id = NEW.claim_id
              AND (
                  (NEW.from_year IS NOT NULL AND i.from_year < NEW.from_year)
                  OR
                  (NEW.to_year IS NOT NULL AND i.to_year > NEW.to_year)
              )
        ) THEN
            RAISE EXCEPTION
                'claim % outer query window no longer contains all asserted intervals',
                NEW.claim_id;
        END IF;
    END IF;

    RETURN NULL;
END;
$;

DROP TRIGGER IF EXISTS claim_post_m1_parent_consistency ON atlas.claim;
CREATE CONSTRAINT TRIGGER claim_post_m1_parent_consistency
AFTER INSERT OR UPDATE ON atlas.claim
DEFERRABLE INITIALLY DEFERRED
FOR EACH ROW EXECUTE FUNCTION atlas.validate_post_m1_claim_parent_state();

CREATE OR REPLACE FUNCTION atlas.validate_evidence_locus_dependents()
RETURNS trigger
LANGUAGE plpgsql
SET search_path = ''
AS $
BEGIN
    IF EXISTS (
        SELECT 1
        FROM atlas.claim_inference_extent e
        WHERE e.claim_id = OLD.claim_id
          AND e.spatial_entity_id = OLD.spatial_entity_id
          AND e.generalization_basis = 'same_as_locus'
    )
    AND NOT EXISTS (
        SELECT 1
        FROM atlas.claim_evidence_locus l
        WHERE l.claim_id = OLD.claim_id
          AND l.spatial_entity_id = OLD.spatial_entity_id
    ) THEN
        RAISE EXCEPTION
            'same_as_locus inference extent requires retained matching evidence locus for claim % spatial entity %',
            OLD.claim_id,
            OLD.spatial_entity_id;
    END IF;

    RETURN NULL;
END;
$;

DROP TRIGGER IF EXISTS claim_evidence_locus_inverse_consistency
    ON atlas.claim_evidence_locus;
CREATE CONSTRAINT TRIGGER claim_evidence_locus_inverse_consistency
AFTER DELETE OR UPDATE ON atlas.claim_evidence_locus
DEFERRABLE INITIALLY DEFERRED
FOR EACH ROW EXECUTE FUNCTION atlas.validate_evidence_locus_dependents();

REVOKE EXECUTE ON FUNCTION atlas.enforce_post_m1_territorial_semantics() FROM PUBLIC;
REVOKE EXECUTE ON FUNCTION atlas.enforce_asserted_interval_within_query_window() FROM PUBLIC;
REVOKE EXECUTE ON FUNCTION atlas.enforce_same_as_locus_inference() FROM PUBLIC;
REVOKE EXECUTE ON FUNCTION atlas.validate_post_m1_claim_parent_state() FROM PUBLIC;
REVOKE EXECUTE ON FUNCTION atlas.validate_evidence_locus_dependents() FROM PUBLIC;
REVOKE EXECUTE ON FUNCTION atlas.claim_applies_at_year(uuid, integer) FROM PUBLIC;
