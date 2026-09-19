from pathlib import Path
import sys
import unittest

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "tools"))

from add_research_case import load_spec  # noqa: E402


class AncientExpansionBatch02Tests(unittest.TestCase):
    def setUp(self):
        self.case_dir = ROOT / "data" / "research" / "ancient_expansion_02"
        self.paths = sorted(self.case_dir.glob("[0-9][0-9]_*.json"))

    def test_every_case_file_validates_and_is_not_directly_published(self):
        self.assertEqual(len(self.paths), 4)
        for path in self.paths:
            with self.subTest(path=path.name):
                spec = load_spec(path)
                claim = spec["claim"]
                self.assertEqual(claim.get("review_status"), "reviewed")
                self.assertIn(claim.get("publication_status"), (None, "unpublished"))
                self.assertTrue(spec["evidence"])

    def test_mauryan_dispute_has_no_p_level(self):
        spec = load_spec(self.case_dir / "02_mauryan_slavery_disputed.json")
        practice = spec["claim"]["territorial_practice"]
        self.assertEqual(practice["coverage_state_code"], "disputed")
        self.assertIsNone(practice["practice_level"])

    def test_silla_date_uncertainty_is_explicit(self):
        spec = load_spec(self.case_dir / "04_silla_village_register_slavery.json")
        claim = spec["claim"]
        self.assertEqual(claim["temporal_certainty"], "disputed")
        self.assertIn("must not be read as a 125-year continuous observation", claim["summary"])


if __name__ == "__main__":
    unittest.main()
