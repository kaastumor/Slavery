from pathlib import Path
import unittest

ROOT = Path(__file__).resolve().parents[1]
PUBLIC_ROOT = ROOT / "web" / "index.html"
CANONICAL_STAGE = ROOT / "tests" / "fixtures" / "gate5" / "v070-index.html"


class Gate5WebEntrypointTests(unittest.TestCase):
    def test_public_root_is_exact_staged_canonical_entrypoint(self) -> None:
        self.assertEqual(PUBLIC_ROOT.read_bytes(), CANONICAL_STAGE.read_bytes())

    def test_canonical_root_uses_release_client_and_nonabsence_language(self) -> None:
        html = PUBLIC_ROOT.read_text(encoding="utf-8")
        self.assertIn('/src/main.ts', html)
        self.assertNotIn('/src/mvp.ts', html)
        self.assertIn("Canonical release evidence", html)
        self.assertIn(
            "Missing evidence, under-review state and unresolved geometry are not historical absence.",
            html,
        )


if __name__ == "__main__":
    unittest.main()
