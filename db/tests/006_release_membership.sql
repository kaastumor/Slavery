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

DO $$
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
END $$;

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
        DELETE FROM audit.release_research_target_result
        WHERE release_version='test-release-membership-0026'
          AND research_target_result_id='00000000-0000-0000-0000-000000002602'::uuid;
    EXCEPTION WHEN others THEN
        blocked := true;
    END;

    IF NOT blocked THEN
        RAISE EXCEPTION 'published research-result release membership was mutable';
    END IF;
END $$;


DO $
DECLARE
    blocked boolean := false;
BEGIN
    IF NOT EXISTS (
        SELECT 1
        FROM pg_trigger
        WHERE tgrelid='audit.release_manifest'::regclass
          AND tgname='release_manifest_immutable'
          AND NOT tgisinternal
    ) THEN
        RAISE EXCEPTION 'release_manifest_immutable trigger is missing';
    END IF;

    BEGIN
        UPDATE audit.release_manifest
        SET qc_summary='tampered after publication'
        WHERE release_version='test-release-membership-0026';
    EXCEPTION WHEN others THEN
        blocked := true;
    END;

    IF NOT blocked THEN
        RAISE EXCEPTION 'published release manifest metadata was mutable';
    END IF;
END $;

-- Archival is a lifecycle label only. It must not rewrite any historical metadata.
UPDATE audit.release_manifest
SET status='archived'
WHERE release_version='test-release-membership-0026'
  AND status='published';

DO $
DECLARE
    blocked_update boolean := false;
    blocked_delete boolean := false;
    archived_status text;
BEGIN
    SELECT status INTO archived_status
    FROM audit.release_manifest
    WHERE release_version='test-release-membership-0026';

    IF archived_status <> 'archived' THEN
        RAISE EXCEPTION 'metadata-identical published -> archived transition failed';
    END IF;

    BEGIN
        UPDATE audit.release_manifest
        SET changelog='tampered after archival'
        WHERE release_version='test-release-membership-0026';
    EXCEPTION WHEN others THEN
        blocked_update := true;
    END;

    BEGIN
        DELETE FROM audit.release_manifest
        WHERE release_version='test-release-membership-0026';
    EXCEPTION WHEN others THEN
        blocked_delete := true;
    END;

    IF NOT blocked_update THEN
        RAISE EXCEPTION 'archived release manifest metadata was mutable';
    END IF;
    IF NOT blocked_delete THEN
        RAISE EXCEPTION 'archived release manifest was deletable';
    END IF;
END $;


ROLLBACK;
