-- Migration 0018: refine Cliopatria render generalization after live visual review.
-- Two Chaikin iterations further reduce residual raster/grid stair-stepping while
-- remaining inside the D-039 QC envelope across the current MVP geometry set.

BEGIN;

SET LOCAL search_path = public, extensions, pg_catalog, cartography, atlas, publish;

UPDATE cartography.geometry_render_policy
SET active = false
WHERE source_url_prefix = 'https://github.com/Seshat-Global-History-Databank/cliopatria'
  AND active;

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
    'cliopatria-boundary-normalization-v3',
    'https://github.com/Seshat-Global-History-Databank/cliopatria',
    25000,
    2,
    35000,
    1.0000,
    4,
    true,
    'Second live-reviewed Cliopatria display policy: two Chaikin iterations further reduce residual grid stair-stepping while staying within D-039 displacement/area QC. Source geometry remains immutable.'
);

COMMIT;
