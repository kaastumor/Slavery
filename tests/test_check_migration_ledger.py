import sys
from pathlib import Path
import unittest

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "tools"))

from check_migration_ledger import compare, remote_names  # noqa: E402


class MigrationLedgerCheckTests(unittest.TestCase):
    def test_clean_history(self):
        result = compare(["0001_a", "0002_b"], ["0001_a", "0002_b"])
        self.assertEqual(result["missing_remote"], [])
        self.assertEqual(result["duplicate_remote"], {})
        self.assertEqual(result["unknown_remote"], [])

    def test_detects_missing_duplicate_and_unknown(self):
        result = compare(
            ["0011_a", "0012_b", "0013_c", "0014_d", "0015_e"],
            ["0011_a", "0015_e", "0015_e", "0099_manual"],
        )
        self.assertEqual(result["missing_remote"], ["0012_b", "0013_c", "0014_d"])
        self.assertEqual(result["duplicate_remote"], {"0015_e": 2})
        self.assertEqual(result["unknown_remote"], ["0099_manual"])

    def test_parses_supabase_shape(self):
        self.assertEqual(
            remote_names({"migrations": [{"version": "x", "name": "0001_a"}]}),
            ["0001_a"],
        )


if __name__ == "__main__":
    unittest.main()
