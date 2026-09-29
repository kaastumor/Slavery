from pathlib import Path
import unittest

ROOT = Path(__file__).resolve().parents[1]
MIGRATION = (
    ROOT / "db" / "migrations" / "0035_cliopatria_source_land_fidelity_render.sql"
).read_text(encoding="utf-8")
DECISIONS = (ROOT / "docs" / "08_DECISIONS_LOG.md").read_text(encoding="utf-8")


class SourceLandFidelityPolicyTests(unittest.TestCase):
    def test_policy_has_zero_recovery_baseline_and_bounded_candidate(self) -> None:
        self.assertIn("'cliopatria-source-land-fidelity-v1'", MIGRATION)
        self.assertIn("    0,\n    25000,\n    2.0000,\n    0,", MIGRATION)
        self.assertIn("zero-recovery source-land baseline", MIGRATION)

    def test_policy_disables_inland_smoothing(self) -> None:
        self.assertIn("no Chaikin/inland-boundary smoothing", MIGRATION)
        self.assertIn("smooth_iterations", MIGRATION)

    def test_policy_does_not_mutate_source_geometry(self) -> None:
        upper = MIGRATION.upper()
        self.assertNotIn("UPDATE ATLAS.GEOMETRY", upper)
        self.assertNotIn("UPDATE PUBLISH.GEOMETRY", upper)

    def test_decision_preserves_source_land_and_caps_recovery(self) -> None:
        d122 = DECISIONS.split("## D-122", 1)[1]
        self.assertIn("source_land = source_geometry ∩ canonical_land", d122)
        self.assertIn("additional canonical land is <=2%", d122)
        self.assertIn("otherwise retain the exact source-land", d122)


if __name__ == "__main__":
    unittest.main()
