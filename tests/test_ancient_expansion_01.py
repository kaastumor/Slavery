from pathlib import Path
import sys
import unittest

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "tools"))

from add_research_case import load_spec  # noqa: E402


class AncientExpansionBatch01Tests(unittest.TestCase):
    def test_every_case_file_validates_and_is_not_directly_published(self):
        case_dir = ROOT / "data" / "research" / "ancient_expansion_01"
        paths = sorted(case_dir.glob("[0-9][0-9]_*.json"))
        self.assertEqual(len(paths), 8)
        for path in paths:
            with self.subTest(path=path.name):
                spec = load_spec(path)
                claim = spec["claim"]
                self.assertEqual(claim.get("review_status"), "reviewed")
                self.assertIn(claim.get("publication_status"), (None, "unpublished"))
                self.assertTrue(spec["evidence"])


if __name__ == "__main__":
    unittest.main()
