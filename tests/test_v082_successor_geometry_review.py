from pathlib import Path
import json
import unittest

ROOT = Path(__file__).resolve().parents[1]
POLICY = ROOT / "config" / "cartography" / "corpus_geometry_qc_envelope_v2.json"
REVIEW = ROOT / "data" / "research" / "geometry_reviews" / "v082_successor_geometry_review.json"


class V082SuccessorGeometryReviewTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.policy = json.loads(POLICY.read_text(encoding="utf-8"))
        cls.review = json.loads(REVIEW.read_text(encoding="utf-8"))

    def test_measurement_model_separates_frontier_and_coastline(self) -> None:
        model = self.policy["measurement_model"]
        self.assertEqual(
            model["frontier_displacement"]["metric"],
            "source_to_smoothed_boundary_hausdorff_m",
        )
        self.assertEqual(model["frontier_displacement"]["max_candidate_m"], 35000)
        self.assertEqual(
            model["raw_to_final_render_hausdorff"]["role"], "diagnostic_only"
        )
        self.assertTrue(model["canonical_land_residual"]["hard_gate"])

    def test_corpus_reassessment_is_bounded(self) -> None:
        corpus = self.review["corpus_reassessment"]
        self.assertEqual(corpus["polygon_count"], 39)
        self.assertEqual(corpus["corrected_rows_requiring_focused_review"], 6)
        self.assertEqual(
            corpus["corrected_rows_passing_quantitative_axes_without_policy_change"], 33
        )

    def test_exact_successor_substitutions_and_override(self) -> None:
        rows = {x["geometry_id"]: x for x in self.review["focused_reviews"]}
        self.assertEqual(len(rows), 6)
        expected_substitutions = {
            "f8a44a0b-f574-4c55-b5b1-b1e803f78543": "cliopatria-boundary-normalization-v2",
            "34ff5048-242f-48a3-8fb2-5eca4dcd9a54": "cliopatria-boundary-normalization-v2",
            "82b2f32f-de79-4a5a-98e0-56db15321588": "cliopatria-boundary-normalization-v2",
            "edb239a8-4d54-44e4-970a-affb7c9af22e": "cliopatria-boundary-normalization-v3",
            "81cb78c1-3b59-4c0a-b51f-f1c0d45bf866": "cliopatria-boundary-normalization-v3",
        }
        for geometry_id, policy in expected_substitutions.items():
            self.assertEqual(rows[geometry_id]["disposition"], "SUBSTITUTE_RENDER_POLICY")
            self.assertEqual(rows[geometry_id]["successor_policy"], policy)
            self.assertLessEqual(
                rows[geometry_id]["metrics"]["smoothing_hausdorff_m"], 35000
            )
            self.assertLessEqual(rows[geometry_id]["metrics"]["final_symdiff_pct"], 5)
            self.assertLessEqual(
                abs(rows[geometry_id]["metrics"]["final_area_delta_pct"]), 2
            )

        baekje = rows["e5a720f8-9e22-45fe-a5b0-c6464686525d"]
        self.assertEqual(baekje["disposition"], "REUSE_WITH_BOUNDED_OVERRIDE")
        self.assertGreater(baekje["metrics"]["final_symdiff_pct"], 5)
        self.assertIn("coastline", baekje["override_reason"].lower())

    def test_visual_review_artifact_is_frozen(self) -> None:
        artifact = self.review["visual_review_artifact"]
        self.assertEqual(artifact["workflow_run_id"], 36341676958)
        self.assertEqual(artifact["artifact_id"], 10939311385)
        self.assertEqual(artifact["result"], "SUCCESS")
        self.assertTrue(artifact["artifact_digest"].startswith("sha256:"))

    def test_mycenaean_loci_are_not_practice_extent(self) -> None:
        disposition = self.review["successor_geometry_disposition"]
        self.assertEqual(disposition["new_evidence_locus_geometries_for_mycenaean_correction"], 2)
        self.assertEqual(disposition["practice_extent_geometries_for_new_claims"], 0)
        self.assertIn("not", disposition["note"].lower())
        self.assertIn("territorial", disposition["note"].lower())


if __name__ == "__main__":
    unittest.main()
