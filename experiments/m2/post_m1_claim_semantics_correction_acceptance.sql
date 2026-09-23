-- M2 #135 rollback-only acceptance for cross-table integrity correction.
BEGIN;

INSERT INTO atlas.spatial_entity(
    spatial_entity_id,entity_type_code,canonical_name,review_status
) VALUES
('13500000-0000-0000-0000-000000000001','polity','M2 correction polity A','reviewed'),
('13500000-0000-0000-0000-000000000002','site','M2 correction evidence site','reviewed');

-- Legacy compatibility control.
INSERT INTO atlas.claim(
    claim_id,claim_kind_code,from_year,to_year,summary,review_status,publication_status
) VALUES (
    '13500000-0000-0000-0000-000000000010',
    'territorial_practice',100,200,'legacy correction control','reviewed','unpublished'
);
INSERT INTO atlas.territorial_practice_claim(
    claim_id,spatial_entity_id,practice_type_code,practice_level,
    coverage_state_code,classification_status
) VALUES (
    '13500000-0000-0000-0000-000000000010',
    '13500000-0000-0000-0000-000000000001',
    'slavery_enslavement','P2','classified','legacy'
);

-- Valid bounded post-M1 package used by reverse-direction attacks.
INSERT INTO atlas.claim(
    claim_id,claim_kind_code,from_year,to_year,summary,review_status,publication_status,
    semantic_model_version,temporal_applicability_mode
) VALUES (
    '13500000-0000-0000-0000-000000000011',
    'territorial_practice',100,200,'bounded post-M1 correction control',
    'reviewed','unpublished','post_m1_v2','continuous_interval'
);
INSERT INTO atlas.territorial_practice_claim(
    claim_id,spatial_entity_id,practice_type_code,practice_level,
    coverage_state_code,classification_status,
    assertion_form,attestation_pattern,interpretive_basis,occurrence_pattern,
    institutionalization,prevalence_scope,structural_significance,
    research_stage,classification_outcome
) VALUES (
    '13500000-0000-0000-0000-000000000011',
    '13500000-0000-0000-0000-000000000001',
    'slavery_enslavement',NULL,'reviewed','post_m1',
    'practice_or_status','recurrent_attestation','specialist_synthesis','continuous_period',
    'unassessed','unassessed','unassessed','review_complete','classified'
);
INSERT INTO atlas.claim_asserted_interval(claim_id,from_year,to_year,interval_role)
VALUES ('13500000-0000-0000-0000-000000000011',120,180,'asserted');
INSERT INTO atlas.claim_evidence_locus(claim_id,spatial_entity_id)
VALUES (
    '13500000-0000-0000-0000-000000000011',
    '13500000-0000-0000-0000-000000000002'
);
INSERT INTO atlas.claim_inference_extent(
    claim_id,spatial_entity_id,generalization_basis
) VALUES (
    '13500000-0000-0000-0000-000000000011',
    '13500000-0000-0000-0000-000000000002','same_as_locus'
);
INSERT INTO atlas.practice_facet_assertion(
    claim_id,facet_dimension,concept_code
) VALUES (
    '13500000-0000-0000-0000-000000000011',
    'status','enslaved_status'
);

-- Valid unknown package: no positive intervals.
INSERT INTO atlas.claim(
    claim_id,claim_kind_code,from_year,to_year,summary,
    semantic_model_version,temporal_applicability_mode
) VALUES (
    '13500000-0000-0000-0000-000000000012',
    'territorial_practice',500,500,'unknown applicability control',
    'post_m1_v2','unknown'
);
INSERT INTO atlas.territorial_practice_claim(
    claim_id,spatial_entity_id,practice_type_code,coverage_state_code,
    assertion_form,attestation_pattern,interpretive_basis,occurrence_pattern,
    institutionalization,prevalence_scope,structural_significance,
    research_stage,classification_outcome
) VALUES (
    '13500000-0000-0000-0000-000000000012',
    '13500000-0000-0000-0000-000000000001',
    'slavery_enslavement','researched_inconclusive',
    'practice_or_status','unassessed','unassessed','unassessed',
    'unassessed','unassessed','unassessed','review_complete','inconclusive'
);

-- Genuine open terminus after: 120 onward.
INSERT INTO atlas.claim(
    claim_id,claim_kind_code,from_year,to_year,summary,
    semantic_model_version,temporal_applicability_mode
) VALUES (
    '13500000-0000-0000-0000-000000000013',
    'territorial_practice',100,NULL,'terminus-after representability control',
    'post_m1_v2','terminus_after'
);
INSERT INTO atlas.territorial_practice_claim(
    claim_id,spatial_entity_id,practice_type_code,coverage_state_code,
    assertion_form,attestation_pattern,interpretive_basis,occurrence_pattern,
    institutionalization,prevalence_scope,structural_significance,
    research_stage,classification_outcome
) VALUES (
    '13500000-0000-0000-0000-000000000013',
    '13500000-0000-0000-0000-000000000001',
    'slavery_enslavement','reviewed',
    'practice_or_status','single_bounded_attestation','specialist_synthesis','continuous_period',
    'unassessed','unassessed','unassessed','review_complete','classified'
);
INSERT INTO atlas.claim_asserted_interval(claim_id,from_year,to_year,interval_role)
VALUES ('13500000-0000-0000-0000-000000000013',120,NULL,'asserted');

-- Genuine open terminus before: through 80.
INSERT INTO atlas.claim(
    claim_id,claim_kind_code,from_year,to_year,summary,
    semantic_model_version,temporal_applicability_mode
) VALUES (
    '13500000-0000-0000-0000-000000000014',
    'territorial_practice',NULL,100,'terminus-before representability control',
    'post_m1_v2','terminus_before'
);
INSERT INTO atlas.territorial_practice_claim(
    claim_id,spatial_entity_id,practice_type_code,coverage_state_code,
    assertion_form,attestation_pattern,interpretive_basis,occurrence_pattern,
    institutionalization,prevalence_scope,structural_significance,
    research_stage,classification_outcome
) VALUES (
    '13500000-0000-0000-0000-000000000014',
    '13500000-0000-0000-0000-000000000001',
    'slavery_enslavement','reviewed',
    'practice_or_status','single_bounded_attestation','specialist_synthesis','continuous_period',
    'unassessed','unassessed','unassessed','review_complete','classified'
);
INSERT INTO atlas.claim_asserted_interval(claim_id,from_year,to_year,interval_role)
VALUES ('13500000-0000-0000-0000-000000000014',NULL,80,'asserted');

-- Force positive package validation explicitly before adversarial subtransactions.
SELECT atlas.validate_post_m1_claim_integrity('13500000-0000-0000-0000-000000000011');
SELECT atlas.validate_post_m1_claim_integrity('13500000-0000-0000-0000-000000000012');
SELECT atlas.validate_post_m1_claim_integrity('13500000-0000-0000-0000-000000000013');
SELECT atlas.validate_post_m1_claim_integrity('13500000-0000-0000-0000-000000000014');

DO $$
DECLARE
    blocked boolean;
BEGIN
    -- Open termini are real selected-year semantics, not just vocabulary labels.
    IF atlas.claim_applies_at_year(
        '13500000-0000-0000-0000-000000000013',119
    ) OR NOT atlas.claim_applies_at_year(
        '13500000-0000-0000-0000-000000000013',120
    ) OR NOT atlas.claim_applies_at_year(
        '13500000-0000-0000-0000-000000000013',10000
    ) THEN
        RAISE EXCEPTION 'terminus_after selected-year behavior is wrong';
    END IF;

    IF NOT atlas.claim_applies_at_year(
        '13500000-0000-0000-0000-000000000014',-10000
    ) OR NOT atlas.claim_applies_at_year(
        '13500000-0000-0000-0000-000000000014',80
    ) OR atlas.claim_applies_at_year(
        '13500000-0000-0000-0000-000000000014',81
    ) THEN
        RAISE EXCEPTION 'terminus_before selected-year behavior is wrong';
    END IF;

    -- 1. Legacy -> post-M1 retyping cannot bypass complete target dimensions.
    blocked := false;
    BEGIN
        UPDATE atlas.claim
        SET semantic_model_version='post_m1_v2',
            temporal_applicability_mode='bounded_occurrence'
        WHERE claim_id='13500000-0000-0000-0000-000000000010';
        PERFORM atlas.validate_post_m1_claim_integrity(
            '13500000-0000-0000-0000-000000000010'
        );
    EXCEPTION WHEN raise_exception THEN
        blocked := true;
    END;
    IF NOT blocked THEN
        RAISE EXCEPTION 'legacy -> post-M1 retyping bypassed complete dimensions';
    END IF;

    -- 2. Post-M1 -> legacy downgrade cannot strand child semantics.
    blocked := false;
    BEGIN
        UPDATE atlas.claim
        SET semantic_model_version=NULL,
            temporal_applicability_mode=NULL
        WHERE claim_id='13500000-0000-0000-0000-000000000011';
        PERFORM atlas.validate_post_m1_claim_integrity(
            '13500000-0000-0000-0000-000000000011'
        );
    EXCEPTION WHEN raise_exception THEN
        blocked := true;
    END;
    IF NOT blocked THEN
        RAISE EXCEPTION 'post-M1 downgrade stranded target child semantics';
    END IF;

    -- 3. Narrowing the outer query window cannot strand old asserted intervals.
    blocked := false;
    BEGIN
        UPDATE atlas.claim
        SET from_year=130,to_year=170
        WHERE claim_id='13500000-0000-0000-0000-000000000011';
        PERFORM atlas.validate_post_m1_claim_integrity(
            '13500000-0000-0000-0000-000000000011'
        );
    EXCEPTION WHEN raise_exception THEN
        blocked := true;
    END;
    IF NOT blocked THEN
        RAISE EXCEPTION 'narrowed query window stranded an out-of-window interval';
    END IF;

    -- 4. Unknown applicability cannot receive a positive interval.
    blocked := false;
    BEGIN
        INSERT INTO atlas.claim_asserted_interval(
            claim_id,from_year,to_year,interval_role
        ) VALUES (
            '13500000-0000-0000-0000-000000000012',500,500,'asserted'
        );
    EXCEPTION WHEN raise_exception THEN
        blocked := true;
    END;
    IF NOT blocked THEN
        RAISE EXCEPTION 'unknown applicability accepted a positive interval';
    END IF;

    -- 5. Positive mode without positive applicability is invalid.
    INSERT INTO atlas.claim(
        claim_id,claim_kind_code,from_year,to_year,summary,
        semantic_model_version,temporal_applicability_mode
    ) VALUES (
        '13500000-0000-0000-0000-000000000020',
        'territorial_practice',10,20,'missing interval negative control',
        'post_m1_v2','continuous_interval'
    );
    INSERT INTO atlas.territorial_practice_claim(
        claim_id,spatial_entity_id,practice_type_code,coverage_state_code,
        assertion_form,attestation_pattern,interpretive_basis,occurrence_pattern,
        institutionalization,prevalence_scope,structural_significance,
        research_stage,classification_outcome
    ) VALUES (
        '13500000-0000-0000-0000-000000000020',
        '13500000-0000-0000-0000-000000000001',
        'slavery_enslavement','reviewed',
        'practice_or_status','unassessed','unassessed','continuous_period',
        'unassessed','unassessed','unassessed','review_complete','classified'
    );
    blocked := false;
    BEGIN
        PERFORM atlas.validate_post_m1_claim_integrity(
            '13500000-0000-0000-0000-000000000020'
        );
    EXCEPTION WHEN raise_exception THEN
        blocked := true;
    END;
    IF NOT blocked THEN
        RAISE EXCEPTION 'positive applicability mode with zero intervals was accepted';
    END IF;
    DELETE FROM atlas.territorial_practice_claim
    WHERE claim_id='13500000-0000-0000-0000-000000000020';
    DELETE FROM atlas.claim
    WHERE claim_id='13500000-0000-0000-0000-000000000020';

    -- 6. Alternative interval role must match alternative_dates.
    blocked := false;
    BEGIN
        INSERT INTO atlas.claim_asserted_interval(
            claim_id,from_year,to_year,interval_role
        ) VALUES (
            '13500000-0000-0000-0000-000000000011',150,150,'alternative'
        );
    EXCEPTION WHEN raise_exception THEN
        blocked := true;
    END;
    IF NOT blocked THEN
        RAISE EXCEPTION 'alternative interval role was accepted for continuous mode';
    END IF;

    -- 7. Reverse spatial validation catches deletion of a required locus.
    blocked := false;
    BEGIN
        DELETE FROM atlas.claim_evidence_locus
        WHERE claim_id='13500000-0000-0000-0000-000000000011'
          AND spatial_entity_id='13500000-0000-0000-0000-000000000002';
        PERFORM atlas.validate_post_m1_claim_integrity(
            '13500000-0000-0000-0000-000000000011'
        );
    EXCEPTION WHEN raise_exception THEN
        blocked := true;
    END;
    IF NOT blocked THEN
        RAISE EXCEPTION 'deleting evidence locus stranded same_as_locus inference';
    END IF;

    -- 8. Legacy claims cannot silently acquire target-only facet/locus semantics.
    blocked := false;
    BEGIN
        INSERT INTO atlas.practice_facet_assertion(
            claim_id,facet_dimension,concept_code
        ) VALUES (
            '13500000-0000-0000-0000-000000000010',
            'status','legacy_should_not_receive_target_facet'
        );
    EXCEPTION WHEN raise_exception THEN
        blocked := true;
    END;
    IF NOT blocked THEN
        RAISE EXCEPTION 'legacy claim accepted post-M1 facet semantics';
    END IF;

    blocked := false;
    BEGIN
        INSERT INTO atlas.claim_evidence_locus(claim_id,spatial_entity_id)
        VALUES (
            '13500000-0000-0000-0000-000000000010',
            '13500000-0000-0000-0000-000000000002'
        );
    EXCEPTION WHEN raise_exception THEN
        blocked := true;
    END;
    IF NOT blocked THEN
        RAISE EXCEPTION 'legacy claim accepted post-M1 locus semantics';
    END IF;

    -- Legacy P-level meaning itself is untouched.
    IF (SELECT practice_level
        FROM atlas.territorial_practice_claim
        WHERE claim_id='13500000-0000-0000-0000-000000000010') <> 'P2' THEN
        RAISE EXCEPTION 'legacy P-level compatibility changed';
    END IF;
END $$;

-- Deferred trigger surface exists for every reverse mutation path.
DO $$
DECLARE n integer;
BEGIN
    SELECT count(*) INTO n
    FROM pg_trigger t
    JOIN pg_class c ON c.oid=t.tgrelid
    JOIN pg_namespace ns ON ns.oid=c.relnamespace
    WHERE NOT t.tgisinternal
      AND ns.nspname='atlas'
      AND t.tgname LIKE 'post_m1_claim_integrity_from_%';
    IF n <> 6 THEN
        RAISE EXCEPTION 'expected 6 deferred cross-table integrity triggers, found %',n;
    END IF;
END $$;

ROLLBACK;
