-- M2 #119 disposable prototype: complete pinned Cliopatria raw/staging ingestion.
-- This is intentionally NOT a production migration. D-059 requires source-native
-- years, hierarchy and feature identity to remain distinct from atlas identities.

CREATE TABLE IF NOT EXISTS staging.cliopatria_dataset (
    dataset_key text PRIMARY KEY,
    source_version_id uuid NOT NULL REFERENCES atlas.source_version(source_version_id) ON DELETE RESTRICT,
    source_asset_id uuid NOT NULL UNIQUE REFERENCES atlas.source_asset(source_asset_id) ON DELETE RESTRICT,
    ingest_run_id uuid NOT NULL UNIQUE REFERENCES audit.ingest_run(ingest_run_id) ON DELETE RESTRICT,
    upstream_repository text NOT NULL,
    upstream_release text NOT NULL,
    upstream_commit text NOT NULL,
    upstream_path text NOT NULL,
    git_blob_sha1 text NOT NULL CHECK (git_blob_sha1 ~ '^[0-9a-f]{40}$'),
    asset_sha256 text NOT NULL CHECK (asset_sha256 ~ '^[0-9a-f]{64}$'),
    feature_count integer NOT NULL CHECK (feature_count >= 0),
    source_crs text NOT NULL,
    status text NOT NULL CHECK (status IN ('loading','completed')),
    loaded_at timestamptz,
    notes text
);

CREATE TABLE IF NOT EXISTS staging.cliopatria_feature (
    dataset_key text NOT NULL
        REFERENCES staging.cliopatria_dataset(dataset_key) ON DELETE RESTRICT,
    source_row_ordinal integer NOT NULL CHECK (source_row_ordinal > 0),
    raw_record_id uuid NOT NULL UNIQUE
        REFERENCES raw.raw_record(raw_record_id) ON DELETE RESTRICT,
    source_feature_id text,
    name_raw text,
    type_raw text,
    from_year_raw integer,
    to_year_raw integer,
    source_years int4range GENERATED ALWAYS AS (
        CASE
            WHEN from_year_raw IS NULL AND to_year_raw IS NULL THEN NULL
            ELSE int4range(
                from_year_raw,
                CASE WHEN to_year_raw IS NULL THEN NULL ELSE to_year_raw + 1 END,
                '[)'
            )
        END
    ) STORED,
    member_of_raw text,
    components_raw text,
    seshat_id_raw text,
    wikidata_raw text,
    wikipedia_raw text,
    geom geometry(Geometry, 4326),
    PRIMARY KEY (dataset_key, source_row_ordinal)
);

CREATE INDEX IF NOT EXISTS cliopatria_feature_name_idx
    ON staging.cliopatria_feature(dataset_key, name_raw);
CREATE INDEX IF NOT EXISTS cliopatria_feature_type_idx
    ON staging.cliopatria_feature(dataset_key, type_raw);
CREATE INDEX IF NOT EXISTS cliopatria_feature_source_years_gist
    ON staging.cliopatria_feature USING gist(source_years);
CREATE INDEX IF NOT EXISTS cliopatria_feature_geom_gist
    ON staging.cliopatria_feature USING gist(geom);

COMMENT ON TABLE staging.cliopatria_dataset IS
'M2 disposable integration metadata for an exact pinned Cliopatria source asset. Presence here does not approve or publish any atlas geometry.';

COMMENT ON TABLE staging.cliopatria_feature IS
'Query-oriented projection of source-native Cliopatria rows. source_row_ordinal is an atlas import locator within the exact immutable asset, not a claimed upstream semantic identifier. No row is an atlas spatial identity.';

COMMENT ON COLUMN staging.cliopatria_feature.source_years IS
'Inclusive source-native Cliopatria integer interval represented as a half-open PostgreSQL range. It is not converted to atlas astronomical-year semantics; D-059 translation happens only at selected-year query time.';
