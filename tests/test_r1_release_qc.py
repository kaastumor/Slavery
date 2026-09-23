import importlib.util
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
VALIDATOR = ROOT / "programmes" / "r1" / "validate_r1_release_qc.py"

spec = importlib.util.spec_from_file_location("r1releaseqc", VALIDATOR)
m = importlib.util.module_from_spec(spec)
spec.loader.exec_module(m)


class R1ReleaseQCTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.result = m.validate_release()

    def test_release_qc_has_no_blocking_errors(self):
        self.assertEqual(self.result["errors"], [])

    def test_expected_research_counts(self):
        self.assertEqual(
            self.result["counts"],
            {
                "c1_rows": 19,
                "classified": 5,
                "inconclusive": 14,
                "c2_completed": 4,
                "adversarially_reviewed": 19,
                "source_relations": 45,
                "source_versions": 45,
                "independence_groups": 37,
                "frozen_targets": 77,
            },
        )

    def test_registry_preserves_nonresearch_as_nonabsence(self):
        self.assertEqual(
            self.result["registry_states"],
            {
                "c1_review_complete": 19,
                "planned_c1_unresearched_ready": 15,
                "held_identity_or_time": 2,
                "c0_registered_unresearched": 41,
            },
        )

    def test_frozen_polity_balance(self):
        self.assertEqual(
            self.result["polity_sectors"],
            {"A": 2, "B": 1, "C": 3, "D": 2, "E": 1, "F": 3},
        )
        self.assertLessEqual(
            max(self.result["polity_sectors"].values())
            / sum(self.result["polity_sectors"].values()),
            0.25,
        )

    def test_geometry_limitation_is_explicit_not_silent(self):
        self.assertTrue(
            any("geometry materialization is deferred to R1.7" in w for w in self.result["warnings"])
        )


if __name__ == "__main__":
    unittest.main()
