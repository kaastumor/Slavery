from pathlib import Path
import json
import unittest

ROOT = Path(__file__).resolve().parents[1]
SELECTION = ROOT / "release" / "selections" / "v0.8.2-post-overnight-claims.json"


class PostOvernightV082SelectionTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.selection = json.loads(SELECTION.read_text(encoding="utf-8"))

    def test_claim_selection_is_exact_and_current_method(self) -> None:
        additions = self.selection["claim_additions"]
        self.assertEqual(len(additions), 11)
        self.assertEqual(len({x["claim_id"] for x in additions}), 11)
        self.assertEqual(len({x["spatial_entity_id"] for x in additions}), 11)
        self.assertEqual(
            self.selection["expected_claim_state"]["successor_claims"], 86
        )
        self.assertEqual(
            self.selection["expected_claim_state"]["successor_spatial_entities"], 61
        )

    def test_geometry_is_independently_gated(self) -> None:
        geometry = self.selection["geometry_policy"]
        self.assertEqual(geometry["new_practice_extent_geometry_ids"], [])
        self.assertTrue(geometry["claim_completeness_independent_of_geometry"])
        self.assertTrue(geometry["modern_country_proxy_as_practice_extent_forbidden"])
        self.assertEqual(
            geometry["inherited_geometry_reuse_status"],
            "BLOCKED_PENDING_D119_SUCCESSOR_REVIEW",
        )
        self.assertEqual(geometry["d119_hausdorff_review_trigger_count"], 29)
        self.assertEqual(geometry["d119_component_change_count"], 38)

    def test_mycenaean_locus_change_cannot_hide_as_predecessor_drift(self) -> None:
        correction = self.selection["predecessor_object_correction_required"]
        self.assertEqual(
            correction["claim_id"],
            "8691d038-1683-5331-bccb-e7a189cdd229",
        )
        self.assertEqual(correction["released_evidence_loci_count"], 0)
        self.assertEqual(len(correction["current_evidence_loci"]), 2)
        self.assertIn("explicit bounded", correction["required_action"])

    def test_candidate_is_not_prematurely_release_ready(self) -> None:
        self.assertFalse(self.selection["release_ready"])
        blockers = self.selection["release_blockers"]
        self.assertEqual(len(blockers), 2)
        self.assertTrue(self.selection["rules"]["explicit_membership_only"])
        self.assertTrue(self.selection["rules"]["reviewed_row_discovery_forbidden"])
        self.assertTrue(self.selection["rules"]["prior_release_immutable"])


if __name__ == "__main__":
    unittest.main()
