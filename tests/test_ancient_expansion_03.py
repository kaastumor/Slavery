from pathlib import Path
import sys
import unittest

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "tools"))

from add_research_case import load_spec  # noqa: E402


class AncientExpansionBatch03Tests(unittest.TestCase):
    def setUp(self):
        self.case_dir = ROOT / "data" / "research" / "ancient_expansion_03"
        self.paths = sorted(self.case_dir.glob("[0-9][0-9]_*.json"))

    def test_current_cases_validate_and_remain_unpublished(self):
        self.assertGreaterEqual(len(self.paths), 2)
        for path in self.paths:
            with self.subTest(path=path.name):
                spec = load_spec(path)
                claim = spec["claim"]
                self.assertEqual(claim.get("review_status"), "reviewed")
                self.assertIn(claim.get("publication_status"), (None, "unpublished"))
                self.assertTrue(spec["evidence"])

    def test_south_arabia_is_not_given_a_false_polity_polygon(self):
        spec = load_spec(self.case_dir / "01_south_arabia_slavery.json")
        self.assertEqual(spec["spatial_entity"]["entity_type_code"], "region")
        self.assertEqual(spec["geometry"]["accuracy_status"], "unresolved")
        self.assertIsNone(spec["geometry"]["geojson"])

    def test_carthage_institutional_classification_stops_below_p4(self):
        spec = load_spec(self.case_dir / "02_punic_carthage_slavery.json")
        practice = spec["claim"]["territorial_practice"]
        self.assertEqual(practice["practice_level"], "P3")
        self.assertEqual(practice["coverage_state_code"], "classified")
        self.assertEqual(spec["geometry"]["accuracy_status"], "unresolved")


if __name__ == "__main__":
    unittest.main()
