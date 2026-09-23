-- M2 #120 rollback-only acceptance: post-M1 semantics in disposable PostGIS.
BEGIN;

INSERT INTO atlas.spatial_entity(
    spatial_entity_id, entity_type_code, canonical_name, display_name, review_status
) VALUES
('12000000-0000-0000-0000-000000000001','polity','Hittite central Anatolia','Hittite central Anatolia','reviewed'),
('12000000-0000-0000-0000-000000000002','polity','Baekje','Baekje','reviewed'),
('12000000-0000-0000-0000-000000000003','region','Silla Village Register villages','Silla Village Register villages','reviewed'),
('12000000-0000-0000-0000-000000000004','polity','Whole Silla synthetic containment target','Whole Silla synthetic containment target','draft'),
('12000000-0000-0000-0000-000000000005','site','Synthetic evidence site B','Synthetic evidence site B','draft'),
('12000000-0000-0000-0000-000000000006','polity','Synthetic polity Y','Synthetic polity Y','draft');

-- Pure legacy row: no post-M1 fields required; legacy P-level stays representable.
INSERT INTO atlas.claim(
    claim_id, claim_kind_code, from_year, to_year, summary,
    review_status, publication_status
) VALUES (
    '12000000-0000-0000-0000-000000000010','territorial_practice',100,100,
    'Legacy compatibility control','draft','unpublished'
);
INSERT INTO atlas.territorial_practice_claim(
    claim_id, spatial_entity_id, practice_type_code, practice_level,
    coverage_state_code, classification_status
) VALUES (
    '12000000-0000-0000-0000-000000000010',
    '12000000-0000-0000-0000-000000000001',
    'slavery_enslavement','P4','classified','legacy_control'
);

-- Hittite period synthesis: broad precision, but continuity is explicit.
INSERT INTO atlas.claim(
    claim_id, claim_kind_code, from_year, to_year, date_text_original,
    temporal_precision, spatial_precision, summary, review_status,
    publication_status, semantic_model_version, temporal_applicability_mode
) VALUES (
    '12000000-0000-0000-0000-000000000011','territorial_practice',
    -1399,-1199,'1400–1200 BCE','broad_range','polity',
    'Hittite post-M1 representability fixture','reviewed','unpublished',
    'post_m1_v2','continuous_interval'
);
INSERT INTO atlas.territorial_practice_claim(
    claim_id, spatial_entity_id, practice_type_code, practice_level,
    coverage_state_code, classification_status,
    assertion_form, attestation_pattern, interpretive_basis,
    occurrence_pattern, institutionalization, prevalence_scope,
    structural_significance, research_stage, classification_outcome
) VALUES (
    '12000000-0000-0000-0000-000000000011',
    '12000000-0000-0000-0000-000000000001',
    'slavery_enslavement','P2','classified','reviewed',
    'practice_or_status','recurrent_attestation','mixed_primary_and_specialist',
    'recurrent','institutional_features_supported','unassessed',
    'unassessed','review_complete','classified'
);
INSERT INTO atlas.claim_asserted_interval(
    claim_id, from_year, to_year, interval_role
) VALUES (
    '12000000-0000-0000-0000-000000000011',-1399,-1199,'asserted'
);
INSERT INTO atlas.claim_evidence_locus(claim_id, spatial_entity_id, role_text)
VALUES (
    '12000000-0000-0000-0000-000000000011',
    '12000000-0000-0000-0000-000000000001','reviewed polity-period evidence package'
);
INSERT INTO atlas.claim_inference_extent(
    claim_id, spatial_entity_id, generalization_basis
) VALUES (
    '12000000-0000-0000-0000-000000000011',
    '12000000-0000-0000-0000-000000000001','same_as_locus'
);
INSERT INTO atlas.practice_facet_assertion(claim_id,facet_dimension,concept_code) VALUES
('12000000-0000-0000-0000-000000000011','status','enslaved_status'),
('12000000-0000-0000-0000-000000000011','property_legal','pricing_property_rules'),
('12000000-0000-0000-0000-000000000011','function','herding_labour'),
('12000000-0000-0000-0000-000000000011','transmission','status_flexibility');

-- Baekje 369: one bounded event, no prevalence inference from captive count.
INSERT INTO atlas.claim(
    claim_id, claim_kind_code, from_year, to_year, date_text_original,
    temporal_precision, spatial_precision, summary, review_status,
    publication_status, semantic_model_version, temporal_applicability_mode
) VALUES (
    '12000000-0000-0000-0000-000000000012','territorial_practice',
    369,369,'369 CE','year','polity_event',
    'Baekje 369 bounded event fixture','reviewed','unpublished',
    'post_m1_v2','bounded_occurrence'
);
INSERT INTO atlas.territorial_practice_claim(
    claim_id, spatial_entity_id, practice_type_code, practice_level,
    coverage_state_code, classification_status,
    assertion_form, attestation_pattern, interpretive_basis,
    occurrence_pattern, institutionalization, prevalence_scope,
    structural_significance, research_stage, classification_outcome
) VALUES (
    '12000000-0000-0000-0000-000000000012',
    '12000000-0000-0000-0000-000000000002',
    'slavery_enslavement','P1','classified','reviewed',
    'event_or_process','single_bounded_attestation','mixed_primary_and_specialist',
    'bounded_occurrence','unassessed','unassessed',
    'unassessed','review_complete','classified'
);
INSERT INTO atlas.claim_asserted_interval(claim_id,from_year,to_year,interval_role)
VALUES ('12000000-0000-0000-0000-000000000012',369,369,'asserted');
INSERT INTO atlas.practice_facet_assertion(claim_id,facet_dimension,concept_code) VALUES
('12000000-0000-0000-0000-000000000012','process','captive_taking'),
('12000000-0000-0000-0000-000000000012','process','enslavement_distribution');

-- Silla: outer query envelope is 695..819, but only alternatives are positive.
INSERT INTO atlas.claim(
    claim_id, claim_kind_code, from_year, to_year, date_text_original,
    temporal_precision, temporal_certainty, spatial_precision, summary,
    review_status, publication_status, semantic_model_version,
    temporal_applicability_mode
) VALUES (
    '12000000-0000-0000-0000-000000000013','territorial_practice',
    695,819,'proposed dates include 695, 755, 815, and 818–819 CE',
    'disputed_alternatives','disputed','four_village_register',
    'Silla alternative-date fixture','reviewed','unpublished',
    'post_m1_v2','alternative_dates'
);
INSERT INTO atlas.territorial_practice_claim(
    claim_id, spatial_entity_id, practice_type_code, practice_level,
    coverage_state_code, classification_status,
    assertion_form, attestation_pattern, interpretive_basis,
    occurrence_pattern, institutionalization, prevalence_scope,
    structural_significance, research_stage, classification_outcome
) VALUES (
    '12000000-0000-0000-0000-000000000013',
    '12000000-0000-0000-0000-000000000003',
    'slavery_enslavement','P2','classified','reviewed_with_date_dispute',
    'practice_or_status','multiple_independent_attestations','specialist_synthesis',
    'bounded_occurrence','institutional_features_supported','localized',
    'unassessed','review_complete','classified'
);
INSERT INTO atlas.claim_asserted_interval(claim_id,from_year,to_year,interval_role) VALUES
('12000000-0000-0000-0000-000000000013',695,695,'alternative'),
('12000000-0000-0000-0000-000000000013',755,755,'alternative'),
('12000000-0000-0000-0000-000000000013',815,815,'alternative'),
('12000000-0000-0000-0000-000000000013',818,819,'alternative');
INSERT INTO atlas.claim_evidence_locus(claim_id, spatial_entity_id, role_text)
VALUES (
    '12000000-0000-0000-0000-000000000013',
    '12000000-0000-0000-0000-000000000003','four uncertain village-register communities'
);
INSERT INTO atlas.claim_inference_extent(
    claim_id, spatial_entity_id, generalization_basis
) VALUES (
    '12000000-0000-0000-0000-000000000013',
    '12000000-0000-0000-0000-000000000003','same_as_locus'
);

-- Reviewed inconclusive remains NULL legacy P-level; no P0 is manufactured.
INSERT INTO atlas.claim(
    claim_id, claim_kind_code, from_year, to_year, summary,
    review_status, publication_status, semantic_model_version,
    temporal_applicability_mode
) VALUES (
    '12000000-0000-0000-0000-000000000014','territorial_practice',
    500,500,'Reviewed inconclusive control','reviewed','unpublished',
    'post_m1_v2','unknown'
);
INSERT INTO atlas.territorial_practice_claim(
    claim_id, spatial_entity_id, practice_type_code, practice_level,
    coverage_state_code, classification_status,
    assertion_form, attestation_pattern, interpretive_basis,
    occurrence_pattern, institutionalization, prevalence_scope,
    structural_significance, research_stage, classification_outcome
) VALUES (
    '12000000-0000-0000-0000-000000000014',
    '12000000-0000-0000-0000-000000000001',
    'slavery_enslavement',NULL,'researched_inconclusive','inconclusive',
    'practice_or_status','unassessed','unassessed',
    'unassessed','unassessed','unassessed',
    'unassessed','review_complete','inconclusive'
);

-- Synthetic broader reviewed inference demonstrates explicit locus vs extent.
INSERT INTO atlas.claim(
    claim_id, claim_kind_code, from_year, to_year, summary,
    review_status, publication_status, semantic_model_version,
    temporal_applicability_mode
) VALUES (
    '12000000-0000-0000-0000-000000000015','territorial_practice',
    600,650,'Synthetic reviewed generalization control','draft','unpublished',
    'post_m1_v2','continuous_interval'
);
INSERT INTO atlas.territorial_practice_claim(
    claim_id, spatial_entity_id, practice_type_code, practice_level,
    coverage_state_code, classification_status,
    assertion_form, attestation_pattern, interpretive_basis,
    occurrence_pattern, institutionalization, prevalence_scope,
    structural_significance, research_stage, classification_outcome
) VALUES (
    '12000000-0000-0000-0000-000000000015',
    '12000000-0000-0000-0000-000000000006',
    'slavery_enslavement',NULL,'reviewed','synthetic',
    'practice_or_status','multiple_independent_attestations','specialist_synthesis',
    'continuous_period','unassessed','broader',
    'unassessed','review_complete','classified'
);
INSERT INTO atlas.claim_asserted_interval(claim_id,from_year,to_year)
VALUES ('12000000-0000-0000-0000-000000000015',600,650);
INSERT INTO atlas.claim_evidence_locus(claim_id,spatial_entity_id)
VALUES (
    '12000000-0000-0000-0000-000000000015',
    '12000000-0000-0000-0000-000000000005'
);
INSERT INTO atlas.claim_inference_extent(
    claim_id,spatial_entity_id,generalization_basis,generalization_rationale
) VALUES (
    '12000000-0000-0000-0000-000000000015',
    '12000000-0000-0000-0000-000000000006',
    'specialist_polity_synthesis',
    'Synthetic fixture: reviewed specialist synthesis explicitly supports the wider polity extent.'
);

DO $$
BEGIN
    -- Query envelope alone must not create selected-year truth.
    IF NOT ('[695,820)'::int4range @> 700) THEN
        RAISE EXCEPTION 'test setup error: 700 must lie in Silla outer query range';
    END IF;
    IF atlas.claim_applies_at_year(
        '12000000-0000-0000-0000-000000000013'::uuid,700
    ) THEN
        RAISE EXCEPTION 'Silla 700 incorrectly became positive from outer query envelope';
    END IF;
    IF NOT atlas.claim_applies_at_year(
        '12000000-0000-0000-0000-000000000013'::uuid,755
    ) THEN
        RAISE EXCEPTION 'Silla asserted alternative 755 must be positive';
    END IF;
    IF atlas.claim_applies_at_year(
        '12000000-0000-0000-0000-000000000012'::uuid,370
    ) THEN
        RAISE EXCEPTION 'Baekje bounded event leaked into 370';
    END IF;
    IF NOT atlas.claim_applies_at_year(
        '12000000-0000-0000-0000-000000000012'::uuid,369
    ) THEN
        RAISE EXCEPTION 'Baekje 369 event must be positive';
    END IF;
    IF NOT atlas.claim_applies_at_year(
        '12000000-0000-0000-0000-000000000011'::uuid,-1300
    ) THEN
        RAISE EXCEPTION 'Hittite reviewed continuous-period year -1300 must be positive';
    END IF;
    IF atlas.claim_applies_at_year(
        '12000000-0000-0000-0000-000000000011'::uuid,-1400
    ) THEN
        RAISE EXCEPTION 'Hittite year outside asserted interval became positive';
    END IF;

    IF (SELECT practice_level FROM atlas.territorial_practice_claim
        WHERE claim_id='12000000-0000-0000-0000-000000000014'::uuid) IS NOT NULL THEN
        RAISE EXCEPTION 'inconclusive post-M1 claim manufactured a legacy P-level';
    END IF;

    IF (SELECT practice_level FROM atlas.territorial_practice_claim
        WHERE claim_id='12000000-0000-0000-0000-000000000010'::uuid) <> 'P4' THEN
        RAISE EXCEPTION 'legacy P-level compatibility row changed';
    END IF;
END $$;

-- Invalid: post-M1 subtype missing explicit dimensions.
DO $$
DECLARE blocked boolean := false;
BEGIN
    INSERT INTO atlas.claim(
        claim_id,claim_kind_code,from_year,to_year,summary,
        semantic_model_version,temporal_applicability_mode
    ) VALUES (
        '12000000-0000-0000-0000-000000000020','territorial_practice',
        700,700,'invalid missing dimensions','post_m1_v2','bounded_occurrence'
    );
    BEGIN
        INSERT INTO atlas.territorial_practice_claim(
            claim_id,spatial_entity_id,practice_type_code,practice_level,
            coverage_state_code
        ) VALUES (
            '12000000-0000-0000-0000-000000000020',
            '12000000-0000-0000-0000-000000000001',
            'slavery_enslavement',NULL,'reviewed'
        );
    EXCEPTION WHEN others THEN
        IF SQLERRM LIKE 'post-M1 territorial claim % must state every target dimension explicitly%' THEN
            blocked := true;
        ELSE RAISE;
        END IF;
    END;
    IF NOT blocked THEN
        RAISE EXCEPTION 'partial post-M1 semantics were accepted';
    END IF;
END $$;

-- Invalid: asserted interval outside outer query window.
DO $$
DECLARE blocked boolean := false;
BEGIN
    BEGIN
        INSERT INTO atlas.claim_asserted_interval(claim_id,from_year,to_year)
        VALUES ('12000000-0000-0000-0000-000000000012',368,369);
    EXCEPTION WHEN others THEN
        IF SQLERRM LIKE 'asserted interval starts before claim outer query window%' THEN
            blocked := true;
        ELSE RAISE;
        END IF;
    END;
    IF NOT blocked THEN
        RAISE EXCEPTION 'out-of-window asserted interval was accepted';
    END IF;
END $$;

-- Invalid: "same as locus" without a matching locus.
DO $$
DECLARE blocked boolean := false;
BEGIN
    BEGIN
        INSERT INTO atlas.claim_inference_extent(
            claim_id,spatial_entity_id,generalization_basis
        ) VALUES (
            '12000000-0000-0000-0000-000000000013',
            '12000000-0000-0000-0000-000000000004',
            'same_as_locus'
        );
    EXCEPTION WHEN others THEN
        IF SQLERRM LIKE 'same_as_locus inference extent requires%' THEN
            blocked := true;
        ELSE RAISE;
        END IF;
    END;
    IF NOT blocked THEN
        RAISE EXCEPTION 'geometry-like enlargement was accepted as same-as-locus';
    END IF;
END $$;

-- Invalid: broader inference without reviewed rationale.
DO $$
DECLARE blocked boolean := false;
BEGIN
    BEGIN
        INSERT INTO atlas.claim_inference_extent(
            claim_id,spatial_entity_id,generalization_basis,generalization_rationale
        ) VALUES (
            '12000000-0000-0000-0000-000000000013',
            '12000000-0000-0000-0000-000000000004',
            'specialist_polity_synthesis',NULL
        );
    EXCEPTION WHEN check_violation THEN
        blocked := true;
    END;
    IF NOT blocked THEN
        RAISE EXCEPTION 'broader inference without rationale was accepted';
    END IF;
END $$;

-- Invalid inverse mutation: a valid post-M1 subtype cannot survive a parent downgrade.
DO $
DECLARE blocked boolean := false;
BEGIN
    BEGIN
        UPDATE atlas.claim
        SET semantic_model_version=NULL,
            temporal_applicability_mode=NULL
        WHERE claim_id='12000000-0000-0000-0000-000000000011'::uuid;

        SET CONSTRAINTS claim_post_m1_parent_consistency IMMEDIATE;
    EXCEPTION WHEN others THEN
        IF SQLERRM LIKE 'legacy/null semantic model cannot retain post-M1 territorial dimensions%' THEN
            blocked := true;
        ELSE
            RAISE;
        END IF;
    END;

    IF NOT blocked THEN
        RAISE EXCEPTION 'parent semantic downgrade bypassed post-M1 subtype invariants';
    END IF;
END $;
SET CONSTRAINTS claim_post_m1_parent_consistency DEFERRED;

-- Invalid inverse mutation: narrowing the outer window cannot strand asserted intervals.
DO $
DECLARE blocked boolean := false;
BEGIN
    BEGIN
        UPDATE atlas.claim
        SET from_year=700
        WHERE claim_id='12000000-0000-0000-0000-000000000013'::uuid;

        SET CONSTRAINTS claim_post_m1_parent_consistency IMMEDIATE;
    EXCEPTION WHEN others THEN
        IF SQLERRM LIKE 'claim % outer query window no longer contains all asserted intervals%' THEN
            blocked := true;
        ELSE
            RAISE;
        END IF;
    END;

    IF NOT blocked THEN
        RAISE EXCEPTION 'parent range edit stranded an asserted interval outside its query window';
    END IF;
END $;
SET CONSTRAINTS claim_post_m1_parent_consistency DEFERRED;

-- Invalid inverse mutation: same_as_locus cannot survive deletion of its matching locus.
DO $
DECLARE blocked boolean := false;
BEGIN
    BEGIN
        DELETE FROM atlas.claim_evidence_locus
        WHERE claim_id='12000000-0000-0000-0000-000000000013'::uuid
          AND spatial_entity_id='12000000-0000-0000-0000-000000000003'::uuid;

        SET CONSTRAINTS claim_evidence_locus_inverse_consistency IMMEDIATE;
    EXCEPTION WHEN others THEN
        IF SQLERRM LIKE 'same_as_locus inference extent requires retained matching evidence locus%' THEN
            blocked := true;
        ELSE
            RAISE;
        END IF;
    END;

    IF NOT blocked THEN
        RAISE EXCEPTION 'same_as_locus inference survived deletion of its evidence locus';
    END IF;
END $;
SET CONSTRAINTS claim_evidence_locus_inverse_consistency DEFERRED;

-- Existing publication views must not silently expose the prototype fields/tables.
DO $$
DECLARE n bigint;
BEGIN
    SELECT count(*) INTO n
    FROM information_schema.columns
    WHERE table_schema='publish' AND table_name='claim'
      AND column_name IN ('semantic_model_version','temporal_applicability_mode');
    IF n <> 0 THEN
        RAISE EXCEPTION 'publish.claim silently switched to post-M1 columns';
    END IF;

    SELECT count(*) INTO n
    FROM information_schema.columns
    WHERE table_schema='publish' AND table_name='territorial_practice_claim'
      AND column_name IN (
        'assertion_form','attestation_pattern','interpretive_basis',
        'occurrence_pattern','institutionalization','prevalence_scope',
        'structural_significance','research_stage','classification_outcome'
      );
    IF n <> 0 THEN
        RAISE EXCEPTION 'publish.territorial_practice_claim silently switched to post-M1 columns';
    END IF;

    SELECT count(*) INTO n
    FROM information_schema.views
    WHERE table_schema='publish'
      AND view_definition ~* '(claim_asserted_interval|claim_evidence_locus|claim_inference_extent|practice_facet_assertion)';
    IF n <> 0 THEN
        RAISE EXCEPTION 'publish views unexpectedly reference post-M1 prototype relations';
    END IF;
END $$;

SELECT
    'Hittite' AS fixture,
    atlas.claim_applies_at_year('12000000-0000-0000-0000-000000000011',-1300) AS representative_year,
    (SELECT count(*) FROM atlas.practice_facet_assertion
     WHERE claim_id='12000000-0000-0000-0000-000000000011') AS facets
UNION ALL
SELECT
    'Baekje',
    atlas.claim_applies_at_year('12000000-0000-0000-0000-000000000012',369),
    (SELECT count(*) FROM atlas.practice_facet_assertion
     WHERE claim_id='12000000-0000-0000-0000-000000000012')
UNION ALL
SELECT
    'Silla',
    atlas.claim_applies_at_year('12000000-0000-0000-0000-000000000013',755),
    (SELECT count(*) FROM atlas.practice_facet_assertion
     WHERE claim_id='12000000-0000-0000-0000-000000000013');

ROLLBACK;
