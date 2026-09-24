import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
R1 = ROOT / "programmes" / "r1"
WEB = ROOT / "web"
sys.path.insert(0, str(R1))

import build_mvp_candidate_bundle as bundle_builder  # noqa: E402


class R1MVPRegisterTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.bundle = bundle_builder.build()
        cls.targets = {row["target_id"]: row for row in cls.bundle["targets"]}
        cls.reviewed = {row["target_id"]: row for row in cls.bundle["reviewed_c1"]}
        cls.geometry = {row["target_id"]: row for row in cls.bundle["geometry_manifest"]["rows"]}

    def test_reviewed_register_rows_have_required_release_fields(self):
        self.assertEqual(len(self.reviewed), 19)
        required = {
            "bounded_proposition",
            "required_abstention",
            "classification_outcome",
            "evidence_locus",
            "inference_extent",
            "review_state",
            "language_access_limitations",
            "coverage_confidence",
            "sources",
        }
        for target_id, row in self.reviewed.items():
            self.assertTrue(required.issubset(row), target_id)
            self.assertEqual(row["review_state"], "internally_adversarially_reviewed")
            self.assertTrue(row["bounded_proposition"].strip())
            self.assertTrue(row["required_abstention"].strip())
            self.assertTrue(row["sources"], target_id)

    def test_source_rows_expose_version_locator_and_dependency_family(self):
        for target_id, row in self.reviewed.items():
            for source in row["sources"]:
                self.assertTrue(source.get("source_version_ref"), target_id)
                self.assertTrue(source.get("locator"), target_id)
                self.assertTrue(source.get("independence_group"), target_id)

    def test_unreviewed_register_rows_do_not_acquire_subject_packets(self):
        unreviewed = set(self.targets) - set(self.reviewed)
        self.assertEqual(len(unreviewed), 58)
        for target_id in unreviewed:
            target = self.targets[target_id]
            self.assertEqual(target["classification_outcome"], "unassessed")
            self.assertTrue(target["absence_inference_prohibited"])
            self.assertNotEqual(target["release_research_state"], "c1_review_complete")

    def test_every_register_target_has_explicit_geometry_state(self):
        self.assertEqual(set(self.geometry), set(self.targets))
        for target_id, row in self.geometry.items():
            self.assertTrue(row["representation_state"], target_id)
            self.assertEqual(row["historical_claim_effect"], "none")

    def test_ui_uses_buttons_and_explicit_internal_review_wording(self):
        source = (WEB / "src" / "mvp.ts").read_text(encoding="utf-8")
        self.assertIn('class="place-card" type="button"', source)
        self.assertIn('aria-label="Open evidence record for', source)
        self.assertIn("internal adversarial review only; not independent review", source)
        self.assertIn("Source family:", source)
        self.assertIn("No historical absence inference.", source)


if __name__ == "__main__":
    unittest.main()
