-- Migration 0035: add a parity-first Cliopatria render policy.
-- Source geometry remains immutable. This policy intentionally removes the
-- inland/general-boundary smoothing step: it retains the exact source footprint
-- on canonical land and permits only bounded additive coastline recovery.
--
-- The policy is cache-gated by publish.map_geometry (D-046/D-116): merely
-- registering it does not replace a released render asset. A geometry uses this
-- policy only after an explicit reviewed cache row is built/promoted.

BEGIN;

SET LOCAL search_path = public, extensions, pg_catalog, cartography, atlas, publish;

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
    'cliopatria-source-land-fidelity-v1',
    'https://github.com/Seshat-Global-History-Databank/cliopatria',
    0,
    25000,
    2.0000,
    0,
    0,
    0,
    0,
    true,
    'postgis',
    'D-122 candidate: preserve exact Cliopatria source footprint on canonical land; no Chaikin/inland-boundary smoothing. Baseline recovery is 0 m. A 25 km overhang-derived recovery candidate is accepted only when added canonical land is <=2% of the zero-recovery source-land baseline; otherwise baseline is retained. Cache/promotion remains explicit and reviewed.'
)
ON CONFLICT (policy_id) DO UPDATE SET
    source_url_prefix=EXCLUDED.source_url_prefix,
    coastal_recovery_m=EXCLUDED.coastal_recovery_m,
    max_coastal_recovery_m=EXCLUDED.max_coastal_recovery_m,
    max_extra_recovery_pct=EXCLUDED.max_extra_recovery_pct,
    smooth_iterations=EXCLUDED.smooth_iterations,
    max_smoothing_displacement_m=EXCLUDED.max_smoothing_displacement_m,
    max_abs_area_delta_pct=EXCLUDED.max_abs_area_delta_pct,
    priority=EXCLUDED.priority,
    active=EXCLUDED.active,
    generator_kind=EXCLUDED.generator_kind,
    notes=EXCLUDED.notes;

COMMIT;
