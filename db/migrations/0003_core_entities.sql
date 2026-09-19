-- Migration 0003: source provenance, actor identity, spatial identity and geometry.

BEGIN;

CREATE TABLE atlas.source (
    source_id uuid PRIMARY KEY DEFAULT gen_random_uuid(),
    title text NOT NULL,
    author_or_institution text,
    source_type text,
    source_classification text,
    language_code text,
    geographic_scope text,
    temporal_scope text,
    independence_notes text,
    reliability_limitations text,
    notes text,
    created_at timestamptz NOT NULL DEFAULT now()
);

CREATE TABLE atlas.source_version (
    source_version_id uuid PRIMARY KEY DEFAULT gen_random_uuid(),
    source_id uuid NOT NULL REFERENCES atlas.source(source_id) ON DELETE RESTRICT,
    version_label text,
    publication_or_creation_date_text text,
    publication_year integer,
    accessed_at timestamptz,
    url_or_identifier text,
    license_status text,
    redistribution_status text,
    notes text,
    created_at timestamptz NOT NULL DEFAULT now()
);

CREATE INDEX source_version_source_idx ON atlas.source_version(source_id);
CREATE INDEX source_version_url_idx ON atlas.source_version(url_or_identifier);

CREATE TABLE atlas.source_asset (
    source_asset_id uuid PRIMARY KEY DEFAULT gen_random_uuid(),
    source_version_id uuid NOT NULL REFERENCES atlas.source_version(source_version_id) ON DELETE RESTRICT,
    filename_or_object_key text NOT NULL,
    media_type text,
    checksum_sha256 text,
    storage_location text,
    redistribution_status text,
    notes text,
    created_at timestamptz NOT NULL DEFAULT now(),
    CONSTRAINT source_asset_sha256_format CHECK (
        checksum_sha256 IS NULL OR checksum_sha256 ~ '^[0-9A-Fa-f]{64}$'
    )
);

CREATE INDEX source_asset_version_idx ON atlas.source_asset(source_version_id);

CREATE TABLE atlas.actor (
    actor_id uuid PRIMARY KEY DEFAULT gen_random_uuid(),
    actor_type_code text NOT NULL REFERENCES atlas.actor_type(code),
    canonical_name text NOT NULL,
    display_name text,
    from_year integer,
    to_year integer,
    valid_years int4range GENERATED ALWAYS AS (atlas.make_year_range(from_year, to_year)) STORED,
    notes text,
    review_status atlas.review_status NOT NULL DEFAULT 'draft',
    created_at timestamptz NOT NULL DEFAULT now(),
    CONSTRAINT actor_year_order CHECK (from_year IS NULL OR to_year IS NULL OR from_year <= to_year)
);

CREATE INDEX actor_valid_years_gist ON atlas.actor USING gist(valid_years);
CREATE INDEX actor_name_idx ON atlas.actor(canonical_name);

CREATE TABLE atlas.actor_name (
    actor_name_id uuid PRIMARY KEY DEFAULT gen_random_uuid(),
    actor_id uuid NOT NULL REFERENCES atlas.actor(actor_id) ON DELETE CASCADE,
    name_text text NOT NULL,
    name_type text NOT NULL CHECK (name_type IN ('canonical', 'alias', 'source_raw', 'variant', 'other')),
    source_version_id uuid REFERENCES atlas.source_version(source_version_id) ON DELETE RESTRICT,
    language_code text,
    is_preferred boolean NOT NULL DEFAULT false,
    notes text,
    UNIQUE(actor_id, name_text, name_type, source_version_id)
);

CREATE INDEX actor_name_actor_idx ON atlas.actor_name(actor_id);

CREATE TABLE atlas.spatial_entity (
    spatial_entity_id uuid PRIMARY KEY DEFAULT gen_random_uuid(),
    entity_type_code text NOT NULL REFERENCES atlas.spatial_entity_type(code),
    canonical_name text NOT NULL,
    display_name text,
    from_year integer,
    to_year integer,
    valid_years int4range GENERATED ALWAYS AS (atlas.make_year_range(from_year, to_year)) STORED,
    notes text,
    review_status atlas.review_status NOT NULL DEFAULT 'draft',
    created_at timestamptz NOT NULL DEFAULT now(),
    CONSTRAINT spatial_entity_year_order CHECK (from_year IS NULL OR to_year IS NULL OR from_year <= to_year)
);

CREATE INDEX spatial_entity_valid_years_gist ON atlas.spatial_entity USING gist(valid_years);
CREATE INDEX spatial_entity_name_idx ON atlas.spatial_entity(canonical_name);
CREATE INDEX spatial_entity_type_idx ON atlas.spatial_entity(entity_type_code);

CREATE TABLE atlas.polity (
    spatial_entity_id uuid PRIMARY KEY REFERENCES atlas.spatial_entity(spatial_entity_id) ON DELETE CASCADE,
    polity_type text,
    source_polity_id text,
    wikidata_id text,
    seshat_id text,
    notes text
);

CREATE INDEX polity_wikidata_idx ON atlas.polity(wikidata_id);
CREATE INDEX polity_seshat_idx ON atlas.polity(seshat_id);
CREATE INDEX polity_source_id_idx ON atlas.polity(source_polity_id);

CREATE TABLE atlas.geometry (
    geometry_id uuid PRIMARY KEY DEFAULT gen_random_uuid(),
    spatial_entity_id uuid NOT NULL REFERENCES atlas.spatial_entity(spatial_entity_id) ON DELETE CASCADE,
    from_year integer,
    to_year integer,
    valid_years int4range GENERATED ALWAYS AS (atlas.make_year_range(from_year, to_year)) STORED,
    geometry_source_version_id uuid REFERENCES atlas.source_version(source_version_id) ON DELETE RESTRICT,
    geometry_source_native_id text,
    resolution_method text NOT NULL,
    accuracy_status atlas.geometry_accuracy NOT NULL,
    geom geometry(Geometry, 4326),
    notes text,
    review_status atlas.review_status NOT NULL DEFAULT 'draft',
    created_at timestamptz NOT NULL DEFAULT now(),
    CONSTRAINT geometry_year_order CHECK (from_year IS NULL OR to_year IS NULL OR from_year <= to_year),
    CONSTRAINT geometry_resolution_shape CHECK (
        (accuracy_status = 'unresolved' AND geom IS NULL)
        OR
        (accuracy_status <> 'unresolved' AND geom IS NOT NULL)
    ),
    CONSTRAINT geometry_source_required CHECK (
        geom IS NULL OR geometry_source_version_id IS NOT NULL
    ),
    CONSTRAINT geometry_valid_if_present CHECK (geom IS NULL OR ST_IsValid(geom))
);

CREATE INDEX geometry_spatial_entity_idx ON atlas.geometry(spatial_entity_id);
CREATE INDEX geometry_valid_years_gist ON atlas.geometry USING gist(valid_years);
CREATE INDEX geometry_geom_gist ON atlas.geometry USING gist(geom);

COMMIT;
