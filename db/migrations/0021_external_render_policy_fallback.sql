-- Migration 0021: allow externally precomputed render policies with cache fallback.
-- A higher-priority standard-GIS render may coexist with the proven v3 cache.
-- publish.map_geometry selects the highest-priority ACTIVE policy that actually has
-- a cache row for the geometry, so pilot coverage cannot degrade unrelated polygons.

BEGIN;

SET LOCAL search_path = public, extensions, pg_catalog, cartography, atlas, publish;

ALTER TABLE cartography.geometry_render_policy
    ADD COLUMN generator_kind text NOT NULL DEFAULT 'postgis'
        CHECK (generator_kind IN ('postgis','external'));

UPDATE cartography.geometry_render_policy
SET generator_kind='postgis';

INSERT INTO cartography.geometry_render_policy(
    policy_id,
    source_url_prefix,
    coastal_recovery_m,
    max_coastal_recovery_m,
    max_extra_recovery_pct,
    smooth_iterations,
    max_smoothing_displacement_m,
    max_abs_area_delta_pct,
    priority,
    active,
    generator_kind,
    notes
) VALUES (
    'cliopatria-qgis-natural-earth-v1',
    'https://github.com/Seshat-Global-History-Databank/cliopatria',
    0,
    0,
    0,
    0,
    0,
    0,
    1,
    true,
    'external',
    'Offline standard-GIS render pilot: QGIS smoothing, reference-layer snapping to the canonical Natural Earth 1:10m land fabric, geometry repair, and final clipping. Source geometry is immutable. Only geometries with an explicit external cache row use this policy; all others fall back to the next populated active policy.'
)
ON CONFLICT (policy_id) DO UPDATE SET
    active=EXCLUDED.active,
    priority=EXCLUDED.priority,
    generator_kind=EXCLUDED.generator_kind,
    notes=EXCLUDED.notes;

-- Keep v3 available as the populated safe fallback.
UPDATE cartography.geometry_render_policy
SET active=true
WHERE policy_id='cliopatria-boundary-normalization-v3';

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
    baseline geometry;
    candidate geometry;
    best_candidate geometry;
    area_delta double precision;
    hausdorff_m double precision;
    extra_pct double precision;
    best_extra_pct double precision := 0;
    chosen_recovery_m integer;
    recovery_try integer;
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
      AND generator_kind='postgis'
      AND src.source_url LIKE source_url_prefix || '%'
    ORDER BY priority, policy_id
    LIMIT 1;

    IF NOT FOUND THEN
        RETURN jsonb_build_object('cached', false, 'reason', 'no_matching_postgis_policy');
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

    baseline := cartography.normalize_coastal_polygon(
        smoothed,
        fab.geom,
        pol.coastal_recovery_m
    );

    IF baseline IS NULL OR st_isempty(baseline) OR NOT st_isvalid(baseline) THEN
        RETURN jsonb_build_object(
            'cached', false,
            'reason', 'baseline_coastal_normalization_failed',
            'policy_id', pol.policy_id
        );
    END IF;

    best_candidate := baseline;
    chosen_recovery_m := pol.coastal_recovery_m;

    IF pol.max_coastal_recovery_m > pol.coastal_recovery_m
       AND pol.max_extra_recovery_pct > 0 THEN
        FOREACH recovery_try IN ARRAY ARRAY[
            pol.max_coastal_recovery_m,
            40000,
            35000,
            30000
        ]
        LOOP
            IF recovery_try <= pol.coastal_recovery_m
               OR recovery_try > pol.max_coastal_recovery_m THEN
                CONTINUE;
            END IF;

            candidate := cartography.normalize_coastal_polygon(
                smoothed,
                fab.geom,
                recovery_try
            );

            IF candidate IS NULL OR st_isempty(candidate) OR NOT st_isvalid(candidate) THEN
                CONTINUE;
            END IF;

            extra_pct :=
                CASE
                    WHEN st_area(baseline::geography) = 0 THEN 0
                    ELSE 100.0 *
                        st_area(st_difference(candidate, baseline)::geography)
                        / st_area(baseline::geography)
                END;

            IF extra_pct <= pol.max_extra_recovery_pct THEN
                best_candidate := candidate;
                best_extra_pct := extra_pct;
                chosen_recovery_m := recovery_try;
                EXIT;
            END IF;
        END LOOP;
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
        coastal_recovery_m_used,
        coastal_extra_area_pct,
        generated_at
    ) VALUES (
        p_geometry_id,
        fab.fabric_id,
        pol.policy_id,
        best_candidate,
        st_npoints(src.geom),
        st_npoints(best_candidate),
        pol.smooth_iterations,
        hausdorff_m,
        area_delta,
        chosen_recovery_m,
        best_extra_pct,
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
        coastal_recovery_m_used = EXCLUDED.coastal_recovery_m_used,
        coastal_extra_area_pct = EXCLUDED.coastal_extra_area_pct,
        generated_at = EXCLUDED.generated_at;

    RETURN jsonb_build_object(
        'cached', true,
        'policy_id', pol.policy_id,
        'fabric_id', fab.fabric_id,
        'source_npoints', st_npoints(src.geom),
        'render_npoints', st_npoints(best_candidate),
        'smoothing_iterations', pol.smooth_iterations,
        'hausdorff_m', hausdorff_m,
        'area_delta_pct', area_delta,
        'coastal_recovery_m_used', chosen_recovery_m,
        'coastal_extra_area_pct', best_extra_pct
    );
END;
$body$;

CREATE OR REPLACE VIEW publish.map_geometry AS
WITH active_fabric AS (
    SELECT fabric_id AS mask_id, geom
    FROM cartography.land_fabric
    WHERE active
    ORDER BY created_at DESC
    LIMIT 1
),
render_mask AS (
    SELECT mask_id, geom FROM active_fabric
    UNION ALL
    SELECT mask_id, geom
    FROM publish.neutral_land_mask
    WHERE mask_id='neutral-world-land-v1'
      AND NOT EXISTS (SELECT 1 FROM active_fabric)
),
source_context AS (
    SELECT g.*, sv.url_or_identifier AS geometry_source_url
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
        WHEN rc.geom IS NOT NULL THEN rc.geom
        WHEN geometrytype(g.geom) IN ('POLYGON','MULTIPOLYGON') THEN
            st_multi(st_collectionextract(st_intersection(g.geom, m.geom), 3))
        ELSE g.geom
    END AS geom,
    g.notes,
    g.review_status,
    g.created_at,
    CASE
        WHEN g.geom IS NULL THEN 'none'
        WHEN rc.geom IS NOT NULL THEN 'boundary_normalized_cache'
        WHEN geometrytype(g.geom) IN ('POLYGON','MULTIPOLYGON') THEN 'land_clip'
        ELSE 'source_geometry'
    END AS render_transform,
    m.mask_id AS render_land_mask_id,
    rc.policy_id AS render_policy_id,
    rc.coastal_recovery_m_used AS render_coastal_recovery_m,
    rc.smoothing_iterations AS render_smoothing_iterations,
    CASE WHEN rc.geom IS NOT NULL THEN
        jsonb_build_object(
            'generator_kind', rc.generator_kind,
            'smoothing_hausdorff_m', rc.smoothing_hausdorff_m,
            'smoothing_area_delta_pct', rc.smoothing_area_delta_pct,
            'coastal_extra_area_pct', rc.coastal_extra_area_pct,
            'source_npoints', rc.source_npoints,
            'render_npoints', rc.render_npoints,
            'generated_at', rc.generated_at
        )
        ELSE NULL
    END AS render_qc
FROM source_context g
CROSS JOIN render_mask m
LEFT JOIN LATERAL (
    SELECT
        c.geom,
        c.policy_id,
        c.coastal_recovery_m_used,
        c.smoothing_iterations,
        c.smoothing_hausdorff_m,
        c.smoothing_area_delta_pct,
        c.coastal_extra_area_pct,
        c.source_npoints,
        c.render_npoints,
        c.generated_at,
        p.generator_kind
    FROM cartography.geometry_render_policy p
    JOIN cartography.render_geometry_cache c
      ON c.geometry_id = g.geometry_id
     AND c.fabric_id = m.mask_id
     AND c.policy_id = p.policy_id
    WHERE p.active
      AND g.geometry_source_url LIKE p.source_url_prefix || '%'
    ORDER BY p.priority, p.policy_id
    LIMIT 1
) rc ON true;

COMMIT;
