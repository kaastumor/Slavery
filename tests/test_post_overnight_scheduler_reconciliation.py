from pathlib import Path
import json
import unittest

ROOT = Path(__file__).resolve().parents[1]
BASE = ROOT / "data" / "research" / "recovery" / "post_overnight_2026_09_27"
RECON = BASE / "scheduler_reconciliation.json"
NAZI = BASE / "nazi_germany_state_forced_labour_v2.json"


class PostOvernightSchedulerReconciliationTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.recon = json.loads(RECON.read_text(encoding="utf-8"))
        cls.nazi = json.loads(NAZI.read_text(encoding="utf-8"))

    def test_nazi_successor_is_post_m1_and_unmapped(self) -> None:
        claim = self.nazi["claim"]
        tp = claim["territorial_practice"]
        self.assertEqual(claim["review_status"], "reviewed")
        self.assertEqual(claim["publication_status"], "unpublished")
        self.assertIsNone(tp["practice_level"])
        self.assertEqual(tp["practice_type_code"], "state_forced_labour")
        self.assertEqual(tp["classification_status"], "reviewed_reconciled_post_m1")
        self.assertNotIn("geometry", self.nazi)
        self.assertIn(
            "ab1f826b-aecf-4f2b-a88a-bccf1eea4f9a",
            claim["notes"],
        )

    def test_existing_balanced_cases_are_not_duplicated(self) -> None:
        dispositions = {
            row["target"]: row["disposition"]
            for row in self.recon["evidence_lane"]
        }
        self.assertEqual(
            dispositions["Funan"],
            "NO_DUPLICATE_CLAIM_KEEP_CURRENT_PACKAGE_PENDING_PRIMARY_LOCATOR_REPLAY",
        )
        self.assertEqual(
            dispositions["Southern Maya Lowlands"],
            "NO_DUPLICATE_CLAIM_KEEP_CURRENT_PACKAGE_PENDING_MONUMENT_PROVENANCE",
        )
        self.assertEqual(
            dispositions["Hawaiian Islands"],
            "NO_DUPLICATE_CLAIM_CURRENT_PACKAGE_REMAINS_VALID",
        )

    def test_resolution_lane_fails_closed_where_location_is_not_exact(self) -> None:
        rows = {
            row["target"]: row
            for row in self.recon["geometry_resolution_lane"]
        }
        self.assertEqual(
            rows["Opone (Ras Hafun identification)"]["disposition"],
            "HOLD_EXACT_PLEIADES_LOCATION_RESOURCE_REQUIRED",
        )
        self.assertEqual(
            rows["Garshana construction project (Ur III)"]["disposition"],
            "REMAIN_UNRESOLVED",
        )
        self.assertEqual(
            rows["Tōdai-ji"]["disposition"],
            "KEEP_REVIEWED_POINT",
        )

    def test_mycenaean_loci_are_evidence_points_not_extent(self) -> None:
        row = next(
            x
            for x in self.recon["geometry_resolution_lane"]
            if x["target"] == "Mycenaean Greece (Pylos/Knossos)"
        )
        self.assertEqual(row["disposition"], "DB_PROMOTED_REVIEWED_EVIDENCE_LOCI")
        ids = {x["geometry_id"] for x in row["loci"]}
        self.assertEqual(
            ids,
            {
                "824cf9ab-5bfd-4d84-8fb6-8c137033424d",
                "78627165-cc6d-4a42-9f4c-3431944526c8",
            },
        )

    def test_d119_outliers_are_not_silently_reused(self) -> None:
        qc = self.recon["qc_lane"]
        self.assertEqual(
            qc["governing_policy"],
            "config/cartography/corpus_geometry_qc_envelope.json",
        )
        rows = {row["target"]: row for row in qc["verified_followups"]}
        self.assertIn("SUCCESSOR_REVIEW_REQUIRED", rows["Qin Empire family"]["disposition"])
        self.assertIn(
            "COMPARATIVE_RE_REVIEW",
            rows["Western Han China"]["disposition"],
        )
        self.assertIn(
            "SUCCESSOR_CANDIDATE",
            rows["Roman Empire — early Principate 6–8 CE"]["disposition"],
        )
        for row in rows.values():
            self.assertNotEqual(row["disposition"], "AUTO_REUSE_IN_SUCCESSOR")

    def test_full_d119_envelope_is_frozen(self) -> None:
        corpus = self.recon["qc_lane"]["corpus_wide_envelope_observation"]
        self.assertEqual(corpus["polygon_count"], 39)
        self.assertEqual(corpus["hard_land_residual_fail_count"], 0)
        self.assertEqual(corpus["hausdorff_review_trigger_count"], 29)
        self.assertEqual(corpus["hausdorff_inside_gate_count"], 10)
        self.assertEqual(corpus["symmetric_difference_over_5pct_count"], 1)
        self.assertEqual(corpus["absolute_area_delta_over_2pct_count"], 1)
        self.assertEqual(corpus["component_count_change_count"], 38)
        self.assertEqual(
            len(corpus["successor_reuse_hausdorff_trigger_rows"]), 29
        )
        self.assertIn("diagnostics", corpus["interpretation"])
        self.assertIn("not be read as 29 automatically bad", corpus["interpretation"])

    def test_current_release_remains_immutable(self) -> None:
        self.assertIn("No mutation of v0.8.1", self.recon["release_effect"])


if __name__ == "__main__":
    unittest.main()
