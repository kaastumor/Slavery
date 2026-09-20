-- Migration 0016: restore low-latency map geometry after 0015.
-- 0015's dynamic geography buffers are too expensive inside the public API view.
-- Keep its policy/function definitions for follow-up precomputation work, but return
-- to the proven land-clip render path so the MVP remains available.

BEGIN;

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
    m.mask_id AS render_land_mask_id,
    NULL::text AS render_policy_id,
    NULL::integer AS render_coastal_recovery_m
FROM publish.geometry g
CROSS JOIN render_mask m;

COMMIT;
