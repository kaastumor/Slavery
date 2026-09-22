from pathlib import Path
import json
import unittest

ROOT = Path(__file__).resolve().parents[1]
FIXTURE = ROOT / "tests" / "fixtures" / "methodology" / "m1_semantic_split_prototype.json"


class M1SemanticSplitPrototypeTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.fixture = json.loads(FIXTURE.read_text(encoding="utf-8"))
        cls.cases = {item["id"]: item for item in cls.fixture["cases"]}

    def test_prototype_is_additive_and_noncanonical(self):
        self.assertEqual(self.fixture["status"], "experimental_not_canonical")
        self.assertEqual(self.fixture["legacy_release"], "v0.6.1")
        compatibility = self.fixture["compatibility"]
        self.assertTrue(compatibility["legacy_practice_level_preserved"])
        self.assertFalse(compatibility["derive_new_dimensions_from_legacy_level"])
        self.assertFalse(compatibility["derive_p0_from_inconclusive"])
        self.assertFalse(compatibility["sql_migration_required_now"])

    def test_research_stage_and_outcome_are_orthogonal(self):
        disputed = self.cases["synthetic_reviewed_disputed"]
        inconclusive = self.cases["synthetic_reviewed_inconclusive"]
        self.assertEqual(disputed["research_stage"], "review_complete")
        self.assertEqual(disputed["classification_outcome"], "disputed")
        self.assertEqual(inconclusive["research_stage"], "review_complete")
        self.assertEqual(inconclusive["classification_outcome"], "inconclusive")
        # Even a preserved legacy P0 cannot be treated as a derivation from outcome.
        self.assertEqual(inconclusive["legacy_practice_level"], "P0")

    def test_baekje_event_is_not_forced_to_mean_enduring_practice(self):
        case = self.cases["baekje_369"]
        source = json.loads((ROOT / case["source_case"]).read_text(encoding="utf-8"))
        self.assertEqual(source["claim"]["from_year"], 369)
        self.assertEqual(source["claim"]["to_year"], 369)
        self.assertEqual(case["assertion_form"], "event_or_process")
        self.assertEqual(case["historical_characterization"], "bounded_occurrence")
        self.assertEqual(case["legacy_practice_level"], "P1")
        self.assertTrue(all(f["dimension"] == "process" for f in case["facets"]))

    def test_hittite_case_supports_simultaneous_facets(self):
        case = self.cases["hittite_central_anatolia"]
        source = json.loads((ROOT / case["source_case"]).read_text(encoding="utf-8"))
        self.assertEqual(source["territorial_practice"]["practice_type_code"], "slavery_enslavement")
        dimensions = {facet["dimension"] for facet in case["facets"]}
        self.assertEqual(dimensions, {"status", "function", "property_legal", "transmission"})
        self.assertEqual(case["assertion_form"], "practice_or_status")
        self.assertEqual(case["legacy_practice_level"], "P3")

    def test_evidence_basis_and_historical_characterization_are_distinct(self):
        dimensions = self.fixture["dimensions"]
        self.assertIn("isolated_attestation", dimensions["evidence_basis"])
        self.assertIn("institutional", dimensions["historical_characterization"])
        self.assertNotIn("institutional", dimensions["evidence_basis"])
        self.assertNotIn("isolated_attestation", dimensions["historical_characterization"])


if __name__ == "__main__":
    unittest.main()
