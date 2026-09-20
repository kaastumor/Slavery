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
        self.assertGreaterEqual(len(self.paths), 3)
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

    def test_aksum_distinguishes_slavery_from_captive_taking_and_trade(self):
        spec = load_spec(self.case_dir / "03_aksumite_slavery.json")
        practice = spec["claim"]["territorial_practice"]
        self.assertEqual(practice["practice_level"], "P2")
        self.assertEqual(practice["coverage_state_code"], "classified")
        self.assertEqual(spec["geometry"]["accuracy_status"], "unresolved")
        directions = {item["direction"] for item in spec["evidence"]}
        self.assertIn("supports", directions)
        self.assertIn("qualifies", directions)
        rie = next(item for item in spec["evidence"] if item["independence_group"] == "rie_190")
        self.assertIn("does not establish", rie["source"]["reliability_limitations"])


if __name__ == "__main__":
    unittest.main()
