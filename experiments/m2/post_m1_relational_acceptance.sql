-- M2 #120 acceptance fixture for disposable post-M1 relational semantics.
-- All fixture data is rollback-only. The prototype DDL remains only in this
-- disposable database so downstream foundation tests can detect interference.

BEGIN;

-- Spatial identities used only by this rollback fixture.
INSERT INTO atlas.spatial_entity(
    spatial_entity_id, entity_type_code, canonical_name, review_status
) VALUES
('00000000-0000-0000-0000-000000012001'::uuid, 'polity', 'Legacy compatibility polity', 'reviewed'),
('00000000-0000-0000-0000-000000012002'::uuid, 'polity', 'Hittite central Anatolia', 'reviewed'),
('00000000-0000-0000-0000-000000012003'::uuid, 'polity', 'Baekje', 'reviewed'),
('00000000-0000-0000-0000-000000012004'::uuid, 'region', 'Silla Village Register villages (Sowon-gyong area)', 'reviewed'),
('00000000-0000-0000-0000-000000012005'::uuid, 'polity', 'Unified Silla broader polity negative control', 'reviewed'),
('00000000-0000-0000-0000-000000012006'::uuid, 'site', 'Synthetic inconclusive site', 'reviewed');

-- Legacy row: P-level remains valid while every post-M1 field stays NULL.
INSERT INTO atlas.claim(
    claim_id, claim_kind_code, from_year, to_year, summary,
    review_status, publication_status
) VALUES (
    '00000000-0000-0000-0000-000000012101'::uuid,
    'territorial_practice',
    100,
    200,
    'Legacy compatibility control: prototype must not rewrite old semantics.',
    'reviewed',
    'unpublished'
);

INSERT INTO atlas.territorial_practice_claim(
    claim_id, spatial_entity_id, practice_type_code,
    practice_level, coverage_state_code, classification_status
) VALUES (
    '00000000-0000-0000-0000-000000012101'::uuid,
    '00000000-0000-0000-0000-000000012001'::uuid,
    'slavery_enslavement',
    'P2',
    'classified',
    'legacy_fixture'
);

-- Hittite real-case fixture: recurrent + institutional can coexist while
-- prevalence and structural significance remain explicitly unassessed.
INSERT INTO atlas.claim(
    claim_id, claim_kind_code, from_year, to_year,
    date_text_original, temporal_applicability_mode, temporal_precision,
    spatial_precision, summary, review_status, publication_status
) VALUES (
    '00000000-0000-0000-0000-000000012102'::uuid,
    'territorial_practice',
    -1399,
    -1199,
    '1400-1200 BCE',
    'continuous_interval',
    'broad_range',
    'polity',
    'Hittite M1 relational representability fixture.',
    'reviewed',
    'unpublished'
);

INSERT INTO atlas.territorial_practice_claim(
    claim_id, spatial_entity_id, practice_type_code,
    practice_level, coverage_state_code, classification_status,
    assertion_form, attestation_pattern, interpretive_basis,
    occurrence_pattern, institutionalization, prevalence_scope,
    structural_significance, research_stage, classification_outcome
) VALUES (
    '00000000-0000-0000-0000-000000012102'::uuid,
    '00000000-0000-0000-0000-000000012002'::uuid,
    'slavery_enslavement',
    'P2',
    'classified',
    'reviewed',
    'practice_or_status',
    'recurrent_attestation',
    'mixed_primary_and_specialist',
    'recurrent',
    'institutional_features_supported',
    'unassessed',
    'unassessed',
    'review_complete',
    'classified'
);

INSERT INTO atlas.claim_asserted_interval(
    claim_id, from_year, to_year, interval_role
) VALUES (
    '00000000-0000-0000-0000-000000012102'::uuid,
    -1399,
    -1199,
    'asserted_applicability'
);

INSERT INTO atlas.practice_facet_assertion(
    claim_id, facet_dimension, concept_code
) VALUES
('00000000-0000-0000-0000-000000012102'::uuid, 'status', 'enslaved_status'),
('00000000-0000-0000-0000-000000012102'::uuid, 'property_legal', 'pricing_property_rules'),
('00000000-0000-0000-0000-000000012102'::uuid, 'function', 'herding_labour'),
('00000000-0000-0000-0000-000000012102'::uuid, 'transmission', 'status_flexibility');

INSERT INTO atlas.claim_evidence_locus(claim_id, spatial_entity_id, role_text)
VALUES (
    '00000000-0000-0000-0000-000000012102'::uuid,
    '00000000-0000-0000-0000-000000012002'::uuid,
    'reviewed polity-level legal/social evidence package'
);

INSERT INTO atlas.claim_inference_extent(
    claim_id, spatial_entity_id, generalization_basis
) VALUES (
    '00000000-0000-0000-0000-000000012102'::uuid,
    '00000000-0000-0000-0000-000000012002'::uuid,
    'same_as_locus'
);

-- Baekje 369 real-case fixture: a bounded captive/enslavement event remains
-- an event/process and does not acquire institution/prevalence claims.
INSERT INTO atlas.claim(
    claim_id, claim_kind_code, from_year, to_year,
    date_text_original, temporal_applicability_mode, temporal_precision,
    spatial_precision, summary, review_status, publication_status
) VALUES (
    '00000000-0000-0000-0000-000000012103'::uuid,
    'territorial_practice',
    369,
    369,
    'King Geunchogo year 24, ninth month (369 CE)',
    'bounded_occurrence',
    'exact',
    'polity_event',
    'Baekje 369 M1 relational representability fixture.',
    'reviewed',
    'unpublished'
);

INSERT INTO atlas.territorial_practice_claim(
    claim_id, spatial_entity_id, practice_type_code,
    practice_level, coverage_state_code, classification_status,
    assertion_form, attestation_pattern, interpretive_basis,
    occurrence_pattern, institutionalization, prevalence_scope,
    structural_significance, research_stage, classification_outcome
) VALUES (
    '00000000-0000-0000-0000-000000012103'::uuid,
    '00000000-0000-0000-0000-000000012003'::uuid,
    'slavery_enslavement',
    'P1',
    'classified',
    'reviewed',
    'event_or_process',
    'single_bounded_attestation',
    'mixed_primary_and_specialist',
    'bounded_occurrence',
    'unassessed',
    'unassessed',
    'unassessed',
    'review_complete',
    'classified'
);

INSERT INTO atlas.claim_asserted_interval(
    claim_id, from_year, to_year, interval_role
) VALUES (
    '00000000-0000-0000-0000-000000012103'::uuid,
    369,
    369,
    'asserted_applicability'
);

INSERT INTO atlas.practice_facet_assertion(
    claim_id, facet_dimension, concept_code
) VALUES
('00000000-0000-0000-0000-000000012103'::uuid, 'process', 'captive_taking'),
('00000000-0000-0000-0000-000000012103'::uuid, 'process', 'enslavement_distribution');

INSERT INTO atlas.claim_evidence_locus(claim_id, spatial_entity_id)
VALUES (
    '00000000-0000-0000-0000-000000012103'::uuid,
    '00000000-0000-0000-0000-000000012003'::uuid
);
INSERT INTO atlas.claim_inference_extent(
    claim_id, spatial_entity_id, generalization_basis
) VALUES (
    '00000000-0000-0000-0000-000000012103'::uuid,
    '00000000-0000-0000-0000-000000012003'::uuid,
    'same_as_locus'
);

-- Silla real-case fixture: the legacy row can gain reviewed temporal/spatial
-- semantics without inventing post-M1 historical-characterization values that
-- were not part of the accepted M1 semantic fixture.
INSERT INTO atlas.claim(
    claim_id, claim_kind_code, from_year, to_year,
    date_text_original, temporal_applicability_mode, temporal_precision,
    temporal_certainty, spatial_precision, summary,
    review_status, publication_status
) VALUES (
    '00000000-0000-0000-0000-000000012104'::uuid,
    'territorial_practice',
    695,
    819,
    'Silla Village Register; proposed dates include 695, 755, 815, and 818-819 CE',
    'alternative_dates',
    'disputed_alternatives',
    'disputed',
    'four_village_register',
    'Silla Village Register M1 temporal/spatial representability fixture.',
    'reviewed',
    'unpublished'
);

INSERT INTO atlas.territorial_practice_claim(
    claim_id, spatial_entity_id, practice_type_code,
    practice_level, coverage_state_code, classification_status
) VALUES (
    '00000000-0000-0000-0000-000000012104'::uuid,
    '00000000-0000-0000-0000-000000012004'::uuid,
    'slavery_enslavement',
    'P2',
    'classified',
    'reviewed_with_date_dispute'
);

INSERT INTO atlas.claim_asserted_interval(
    claim_id, from_year, to_year, interval_role
) VALUES
('00000000-0000-0000-0000-000000012104'::uuid, 695, 695, 'alternative'),
('00000000-0000-0000-0000-000000012104'::uuid, 755, 755, 'alternative'),
('00000000-0000-0000-0000-000000012104'::uuid, 815, 815, 'alternative'),
('00000000-0000-0000-0000-000000012104'::uuid, 818, 819, 'alternative');

INSERT INTO atlas.claim_evidence_locus(
    claim_id, spatial_entity_id, role_text
) VALUES (
    '00000000-0000-0000-0000-000000012104'::uuid,
    '00000000-0000-0000-0000-000000012004'::uuid,
    'four village-register communities; exact village locations unresolved'
);

INSERT INTO atlas.claim_inference_extent(
    claim_id, spatial_entity_id, generalization_basis
) VALUES (
    '00000000-0000-0000-0000-000000012104'::uuid,
    '00000000-0000-0000-0000-000000012004'::uuid,
    'same_as_locus'
);

-- Reviewed inconclusive control: explicit post-M1 dimensions do not create P0.
INSERT INTO atlas.claim(
    claim_id, claim_kind_code, from_year, to_year,
    temporal_applicability_mode, temporal_precision,
    summary, review_status, publication_status
) VALUES (
    '00000000-0000-0000-0000-000000012105'::uuid,
    'territorial_practice',
    500,
    500,
    'unknown',
    'unknown',
    'Reviewed inconclusive control; no positive applicability is asserted.',
    'reviewed',
    'unpublished'
);

INSERT INTO atlas.territorial_practice_claim(
    claim_id, spatial_entity_id, practice_type_code,
    practice_level, coverage_state_code, classification_status,
    assertion_form, attestation_pattern, interpretive_basis,
    occurrence_pattern, institutionalization, prevalence_scope,
    structural_significance, research_stage, classification_outcome
) VALUES (
    '00000000-0000-0000-0000-000000012105'::uuid,
    '00000000-0000-0000-0000-000000012006'::uuid,
    'slavery_enslavement',
    NULL,
    'researched_inconclusive',
    'reviewed_inconclusive',
    'practice_or_status',
    'unassessed',
    'unassessed',
    'unassessed',
    'unassessed',
    'unassessed',
    'unassessed',
    'review_complete',
    'inconclusive'
);

-- Force deferred semantic/spatial checks now so the positive fixture is proven
-- internally valid before negative controls start.
SET CONSTRAINTS ALL IMMEDIATE;
SET CONSTRAINTS ALL DEFERRED;

DO $$
DECLARE
    v_blocked boolean;
BEGIN
    -- Legacy P-level survives; post-M1 dimensions were not backfilled.
    IF (SELECT practice_level
          FROM atlas.territorial_practice_claim
         WHERE claim_id='00000000-0000-0000-0000-000000012101'::uuid) <> 'P2' THEN
        RAISE EXCEPTION 'legacy practice level changed';
    END IF;
    IF EXISTS (
        SELECT 1
          FROM atlas.territorial_practice_claim
         WHERE claim_id='00000000-0000-0000-0000-000000012101'::uuid
           AND (
               assertion_form IS NOT NULL
               OR attestation_pattern IS NOT NULL
               OR interpretive_basis IS NOT NULL
               OR occurrence_pattern IS NOT NULL
               OR institutionalization IS NOT NULL
               OR prevalence_scope IS NOT NULL
               OR structural_significance IS NOT NULL
               OR research_stage IS NOT NULL
               OR classification_outcome IS NOT NULL
           )
    ) THEN
        RAISE EXCEPTION 'legacy row was silently backfilled with post-M1 semantics';
    END IF;

    -- Hittite: broad precision does not interfere with explicitly reviewed
    -- continuous applicability.
    IF NOT atlas.post_m1_claim_active_at(
        '00000000-0000-0000-0000-000000012102'::uuid, -1300
    ) THEN
        RAISE EXCEPTION 'Hittite continuous-period midpoint is not active';
    END IF;
    IF atlas.post_m1_claim_active_at(
        '00000000-0000-0000-0000-000000012102'::uuid, -1400
    ) THEN
        RAISE EXCEPTION 'Hittite year outside asserted interval became active';
    END IF;

    -- Baekje remains one bounded event.
    IF NOT atlas.post_m1_claim_active_at(
        '00000000-0000-0000-0000-000000012103'::uuid, 369
    ) OR atlas.post_m1_claim_active_at(
        '00000000-0000-0000-0000-000000012103'::uuid, 370
    ) THEN
        RAISE EXCEPTION 'Baekje bounded-event applicability drifted';
    END IF;

    -- Silla proves query-window membership is not positive selected-year truth.
    IF NOT (
        SELECT valid_years @> 700
          FROM atlas.claim
         WHERE claim_id='00000000-0000-0000-0000-000000012104'::uuid
    ) THEN
        RAISE EXCEPTION 'Silla negative probe is not inside outer query window';
    END IF;
    IF atlas.post_m1_claim_active_at(
        '00000000-0000-0000-0000-000000012104'::uuid, 700
    ) THEN
        RAISE EXCEPTION 'Silla uncertainty envelope became continuous presence';
    END IF;
    IF NOT atlas.post_m1_claim_active_at(
        '00000000-0000-0000-0000-000000012104'::uuid, 695
    ) OR NOT atlas.post_m1_claim_active_at(
        '00000000-0000-0000-0000-000000012104'::uuid, 755
    ) OR NOT atlas.post_m1_claim_active_at(
        '00000000-0000-0000-0000-000000012104'::uuid, 815
    ) OR NOT atlas.post_m1_claim_active_at(
        '00000000-0000-0000-0000-000000012104'::uuid, 818
    ) OR NOT atlas.post_m1_claim_active_at(
        '00000000-0000-0000-0000-000000012104'::uuid, 819
    ) THEN
        RAISE EXCEPTION 'Silla asserted alternative dates are not active';
    END IF;

    -- Inconclusive is not P0 and unknown applicability produces no positive year.
    IF (SELECT practice_level IS NOT NULL
          FROM atlas.territorial_practice_claim
         WHERE claim_id='00000000-0000-0000-0000-000000012105'::uuid) THEN
        RAISE EXCEPTION 'inconclusive post-M1 claim acquired a legacy P-level';
    END IF;
    IF atlas.post_m1_claim_active_at(
        '00000000-0000-0000-0000-000000012105'::uuid, 500
    ) THEN
        RAISE EXCEPTION 'unknown applicability produced positive selected-year truth';
    END IF;

    -- Simultaneous facets survive without one exclusive taxonomy.
    IF (SELECT count(*)
          FROM atlas.practice_facet_assertion
         WHERE claim_id='00000000-0000-0000-0000-000000012102'::uuid) <> 4 THEN
        RAISE EXCEPTION 'Hittite simultaneous facet set not representable';
    END IF;

    -- Silla spatial truth remains bounded to the register communities and no
    -- whole-Silla inference row is manufactured from geometry/containment.
    IF EXISTS (
        SELECT 1
          FROM atlas.claim_inference_extent
         WHERE claim_id='00000000-0000-0000-0000-000000012104'::uuid
           AND spatial_entity_id='00000000-0000-0000-0000-000000012005'::uuid
    ) THEN
        RAISE EXCEPTION 'Silla claim was generalized to whole polity';
    END IF;

    -- Publication contract is unchanged: prototype columns/tables are not
    -- automatically exposed through the existing publish views.
    IF EXISTS (
        SELECT 1 FROM information_schema.columns
        WHERE table_schema='publish'
          AND table_name='claim'
          AND column_name='temporal_applicability_mode'
    ) THEN
        RAISE EXCEPTION 'publish.claim silently switched to prototype temporal semantics';
    END IF;
    IF EXISTS (
        SELECT 1 FROM information_schema.columns
        WHERE table_schema='publish'
          AND table_name='territorial_practice_claim'
          AND column_name IN (
              'assertion_form',
              'attestation_pattern',
              'classification_outcome'
          )
    ) THEN
        RAISE EXCEPTION 'publish.territorial_practice_claim silently exposed prototype semantics';
    END IF;
    IF EXISTS (
        SELECT 1
          FROM information_schema.views
         WHERE table_schema='publish'
           AND (
               view_definition ILIKE '%claim_asserted_interval%'
               OR view_definition ILIKE '%claim_evidence_locus%'
               OR view_definition ILIKE '%claim_inference_extent%'
               OR view_definition ILIKE '%practice_facet_assertion%'
           )
    ) THEN
        RAISE EXCEPTION 'publish layer depends on disposable prototype tables';
    END IF;

    -- Adversary 1: activating only part of the post-M1 dimension set fails.
    v_blocked := false;
    BEGIN
        INSERT INTO atlas.claim(
            claim_id, claim_kind_code, from_year, to_year,
            temporal_applicability_mode, summary
        ) VALUES (
            '00000000-0000-0000-0000-000000012201'::uuid,
            'territorial_practice', 1, 1, 'bounded_occurrence',
            'invalid partial-dimension fixture'
        );
        INSERT INTO atlas.territorial_practice_claim(
            claim_id, spatial_entity_id, practice_type_code,
            coverage_state_code, assertion_form
        ) VALUES (
            '00000000-0000-0000-0000-000000012201'::uuid,
            '00000000-0000-0000-0000-000000012001'::uuid,
            'slavery_enslavement', 'reviewed', 'event_or_process'
        );
    EXCEPTION WHEN check_violation THEN
        v_blocked := true;
    END;
    IF NOT v_blocked THEN
        RAISE EXCEPTION 'partial post-M1 dimension set was accepted';
    END IF;

    -- Adversary 2: outer query window cannot be exceeded by a positive interval.
    v_blocked := false;
    BEGIN
        INSERT INTO atlas.claim_asserted_interval(
            claim_id, from_year, to_year, interval_role
        ) VALUES (
            '00000000-0000-0000-0000-000000012103'::uuid,
            368, 369, 'asserted_applicability'
        );
    EXCEPTION WHEN raise_exception THEN
        v_blocked := true;
    END;
    IF NOT v_blocked THEN
        RAISE EXCEPTION 'out-of-window asserted interval was accepted';
    END IF;

    -- Adversary 3: unknown applicability cannot smuggle in positive intervals.
    v_blocked := false;
    BEGIN
        INSERT INTO atlas.claim_asserted_interval(
            claim_id, from_year, to_year, interval_role
        ) VALUES (
            '00000000-0000-0000-0000-000000012105'::uuid,
            500, 500, 'asserted_applicability'
        );
    EXCEPTION WHEN raise_exception THEN
        v_blocked := true;
    END;
    IF NOT v_blocked THEN
        RAISE EXCEPTION 'unknown applicability accepted a positive interval';
    END IF;

    -- Adversary 4: a broader inference extent needs an explicit reviewed
    -- generalization basis and non-empty rationale.
    v_blocked := false;
    BEGIN
        INSERT INTO atlas.claim_inference_extent(
            claim_id, spatial_entity_id,
            generalization_basis, generalization_rationale
        ) VALUES (
            '00000000-0000-0000-0000-000000012104'::uuid,
            '00000000-0000-0000-0000-000000012005'::uuid,
            'specialist_polity_synthesis',
            NULL
        );
        PERFORM atlas.validate_claim_spatial_scope(
            '00000000-0000-0000-0000-000000012104'::uuid
        );
    EXCEPTION WHEN raise_exception THEN
        v_blocked := true;
    END;
    IF NOT v_blocked THEN
        RAISE EXCEPTION 'broader inference without rationale was accepted';
    END IF;

    -- Adversary 5: a post-M1 territorial claim cannot claim a positive
    -- applicability mode without at least one explicit asserted interval.
    v_blocked := false;
    BEGIN
        INSERT INTO atlas.claim(
            claim_id, claim_kind_code, from_year, to_year,
            temporal_applicability_mode, summary
        ) VALUES (
            '00000000-0000-0000-0000-000000012202'::uuid,
            'territorial_practice',
            10, 20, 'continuous_interval',
            'invalid missing asserted interval fixture'
        );
        INSERT INTO atlas.territorial_practice_claim(
            claim_id, spatial_entity_id, practice_type_code,
            coverage_state_code,
            assertion_form, attestation_pattern, interpretive_basis,
            occurrence_pattern, institutionalization, prevalence_scope,
            structural_significance, research_stage, classification_outcome
        ) VALUES (
            '00000000-0000-0000-0000-000000012202'::uuid,
            '00000000-0000-0000-0000-000000012001'::uuid,
            'slavery_enslavement',
            'reviewed',
            'practice_or_status',
            'unassessed',
            'unassessed',
            'continuous_period',
            'unassessed',
            'unassessed',
            'unassessed',
            'review_complete',
            'classified'
        );
        PERFORM atlas.validate_claim_temporal_semantics(
            '00000000-0000-0000-0000-000000012202'::uuid
        );
    EXCEPTION WHEN raise_exception THEN
        v_blocked := true;
    END;
    IF NOT v_blocked THEN
        RAISE EXCEPTION 'positive applicability without asserted interval was accepted';
    END IF;
END;
$$;

-- Final deferred pass after the adversarial subtransactions.
SET CONSTRAINTS ALL IMMEDIATE;

DO $$
BEGIN
    RAISE NOTICE 'M2 #120 post-M1 relational acceptance fixtures passed';
END;
$$;

ROLLBACK;
