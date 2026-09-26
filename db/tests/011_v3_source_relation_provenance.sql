-- Gate 2 / D-104 regression: preserve v3 target-source provenance fields.
BEGIN;

DO $$
DECLARE
    missing text;
BEGIN
    SELECT string_agg(name, ', ')
    INTO missing
    FROM (VALUES
        ('source_id_raw'),
        ('decisive'),
        ('access_limitation'),
        ('accessed_at_text'),
        ('asset_sha256'),
        ('dependency_note')
    ) AS required(name)
    WHERE NOT EXISTS (
        SELECT 1
        FROM information_schema.columns
        WHERE table_schema='audit'
          AND table_name='research_target_source'
          AND column_name=required.name
    );

    IF missing IS NOT NULL THEN
        RAISE EXCEPTION 'Missing v3 source-relation columns: %', missing;
    END IF;
END $$;

INSERT INTO atlas.source(source_id,title,source_classification)
VALUES (
    '00000000-0000-0000-0000-000000003201'::uuid,
    'Gate 2 lossless source relation',
    'secondary_specialist'
);

INSERT INTO atlas.source_version(source_version_id,source_id,version_label,url_or_identifier)
VALUES (
    '00000000-0000-0000-0000-000000003202'::uuid,
    '00000000-0000-0000-0000-000000003201'::uuid,
    'test:v1',
    'urn:test:gate2:lossless'
);

INSERT INTO audit.research_target(
    target_key,target_label,anchor_label,frame_class,review_status
) VALUES (
    'TEST:LOSSLESS-SOURCE',
    'Gate 2 source-relation test',
    '1300 CE',
    'node_site',
    'reviewed'
);

INSERT INTO audit.research_target_result(
    research_target_result_id,target_key,research_stage,research_outcome,
    content_sha256,review_status
) VALUES (
    '00000000-0000-0000-0000-000000003203'::uuid,
    'TEST:LOSSLESS-SOURCE',
    'researched_internal',
    'BOUNDED_SUPPORTED',
    repeat('b',64),
    'reviewed'
);

INSERT INTO audit.research_target_source(
    research_target_result_id,source_version_id,source_relation_key,
    source_version_ref_raw,source_id_raw,evidence_role,independence_group,
    claim_fitness,direction_raw,normalized_direction,locator,decisive,
    access_limitation,accessed_at_text,asset_sha256,dependency_note
) VALUES (
    '00000000-0000-0000-0000-000000003203'::uuid,
    '00000000-0000-0000-0000-000000003202'::uuid,
    'TEST:LOSSLESS-SOURCE:1',
    'test:v1',
    'RAW-SOURCE-ID',
    'bounded support',
    'one-primary-family',
    'Fit only for the bounded event.',
    'supports',
    'supports',
    'p. 1',
    true,
    'Read through a modern edition.',
    '2026-09-26',
    repeat('c',64),
    'Do not count derivative editions independently.'
);

DO $$
DECLARE
    r record;
BEGIN
    SELECT * INTO r
    FROM audit.research_target_source
    WHERE research_target_result_id='00000000-0000-0000-0000-000000003203'::uuid;

    IF r.source_id_raw IS DISTINCT FROM 'RAW-SOURCE-ID'
       OR r.decisive IS DISTINCT FROM true
       OR r.access_limitation IS DISTINCT FROM 'Read through a modern edition.'
       OR r.accessed_at_text IS DISTINCT FROM '2026-09-26'
       OR r.asset_sha256 IS DISTINCT FROM repeat('c',64)
       OR r.dependency_note IS DISTINCT FROM 'Do not count derivative editions independently.'
    THEN
        RAISE EXCEPTION 'Lossless source-relation round trip failed';
    END IF;
END $$;

ROLLBACK;
