from pathlib import Path
import json
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
        self.assertGreaterEqual(len(self.paths), 5)
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
        directions = {item["direction"] for item in spec["evidence"]}
        self.assertIn("supports", directions)
        self.assertIn("qualifies", directions)
        rie = next(item for item in spec["evidence"] if item["independence_group"] == "rie_190")
        self.assertIn("does not establish", rie["source"]["reliability_limitations"])

    def test_late_period_egypt_chattel_evidence_stops_below_p4(self):
        spec = load_spec(self.case_dir / "04_late_period_egypt_slavery.json")
        practice = spec["claim"]["territorial_practice"]
        self.assertEqual(practice["practice_level"], "P3")
        self.assertEqual(spec["geometry"]["accuracy_status"], "unresolved")
        self.assertIsNone(spec["geometry"]["geojson"])
        self.assertIn("stops below P4", practice["notes"])

    def test_sasanian_legal_richness_does_not_mechanically_become_p4(self):
        spec = load_spec(self.case_dir / "05_sasanian_iran_slavery.json")
        practice = spec["claim"]["territorial_practice"]
        self.assertEqual(practice["practice_level"], "P3")
        self.assertEqual(practice["coverage_state_code"], "classified")
        self.assertEqual(spec["claim"]["publication_status"], "unpublished")
        self.assertEqual(spec["geometry"]["accuracy_status"], "unresolved")
        self.assertIsNone(spec["geometry"]["geojson"])
        self.assertIn("stops below P4", practice["notes"])
        groups = {item["independence_group"] for item in spec["evidence"]}
        self.assertIn("macuch_sasanian_slavery", groups)
        self.assertIn("tamari_fire_foundations_2023", groups)

    def test_opone_slave_export_stays_external_to_territorial_p_levels(self):
        spec = json.loads((self.case_dir / "external_01_opone_slave_export.json").read_text(encoding="utf-8"))
        claim = spec["claim"]
        self.assertEqual(claim["claim_kind"], "external_participation")
        self.assertEqual(claim["publication_status"], "unpublished")
        self.assertNotIn("territorial_practice", claim)
        self.assertNotIn("practice_level", claim["external_participation"])
        self.assertEqual(claim["external_participation"]["participation_type_code"], "captive_export")
        self.assertEqual(spec["geometry"]["accuracy_status"], "unresolved")
        periplus = next(item for item in spec["evidence"] if item["independence_group"] == "periplus_opone")
        self.assertEqual(periplus["locator"], "section 13")

if __name__ == "__main__":
    unittest.main()
