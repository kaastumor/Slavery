from pathlib import Path
import json
import unittest

ROOT = Path(__file__).resolve().parents[1]
FIXTURE = ROOT / "tests" / "fixtures" / "methodology" / "m1_adversarial_semantics.json"

ALLOWED_DISPOSITIONS = {"survives", "revise", "reject", "park", "experiment"}


class MethodologyAdversarialFixtureTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.fixture = json.loads(FIXTURE.read_text(encoding="utf-8"))
        cls.attacks = {item["id"]: item for item in cls.fixture["attacks"]}

    def load_case(self, attack_id):
        path = ROOT / self.attacks[attack_id]["case_path"]
        self.assertTrue(path.exists(), path)
        return json.loads(path.read_text(encoding="utf-8"))

    def test_fixture_covers_required_attack_dimensions(self):
        self.assertEqual(
            set(self.attacks),
            {
                "M1-A01", "M1-A02", "M1-A03", "M1-A04",
                "M1-A05", "M1-A06", "M1-A07", "M1-A08",
            },
        )
        for attack in self.attacks.values():
            self.assertIn(attack["disposition"], ALLOWED_DISPOSITIONS)
            self.assertTrue(attack["strongest_simpler_defense"] if "strongest_simpler_defense" in attack else attack["strongest_attack"])
            self.assertTrue(attack["discriminating_reason"])

    def test_silla_witness_separates_possible_date_window_from_duration(self):
        spec = self.load_case("M1-A03")
        claim = spec["claim"]
        self.assertEqual(claim["temporal_certainty"], "disputed")
        self.assertLess(claim["from_year"], claim["to_year"])
        self.assertIn("must not be read as a 125-year continuous observation", claim["summary"])
        self.assertEqual(self.attacks["M1-A03"]["disposition"], "revise")

    def test_silla_witness_preserves_narrow_spatial_scope(self):
        spec = self.load_case("M1-A04")
        self.assertEqual(spec["spatial_entity"]["entity_type_code"], "region")
        self.assertEqual(spec["geometry"]["accuracy_status"], "unresolved")
        self.assertIn("no whole-Silla polygon", spec["geometry"]["resolution_method"])
        self.assertEqual(self.attacks["M1-A04"]["disposition"], "revise")

    def test_baekje_witness_is_bounded_event_inside_current_practice_model(self):
        spec = self.load_case("M1-A05")
        claim = spec["claim"]
        self.assertEqual(claim["from_year"], 369)
        self.assertEqual(claim["to_year"], 369)
        self.assertEqual(claim["spatial_precision"], "polity_event")
        self.assertEqual(claim["territorial_practice"]["practice_type_code"], "slavery_enslavement")
        self.assertIn("not by itself for prevalence", claim["summary"])
        self.assertEqual(self.attacks["M1-A05"]["disposition"], "revise")

    def test_hittite_witness_contains_more_than_one_analytical_dimension(self):
        spec = self.load_case("M1-A06")
        claim = spec["claim"]
        self.assertEqual(claim["territorial_practice"]["practice_type_code"], "slavery_enslavement")
        summary = claim["summary"].lower()
        self.assertIn("priced", summary)
        self.assertIn("herdsmen", summary)
        self.assertIn("status flexibility", summary)
        self.assertEqual(self.attacks["M1-A06"]["disposition"], "revise")

    def test_mauryan_counterevidence_model_survives(self):
        spec = self.load_case("M1-A07")
        directions = {item["direction"] for item in spec["evidence"]}
        self.assertTrue({"supports", "challenges", "qualifies"} <= directions)
        self.assertEqual(spec["claim"]["territorial_practice"]["coverage_state_code"], "classified")
        self.assertEqual(self.attacks["M1-A07"]["disposition"], "survives")

    def test_maya_unresolved_geometry_restraint_survives(self):
        spec = self.load_case("M1-A08")
        self.assertEqual(spec["spatial_entity"]["entity_type_code"], "region")
        self.assertEqual(spec["geometry"]["accuracy_status"], "unresolved")
        self.assertIsNone(spec["geometry"]["geojson"])
        self.assertIn("must not be rendered as a single empire", spec["spatial_entity"]["notes"])
        self.assertEqual(self.attacks["M1-A08"]["disposition"], "survives")


if __name__ == "__main__":
    unittest.main()
