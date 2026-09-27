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
        # Eleven new claim subjects plus two evidence-locus site entities.
        self.assertEqual(
            self.selection["expected_claim_state"]["successor_spatial_entities"], 63
        )

    def test_geometry_is_independently_gated_and_cleared(self) -> None:
        geometry = self.selection["geometry_policy"]
        self.assertEqual(geometry["new_practice_extent_geometry_ids"], [])
        self.assertTrue(geometry["claim_completeness_independent_of_geometry"])
        self.assertTrue(geometry["modern_country_proxy_as_practice_extent_forbidden"])
        self.assertEqual(
            geometry["inherited_geometry_reuse_status"],
            "CLEARED_BY_D120_SUCCESSOR_REVIEW",
        )
        self.assertEqual(geometry["d120_corrected_focused_review_count"], 6)
        self.assertEqual(geometry["d120_unchanged_polygon_reuse_count"], 33)
        self.assertEqual(len(geometry["render_policy_substitutions"]), 5)
        self.assertEqual(
            geometry["bounded_render_overrides"],
            ["e5a720f8-9e22-45fe-a5b0-c6464686525d"],
        )
        self.assertEqual(geometry["expected_successor_geometry_membership"], 48)

    def test_mycenaean_locus_change_is_explicit_successor_augmentation(self) -> None:
        correction = self.selection["predecessor_object_correction_required"]
        self.assertEqual(
            correction["claim_id"],
            "8691d038-1683-5331-bccb-e7a189cdd229",
        )
        self.assertEqual(correction["released_evidence_loci_count"], 0)
        self.assertEqual(len(correction["current_evidence_loci"]), 2)
        self.assertEqual(
            correction["disposition"],
            "INCLUDE_AS_EXPLICIT_BOUNDED_SUCCESSOR_AUGMENTATION",
        )
        self.assertEqual(len(correction["add_spatial_entity_ids"]), 2)
        self.assertEqual(len(correction["add_geometry_ids"]), 2)
        self.assertEqual(
            correction["semantic_scope"],
            "claim_evidence_locus_only_not_territorial_extent",
        )

    def test_candidate_is_release_ready_for_authority_freeze(self) -> None:
        self.assertTrue(self.selection["release_ready"])
        self.assertEqual(self.selection["release_blockers"], [])
        self.assertEqual(
            self.selection["status"], "RELEASE_READY_PENDING_AUTHORITY_FREEZE"
        )
        self.assertEqual(
            self.selection["rules"]["geometry_successor_review_decision"], "D-120"
        )
        self.assertTrue(
            self.selection["rules"]["mycenaean_locus_augmentation_explicit"]
        )
        self.assertTrue(self.selection["rules"]["explicit_membership_only"])
        self.assertTrue(self.selection["rules"]["reviewed_row_discovery_forbidden"])
        self.assertTrue(self.selection["rules"]["prior_release_immutable"])


if __name__ == "__main__":
    unittest.main()
