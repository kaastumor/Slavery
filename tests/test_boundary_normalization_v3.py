from pathlib import Path
import unittest

ROOT = Path(__file__).resolve().parents[1]
MIGRATION = (ROOT / "db" / "migrations" / "0018_refine_cliopatria_boundary_normalization.sql").read_text(encoding="utf-8")
WEB = (ROOT / "web" / "src" / "main.ts").read_text(encoding="utf-8")


class BoundaryNormalizationV3Tests(unittest.TestCase):
    def test_cliopatria_v3_uses_two_iterations(self):
        self.assertIn("'cliopatria-boundary-normalization-v3'", MIGRATION)
        self.assertIn("25000,\n    2,\n    35000,\n    1.0000", MIGRATION)

    def test_previous_active_cliopatria_policy_is_deactivated(self):
        self.assertIn("SET active = false", MIGRATION)
        self.assertIn("source_url_prefix = 'https://github.com/Seshat-Global-History-Databank/cliopatria'", MIGRATION)

    def test_approximate_geometry_has_softer_outline(self):
        self.assertIn('"approximate_historical", "rgba(89, 52, 47, 0.55)"', WEB)
        self.assertIn('"modern_proxy", "rgba(89, 52, 47, 0.38)"', WEB)


if __name__ == "__main__":
    unittest.main()
