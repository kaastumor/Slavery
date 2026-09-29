from pathlib import Path
import unittest

ROOT = Path(__file__).resolve().parents[1]
BUILDER = (ROOT / "tools" / "build_v081_mapfix_materialization.py").read_text(encoding="utf-8")
DECISIONS = (ROOT / "docs" / "08_DECISIONS_LOG.md").read_text(encoding="utf-8")


class V081MapFixCandidateContractTests(unittest.TestCase):
    def test_candidate_is_new_immutable_adapter(self) -> None:
        self.assertIn('OLD_ID = "v0.8.1-public-mvp-v1"', BUILDER)
        self.assertIn('NEW_ID = "v0.8.1-public-mvp-v2"', BUILDER)
        self.assertNotIn("rmtree(OLD", BUILDER)
        self.assertIn('"rollback_materialization"', BUILDER)

    def test_claim_semantics_and_historical_identity_are_invariants(self) -> None:
        self.assertIn("semantic_projection(old_payload) != semantic_projection(new_payload)", BUILDER)
        self.assertIn("stable_geometry_identity(old_record)", BUILDER)
        self.assertIn("historical geometry identity/source metadata changed", BUILDER)

    def test_all_polygon_candidates_are_source_land_gated(self) -> None:
        self.assertIn("source_land_loss_pct > LOSS_EPSILON_PCT", BUILDER)
        self.assertIn("outside_land_pct > OUTSIDE_EPSILON_PCT", BUILDER)
        self.assertIn("added_pct > MAX_RECOVERY_ADDED_PCT", BUILDER)
        self.assertIn('"source_land_fidelity"', BUILDER)

    def test_specialist_geometry_keeps_source_choice(self) -> None:
        d122 = DECISIONS.split("## D-122", 1)[1].split("## D-123", 1)[0]
        self.assertIn("specialist substitutions", d122)
        self.assertIn("without changing that specialist source choice", d122)


if __name__ == "__main__":
    unittest.main()
