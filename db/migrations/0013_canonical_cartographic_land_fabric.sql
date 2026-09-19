-- Migration 0013: introduce one canonical cartographic land fabric.
-- Historical source geometry remains untouched. Public map geometry derives its coastline
-- from the active cartography.land_fabric, falling back to the legacy 110m mask until loaded.

BEGIN;

CREATE SCHEMA IF NOT EXISTS cartography;

CREATE TABLE cartography.land_fabric AS
SELECT
    NULL::text AS fabric_id,
    NULL::text AS source_name,
    NULL::text AS source_version,
    NULL::text AS source_url,
    NULL::text AS source_commit_sha,
    NULL::text AS source_blob_sha,
    NULL::text AS content_md5,
    NULL::text AS content_sha256,
    FALSE::boolean AS active,
    geom,
    now()::timestamptz AS created_at
FROM publish.neutral_land_mask
WHERE FALSE;

ALTER TABLE cartography.land_fabric
    ALTER COLUMN fabric_id SET NOT NULL,
    ALTER COLUMN source_name SET NOT NULL,
    ALTER COLUMN source_version SET NOT NULL,
    ALTER COLUMN source_url SET NOT NULL,
    ALTER COLUMN source_commit_sha SET NOT NULL,
    ALTER COLUMN source_blob_sha SET NOT NULL,
    ALTER COLUMN content_md5 SET NOT NULL,
    ALTER COLUMN content_sha256 SET NOT NULL,
    ALTER COLUMN active SET NOT NULL,
    ALTER COLUMN geom SET NOT NULL,
    ALTER COLUMN created_at SET NOT NULL;

ALTER TABLE cartography.land_fabric
    ADD CONSTRAINT land_fabric_pkey PRIMARY KEY (fabric_id),
    ADD CONSTRAINT land_fabric_valid CHECK (st_isvalid(geom));

CREATE UNIQUE INDEX land_fabric_one_active
ON cartography.land_fabric ((active))
WHERE active;

CREATE INDEX land_fabric_geom_gist
ON cartography.land_fabric
USING gist(geom);

CREATE OR REPLACE VIEW publish.map_geometry AS
WITH active_fabric AS (
    SELECT
        fabric_id AS mask_id,
        geom
    FROM cartography.land_fabric
    WHERE active
    ORDER BY created_at DESC
    LIMIT 1
),
render_mask AS (
    SELECT mask_id, geom
    FROM active_fabric

    UNION ALL

    SELECT
        mask_id,
        geom
    FROM publish.neutral_land_mask
    WHERE mask_id='neutral-world-land-v1'
      AND NOT EXISTS (SELECT 1 FROM active_fabric)
)
SELECT
    g.geometry_id,
    g.spatial_entity_id,
    g.from_year,
    g.to_year,
    g.valid_years,
    g.geometry_source_version_id,
    g.geometry_source_native_id,
    g.resolution_method,
    g.accuracy_status,
    CASE
        WHEN g.geom IS NULL THEN NULL
        WHEN geometrytype(g.geom) IN ('POLYGON','MULTIPOLYGON') THEN
            st_multi(
                st_collectionextract(
                    st_intersection(g.geom, m.geom),
                    3
                )
            )
        ELSE g.geom
    END AS geom,
    g.notes,
    g.review_status,
    g.created_at,
    CASE
        WHEN g.geom IS NULL THEN 'none'
        WHEN geometrytype(g.geom) IN ('POLYGON','MULTIPOLYGON')
            THEN 'land_clip'
        ELSE 'source_geometry'
    END AS render_transform,
    m.mask_id AS render_land_mask_id
FROM publish.geometry g
CROSS JOIN render_mask m;

COMMIT;
