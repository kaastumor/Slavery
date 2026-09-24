import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
R1 = ROOT / "programmes" / "r1"
sys.path.insert(0, str(R1))

import build_mvp_candidate_bundle as bundle_builder  # noqa: E402


class R1MVPOverviewTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.bundle = bundle_builder.build()
        cls.semantics = cls.bundle["overview_semantics"]
        cls.target_by_id = {row["target_id"]: row for row in cls.bundle["targets"]}
        cls.overview_by_id = {row["target_id"]: row for row in cls.semantics["targets"]}

    def test_research_state_mapping_is_complete_and_categorical(self):
        counts = {row["id"]: row["count"] for row in self.semantics["research_states"]}
        self.assertEqual(
            counts,
            {
                "reviewed_classified": 5,
                "reviewed_inconclusive": 14,
                "planned_unresearched": 15,
                "held": 2,
                "c0_only": 41,
            },
        )
        self.assertEqual(sum(counts.values()), 77)
        self.assertNotIn("P1", self.semantics["rule"])
        self.assertIn("not a historical intensity", self.semantics["rule"])

    def test_every_frozen_target_has_exactly_one_overview_state(self):
        self.assertEqual(len(self.overview_by_id), 77)
        self.assertEqual(set(self.overview_by_id), set(self.target_by_id))

    def test_reviewed_state_tracks_reviewed_outcome_only(self):
        for target_id, overview in self.overview_by_id.items():
            target = self.target_by_id[target_id]
            if overview["research_state"] == "reviewed_classified":
                self.assertEqual(target["release_research_state"], "c1_review_complete")
                self.assertEqual(target["classification_outcome"], "classified")
            elif overview["research_state"] == "reviewed_inconclusive":
                self.assertEqual(target["release_research_state"], "c1_review_complete")
                self.assertEqual(target["classification_outcome"], "inconclusive")

    def test_unresearched_and_held_states_remain_nonabsence(self):
        protected = {"planned_unresearched", "held", "c0_only"}
        for target_id, overview in self.overview_by_id.items():
            if overview["research_state"] in protected:
                self.assertTrue(self.target_by_id[target_id]["absence_inference_prohibited"])
                self.assertEqual(self.target_by_id[target_id]["classification_outcome"], "unassessed")

    def test_unresolved_geometry_is_explicit_and_independent(self):
        counts = {row["id"]: row["count"] for row in self.semantics["geometry_states"]}
        self.assertEqual(counts, {"unresolved_no_geometry": 77})
        self.assertTrue(all(row["geometry_state"] == "unresolved_no_geometry" for row in self.semantics["targets"]))
        geometry = self.bundle["geometry_manifest"]
        self.assertTrue(geometry["policy"]["unresolved_is_not_absence"])
        self.assertTrue(geometry["policy"]["neutral_world_land_always_visible"])
        self.assertTrue(all(row["historical_claim_effect"] == "none" for row in geometry["rows"]))


if __name__ == "__main__":
    unittest.main()
