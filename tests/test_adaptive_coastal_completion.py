from pathlib import Path
import unittest

ROOT = Path(__file__).resolve().parents[1]
MIGRATION = (ROOT / "db" / "migrations" / "0019_adaptive_coastal_completion.sql").read_text(encoding="utf-8")


class AdaptiveCoastalCompletionTests(unittest.TestCase):
    def test_policy_is_source_family_based(self):
        self.assertIn("cliopatria-boundary-normalization-v4", MIGRATION)
        self.assertIn("source_url_prefix", MIGRATION)
        self.assertNotIn("Achaemenid", MIGRATION)
        self.assertNotIn("Baekje", MIGRATION)

    def test_policy_uses_bounded_adaptive_recovery(self):
        self.assertIn("max_coastal_recovery_m", MIGRATION)
        self.assertIn("max_extra_recovery_pct", MIGRATION)
        self.assertIn("50000", MIGRATION)
        self.assertIn("2.0000", MIGRATION)
        self.assertIn("coastal_recovery_m_used", MIGRATION)
        self.assertIn("coastal_extra_area_pct", MIGRATION)

    def test_request_view_reads_cache_only(self):
        view = MIGRATION.split("CREATE OR REPLACE VIEW publish.map_geometry AS", 1)[1]
        self.assertIn("render_geometry_cache", view)
        self.assertNotIn("normalize_coastal_polygon(", view)
        self.assertNotIn("st_chaikinsmoothing(", view)

    def test_source_geometry_is_not_mutated(self):
        upper = MIGRATION.upper()
        self.assertNotIn("UPDATE ATLAS.GEOMETRY", upper)
        self.assertNotIn("UPDATE PUBLISH.GEOMETRY", upper)


if __name__ == "__main__":
    unittest.main()
