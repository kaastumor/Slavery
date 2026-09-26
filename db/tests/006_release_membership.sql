-- D-054 typed release membership regression test.
BEGIN;

DO $$
DECLARE
    required_table text;
BEGIN
    FOREACH required_table IN ARRAY ARRAY[
        'release_claim',
        'release_actor',
        'release_spatial_entity',
        'release_geometry',
        'release_voyage',
        'release_coverage_assessment',
        'release_research_target_result',
        'release_artifact'
    ] LOOP
        IF to_regclass('audit.' || required_table) IS NULL THEN
            RAISE EXCEPTION 'audit.% is missing', required_table;
        END IF;
    END LOOP;
END $$;

INSERT INTO atlas.claim(
    claim_id, claim_kind_code, summary, review_status, publication_status
) VALUES (
    '00000000-0000-0000-0000-000000002601'::uuid,
    (select code from atlas.claim_kind order by code limit 1),
    'release membership test claim',
    'reviewed',
    'unpublished'
);

INSERT INTO audit.release_manifest(
    release_version, schema_version, status, changelog, qc_summary, unresolved_issues, manifest
) VALUES (
    'test-release-membership-0026',
    'test',
    'validated',
    'test',
    'test',
    'test',
    '{"purpose":"public_mvp_preview","claim_ids":["00000000-0000-0000-0000-000000002601"]}'::jsonb
);

INSERT INTO audit.release_claim(
    release_version, claim_id, object_sha256, capture_status
) VALUES (
    'test-release-membership-0026',
    '00000000-0000-0000-0000-000000002601'::uuid,
    repeat('a',64),
    'captured_at_release'
);

INSERT INTO audit.release_manifest(
    release_version, schema_version, status, changelog, qc_summary, unresolved_issues, manifest
) VALUES (
    'test-release-membership-0026-null',
    'test',
    'validated',
    'test',
    'test',
    'test',
    '{"purpose":"public_mvp_preview","claim_ids":["00000000-0000-0000-0000-000000002601"]}'::jsonb
);

DO $$
DECLARE
    blocked boolean := false;
BEGIN
    BEGIN
        INSERT INTO audit.release_claim(
            release_version, claim_id, object_sha256, capture_status
        ) VALUES (
            'test-release-membership-0026-null',
            '00000000-0000-0000-0000-000000002601'::uuid,
            NULL,
            'captured_at_release'
        );
    EXCEPTION WHEN others THEN
        blocked := true;
    END;

    IF NOT blocked THEN
        RAISE EXCEPTION 'captured_at_release membership accepted a NULL digest';
    END IF;
END $$;


INSERT INTO audit.research_target(
    target_key, target_label, anchor_label, anchor_year, frame_class,
    origin, review_status
) VALUES (
    'TEST:RELEASE-RESULT',
    'release membership test research target',
    '1300 CE',
    1300,
    'node_site',
    'regression',
    'reviewed'
);

INSERT INTO audit.research_target_result(
    research_target_result_id, target_key, research_stage, research_outcome,
    bounded_proposition, required_abstention, content_sha256, review_status
) VALUES (
    '00000000-0000-0000-0000-000000002602'::uuid,
    'TEST:RELEASE-RESULT',
    'researched_internal',
    'RESEARCHED_INCONCLUSIVE',
    'bounded result for release membership regression',
    'do not infer absence',
    repeat('b',64),
    'reviewed'
);

INSERT INTO audit.release_research_target_result(
    release_version, research_target_result_id, object_sha256, capture_status
) VALUES (
    'test-release-membership-0026',
    '00000000-0000-0000-0000-000000002602'::uuid,
    repeat('c',64),
    'captured_at_release'
);

INSERT INTO audit.release_research_target_result(
    release_version, research_target_result_id, object_sha256, capture_status
) VALUES (
    'test-release-membership-0026-null',
    '00000000-0000-0000-0000-000000002602'::uuid,
    NULL,
    'legacy_membership_backfill'
);

DO $
DECLARE
    blocked boolean := false;
BEGIN
    BEGIN
        UPDATE audit.release_research_target_result
        SET capture_status='captured_at_release', object_sha256=NULL
        WHERE release_version='test-release-membership-0026-null'
          AND research_target_result_id='00000000-0000-0000-0000-000000002602'::uuid;
    EXCEPTION WHEN others THEN
        blocked := true;
    END;

    IF NOT blocked THEN
        RAISE EXCEPTION 'captured_at_release research-result membership accepted a NULL digest';
    END IF;
END $;

UPDATE audit.release_manifest
SET status='published'
WHERE release_version='test-release-membership-0026';

DO $$
DECLARE
    blocked boolean := false;
BEGIN
    BEGIN
        DELETE FROM audit.release_claim
        WHERE release_version='test-release-membership-0026'
          AND claim_id='00000000-0000-0000-0000-000000002601'::uuid;
    EXCEPTION WHEN others THEN
        blocked := true;
    END;

    IF NOT blocked THEN
        RAISE EXCEPTION 'published release membership was mutable';
    END IF;
END $;


DO $
DECLARE
    blocked boolean := false;
BEGIN
    BEGIN
        DELETE FROM audit.release_research_target_result
        WHERE release_version='test-release-membership-0026'
          AND research_target_result_id='00000000-0000-0000-0000-000000002602'::uuid;
    EXCEPTION WHEN others THEN
        blocked := true;
    END;

    IF NOT blocked THEN
        RAISE EXCEPTION 'published research-result release membership was mutable';
    END IF;
END $;


ROLLBACK;
