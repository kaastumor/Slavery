from pathlib import Path
import sys
import unittest

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "tools"))
from migrate import discover, migration_body  # noqa: E402


class MigrationRunnerTests(unittest.TestCase):
    def test_migrations_are_ordered_and_complete(self):
        names = [p.name for p in discover()]
        self.assertEqual(names[0], "0001_bootstrap.sql")
        self.assertEqual(names[-1], "0025_release_channel_pointer.sql")
        self.assertEqual(len(names), 25)

    def test_legacy_transaction_wrappers_are_removed(self):
        for path in discover():
            body = migration_body(path)
            self.assertNotIn("\nBEGIN;", "\n" + body.upper())
            self.assertFalse(body.upper().rstrip().endswith("COMMIT;"))


if __name__ == "__main__":
    unittest.main()
