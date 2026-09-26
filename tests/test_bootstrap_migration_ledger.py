import sys
from pathlib import Path
import unittest

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "tools"))

from bootstrap_migration_ledger import (  # noqa: E402
    evaluate_platform_history,
    repository_inventory,
    validate_existing_ledger,
)


class BootstrapMigrationLedgerTests(unittest.TestCase):
    def test_repository_inventory_is_exact_0001_to_0031(self):
        inventory = repository_inventory()
        self.assertEqual(len(inventory), 31)
        self.assertEqual(inventory[0]["filename"], "0001_bootstrap.sql")
        self.assertEqual(inventory[-1]["filename"], "0031_v3_research_evidence_model.sql")
        self.assertTrue(all(len(row["checksum_sha256"]) == 64 for row in inventory))

    def test_known_platform_history_irregularities_can_be_explicitly_accepted(self):
        inventory = [
            {"name": "0011_a", "filename": "0011_a.sql", "checksum_sha256": "a" * 64},
            {"name": "0012_b", "filename": "0012_b.sql", "checksum_sha256": "b" * 64},
            {"name": "0013_c", "filename": "0013_c.sql", "checksum_sha256": "c" * 64},
            {"name": "0014_d", "filename": "0014_d.sql", "checksum_sha256": "d" * 64},
            {"name": "0015_e", "filename": "0015_e.sql", "checksum_sha256": "e" * 64},
        ]
        history = [
            {"version": "1", "name": "0011_a"},
            {"version": "2", "name": "0015_e"},
            {"version": "3", "name": "0015_e"},
        ]
        policy = {
            "allowed_missing_remote": ["0012_b", "0013_c", "0014_d"],
            "allowed_duplicate_remote": {"0015_e": 2},
        }
        result = evaluate_platform_history(inventory, history, policy)
        self.assertTrue(result["pass"])

    def test_existing_checksum_mismatch_blocks(self):
        inventory = [
            {"name": "0001_a", "filename": "0001_a.sql", "checksum_sha256": "a" * 64}
        ]
        result = validate_existing_ledger(inventory, [("0001_a.sql", "b" * 64)])
        self.assertFalse(result["pass"])
        self.assertIn("0001_a.sql", result["checksum_mismatch"])


if __name__ == "__main__":
    unittest.main()
