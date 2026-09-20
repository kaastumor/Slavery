-- Migration 0019: make the canonical-land bound an explicit final invariant.
--
-- Coastal recovery and unary union are topology operations. Even when every input
-- is derived from the canonical land fabric, floating-point overlay can leave
-- tiny slivers outside that fabric. The render contract is stronger: every
-- normalized polygon must be clipped to the active canonical land geometry as
-- the final operation. Source geometry remains immutable.

BEGIN;

SET LOCAL search_path = public, extensions, pg_catalog, cartography, atlas, publish;

CREATE OR REPLACE FUNCTION cartography.normalize_coastal_polygon(
    source_geom geometry,
    land_geom geometry,
    recovery_m integer
)
RETURNS geometry
LANGUAGE sql
IMMUTABLE
PARALLEL SAFE
SET search_path = public, extensions, pg_catalog, cartography
AS $body$
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
),
assembled AS (
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
    END AS geom
    FROM kept
    RIGHT JOIN (SELECT 1 AS singleton) s ON true
    GROUP BY s.singleton
)
SELECT CASE
    WHEN assembled.geom IS NULL THEN NULL::geometry
    WHEN geometrytype(source_geom) NOT IN ('POLYGON','MULTIPOLYGON') THEN assembled.geom
    ELSE st_multi(
        st_collectionextract(
            st_intersection(assembled.geom, land_geom),
            3
        )
    )
END
FROM assembled;
$body$;

COMMIT;
