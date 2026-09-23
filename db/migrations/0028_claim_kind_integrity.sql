-- Migration 0028: enforce semantic compatibility between universal claims and typed subtype/relationship rows.
-- D-060: claim kind is structural and immutable; corrections supersede with a new claim.

create or replace function atlas.enforce_claim_kind()
returns trigger
language plpgsql
set search_path = ''
as $$
declare
    expected_kind text := TG_ARGV[0];
    actual_kind text;
begin
    if NEW.claim_id is null then
        return NEW;
    end if;

    select c.claim_kind_code
      into actual_kind
      from atlas.claim c
     where c.claim_id = NEW.claim_id;

    if actual_kind is null then
        raise exception 'Claim % does not exist for %.%', NEW.claim_id, TG_TABLE_SCHEMA, TG_TABLE_NAME;
    end if;

    if actual_kind is distinct from expected_kind then
        raise exception 'Claim-kind mismatch for %.%: claim % has kind %, expected %',
            TG_TABLE_SCHEMA, TG_TABLE_NAME, NEW.claim_id, actual_kind, expected_kind;
    end if;

    return NEW;
end;
$$;

create or replace function atlas.prevent_claim_kind_change()
returns trigger
language plpgsql
set search_path = ''
as $$
begin
    if NEW.claim_kind_code is distinct from OLD.claim_kind_code then
        raise exception 'claim_kind_code is immutable for claim % (% -> %); supersede with a new claim instead',
            OLD.claim_id, OLD.claim_kind_code, NEW.claim_kind_code;
    end if;
    return NEW;
end;
$$;

create trigger claim_kind_immutable
before update of claim_kind_code on atlas.claim
for each row execute function atlas.prevent_claim_kind_change();

create trigger territorial_practice_claim_kind_check
before insert or update of claim_id on atlas.territorial_practice_claim
for each row execute function atlas.enforce_claim_kind('territorial_practice');

create trigger legal_event_claim_kind_check
before insert or update of claim_id on atlas.legal_event
for each row execute function atlas.enforce_claim_kind('legal_event');

create trigger actor_attribute_claim_kind_check
before insert or update of claim_id on atlas.actor_attribute_claim
for each row execute function atlas.enforce_claim_kind('actor_attribute');

create trigger external_participation_claim_kind_check
before insert or update of claim_id on atlas.external_participation_claim
for each row execute function atlas.enforce_claim_kind('external_participation');

create trigger spatial_relation_claim_kind_check
before insert or update of claim_id on atlas.spatial_relation
for each row execute function atlas.enforce_claim_kind('spatial_relation');

create trigger voyage_owner_claim_kind_check
before insert or update of claim_id on atlas.voyage_owner
for each row execute function atlas.enforce_claim_kind('voyage_owner');

create trigger voyage_finance_claim_kind_check
before insert or update of claim_id on atlas.voyage_finance
for each row execute function atlas.enforce_claim_kind('voyage_finance');

create trigger voyage_stop_claim_kind_check
before insert or update of claim_id on atlas.voyage_stop
for each row execute function atlas.enforce_claim_kind('voyage_stop');
