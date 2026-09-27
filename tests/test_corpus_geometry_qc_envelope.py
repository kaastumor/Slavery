from pathlib import Path
import json
import unittest

ROOT = Path(__file__).resolve().parents[1]
POLICY = ROOT / "config" / "cartography" / "corpus_geometry_qc_envelope.json"
REVIEW = (
    ROOT
    / "data"
    / "research"
    / "geometry_reviews"
    / "overnight_2026_09_27_corpus_qc_review.json"
)
TOPOLOGY = (
    ROOT
    / "data"
    / "research"
    / "geometry_reviews"
    / "v081_corpus_topology_snapshot.json"
)


class CorpusGeometryQcEnvelopeTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.policy = json.loads(POLICY.read_text(encoding="utf-8"))
        cls.review = json.loads(REVIEW.read_text(encoding="utf-8"))
        cls.topology = json.loads(TOPOLOGY.read_text(encoding="utf-8"))

    def test_envelope_has_no_weighted_score(self) -> None:
        self.assertTrue(self.policy["principles"]["weighted_overall_score_forbidden"])
        self.assertTrue(self.review["envelope"]["no_weighted_score"])

    def test_land_alignment_is_only_one_axis(self) -> None:
        axes = set(self.policy["required_axes"])
        self.assertIn("canonical_land_residual", axes)
        self.assertIn("source_to_render_hausdorff_displacement", axes)
        self.assertIn("component_and_ring_topology", axes)
        self.assertIn("temporal_family_consistency", axes)
        self.assertEqual(
            self.policy["hard_gates"]["max_render_outside_land_pct"],
            0.0001,
        )

    def test_new_candidate_displacement_ceiling_is_35km(self) -> None:
        self.assertEqual(self.policy["candidate_gates"]["max_hausdorff_m"], 35000)
        self.assertTrue(self.policy["candidate_gates"]["visual_review_required"])

    def test_v081_topology_snapshot_covers_all_release_polygons(self) -> None:
        self.assertEqual(self.topology["canonical_release"], "v0.8.1")
        self.assertEqual(self.topology["polygon_count"], 39)
        self.assertEqual(len(self.topology["rows"]), 39)
        for row in self.topology["rows"]:
            self.assertTrue(row["raw_valid"])
            self.assertTrue(row["render_valid"])
            self.assertEqual(
                row["render_land_mask_id"],
                "natural-earth-ne_10m_land-v5.1.1-ca96624",
            )

    def test_known_high_displacement_renders_require_successor_review(self) -> None:
        by_name = {row["name"]: row for row in self.review["named_reviews"]}
        self.assertEqual(
            by_name["Roman Empire — early Principate"]["disposition"],
            "SUCCESSOR_CANDIDATE_V3_REQUIRES_VISUAL_REVIEW",
        )
        self.assertEqual(
            by_name["Western Han China (202 BCE–5 CE slice)"]["disposition"],
            "COMPARATIVE_RE_REVIEW_V2_PROVISIONALLY_PREFERRED",
        )
        self.assertEqual(
            by_name["Mauryan Empire (318–185 BCE mapped slice)"]["disposition"],
            "COMPARATIVE_RE_REVIEW_V2_PROVISIONALLY_PREFERRED",
        )

    def test_baekje_is_not_auto_rejected_or_auto_promoted(self) -> None:
        row = next(r for r in self.review["named_reviews"] if r["name"] == "Baekje")
        self.assertEqual(row["disposition"], "COMPARATIVE_VISUAL_REVIEW_REQUIRED_KEEP_CURRENT")
        self.assertGreater(row["metrics"]["symmetric_difference_pct"], 5)
        self.assertLess(row["metrics"]["hausdorff_m"], 35000)


if __name__ == "__main__":
    unittest.main()
