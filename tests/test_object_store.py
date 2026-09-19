from pathlib import Path
import sys
import tempfile
import unittest

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "experiments" / "release_artifacts"))

from object_store import put_immutable, retrieve_verified, sha256_file  # noqa: E402


class ObjectStoreProofTests(unittest.TestCase):
    def test_put_is_content_addressed_and_idempotent(self):
        with tempfile.TemporaryDirectory() as td:
            root = Path(td)
            source = root / "input.bin"
            source.write_bytes(b"same immutable content")
            store = root / "store"

            first = put_immutable(source, store)
            second = put_immutable(source, store)

            self.assertTrue(first["created"])
            self.assertFalse(second["created"])
            self.assertEqual(first["object_key"], second["object_key"])
            self.assertEqual(first["sha256"], second["sha256"])

    def test_retrieve_verifies_bytes(self):
        with tempfile.TemporaryDirectory() as td:
            root = Path(td)
            source = root / "input.bin"
            source.write_bytes(b"canonical")
            store = root / "store"
            stored = put_immutable(source, store)

            output = root / "out" / "restored.bin"
            retrieve_verified(store, stored["object_key"], output, stored["sha256"])
            self.assertEqual(source.read_bytes(), output.read_bytes())
            self.assertEqual(sha256_file(output), stored["sha256"])


if __name__ == "__main__":
    unittest.main()
