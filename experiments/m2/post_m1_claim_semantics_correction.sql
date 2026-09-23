-- M2 #135 correction: close reverse-direction/cross-table gaps in #120.
-- Additive disposable layer; NOT a production migration.

ALTER TABLE atlas.claim_asserted_interval
    ALTER COLUMN from_year DROP NOT NULL,
    ALTER COLUMN to_year DROP NOT NULL;

ALTER TABLE atlas.claim_asserted_interval
    DROP CONSTRAINT IF EXISTS claim_asserted_interval_has_bound,
    ADD CONSTRAINT claim_asserted_interval_has_bound CHECK (
        from_year IS NOT NULL OR to_year IS NOT NULL
    );

-- Replace the row guard with mode-aware/open-terminus validation.
CREATE OR REPLACE FUNCTION atlas.enforce_asserted_interval_within_query_window()
RETURNS trigger
LANGUAGE plpgsql
SET search_path = ''
AS $$
DECLARE
    outer_from integer;
    outer_to integer;
    model_version text;
    applicability_mode text;
BEGIN
    SELECT from_year, to_year, semantic_model_version, temporal_applicability_mode
      INTO outer_from, outer_to, model_version, applicability_mode
    FROM atlas.claim
    WHERE claim_id = NEW.claim_id;

    IF model_version IS DISTINCT FROM 'post_m1_v2' THEN
        RAISE EXCEPTION
            'asserted intervals are post-M1 semantics and require claim semantic_model_version=post_m1_v2';
    END IF;

    IF applicability_mode = 'unknown' THEN
        RAISE EXCEPTION 'unknown applicability cannot carry a positive asserted interval';
    END IF;

    IF applicability_mode = 'alternative_dates' AND NEW.interval_role <> 'alternative' THEN
        RAISE EXCEPTION 'alternative_dates requires interval_role=alternative';
    ELSIF applicability_mode <> 'alternative_dates' AND NEW.interval_role = 'alternative' THEN
        RAISE EXCEPTION 'alternative interval role requires alternative_dates mode';
    END IF;

    IF applicability_mode = 'terminus_after' THEN
        IF NEW.from_year IS NULL OR NEW.to_year IS NOT NULL THEN
            RAISE EXCEPTION 'terminus_after requires one asserted interval with lower bound and open upper bound';
        END IF;
    ELSIF applicability_mode = 'terminus_before' THEN
        IF NEW.from_year IS NOT NULL OR NEW.to_year IS NULL THEN
            RAISE EXCEPTION 'terminus_before requires one asserted interval with open lower bound and upper bound';
        END IF;
    ELSE
        IF NEW.from_year IS NULL OR NEW.to_year IS NULL THEN
            RAISE EXCEPTION 'applicability mode % requires bounded asserted intervals', applicability_mode;
        END IF;
    END IF;

    IF outer_from IS NOT NULL THEN
        IF NEW.from_year IS NULL OR NEW.from_year < outer_from THEN
            RAISE EXCEPTION 'asserted interval starts before claim outer query window';
        END IF;
    END IF;

    IF outer_to IS NOT NULL THEN
        IF NEW.to_year IS NULL OR NEW.to_year > outer_to THEN
            RAISE EXCEPTION 'asserted interval ends after claim outer query window';
        END IF;
    END IF;

    RETURN NEW;
END;
$$;

-- New target-only child structures require explicit post-M1 opt-in.
CREATE OR REPLACE FUNCTION atlas.require_post_m1_child_semantics()
RETURNS trigger
LANGUAGE plpgsql
SET search_path = ''
AS $$
DECLARE
    v_claim_id uuid;
    v_model text;
BEGIN
    v_claim_id := CASE WHEN TG_OP = 'DELETE' THEN OLD.claim_id ELSE NEW.claim_id END;

    SELECT semantic_model_version INTO v_model
    FROM atlas.claim
    WHERE claim_id = v_claim_id;

    IF v_model IS DISTINCT FROM 'post_m1_v2' THEN
        RAISE EXCEPTION
            'post-M1 child semantics require claim semantic_model_version=post_m1_v2';
    END IF;

    RETURN CASE WHEN TG_OP = 'DELETE' THEN OLD ELSE NEW END;
END;
$$;

DROP TRIGGER IF EXISTS claim_evidence_locus_post_m1_guard ON atlas.claim_evidence_locus;
CREATE TRIGGER claim_evidence_locus_post_m1_guard
BEFORE INSERT OR UPDATE ON atlas.claim_evidence_locus
FOR EACH ROW EXECUTE FUNCTION atlas.require_post_m1_child_semantics();

DROP TRIGGER IF EXISTS claim_inference_extent_post_m1_guard ON atlas.claim_inference_extent;
CREATE TRIGGER claim_inference_extent_post_m1_guard
BEFORE INSERT OR UPDATE ON atlas.claim_inference_extent
FOR EACH ROW EXECUTE FUNCTION atlas.require_post_m1_child_semantics();

DROP TRIGGER IF EXISTS practice_facet_post_m1_guard ON atlas.practice_facet_assertion;
CREATE TRIGGER practice_facet_post_m1_guard
BEFORE INSERT OR UPDATE ON atlas.practice_facet_assertion
FOR EACH ROW EXECUTE FUNCTION atlas.require_post_m1_child_semantics();

-- One canonical cross-table validator. It is called by deferred triggers from
-- every relation that can invalidate an already-valid post-M1 package.
CREATE OR REPLACE FUNCTION atlas.validate_post_m1_claim_integrity(p_claim_id uuid)
RETURNS void
LANGUAGE plpgsql
SET search_path = ''
AS $$
DECLARE
    c record;
    t record;
    interval_count integer;
    locus_count integer;
    extent_count integer;
    facet_count integer;
    invalid_count integer;
BEGIN
    SELECT
        claim_kind_code, semantic_model_version, temporal_applicability_mode,
        from_year, to_year
    INTO c
    FROM atlas.claim
    WHERE claim_id = p_claim_id;

    IF NOT FOUND THEN
        RETURN;
    END IF;

    SELECT count(*) INTO interval_count
    FROM atlas.claim_asserted_interval
    WHERE claim_id = p_claim_id;

    SELECT count(*) INTO locus_count
    FROM atlas.claim_evidence_locus
    WHERE claim_id = p_claim_id;

    SELECT count(*) INTO extent_count
    FROM atlas.claim_inference_extent
    WHERE claim_id = p_claim_id;

    SELECT count(*) INTO facet_count
    FROM atlas.practice_facet_assertion
    WHERE claim_id = p_claim_id;

    IF c.claim_kind_code = 'territorial_practice' THEN
        SELECT
            assertion_form, attestation_pattern, interpretive_basis,
            occurrence_pattern, institutionalization, prevalence_scope,
            structural_significance, research_stage, classification_outcome
        INTO t
        FROM atlas.territorial_practice_claim
        WHERE claim_id = p_claim_id;
    END IF;

    IF c.semantic_model_version IS NULL THEN
        IF interval_count > 0 OR locus_count > 0 OR extent_count > 0 OR facet_count > 0 THEN
            RAISE EXCEPTION
                'legacy/null semantic-model claim % cannot retain post-M1 child semantics',
                p_claim_id;
        END IF;

        IF c.claim_kind_code = 'territorial_practice' AND FOUND AND (
            t.assertion_form IS NOT NULL
            OR t.attestation_pattern IS NOT NULL
            OR t.interpretive_basis IS NOT NULL
            OR t.occurrence_pattern IS NOT NULL
            OR t.institutionalization IS NOT NULL
            OR t.prevalence_scope IS NOT NULL
            OR t.structural_significance IS NOT NULL
            OR t.research_stage IS NOT NULL
            OR t.classification_outcome IS NOT NULL
        ) THEN
            RAISE EXCEPTION
                'legacy/null semantic-model territorial claim % cannot retain post-M1 dimensions',
                p_claim_id;
        END IF;
        RETURN;
    END IF;

    IF c.semantic_model_version <> 'post_m1_v2' THEN
        RAISE EXCEPTION 'unsupported semantic model version %', c.semantic_model_version;
    END IF;

    IF c.claim_kind_code = 'territorial_practice' THEN
        IF NOT FOUND THEN
            RAISE EXCEPTION 'post-M1 territorial claim % has no territorial subtype', p_claim_id;
        END IF;

        IF t.assertion_form IS NULL
           OR t.attestation_pattern IS NULL
           OR t.interpretive_basis IS NULL
           OR t.occurrence_pattern IS NULL
           OR t.institutionalization IS NULL
           OR t.prevalence_scope IS NULL
           OR t.structural_significance IS NULL
           OR t.research_stage IS NULL
           OR t.classification_outcome IS NULL THEN
            RAISE EXCEPTION
                'post-M1 territorial claim % must state every target dimension explicitly',
                p_claim_id;
        END IF;
    END IF;

    -- Every post-M1 interval must still fit the current query envelope.
    SELECT count(*) INTO invalid_count
    FROM atlas.claim_asserted_interval i
    WHERE i.claim_id = p_claim_id
      AND (
          (c.from_year IS NOT NULL AND (i.from_year IS NULL OR i.from_year < c.from_year))
          OR
          (c.to_year IS NOT NULL AND (i.to_year IS NULL OR i.to_year > c.to_year))
      );
    IF invalid_count > 0 THEN
        RAISE EXCEPTION
            'claim % has asserted intervals outside its current outer query window',
            p_claim_id;
    END IF;

    CASE c.temporal_applicability_mode
        WHEN 'unknown' THEN
            IF interval_count <> 0 THEN
                RAISE EXCEPTION 'unknown applicability claim % cannot carry positive intervals', p_claim_id;
            END IF;

        WHEN 'continuous_interval', 'bounded_occurrence' THEN
            IF interval_count = 0 THEN
                RAISE EXCEPTION
                    'positive applicability mode % requires at least one asserted interval for claim %',
                    c.temporal_applicability_mode, p_claim_id;
            END IF;
            SELECT count(*) INTO invalid_count
            FROM atlas.claim_asserted_interval i
            WHERE i.claim_id=p_claim_id
              AND (i.interval_role <> 'asserted' OR i.from_year IS NULL OR i.to_year IS NULL);
            IF invalid_count > 0 THEN
                RAISE EXCEPTION
                    'mode % requires bounded asserted intervals for claim %',
                    c.temporal_applicability_mode, p_claim_id;
            END IF;

        WHEN 'alternative_dates' THEN
            IF interval_count = 0 THEN
                RAISE EXCEPTION 'alternative_dates requires at least one alternative interval for claim %', p_claim_id;
            END IF;
            SELECT count(*) INTO invalid_count
            FROM atlas.claim_asserted_interval i
            WHERE i.claim_id=p_claim_id
              AND (i.interval_role <> 'alternative' OR i.from_year IS NULL OR i.to_year IS NULL);
            IF invalid_count > 0 THEN
                RAISE EXCEPTION
                    'alternative_dates requires bounded alternative intervals for claim %',
                    p_claim_id;
            END IF;

        WHEN 'terminus_after' THEN
            IF interval_count <> 1 OR c.to_year IS NOT NULL THEN
                RAISE EXCEPTION
                    'terminus_after claim % requires one open-upper interval and open outer upper bound',
                    p_claim_id;
            END IF;
            SELECT count(*) INTO invalid_count
            FROM atlas.claim_asserted_interval i
            WHERE i.claim_id=p_claim_id
              AND (i.interval_role <> 'asserted' OR i.from_year IS NULL OR i.to_year IS NOT NULL);
            IF invalid_count <> 0 THEN
                RAISE EXCEPTION 'terminus_after interval shape invalid for claim %', p_claim_id;
            END IF;

        WHEN 'terminus_before' THEN
            IF interval_count <> 1 OR c.from_year IS NOT NULL THEN
                RAISE EXCEPTION
                    'terminus_before claim % requires one open-lower interval and open outer lower bound',
                    p_claim_id;
            END IF;
            SELECT count(*) INTO invalid_count
            FROM atlas.claim_asserted_interval i
            WHERE i.claim_id=p_claim_id
              AND (i.interval_role <> 'asserted' OR i.from_year IS NOT NULL OR i.to_year IS NULL);
            IF invalid_count <> 0 THEN
                RAISE EXCEPTION 'terminus_before interval shape invalid for claim %', p_claim_id;
            END IF;

        ELSE
            RAISE EXCEPTION
                'post-M1 claim % has missing/unsupported temporal applicability mode %',
                p_claim_id, c.temporal_applicability_mode;
    END CASE;

    -- Reverse-direction spatial integrity: changing/deleting a locus must not
    -- strand a same_as_locus inference extent.
    SELECT count(*) INTO invalid_count
    FROM atlas.claim_inference_extent e
    WHERE e.claim_id=p_claim_id
      AND (
        (
          e.generalization_basis='same_as_locus'
          AND NOT EXISTS (
              SELECT 1
              FROM atlas.claim_evidence_locus l
              WHERE l.claim_id=e.claim_id
                AND l.spatial_entity_id=e.spatial_entity_id
          )
        )
        OR
        (
          e.generalization_basis<>'same_as_locus'
          AND EXISTS (
              SELECT 1
              FROM atlas.claim_evidence_locus l
              WHERE l.claim_id=e.claim_id
                AND l.spatial_entity_id=e.spatial_entity_id
          )
        )
      );
    IF invalid_count > 0 THEN
        RAISE EXCEPTION 'claim % has inconsistent evidence-locus/inference-extent semantics', p_claim_id;
    END IF;
END;
$$;

CREATE OR REPLACE FUNCTION atlas.check_post_m1_claim_integrity()
RETURNS trigger
LANGUAGE plpgsql
SET search_path = ''
AS $$
DECLARE
    v_claim_id uuid;
BEGIN
    v_claim_id := CASE WHEN TG_OP='DELETE' THEN OLD.claim_id ELSE NEW.claim_id END;
    PERFORM atlas.validate_post_m1_claim_integrity(v_claim_id);
    RETURN NULL;
END;
$$;

DROP TRIGGER IF EXISTS post_m1_claim_integrity_from_claim ON atlas.claim;
CREATE CONSTRAINT TRIGGER post_m1_claim_integrity_from_claim
AFTER INSERT OR UPDATE ON atlas.claim
DEFERRABLE INITIALLY DEFERRED
FOR EACH ROW EXECUTE FUNCTION atlas.check_post_m1_claim_integrity();

DROP TRIGGER IF EXISTS post_m1_claim_integrity_from_territorial ON atlas.territorial_practice_claim;
CREATE CONSTRAINT TRIGGER post_m1_claim_integrity_from_territorial
AFTER INSERT OR UPDATE OR DELETE ON atlas.territorial_practice_claim
DEFERRABLE INITIALLY DEFERRED
FOR EACH ROW EXECUTE FUNCTION atlas.check_post_m1_claim_integrity();

DROP TRIGGER IF EXISTS post_m1_claim_integrity_from_interval ON atlas.claim_asserted_interval;
CREATE CONSTRAINT TRIGGER post_m1_claim_integrity_from_interval
AFTER INSERT OR UPDATE OR DELETE ON atlas.claim_asserted_interval
DEFERRABLE INITIALLY DEFERRED
FOR EACH ROW EXECUTE FUNCTION atlas.check_post_m1_claim_integrity();

DROP TRIGGER IF EXISTS post_m1_claim_integrity_from_locus ON atlas.claim_evidence_locus;
CREATE CONSTRAINT TRIGGER post_m1_claim_integrity_from_locus
AFTER INSERT OR UPDATE OR DELETE ON atlas.claim_evidence_locus
DEFERRABLE INITIALLY DEFERRED
FOR EACH ROW EXECUTE FUNCTION atlas.check_post_m1_claim_integrity();

DROP TRIGGER IF EXISTS post_m1_claim_integrity_from_extent ON atlas.claim_inference_extent;
CREATE CONSTRAINT TRIGGER post_m1_claim_integrity_from_extent
AFTER INSERT OR UPDATE OR DELETE ON atlas.claim_inference_extent
DEFERRABLE INITIALLY DEFERRED
FOR EACH ROW EXECUTE FUNCTION atlas.check_post_m1_claim_integrity();

DROP TRIGGER IF EXISTS post_m1_claim_integrity_from_facet ON atlas.practice_facet_assertion;
CREATE CONSTRAINT TRIGGER post_m1_claim_integrity_from_facet
AFTER INSERT OR UPDATE OR DELETE ON atlas.practice_facet_assertion
DEFERRABLE INITIALLY DEFERRED
FOR EACH ROW EXECUTE FUNCTION atlas.check_post_m1_claim_integrity();

COMMENT ON FUNCTION atlas.validate_post_m1_claim_integrity(uuid) IS
'M2 #135 cross-table integrity for the post-M1 prototype. Validates semantic-model opt-in, complete territorial dimensions, temporal interval/mode/query-window coherence, open termini and reverse spatial locus/extent consistency.';

REVOKE EXECUTE ON FUNCTION atlas.require_post_m1_child_semantics() FROM PUBLIC;
REVOKE EXECUTE ON FUNCTION atlas.validate_post_m1_claim_integrity(uuid) FROM PUBLIC;
REVOKE EXECUTE ON FUNCTION atlas.check_post_m1_claim_integrity() FROM PUBLIC;
