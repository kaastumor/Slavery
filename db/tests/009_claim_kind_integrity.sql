-- D-060 claim-kind integrity regression test.
BEGIN;

INSERT INTO atlas.spatial_entity(
    spatial_entity_id, entity_type_code, canonical_name, review_status
) VALUES (
    '00000000-0000-0000-0000-000000002801'::uuid,
    'other',
    'claim-kind integrity test place',
    'draft'
);

INSERT INTO atlas.claim(
    claim_id, claim_kind_code, summary, review_status, publication_status
) VALUES (
    '00000000-0000-0000-0000-000000002802'::uuid,
    'territorial_practice',
    'claim-kind integrity territorial claim',
    'draft',
    'unpublished'
);

INSERT INTO atlas.territorial_practice_claim(
    claim_id, spatial_entity_id, practice_type_code, practice_level, coverage_state_code
) VALUES (
    '00000000-0000-0000-0000-000000002802'::uuid,
    '00000000-0000-0000-0000-000000002801'::uuid,
    (select code from atlas.practice_type order by code limit 1),
    'P1',
    (select code from atlas.coverage_state order by code limit 1)
);

DO $$
DECLARE
    blocked boolean := false;
BEGIN
    BEGIN
        INSERT INTO atlas.legal_event(
            claim_id, jurisdiction_spatial_entity_id, event_type, legal_status_after
        ) VALUES (
            '00000000-0000-0000-0000-000000002802'::uuid,
            '00000000-0000-0000-0000-000000002801'::uuid,
            'negative_control',
            'unknown'
        );
    EXCEPTION WHEN others THEN
        IF SQLERRM LIKE 'Claim-kind mismatch%' THEN
            blocked := true;
        ELSE
            RAISE;
        END IF;
    END;

    IF NOT blocked THEN
        RAISE EXCEPTION 'wrong-kind legal_event insert was accepted';
    END IF;
END $$;

DO $$
DECLARE
    blocked boolean := false;
BEGIN
    BEGIN
        UPDATE atlas.claim
        SET claim_kind_code = 'legal_event'
        WHERE claim_id = '00000000-0000-0000-0000-000000002802'::uuid;
    EXCEPTION WHEN others THEN
        IF SQLERRM LIKE 'claim_kind_code is immutable%' THEN
            blocked := true;
        ELSE
            RAISE;
        END IF;
    END;

    IF NOT blocked THEN
        RAISE EXCEPTION 'claim_kind_code mutation was accepted';
    END IF;
END $$;

ROLLBACK;
