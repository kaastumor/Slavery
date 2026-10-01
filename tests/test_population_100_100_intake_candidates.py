from pathlib import Path
import json
import unittest

from tools.add_research_case import load_spec, plan


ROOT = Path(__file__).resolve().parents[1]
CANDIDATE = (
    ROOT
    / "data/research/recovery/population_100_100_intake_2026_10_01/candidates"
    / "01_samarkand_captive_skilled_forced_labour_1404.json"
)
TIMBUKTU_CANDIDATE = (
    ROOT
    / "data/research/recovery/population_100_100_intake_2026_10_01/candidates"
    / "02_timbuktu_slavery_c1509_1512.json"
)


class Population100100IntakeCandidateTests(unittest.TestCase):
    def test_samarkand_1404_is_bounded_forced_labour_without_p_level(self):
        spec = load_spec(CANDIDATE, require_case_key=True)
        candidate_plan = plan(spec)

        self.assertEqual(
            candidate_plan["case_key"],
            "atlas-100x100/samarkand/captive-skilled-forced-labour-1404-v1",
        )
        self.assertEqual(candidate_plan["claim_interval"], [1404, 1404])
        self.assertEqual(candidate_plan["practice_type"], "forced_labour")
        self.assertIsNone(candidate_plan["practice_level"])
        self.assertEqual(candidate_plan["coverage_state"], "classified")
        self.assertEqual(candidate_plan["review_status"], "reviewed")
        self.assertEqual(candidate_plan["publication_status"], "unpublished")

    def test_samarkand_sources_preserve_directness_and_dependence(self):
        spec = json.loads(CANDIDATE.read_text(encoding="utf-8"))
        evidence = spec["evidence"]

        self.assertEqual(len(evidence), 4)
        self.assertEqual(
            evidence[0]["independence_group"],
            evidence[1]["independence_group"],
        )
        self.assertEqual(
            evidence[2]["independence_group"],
            evidence[3]["independence_group"],
        )
        self.assertIn("not an independent event attestation",
                      evidence[1]["source"]["independence_notes"])
        self.assertIn("not direct corroboration",
                      evidence[2]["notes"].lower())
        self.assertIn("captives",
                      spec["claim"]["notes"].lower())

    def test_samarkand_geometry_is_navigation_context_not_castle_or_extent(self):
        spec = load_spec(CANDIDATE, require_case_key=True)
        geometry = spec["geometry"]

        self.assertEqual(geometry["accuracy_status"], "modern_proxy")
        self.assertEqual(
            geometry["source_native_id"],
            "UNESCO-WHC-603rev-002",
        )
        self.assertEqual(
            geometry["version"]["url_or_identifier"],
            "https://whc.unesco.org/en/list/603/maps/#603rev-002",
        )
        self.assertEqual(
            geometry["geojson"],
            {"type": "Point", "coordinates": [66.9666667, 39.65]},
        )
        self.assertIn("carrying 60 seconds", geometry["resolution_method"])
        self.assertIn("not the exact 1404 castle", geometry["resolution_method"])
        self.assertIn("do not locate the exact 1404 castle",
                      geometry["source"]["reliability_limitations"])

    def test_timbuktu_keeps_uncertain_time_single_lineage_and_navigation_role(self):
        spec = load_spec(TIMBUKTU_CANDIDATE, require_case_key=True)
        candidate_plan = plan(spec)

        self.assertEqual(candidate_plan["claim_interval"], [1509, 1512])
        self.assertEqual(candidate_plan["practice_type"], "slavery_enslavement")
        self.assertIsNone(candidate_plan["practice_level"])
        self.assertEqual(candidate_plan["publication_status"], "unpublished")
        self.assertEqual(spec["claim"]["temporal_precision"],
                         "approximate_disputed_visit_window")
        self.assertEqual(
            {spec["evidence"][i]["independence_group"] for i in (0, 1, 3)},
            {"leo-africanus-timbuktu-description"},
        )
        self.assertEqual(spec["evidence"][2]["direction"], "qualifies")
        self.assertIn("not a separately established market location",
                      spec["evidence"][0]["notes"])
        self.assertEqual(candidate_plan["geometry_accuracy"], "modern_proxy")
        self.assertEqual(spec["geometry"]["geojson"]["coordinates"],
                         [-2.9994444, 16.7733333])
        self.assertIn("not a sixteenth-century city boundary",
                      spec["geometry"]["resolution_method"])


if __name__ == "__main__":
    unittest.main()
