from pathlib import Path
import unittest

ROOT = Path(__file__).resolve().parents[1]
MIGRATION = (ROOT / "db" / "migrations" / "0021_external_render_policy_fallback.sql").read_text(encoding="utf-8")


class ExternalRenderPolicyFallbackTests(unittest.TestCase):
    def test_external_generator_is_explicit(self):
        self.assertIn("generator_kind", MIGRATION)
        self.assertIn("cliopatria-qgis-natural-earth-v1", MIGRATION)
        self.assertIn("'external'", MIGRATION)

    def test_postgis_refresh_does_not_generate_external_policy(self):
        fn = MIGRATION.split("CREATE OR REPLACE FUNCTION cartography.refresh_render_geometry_cache", 1)[1]
        self.assertIn("generator_kind='postgis'", fn)

    def test_public_view_prefers_available_cache_not_unpopulated_policy(self):
        view = MIGRATION.split("CREATE OR REPLACE VIEW publish.map_geometry AS", 1)[1]
        self.assertIn("JOIN cartography.render_geometry_cache c", view)
        self.assertIn("ORDER BY p.priority, p.policy_id", view)
        self.assertIn("LIMIT 1", view)

    def test_selected_real_pilot_fixture_is_present(self):
        pilot = ROOT / "data" / "cartography" / "pilots" / "achaemenid_qgis_20000m.geojson"
        self.assertTrue(pilot.exists())
        self.assertGreater(pilot.stat().st_size, 1000)

    def test_v3_remains_active_fallback(self):
        self.assertIn("cliopatria-boundary-normalization-v3", MIGRATION)
        self.assertIn("SET active=true", MIGRATION)


if __name__ == "__main__":
    unittest.main()
