-- Migration 0015: normalize physical coastlines for coarse historical source families.
-- Source geometry remains immutable. This transformation is publication/render-only.

BEGIN;

CREATE TABLE cartography.geometry_render_policy (
    policy_id text PRIMARY KEY,
    source_url_prefix text NOT NULL,
    coastal_recovery_m integer NOT NULL CHECK (coastal_recovery_m BETWEEN 0 AND 100000),
    priority integer NOT NULL DEFAULT 100,
    active boolean NOT NULL DEFAULT true,
    notes text,
    created_at timestamptz NOT NULL DEFAULT now()
);

INSERT INTO cartography.geometry_render_policy(
    policy_id,
    source_url_prefix,
    coastal_recovery_m,
    priority,
    notes
) VALUES (
    'cliopatria-coastal-normalization-v1',
    'https://github.com/Seshat-Global-History-Databank/cliopatria',
    25000,
    10,
    'Render-only physical-coastline normalization for coarse/raster-derived Cliopatria polygons. Inland historical frontiers remain source-derived; canonical source geometry is unchanged.'
);

CREATE OR REPLACE FUNCTION cartography.normalize_coastal_polygon(
    source_geom geometry,
    land_geom geometry,
    recovery_m integer
)
RETURNS geometry
LANGUAGE sql
IMMUTABLE
PARALLEL SAFE
AS $$
WITH base AS (
    SELECT st_collectionextract(st_intersection(source_geom, land_geom), 3) AS geom
),
overhang AS (
    SELECT st_collectionextract(st_difference(source_geom, land_geom), 3) AS geom
),
recovery AS (
    SELECT CASE
        WHEN source_geom IS NULL
          OR land_geom IS NULL
          OR recovery_m <= 0
          OR st_isempty(overhang.geom)
        THEN NULL::geometry
        ELSE st_collectionextract(
            st_intersection(
                land_geom,
                st_buffer(overhang.geom::geography, recovery_m)::geometry
            ),
            3
        )
    END AS geom
    FROM overhang
),
merged AS (
    SELECT CASE
        WHEN recovery.geom IS NULL OR st_isempty(recovery.geom) THEN base.geom
        ELSE st_collectionextract(
            st_unaryunion(st_collect(base.geom, recovery.geom)),
            3
        )
    END AS geom,
    base.geom AS base_geom
    FROM base, recovery
),
parts AS (
    SELECT (st_dump(merged.geom)).geom AS geom, merged.base_geom
    FROM merged
    WHERE merged.geom IS NOT NULL AND NOT st_isempty(merged.geom)
),
kept AS (
    SELECT geom
    FROM parts
    WHERE st_intersects(geom, base_geom)
)
SELECT CASE
    WHEN source_geom IS NULL OR land_geom IS NULL THEN NULL::geometry
    WHEN geometrytype(source_geom) NOT IN ('POLYGON','MULTIPOLYGON') THEN source_geom
    WHEN NOT EXISTS (SELECT 1 FROM kept) THEN st_multi((SELECT geom FROM base))
    ELSE st_multi(
        st_collectionextract(
            st_unaryunion(st_collect(geom)),
            3
        )
    )
END
FROM kept
RIGHT JOIN (SELECT 1 AS singleton) s ON true
GROUP BY s.singleton;
$$;

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
),
source_context AS (
    SELECT
        g.*,
        sv.url_or_identifier AS geometry_source_url
    FROM publish.geometry g
    LEFT JOIN atlas.source_version sv
      ON sv.source_version_id=g.geometry_source_version_id
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
        WHEN geometrytype(g.geom) IN ('POLYGON','MULTIPOLYGON') AND p.policy_id IS NOT NULL THEN
            cartography.normalize_coastal_polygon(
                g.geom,
                m.geom,
                p.coastal_recovery_m
            )
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
        WHEN geometrytype(g.geom) IN ('POLYGON','MULTIPOLYGON') AND p.policy_id IS NOT NULL
            THEN 'coastal_normalize'
        WHEN geometrytype(g.geom) IN ('POLYGON','MULTIPOLYGON')
            THEN 'land_clip'
        ELSE 'source_geometry'
    END AS render_transform,
    m.mask_id AS render_land_mask_id,
    p.policy_id AS render_policy_id,
    p.coastal_recovery_m AS render_coastal_recovery_m
FROM source_context g
CROSS JOIN render_mask m
LEFT JOIN LATERAL (
    SELECT rp.policy_id, rp.coastal_recovery_m
    FROM cartography.geometry_render_policy rp
    WHERE rp.active
      AND g.geometry_source_url LIKE rp.source_url_prefix || '%'
    ORDER BY rp.priority, rp.policy_id
    LIMIT 1
) p ON true;

COMMIT;
