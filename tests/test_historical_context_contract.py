from pathlib import Path
import unittest

ROOT = Path(__file__).resolve().parents[1]
BUILDER = (ROOT / "tools" / "build_historical_context_snapshot.py").read_text(encoding="utf-8")
DECISIONS = (ROOT / "docs" / "08_DECISIONS_LOG.md").read_text(encoding="utf-8")


class HistoricalContextContractTests(unittest.TestCase):
    def test_decision_keeps_context_separate_from_evidence(self) -> None:
        d123 = DECISIONS.split("## D-123", 1)[1]
        self.assertIn("never creates, strengthens, weakens or negates", d123)
        self.assertIn("historical-polity context", d123)
        self.assertIn("Missing context is not historical absence", d123)

    def test_builder_uses_top_level_polity_semantics(self) -> None:
        self.assertIn('props.get("Type") != "POLITY"', BUILDER)
        self.assertIn('props.get("MemberOf")', BUILDER)
        self.assertIn('"claim_semantics": "none"', BUILDER)

    def test_builder_pins_source_and_land(self) -> None:
        self.assertIn("ad28a691b7c07c1fca89d0e0636d324667d2a258", BUILDER)
        self.assertIn("d01ae3a20d358cc5d54f69d9d725d390767d9c8759ac89ad6f90c58d106f3370", BUILDER)
        self.assertIn("1ac90796408bc6ad6911d69448485d3c4dbf2190370080368a09976e1c9f7416", BUILDER)

    def test_builder_does_not_write_claim_or_release_state(self) -> None:
        self.assertNotIn("practice_level", BUILDER)
        self.assertNotIn("publication_status", BUILDER)
        self.assertNotIn("audit.release_channel", BUILDER)
        self.assertNotIn("atlas.territorial", BUILDER)


if __name__ == "__main__":
    unittest.main()
