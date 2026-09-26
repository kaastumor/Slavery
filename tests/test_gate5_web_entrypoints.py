from pathlib import Path
import unittest

ROOT = Path(__file__).resolve().parents[1]
CURRENT_ROOT = ROOT / "web" / "index.html"
CANONICAL_STAGE = ROOT / "tests" / "fixtures" / "gate5" / "v070-index.html"


class Gate5WebEntrypointTests(unittest.TestCase):
    def test_current_public_root_remains_r1_candidate_before_cutover(self) -> None:
        html = CURRENT_ROOT.read_text(encoding="utf-8")
        self.assertIn('/src/mvp.ts', html)
        self.assertNotIn('/src/main.ts', html)
        self.assertIn("R1 candidate evidence", html)

    def test_gate5_stage_root_is_canonical_client_without_publishing_it(self) -> None:
        html = CANONICAL_STAGE.read_text(encoding="utf-8")
        self.assertIn('/src/main.ts', html)
        self.assertNotIn('/src/mvp.ts', html)
        self.assertIn("Canonical release evidence", html)
        self.assertIn(
            "Missing evidence, under-review state and unresolved geometry are not historical absence.",
            html,
        )


if __name__ == "__main__":
    unittest.main()
