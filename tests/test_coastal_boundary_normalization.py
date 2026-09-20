from pathlib import Path
import unittest

ROOT = Path(__file__).resolve().parents[1]
MIGRATION = (ROOT / "db" / "migrations" / "0015_coastal_boundary_normalization.sql").read_text(encoding="utf-8")
API = (ROOT / "supabase" / "functions" / "atlas-data" / "index.ts").read_text(encoding="utf-8")


class CoastalBoundaryNormalizationTests(unittest.TestCase):
    def test_policy_is_source_family_based_not_entity_specific(self):
        self.assertIn("geometry_render_policy", MIGRATION)
        self.assertIn("source_url_prefix", MIGRATION)
        self.assertIn("Seshat-Global-History-Databank/cliopatria", MIGRATION)
        self.assertNotIn("Achaemenid", MIGRATION)
        self.assertNotIn("Lebanon", MIGRATION)

    def test_source_geometry_is_not_updated(self):
        upper = MIGRATION.upper()
        self.assertNotIn("UPDATE ATLAS.GEOMETRY", upper)
        self.assertNotIn("UPDATE PUBLISH.GEOMETRY", upper)

    def test_normalization_is_land_bounded_and_render_only(self):
        self.assertIn("st_intersection(", MIGRATION.lower())
        self.assertIn("land_geom", MIGRATION)
        self.assertIn("coastal_normalize", MIGRATION)
        self.assertIn("render_policy_id", MIGRATION)
        self.assertIn("render_coastal_recovery_m", MIGRATION)

    def test_recovery_originates_from_ocean_overhang(self):
        normalized = " ".join(MIGRATION.lower().split())
        self.assertIn("st_difference(source_geom, land_geom)", normalized)
        self.assertIn("st_buffer(overhang.geom::geography, recovery_m)", normalized)

    def test_api_exposes_render_policy_metadata(self):
        self.assertIn("'render_policy_id'", API)
        self.assertIn("'render_coastal_recovery_m'", API)


if __name__ == "__main__":
    unittest.main()
