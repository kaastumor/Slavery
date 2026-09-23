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

    def test_prototype_is_additive_noncanonical_and_legacy_bounded(self):
        self.assertEqual(self.fixture["status"], "experimental_not_canonical")
        self.assertEqual(self.fixture["legacy_release"], "v0.6.1")
        compatibility = self.fixture["compatibility"]
        self.assertTrue(compatibility["legacy_practice_level_preserved"])
        self.assertEqual(compatibility["legacy_practice_level_role"], "compatibility_only")
        self.assertFalse(compatibility["target_universal_ordinal"])
        self.assertFalse(compatibility["derive_new_dimensions_from_legacy_level"])
        self.assertFalse(compatibility["derive_p0_from_inconclusive"])
        self.assertTrue(compatibility["future_serving_requires_semantic_integration"])
        self.assertTrue(compatibility["public_preview_unchanged_during_m1"])
        self.assertFalse(compatibility["sql_migration_required_now"])

    def test_research_stage_and_outcome_are_orthogonal(self):
        disputed = self.cases["synthetic_reviewed_disputed"]
        inconclusive = self.cases["synthetic_reviewed_inconclusive"]
        self.assertEqual(disputed["research_stage"], "review_complete")
        self.assertEqual(disputed["classification_outcome"], "disputed")
        self.assertEqual(inconclusive["research_stage"], "review_complete")
        self.assertEqual(inconclusive["classification_outcome"], "inconclusive")
        self.assertIsNone(inconclusive["legacy_practice_level"])

    def test_inconclusive_does_not_create_p0(self):
        ordinary = self.cases["synthetic_reviewed_inconclusive"]
        explicit = self.cases["synthetic_explicit_legacy_p0"]
        self.assertIsNone(ordinary["legacy_practice_level"])
        self.assertEqual(explicit["legacy_practice_level"], "P0")
        self.assertTrue(explicit["legacy_p0_explicitly_reviewed"])

    def test_baekje_event_is_not_forced_to_mean_enduring_practice(self):
        case = self.cases["baekje_369"]
        source = json.loads((ROOT / case["source_case"]).read_text(encoding="utf-8"))
        self.assertEqual(source["claim"]["from_year"], 369)
        self.assertEqual(source["claim"]["to_year"], 369)
        self.assertEqual(case["assertion_form"], "event_or_process")
        self.assertEqual(case["occurrence_pattern"], "bounded_occurrence")
        self.assertEqual(case["institutionalization"], "unassessed")
        self.assertEqual(case["legacy_practice_level"], "P1")
        self.assertTrue(all(f["dimension"] == "process" for f in case["facets"]))

    def test_hittite_case_can_be_recurrent_and_institutional_simultaneously(self):
        case = self.cases["hittite_central_anatolia"]
        source = json.loads((ROOT / case["source_case"]).read_text(encoding="utf-8"))
        legacy = source["claim"]["territorial_practice"]
        self.assertEqual(legacy["practice_type_code"], "slavery_enslavement")
        self.assertEqual(legacy["practice_level"], "P2")
        self.assertEqual(case["occurrence_pattern"], "recurrent")
        self.assertEqual(case["institutionalization"], "institutional_features_supported")
        self.assertEqual(case["prevalence_scope"], "unassessed")
        self.assertEqual(case["structural_significance"], "unassessed")
        dimensions = {facet["dimension"] for facet in case["facets"]}
        self.assertEqual(dimensions, {"status", "function", "property_legal", "transmission"})

    def test_occurrence_institution_and_prevalence_do_not_force_ordering(self):
        case = self.cases["synthetic_recurrent_institutional_localized"]
        self.assertEqual(case["occurrence_pattern"], "recurrent")
        self.assertEqual(case["institutionalization"], "institutional_features_supported")
        self.assertEqual(case["prevalence_scope"], "localized")
        self.assertEqual(case["structural_significance"], "unassessed")

    def test_attestation_pattern_is_independent_from_interpretive_basis(self):
        baekje = self.cases["baekje_369"]
        synthetic = self.cases["synthetic_recurrent_institutional_localized"]
        self.assertEqual(baekje["attestation_pattern"], "single_bounded_attestation")
        self.assertEqual(baekje["interpretive_basis"], "mixed_primary_and_specialist")
        self.assertEqual(synthetic["attestation_pattern"], "multiple_independent_attestations")
        self.assertEqual(synthetic["interpretive_basis"], "specialist_synthesis")
        dimensions = self.fixture["dimensions"]
        self.assertNotIn("specialist_synthesis", dimensions["attestation_pattern"])
        self.assertNotIn("recurrent_attestation", dimensions["interpretive_basis"])


if __name__ == "__main__":
    unittest.main()
