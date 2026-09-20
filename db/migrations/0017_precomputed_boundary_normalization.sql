-- Migration 0017: precompute bounded render generalization for coarse historical polygons.
-- Expensive smoothing/coastline normalization is performed only during explicit cache refresh,
-- never in the public request path.

BEGIN;

SET LOCAL search_path = public, extensions, pg_catalog, cartography, atlas, publish;

ALTER TABLE cartography.geometry_render_policy
    ADD COLUMN smooth_iterations integer NOT NULL DEFAULT 0
        CHECK (smooth_iterations BETWEEN 0 AND 3),
    ADD COLUMN max_smoothing_displacement_m integer NOT NULL DEFAULT 0
        CHECK (max_smoothing_displacement_m BETWEEN 0 AND 100000),
    ADD COLUMN max_abs_area_delta_pct numeric(8,4) NOT NULL DEFAULT 0
        CHECK (max_abs_area_delta_pct BETWEEN 0 AND 10);

UPDATE cartography.geometry_render_policy
SET active = false
WHERE policy_id = 'cliopatria-coastal-normalization-v1';

INSERT INTO cartography.geometry_render_policy(
    policy_id,
    source_url_prefix,
    coastal_recovery_m,
    smooth_iterations,
    max_smoothing_displacement_m,
    max_abs_area_delta_pct,
    priority,
    active,
    notes
) VALUES (
    'cliopatria-boundary-normalization-v2',
    'https://github.com/Seshat-Global-History-Databank/cliopatria',
    25000,
    1,
    35000,
    1.0000,
    5,
    true,
    'Render-only bounded generalization for coarse/raster-derived Cliopatria polygons. One Chaikin iteration removes grid stair-stepping; coastline recovery uses the canonical land fabric. Source geometry remains immutable.'
);

CREATE TABLE cartography.render_geometry_cache (
    geometry_id uuid NOT NULL REFERENCES atlas.geometry(geometry_id) ON DELETE CASCADE,
    fabric_id text NOT NULL REFERENCES cartography.land_fabric(fabric_id) ON DELETE CASCADE,
    policy_id text NOT NULL REFERENCES cartography.geometry_render_policy(policy_id),
    geom geometry NOT NULL,
    source_npoints integer NOT NULL,
    render_npoints integer NOT NULL,
    smoothing_iterations integer NOT NULL,
    smoothing_hausdorff_m double precision NOT NULL,
    smoothing_area_delta_pct double precision NOT NULL,
    generated_at timestamptz NOT NULL DEFAULT now(),
    PRIMARY KEY (geometry_id, fabric_id, policy_id),
    CONSTRAINT render_geometry_cache_valid CHECK (st_isvalid(geom)),
    CONSTRAINT render_geometry_cache_srid CHECK (st_srid(geom) = 4326)
);

CREATE INDEX render_geometry_cache_geom_gist
ON cartography.render_geometry_cache USING gist(geom);

CREATE OR REPLACE FUNCTION cartography.refresh_render_geometry_cache(p_geometry_id uuid)
RETURNS jsonb
LANGUAGE plpgsql
SET search_path = public, extensions, pg_catalog, cartography, atlas, publish
AS $body$
DECLARE
    src record;
    fab record;
    pol record;
    smoothed geometry;
    candidate geometry;
    area_delta double precision;
    hausdorff_m double precision;
BEGIN
    SELECT
        g.geometry_id,
        g.geom,
        sv.url_or_identifier AS source_url
    INTO src
    FROM publish.geometry g
    LEFT JOIN atlas.source_version sv
      ON sv.source_version_id = g.geometry_source_version_id
    WHERE g.geometry_id = p_geometry_id;

    IF NOT FOUND THEN
        RETURN jsonb_build_object('cached', false, 'reason', 'geometry_not_found');
    END IF;

    IF src.geom IS NULL OR geometrytype(src.geom) NOT IN ('POLYGON','MULTIPOLYGON') THEN
        RETURN jsonb_build_object('cached', false, 'reason', 'not_polygonal');
    END IF;

    SELECT fabric_id, geom
    INTO fab
    FROM cartography.land_fabric
    WHERE active
    ORDER BY created_at DESC
    LIMIT 1;

    IF NOT FOUND THEN
        RETURN jsonb_build_object('cached', false, 'reason', 'no_active_land_fabric');
    END IF;

    SELECT *
    INTO pol
    FROM cartography.geometry_render_policy
    WHERE active
      AND src.source_url LIKE source_url_prefix || '%'
    ORDER BY priority, policy_id
    LIMIT 1;

    IF NOT FOUND THEN
        RETURN jsonb_build_object('cached', false, 'reason', 'no_matching_policy');
    END IF;

    smoothed := CASE
        WHEN pol.smooth_iterations > 0
            THEN st_chaikinsmoothing(src.geom, pol.smooth_iterations, false)
        ELSE src.geom
    END;

    IF NOT st_isvalid(smoothed) THEN
        RETURN jsonb_build_object('cached', false, 'reason', 'invalid_smoothed_geometry', 'policy_id', pol.policy_id);
    END IF;

    area_delta :=
        CASE
            WHEN st_area(src.geom::geography) = 0 THEN 0
            ELSE 100.0 * (
                st_area(smoothed::geography) - st_area(src.geom::geography)
            ) / st_area(src.geom::geography)
        END;

    hausdorff_m := st_hausdorffdistance(
        st_transform(smoothed, 3857),
        st_transform(src.geom, 3857)
    );

    IF abs(area_delta) > pol.max_abs_area_delta_pct THEN
        DELETE FROM cartography.render_geometry_cache
        WHERE geometry_id = p_geometry_id
          AND fabric_id = fab.fabric_id
          AND policy_id = pol.policy_id;

        RETURN jsonb_build_object(
            'cached', false,
            'reason', 'area_delta_qc_failed',
            'policy_id', pol.policy_id,
            'area_delta_pct', area_delta
        );
    END IF;

    IF hausdorff_m > pol.max_smoothing_displacement_m THEN
        DELETE FROM cartography.render_geometry_cache
        WHERE geometry_id = p_geometry_id
          AND fabric_id = fab.fabric_id
          AND policy_id = pol.policy_id;

        RETURN jsonb_build_object(
            'cached', false,
            'reason', 'displacement_qc_failed',
            'policy_id', pol.policy_id,
            'hausdorff_m', hausdorff_m
        );
    END IF;

    candidate := cartography.normalize_coastal_polygon(
        smoothed,
        fab.geom,
        pol.coastal_recovery_m
    );

    IF candidate IS NULL OR st_isempty(candidate) OR NOT st_isvalid(candidate) THEN
        DELETE FROM cartography.render_geometry_cache
        WHERE geometry_id = p_geometry_id
          AND fabric_id = fab.fabric_id
          AND policy_id = pol.policy_id;

        RETURN jsonb_build_object(
            'cached', false,
            'reason', 'normalized_geometry_qc_failed',
            'policy_id', pol.policy_id
        );
    END IF;

    INSERT INTO cartography.render_geometry_cache(
        geometry_id,
        fabric_id,
        policy_id,
        geom,
        source_npoints,
        render_npoints,
        smoothing_iterations,
        smoothing_hausdorff_m,
        smoothing_area_delta_pct,
        generated_at
    ) VALUES (
        p_geometry_id,
        fab.fabric_id,
        pol.policy_id,
        candidate,
        st_npoints(src.geom),
        st_npoints(candidate),
        pol.smooth_iterations,
        hausdorff_m,
        area_delta,
        now()
    )
    ON CONFLICT (geometry_id, fabric_id, policy_id)
    DO UPDATE SET
        geom = EXCLUDED.geom,
        source_npoints = EXCLUDED.source_npoints,
        render_npoints = EXCLUDED.render_npoints,
        smoothing_iterations = EXCLUDED.smoothing_iterations,
        smoothing_hausdorff_m = EXCLUDED.smoothing_hausdorff_m,
        smoothing_area_delta_pct = EXCLUDED.smoothing_area_delta_pct,
        generated_at = EXCLUDED.generated_at;

    RETURN jsonb_build_object(
        'cached', true,
        'policy_id', pol.policy_id,
        'fabric_id', fab.fabric_id,
        'source_npoints', st_npoints(src.geom),
        'render_npoints', st_npoints(candidate),
        'smoothing_iterations', pol.smooth_iterations,
        'hausdorff_m', hausdorff_m,
        'area_delta_pct', area_delta
    );
END;
$body$;

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
      ON sv.source_version_id = g.geometry_source_version_id
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
        WHEN c.geom IS NOT NULL THEN c.geom
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
        WHEN c.geom IS NOT NULL THEN 'boundary_normalized_cache'
        WHEN geometrytype(g.geom) IN ('POLYGON','MULTIPOLYGON') THEN 'land_clip'
        ELSE 'source_geometry'
    END AS render_transform,
    m.mask_id AS render_land_mask_id,
    CASE WHEN c.geom IS NOT NULL THEN c.policy_id ELSE NULL END AS render_policy_id,
    CASE WHEN c.geom IS NOT NULL THEN p.coastal_recovery_m ELSE NULL END AS render_coastal_recovery_m,
    CASE WHEN c.geom IS NOT NULL THEN c.smoothing_iterations ELSE NULL END AS render_smoothing_iterations,
    CASE WHEN c.geom IS NOT NULL THEN
        jsonb_build_object(
            'smoothing_hausdorff_m', c.smoothing_hausdorff_m,
            'smoothing_area_delta_pct', c.smoothing_area_delta_pct,
            'source_npoints', c.source_npoints,
            'render_npoints', c.render_npoints,
            'generated_at', c.generated_at
        )
        ELSE NULL
    END AS render_qc
FROM source_context g
CROSS JOIN render_mask m
LEFT JOIN LATERAL (
    SELECT rp.*
    FROM cartography.geometry_render_policy rp
    WHERE rp.active
      AND g.geometry_source_url LIKE rp.source_url_prefix || '%'
    ORDER BY rp.priority, rp.policy_id
    LIMIT 1
) p ON true
LEFT JOIN cartography.render_geometry_cache c
  ON c.geometry_id = g.geometry_id
 AND c.fabric_id = m.mask_id
 AND c.policy_id = p.policy_id;

COMMIT;
