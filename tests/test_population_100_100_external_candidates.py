from pathlib import Path
import copy
import json
import sys
import unittest

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "tools"))

from validate_external_case import validate  # noqa: E402

CASE_PATH = (
    ROOT
    / "data/research/recovery/population_100_100_intake_2026_10_01/candidates"
    / "03_swahili_maritime_network_1400.json"
)


class Population100100ExternalCandidateTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.case = json.loads(CASE_PATH.read_text(encoding="utf-8"))

    def test_swahili_packet_validates_as_external_participation(self):
        validate(copy.deepcopy(self.case))
        self.assertEqual(self.case["claim_kind"], "external_participation")
        self.assertEqual(
            self.case["claim"]["external_participation"]["participation_type_code"],
            "slave_trade_network",
        )

    def test_swahili_packet_does_not_leak_into_territorial_practice(self):
        claim = self.case["claim"]
        self.assertNotIn("territorial_practice", claim)
        self.assertNotIn("practice_level", claim)
        self.assertFalse(self.case["guardrails"]["territorial_practice_inferred"])
        self.assertFalse(self.case["guardrails"]["practice_level_assigned"])

    def test_swahili_network_geometry_remains_unresolved(self):
        geometry = self.case["geometry"]
        self.assertEqual(geometry["accuracy_status"], "unresolved")
        self.assertIsNone(geometry["geojson"])
        self.assertIn("No single point", geometry["resolution_method"])
        self.assertIn("100/100 geo numerator does not advance", geometry["notes"])

    def test_swahili_sources_preserve_claim_specific_roles(self):
        evidence = self.case["evidence"]
        supports = [row for row in evidence if row["direction"] == "supports"]
        self.assertEqual(len(supports), 1)
        self.assertEqual(
            supports[0]["version"]["url_or_identifier"],
            "https://doi.org/10.1111/aman.12171",
        )
        self.assertIn(
            "node-level territorial evidence does not transfer",
            evidence[2]["notes"],
        )
        self.assertEqual(evidence[3]["direction"], "qualifies")


if __name__ == "__main__":
    unittest.main()
