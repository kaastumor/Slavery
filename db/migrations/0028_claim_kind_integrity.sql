-- Migration 0028: enforce semantic claim-kind integrity at subtype/relationship boundaries.
-- D-060: claim kind is immutable; subtype/relationship rows must reference the matching claim kind.

BEGIN;

CREATE OR REPLACE FUNCTION atlas.enforce_claim_kind()
RETURNS trigger
LANGUAGE plpgsql
SET search_path = ''
AS $$
DECLARE
    expected_kind text := TG_ARGV[0];
    actual_kind text;
BEGIN
    IF NEW.claim_id IS NULL THEN
        RETURN NEW;
    END IF;

    SELECT c.claim_kind_code
      INTO actual_kind
      FROM atlas.claim c
     WHERE c.claim_id = NEW.claim_id;

    IF actual_kind IS NULL THEN
        RAISE EXCEPTION 'Claim % does not exist for %.%', NEW.claim_id, TG_TABLE_SCHEMA, TG_TABLE_NAME;
    END IF;

    IF actual_kind IS DISTINCT FROM expected_kind THEN
        RAISE EXCEPTION 'Claim-kind mismatch for %.%: claim % has kind %, expected %',
            TG_TABLE_SCHEMA, TG_TABLE_NAME, NEW.claim_id, actual_kind, expected_kind;
    END IF;

    RETURN NEW;
END;
$$;

CREATE OR REPLACE FUNCTION atlas.prevent_claim_kind_change()
RETURNS trigger
LANGUAGE plpgsql
SET search_path = ''
AS $$
BEGIN
    IF NEW.claim_kind_code IS DISTINCT FROM OLD.claim_kind_code THEN
        RAISE EXCEPTION 'claim_kind_code is immutable for claim % (% -> %); supersede with a new claim instead',
            OLD.claim_id, OLD.claim_kind_code, NEW.claim_kind_code;
    END IF;
    RETURN NEW;
END;
$$;

CREATE TRIGGER claim_kind_immutable
BEFORE UPDATE OF claim_kind_code ON atlas.claim
FOR EACH ROW EXECUTE FUNCTION atlas.prevent_claim_kind_change();

CREATE TRIGGER territorial_practice_claim_kind_check
BEFORE INSERT OR UPDATE OF claim_id ON atlas.territorial_practice_claim
FOR EACH ROW EXECUTE FUNCTION atlas.enforce_claim_kind('territorial_practice');

CREATE TRIGGER legal_event_claim_kind_check
BEFORE INSERT OR UPDATE OF claim_id ON atlas.legal_event
FOR EACH ROW EXECUTE FUNCTION atlas.enforce_claim_kind('legal_event');

CREATE TRIGGER actor_attribute_claim_kind_check
BEFORE INSERT OR UPDATE OF claim_id ON atlas.actor_attribute_claim
FOR EACH ROW EXECUTE FUNCTION atlas.enforce_claim_kind('actor_attribute');

CREATE TRIGGER external_participation_claim_kind_check
BEFORE INSERT OR UPDATE OF claim_id ON atlas.external_participation_claim
FOR EACH ROW EXECUTE FUNCTION atlas.enforce_claim_kind('external_participation');

CREATE TRIGGER spatial_relation_claim_kind_check
BEFORE INSERT OR UPDATE OF claim_id ON atlas.spatial_relation
FOR EACH ROW EXECUTE FUNCTION atlas.enforce_claim_kind('spatial_relation');

CREATE TRIGGER voyage_owner_claim_kind_check
BEFORE INSERT OR UPDATE OF claim_id ON atlas.voyage_owner
FOR EACH ROW EXECUTE FUNCTION atlas.enforce_claim_kind('voyage_owner');

CREATE TRIGGER voyage_finance_claim_kind_check
BEFORE INSERT OR UPDATE OF claim_id ON atlas.voyage_finance
FOR EACH ROW EXECUTE FUNCTION atlas.enforce_claim_kind('voyage_finance');

CREATE TRIGGER voyage_stop_claim_kind_check
BEFORE INSERT OR UPDATE OF claim_id ON atlas.voyage_stop
FOR EACH ROW EXECUTE FUNCTION atlas.enforce_claim_kind('voyage_stop');

COMMIT;
