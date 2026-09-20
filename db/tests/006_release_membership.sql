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
END $$;

DO $$
DECLARE
    blocked boolean := false;
BEGIN
    BEGIN
        INSERT INTO audit.release_claim(
            release_version, claim_id, object_sha256, capture_status
        ) VALUES (
            'test-release-membership-0026',
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

ROLLBACK;
