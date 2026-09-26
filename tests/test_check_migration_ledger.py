import json
import sys
from pathlib import Path
import unittest

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "tools"))

from check_migration_ledger import compare, evaluate, remote_names  # noqa: E402


class Tests(unittest.TestCase):
    def test_clean(self):
        result = evaluate(compare(["0001_a"], ["0001_a"]), None)
        self.assertTrue(result["pass"])

    def test_irregular_without_policy_fails(self):
        result = evaluate(
            compare(
                ["0011_a", "0012_b", "0013_c", "0014_d", "0015_e"],
                ["0011_a", "0015_e", "0015_e", "0099_manual"],
            ),
            None,
        )
        self.assertFalse(result["pass"])
        self.assertEqual(result["missing_remote"], ["0012_b", "0013_c", "0014_d"])
        self.assertEqual(result["duplicate_remote"], {"0015_e": 2})
        self.assertEqual(result["unknown_remote"], ["0099_manual"])

    def test_exact_exception_policy_passes(self):
        raw = compare(
            ["0011_a", "0012_b", "0013_c", "0014_d", "0015_e"],
            ["0011_a", "0015_e", "0015_e"],
        )
        policy = {
            "schema_version": "migration-ledger-exceptions-v1",
            "allowed_missing_remote": ["0012_b", "0013_c", "0014_d"],
            "allowed_duplicate_remote": {"0015_e": 2},
        }
        result = evaluate(raw, policy)
        self.assertTrue(result["pass"])

    def test_changed_exception_shape_fails(self):
        raw = compare(
            ["0011_a", "0012_b", "0015_e"],
            ["0011_a", "0015_e", "0015_e", "0015_e"],
        )
        policy = {
            "schema_version": "migration-ledger-exceptions-v1",
            "allowed_missing_remote": ["0012_b"],
            "allowed_duplicate_remote": {"0015_e": 2},
        }
        result = evaluate(raw, policy)
        self.assertFalse(result["pass"])
        self.assertIn("0015_e", result["unexpected_duplicate_remote"])

    def test_supabase_shape(self):
        self.assertEqual(
            remote_names({"migrations": [{"version": "x", "name": "0001_a"}]}),
            ["0001_a"],
        )


if __name__ == "__main__":
    unittest.main()
