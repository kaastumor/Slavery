-- Release reconstruction acceptance test.
-- This test is rollback-only and must leave no fixture data behind.

BEGIN;

DO $$
DECLARE
    missing text[];
BEGIN
    SELECT array_agg(name ORDER BY name)
    INTO missing
    FROM (
        VALUES
            ('audit.release_claim'),
            ('audit.release_actor'),
            ('audit.release_spatial_entity'),
            ('audit.release_geometry'),
            ('audit.release_spatial_relation'),
            ('audit.release_voyage'),
            ('audit.release_voyage_owner'),
            ('audit.release_voyage_finance'),
            ('audit.release_voyage_stop'),
            ('audit.release_coverage_assessment'),
            ('audit.release_artifact'),
            ('audit.release_membership_summary')
    ) expected(name)
    WHERE to_regclass(name) IS NULL;

    IF missing IS NOT NULL THEN
        RAISE EXCEPTION 'missing release reconstruction objects: %', missing;
    END IF;
END $$;

WITH s AS (
    INSERT INTO atlas.source(title, source_type, source_classification)
    VALUES ('release reconstruction fixture source', 'test', 'test')
    RETURNING source_id
),
sv AS (
    INSERT INTO atlas.source_version(source_id, version_label)
    SELECT source_id, 'fixture-v1' FROM s
    RETURNING source_version_id
),
a AS (
    INSERT INTO atlas.actor(actor_type_code, canonical_name, review_status)
    SELECT code, 'Release Fixture Actor', 'reviewed'
    FROM atlas.actor_type ORDER BY code LIMIT 1
    RETURNING actor_id
),
c AS (
    INSERT INTO atlas.claim(claim_kind_code, summary, review_status, publication_status)
    SELECT code, 'Release fixture claim', 'reviewed', 'published'
    FROM atlas.claim_kind ORDER BY code LIMIT 1
    RETURNING claim_id
),
r AS (
    INSERT INTO audit.release_manifest(
        release_version, schema_version, status, changelog, qc_summary, unresolved_issues, manifest
    )
    VALUES (
        'test-release-reconstruction',
        'draft-test',
        'draft',
        'fixture',
        'fixture',
        'none',
        '{"fixture": true}'::jsonb
    )
    RETURNING release_version
)
INSERT INTO audit.release_source_version(release_version, source_version_id)
SELECT r.release_version, sv.source_version_id FROM r CROSS JOIN sv;

INSERT INTO audit.release_actor(release_version, actor_id)
SELECT 'test-release-reconstruction', actor_id
FROM atlas.actor
WHERE canonical_name = 'Release Fixture Actor';

INSERT INTO audit.release_claim(release_version, claim_id)
SELECT 'test-release-reconstruction', claim_id
FROM atlas.claim
WHERE summary = 'Release fixture claim';

INSERT INTO audit.release_artifact(
    release_version, artifact_role, filename, checksum_sha256, size_bytes, media_type
)
VALUES (
    'test-release-reconstruction',
    'release_manifest',
    'manifest.json',
    repeat('a', 64),
    123,
    'application/json'
);

DO $$
DECLARE
    summary record;
BEGIN
    SELECT * INTO summary
    FROM audit.release_membership_summary
    WHERE release_version = 'test-release-reconstruction';

    IF summary.claim_count <> 1
       OR summary.actor_count <> 1
       OR summary.source_version_count <> 1
       OR summary.artifact_count <> 1 THEN
        RAISE EXCEPTION 'unexpected draft release membership summary: %', row_to_json(summary);
    END IF;
END $$;

UPDATE audit.release_manifest
SET status = 'validated'
WHERE release_version = 'test-release-reconstruction';

DO $$
BEGIN
    BEGIN
        INSERT INTO audit.release_artifact(
            release_version, artifact_role, filename, checksum_sha256, size_bytes
        )
        VALUES (
            'test-release-reconstruction',
            'unexpected_after_validation',
            'late.bin',
            repeat('b', 64),
            1
        );
        RAISE EXCEPTION 'release membership mutation unexpectedly succeeded after validation';
    EXCEPTION
        WHEN OTHERS THEN
            IF SQLERRM = 'release membership mutation unexpectedly succeeded after validation' THEN
                RAISE;
            END IF;
            IF position('membership is immutable' in SQLERRM) = 0 THEN
                RAISE;
            END IF;
    END;
END $$;

DO $$
BEGIN
    BEGIN
        UPDATE audit.release_manifest
        SET changelog = 'mutated after validation'
        WHERE release_version = 'test-release-reconstruction';
        RAISE EXCEPTION 'release content mutation unexpectedly succeeded after validation';
    EXCEPTION
        WHEN OTHERS THEN
            IF SQLERRM = 'release content mutation unexpectedly succeeded after validation' THEN
                RAISE;
            END IF;
            IF position('content is immutable after validation' in SQLERRM) = 0 THEN
                RAISE;
            END IF;
    END;
END $$;

UPDATE audit.release_manifest
SET status = 'published'
WHERE release_version = 'test-release-reconstruction';

UPDATE audit.release_manifest
SET status = 'archived'
WHERE release_version = 'test-release-reconstruction';

DO $$
DECLARE
    s text;
BEGIN
    SELECT status INTO s
    FROM audit.release_manifest
    WHERE release_version = 'test-release-reconstruction';

    IF s <> 'archived' THEN
        RAISE EXCEPTION 'expected archived status, found %', s;
    END IF;
END $$;

ROLLBACK;
