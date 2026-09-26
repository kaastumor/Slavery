-- Gate 2 / D-103 regression: lossless research-target/result representation.
BEGIN;

DO $$
DECLARE
    missing text;
BEGIN
    SELECT string_agg(name, ', ')
    INTO missing
    FROM (VALUES
        ('atlas.claim_asserted_interval'),
        ('atlas.claim_evidence_locus'),
        ('atlas.claim_inference_extent'),
        ('atlas.practice_facet_assertion'),
        ('audit.research_target'),
        ('audit.research_target_result'),
        ('audit.research_target_review'),
        ('audit.research_target_source'),
        ('audit.research_target_claim')
    ) AS required(name)
    WHERE to_regclass(name) IS NULL;

    IF missing IS NOT NULL THEN
        RAISE EXCEPTION 'Missing Gate-2 relations: %', missing;
    END IF;
END $$;

INSERT INTO atlas.spatial_entity(
    spatial_entity_id, entity_type_code, canonical_name, review_status
) VALUES (
    '00000000-0000-0000-0000-000000003101'::uuid,
    'region',
    'Gate 2 test region',
    'draft'
);

INSERT INTO audit.research_target(
    target_key, target_label, anchor_label, anchor_year, frame_class,
    spatial_entity_id, origin, review_status
) VALUES (
    'TEST:INCONCLUSIVE',
    'Gate 2 inconclusive target',
    '1300 CE',
    1300,
    'region_community',
    '00000000-0000-0000-0000-000000003101'::uuid,
    'regression',
    'reviewed'
);

INSERT INTO audit.research_target_result(
    research_target_result_id, target_key, research_stage, research_outcome,
    bounded_proposition, required_abstention, content_sha256, review_status
) VALUES (
    '00000000-0000-0000-0000-000000003102'::uuid,
    'TEST:INCONCLUSIVE',
    'researched_internal',
    'RESEARCHED_INCONCLUSIVE',
    'No positive target-specific status is established.',
    'Do not infer absence.',
    repeat('a',64),
    'reviewed'
);

INSERT INTO audit.research_target_review(
    research_target_result_id, candidate_id, review_level, review_disposition,
    admitted, review_reason, failure_guards
) VALUES (
    '00000000-0000-0000-0000-000000003102'::uuid,
    'test-candidate',
    'internal',
    'ACCEPT_INTERNAL_REVIEW',
    true,
    'Accept bounded inconclusive result.',
    ARRAY['absence_inference']
);

DO $$
BEGIN
    IF EXISTS (
        SELECT 1
        FROM audit.research_target_claim
        WHERE research_target_result_id = '00000000-0000-0000-0000-000000003102'::uuid
    ) THEN
        RAISE EXCEPTION 'Inconclusive target unexpectedly requires a positive claim';
    END IF;
END $$;

INSERT INTO atlas.source(
    source_id, title, source_classification
) VALUES (
    '00000000-0000-0000-0000-000000003103'::uuid,
    'Gate 2 source',
    'secondary'
);

INSERT INTO atlas.source_version(
    source_version_id, source_id, version_label, url_or_identifier
) VALUES (
    '00000000-0000-0000-0000-000000003104'::uuid,
    '00000000-0000-0000-0000-000000003103'::uuid,
    'v1',
    'urn:test:gate2'
);

INSERT INTO audit.research_target_source(
    research_target_result_id, source_version_id, source_relation_key,
    source_version_ref_raw, evidence_role, independence_group, claim_fitness,
    direction_raw, normalized_direction
) VALUES (
    '00000000-0000-0000-0000-000000003102'::uuid,
    '00000000-0000-0000-0000-000000003104'::uuid,
    'TEST-SOURCE-1',
    'urn:test:gate2:v1',
    'category_control',
    'gate2-test-group',
    'Strong for category control; not a positive target attestation.',
    'qualifies',
    'qualifies'
);

INSERT INTO atlas.claim(
    claim_id, claim_kind_code, from_year, to_year, temporal_applicability_mode,
    summary, review_status, publication_status
) VALUES
(
    '00000000-0000-0000-0000-000000003105'::uuid,
    'other',
    1290,
    1310,
    'bounded_occurrence',
    'Gate 2 first dimension claim',
    'reviewed',
    'unpublished'
),
(
    '00000000-0000-0000-0000-000000003106'::uuid,
    'other',
    1300,
    1300,
    'bounded_occurrence',
    'Gate 2 second dimension claim',
    'reviewed',
    'unpublished'
);

INSERT INTO atlas.claim_asserted_interval(
    claim_id, from_year, to_year, interval_role
) VALUES (
    '00000000-0000-0000-0000-000000003105'::uuid,
    1300,
    1300,
    'asserted_applicability'
);

INSERT INTO atlas.claim_evidence_locus(
    claim_id, spatial_entity_id, role_text
) VALUES (
    '00000000-0000-0000-0000-000000003105'::uuid,
    '00000000-0000-0000-0000-000000003101'::uuid,
    'documented locus'
);

INSERT INTO atlas.claim_inference_extent(
    claim_id, spatial_entity_id, generalization_basis, generalization_rationale
) VALUES (
    '00000000-0000-0000-0000-000000003105'::uuid,
    '00000000-0000-0000-0000-000000003101'::uuid,
    'same bounded locus',
    'No spatial generalization beyond the documented target.'
);

INSERT INTO atlas.claim_source(
    claim_id, source_version_id, evidence_role, independence_group, claim_fitness,
    direction
) VALUES (
    '00000000-0000-0000-0000-000000003105'::uuid,
    '00000000-0000-0000-0000-000000003104'::uuid,
    'bounded support',
    'gate2-test-group',
    'Strong for this bounded claim only.',
    'supports'
);

INSERT INTO audit.research_target_claim(
    research_target_result_id, claim_id, claim_role
) VALUES
(
    '00000000-0000-0000-0000-000000003102'::uuid,
    '00000000-0000-0000-0000-000000003105'::uuid,
    'context_dimension'
),
(
    '00000000-0000-0000-0000-000000003102'::uuid,
    '00000000-0000-0000-0000-000000003106'::uuid,
    'external_dimension'
);

DO $$
DECLARE
    n integer;
BEGIN
    SELECT count(*) INTO n
    FROM audit.research_target_claim
    WHERE research_target_result_id='00000000-0000-0000-0000-000000003102'::uuid;

    IF n <> 2 THEN
        RAISE EXCEPTION 'Expected one research result to link to two claims, found %', n;
    END IF;
END $$;

INSERT INTO atlas.claim(
    claim_id, claim_kind_code, summary, review_status, publication_status
) VALUES (
    '00000000-0000-0000-0000-000000003107'::uuid,
    'territorial_practice',
    'Gate 2 nullable legacy classification control',
    'reviewed',
    'unpublished'
);

INSERT INTO atlas.territorial_practice_claim(
    claim_id, spatial_entity_id, practice_type_code, practice_level,
    coverage_state_code, assertion_form, research_stage, classification_outcome
) VALUES (
    '00000000-0000-0000-0000-000000003107'::uuid,
    '00000000-0000-0000-0000-000000003101'::uuid,
    NULL,
    NULL,
    NULL,
    'event_or_process',
    'researched_internal',
    'researched_inconclusive'
);

DO $$
BEGIN
    IF (SELECT practice_level FROM atlas.territorial_practice_claim
        WHERE claim_id='00000000-0000-0000-0000-000000003107'::uuid) IS NOT NULL THEN
        RAISE EXCEPTION 'Gate 2 test assigned a P-level unexpectedly';
    END IF;
END $$;

ROLLBACK;
