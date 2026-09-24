import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
R1 = ROOT / "programmes" / "r1"
WEB = ROOT / "web"
sys.path.insert(0, str(R1))

import build_mvp_candidate_bundle as bundle_builder  # noqa: E402


class R1MVPTemporalTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.bundle = bundle_builder.build()
        cls.temporal = cls.bundle["temporal_navigation"]
        cls.by_id = {row["target_id"]: row for row in cls.temporal["targets"]}

    def test_frozen_source_year_to_atlas_astronomical_conversion(self):
        self.assertEqual(bundle_builder.source_year_from_anchor("2000 BCE"), -2000)
        self.assertEqual(bundle_builder.source_year_from_anchor("-100"), -100)
        self.assertEqual(bundle_builder.source_year_from_anchor(-500), -500)
        self.assertEqual(bundle_builder.source_year_from_anchor("500 CE"), 500)
        self.assertEqual(bundle_builder.atlas_year_from_source(-500), -499)
        self.assertEqual(bundle_builder.atlas_year_from_source(-1), 0)
        self.assertEqual(bundle_builder.atlas_year_from_source(1), 1)
        self.assertEqual(bundle_builder.display_source_year(-500), "500 BCE")
        self.assertEqual(bundle_builder.display_source_year(-100), "100 BCE")

    def test_temporal_state_counts_cover_reviewed_and_unresearched_targets(self):
        counts = {row["id"]: row["count"] for row in self.temporal["states"]}
        self.assertEqual(
            counts,
            {
                "supported_exact_cross_section": 1,
                "supported_period_level": 3,
                "supported_near_anchor_approximate": 1,
                "unknown": 13,
                "not_applicable_aggregate": 1,
                "unassessed_not_researched": 58,
            },
        )
        self.assertEqual(sum(counts.values()), 77)

    def test_required_reviewed_examples_keep_their_precision(self):
        expected = {
            "R1:P:-2000:C:r1": "supported_period_level",       # Middle Kingdom
            "R1:N:gao_1500": "supported_near_anchor_approximate",
            "R1:L:-500:D": "supported_period_level",           # Carthage
            "R1:L:1800:A": "supported_exact_cross_section",    # U.S. census
            "R1:L:COV2:1300:B": "supported_period_level",      # Chimu
            "R1:P:500:A:r1": "unknown",                        # Teotihuacan
        }
        for target_id, state in expected.items():
            self.assertEqual(self.by_id[target_id]["state"], state, target_id)

    def test_every_target_has_one_discrete_anchor_and_display_rule(self):
        self.assertEqual(len(self.by_id), 77)
        allowed_anchor_years = {row["source_year"] for row in self.temporal["anchors"]}
        for target_id, row in self.by_id.items():
            self.assertIn(row["source_year"], allowed_anchor_years, target_id)
            self.assertTrue(row["display_anchor"], target_id)
            self.assertTrue(row["display_rule"], target_id)

    def test_frontend_uses_discrete_anchor_navigation_not_annual_truth(self):
        index = (WEB / "index.html").read_text(encoding="utf-8")
        source = (WEB / "src" / "mvp.ts").read_text(encoding="utf-8")
        self.assertIn(">Frozen anchor<", index)
        self.assertIn("discrete frozen research anchors", index)
        self.assertNotIn('aria-label="Historical year"', index)
        self.assertIn('slider.min = "0"', source)
        self.assertIn("candidate.temporal_navigation.anchors", source)
        self.assertIn("Temporal rendering guard", source)
        self.assertIn("Atlas astronomical internal year", source)


if __name__ == "__main__":
    unittest.main()
