-- D-053 release-channel pointer regression test.
BEGIN;

DO $$
BEGIN
    IF to_regclass('audit.release_channel') IS NULL THEN
        RAISE EXCEPTION 'audit.release_channel is missing';
    END IF;
END $$;

INSERT INTO audit.release_manifest(
    release_version, schema_version, status, changelog, qc_summary, unresolved_issues, manifest
) VALUES
(
    'test-channel-v1', 'test', 'published', 'test', 'test', 'test',
    '{"purpose":"public_mvp_preview","claim_ids":[],"geometry_ids":[]}'::jsonb
),
(
    'test-channel-v2', 'test', 'published', 'test', 'test', 'test',
    '{"purpose":"public_mvp_preview","claim_ids":[],"geometry_ids":[]}'::jsonb
),
(
    'test-channel-draft', 'test', 'draft', 'test', 'test', 'test',
    '{"purpose":"public_mvp_preview","claim_ids":[],"geometry_ids":[]}'::jsonb
),
(
    'test-channel-wrong-purpose', 'test', 'published', 'test', 'test', 'test',
    '{"purpose":"other_preview","claim_ids":[],"geometry_ids":[]}'::jsonb
);

INSERT INTO audit.release_channel(channel_code, release_version, updated_by)
VALUES ('public_mvp_preview', 'test-channel-v1', 'ci');

UPDATE audit.release_channel
SET release_version='test-channel-v2', updated_by='ci'
WHERE channel_code='public_mvp_preview';

DO $$
DECLARE
    blocked boolean := false;
BEGIN
    BEGIN
        UPDATE audit.release_channel
        SET release_version='test-channel-draft'
        WHERE channel_code='public_mvp_preview';
    EXCEPTION WHEN others THEN
        blocked := true;
    END;

    IF NOT blocked THEN
        RAISE EXCEPTION 'draft release channel target was not blocked';
    END IF;
END $$;

DO $$
DECLARE
    blocked boolean := false;
BEGIN
    BEGIN
        UPDATE audit.release_channel
        SET release_version='test-channel-wrong-purpose'
        WHERE channel_code='public_mvp_preview';
    EXCEPTION WHEN others THEN
        blocked := true;
    END;

    IF NOT blocked THEN
        RAISE EXCEPTION 'wrong-purpose release channel target was not blocked';
    END IF;
END $$;

DO $$
DECLARE
    current_release text;
BEGIN
    SELECT release_version INTO current_release
    FROM audit.release_channel
    WHERE channel_code='public_mvp_preview';

    IF current_release <> 'test-channel-v2' THEN
        RAISE EXCEPTION 'release channel changed after rejected updates: %', current_release;
    END IF;
END $$;

ROLLBACK;
