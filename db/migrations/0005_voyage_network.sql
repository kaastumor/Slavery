-- Migration 0005: voyage/network layer.
-- Internal UUIDs are distinct from source-native voyage IDs.

BEGIN;

CREATE TABLE atlas.voyage (
    voyage_id uuid PRIMARY KEY DEFAULT gen_random_uuid(),
    source_dataset text NOT NULL,
    source_native_voyage_id text NOT NULL,
    primary_source_version_id uuid NOT NULL REFERENCES atlas.source_version(source_version_id) ON DELETE RESTRICT,
    vessel_name text,
    year_arrived integer,
    year_status text,
    flag_documented text,
    flag_imputed text,
    seed_carrier_bucket text,
    carrier_bucket_basis text,
    flag_carrier_note text,
    constructed_at_raw text,
    registered_at_raw text,
    registration_year integer,
    voyage_origin_raw text,
    origin_status text,
    principal_embarkation_raw text,
    embarkation_status text,
    principal_landing_raw text,
    landing_status text,
    embarked_count integer,
    embarked_status text,
    disembarked_count integer,
    disembarked_status text,
    outcome text,
    notes text,
    review_status atlas.review_status NOT NULL DEFAULT 'draft',
    created_at timestamptz NOT NULL DEFAULT now(),
    UNIQUE(source_dataset, source_native_voyage_id),
    CONSTRAINT voyage_counts_nonnegative CHECK (
        (embarked_count IS NULL OR embarked_count >= 0)
        AND (disembarked_count IS NULL OR disembarked_count >= 0)
    )
);

CREATE INDEX voyage_year_idx ON atlas.voyage(year_arrived);
CREATE INDEX voyage_source_version_idx ON atlas.voyage(primary_source_version_id);

CREATE TABLE atlas.voyage_owner (
    voyage_owner_id uuid PRIMARY KEY DEFAULT gen_random_uuid(),
    voyage_id uuid NOT NULL REFERENCES atlas.voyage(voyage_id) ON DELETE CASCADE,
    actor_id uuid REFERENCES atlas.actor(actor_id) ON DELETE RESTRICT,
    claim_id uuid NOT NULL REFERENCES atlas.claim(claim_id) ON DELETE RESTRICT,
    raw_owner_text text,
    relationship_role text,
    owner_sequence integer,
    ownership_share numeric(12,10),
    share_status text,
    relationship_status text NOT NULL CHECK (relationship_status IN ('documented','missing_owner','disputed','inferred','other')),
    notes text,
    created_at timestamptz NOT NULL DEFAULT now(),
    CONSTRAINT voyage_owner_share_range CHECK (
        ownership_share IS NULL OR (ownership_share > 0 AND ownership_share <= 1)
    ),
    CONSTRAINT voyage_owner_missingness CHECK (
        (relationship_status = 'missing_owner' AND actor_id IS NULL)
        OR
        (relationship_status <> 'missing_owner' AND actor_id IS NOT NULL)
    )
);

CREATE INDEX voyage_owner_voyage_idx ON atlas.voyage_owner(voyage_id);
CREATE INDEX voyage_owner_actor_idx ON atlas.voyage_owner(actor_id);
CREATE INDEX voyage_owner_claim_idx ON atlas.voyage_owner(claim_id);

CREATE TABLE atlas.voyage_finance (
    voyage_finance_id uuid PRIMARY KEY DEFAULT gen_random_uuid(),
    voyage_id uuid NOT NULL REFERENCES atlas.voyage(voyage_id) ON DELETE CASCADE,
    actor_id uuid NOT NULL REFERENCES atlas.actor(actor_id) ON DELETE RESTRICT,
    claim_id uuid NOT NULL REFERENCES atlas.claim(claim_id) ON DELETE RESTRICT,
    finance_role_code text NOT NULL REFERENCES atlas.finance_role(code),
    amount numeric,
    currency_text text,
    share numeric(12,10),
    notes text,
    created_at timestamptz NOT NULL DEFAULT now(),
    CONSTRAINT voyage_finance_share_range CHECK (share IS NULL OR (share > 0 AND share <= 1))
);

CREATE INDEX voyage_finance_voyage_idx ON atlas.voyage_finance(voyage_id);
CREATE INDEX voyage_finance_actor_idx ON atlas.voyage_finance(actor_id);
CREATE INDEX voyage_finance_claim_idx ON atlas.voyage_finance(claim_id);

CREATE TABLE atlas.voyage_stop (
    voyage_stop_id uuid PRIMARY KEY DEFAULT gen_random_uuid(),
    voyage_id uuid NOT NULL REFERENCES atlas.voyage(voyage_id) ON DELETE CASCADE,
    spatial_entity_id uuid REFERENCES atlas.spatial_entity(spatial_entity_id) ON DELETE RESTRICT,
    claim_id uuid NOT NULL REFERENCES atlas.claim(claim_id) ON DELETE RESTRICT,
    stop_role_code text NOT NULL REFERENCES atlas.voyage_stop_role(code),
    stop_sequence integer,
    raw_place_text text,
    documented_or_imputed text,
    from_year integer,
    to_year integer,
    valid_years int4range GENERATED ALWAYS AS (atlas.make_year_range(from_year, to_year)) STORED,
    notes text,
    created_at timestamptz NOT NULL DEFAULT now(),
    CONSTRAINT voyage_stop_has_place CHECK (spatial_entity_id IS NOT NULL OR raw_place_text IS NOT NULL),
    CONSTRAINT voyage_stop_year_order CHECK (from_year IS NULL OR to_year IS NULL OR from_year <= to_year)
);

CREATE INDEX voyage_stop_voyage_idx ON atlas.voyage_stop(voyage_id);
CREATE INDEX voyage_stop_spatial_idx ON atlas.voyage_stop(spatial_entity_id);
CREATE INDEX voyage_stop_valid_years_gist ON atlas.voyage_stop USING gist(valid_years);

COMMIT;
