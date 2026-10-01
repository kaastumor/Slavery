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
            geometry["geojson"],
            {"type": "Point", "coordinates": [66.9666667, 39.65]},
        )
        self.assertIn("carrying 60 seconds", geometry["resolution_method"])
        self.assertIn("not the exact 1404 castle", geometry["resolution_method"])
        self.assertIn("do not locate the exact 1404 castle",
                      geometry["source"]["reliability_limitations"])


if __name__ == "__main__":
    unittest.main()
