from pathlib import Path
import unittest

ROOT = Path(__file__).resolve().parents[1]
MIGRATION = (ROOT / "db" / "migrations" / "0017_precomputed_boundary_normalization.sql").read_text(encoding="utf-8")


class PrecomputedBoundaryNormalizationTests(unittest.TestCase):
    def test_cliopatria_policy_is_source_family_based(self):
        self.assertIn("cliopatria-boundary-normalization-v2", MIGRATION)
        self.assertIn("source_url_prefix", MIGRATION)
        self.assertNotIn("Achaemenid", MIGRATION)
        self.assertNotIn("Lebanon", MIGRATION)

    def test_policy_uses_bounded_smoothing(self):
        self.assertIn("smooth_iterations", MIGRATION)
        self.assertIn("35000", MIGRATION)
        self.assertIn("1.0000", MIGRATION)
        self.assertIn("st_chaikinsmoothing", MIGRATION.lower())

    def test_request_view_uses_cache_not_dynamic_normalizer(self):
        view = MIGRATION.split("CREATE OR REPLACE VIEW publish.map_geometry AS", 1)[1]
        self.assertIn("render_geometry_cache", view)
        self.assertIn("boundary_normalized_cache", view)
        self.assertNotIn("normalize_coastal_polygon(", view)
        self.assertNotIn("st_chaikinsmoothing(", view)

    def test_fallback_remains_fast_land_clip(self):
        view = MIGRATION.split("CREATE OR REPLACE VIEW publish.map_geometry AS", 1)[1]
        self.assertIn("st_intersection(g.geom, m.geom)", view)
        self.assertIn("land_clip", view)

    def test_source_geometry_is_never_updated(self):
        upper = MIGRATION.upper()
        self.assertNotIn("UPDATE ATLAS.GEOMETRY", upper)
        self.assertNotIn("UPDATE PUBLISH.GEOMETRY", upper)

    def test_cache_refresh_rejects_failed_qc(self):
        self.assertIn("area_delta_qc_failed", MIGRATION)
        self.assertIn("displacement_qc_failed", MIGRATION)
        self.assertIn("normalized_geometry_qc_failed", MIGRATION)


if __name__ == "__main__":
    unittest.main()
