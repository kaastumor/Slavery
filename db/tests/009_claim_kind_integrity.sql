-- D-060 claim-kind integrity regression test.
BEGIN;

DO $$
DECLARE
    c uuid;
    s uuid;
    rejected boolean := false;
BEGIN
    INSERT INTO atlas.spatial_entity(entity_type_code, canonical_name, review_status)
    VALUES ('region', '__claim_kind_test_region__', 'draft')
    RETURNING spatial_entity_id INTO s;

    INSERT INTO atlas.claim(claim_kind_code, summary)
    VALUES ('actor_attribute', '__claim_kind_mismatch_negative_control__')
    RETURNING claim_id INTO c;

    BEGIN
        INSERT INTO atlas.legal_event(
            claim_id, jurisdiction_spatial_entity_id, event_type, legal_status_after
        ) VALUES (
            c, s, 'integrity_negative_control', 'unknown'
        );
    EXCEPTION WHEN OTHERS THEN
        rejected := true;
    END;

    IF NOT rejected THEN
        RAISE EXCEPTION 'mismatched actor_attribute claim was accepted as legal_event';
    END IF;
END $$;

DO $$
DECLARE
    c uuid;
    rejected boolean := false;
BEGIN
    INSERT INTO atlas.claim(claim_kind_code, summary)
    VALUES ('other', '__claim_kind_immutability_negative_control__')
    RETURNING claim_id INTO c;

    BEGIN
        UPDATE atlas.claim
        SET claim_kind_code = 'legal_event'
        WHERE claim_id = c;
    EXCEPTION WHEN OTHERS THEN
        rejected := true;
    END;

    IF NOT rejected THEN
        RAISE EXCEPTION 'claim_kind_code update was accepted after claim creation';
    END IF;
END $$;

ROLLBACK;
