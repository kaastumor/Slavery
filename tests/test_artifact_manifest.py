from pathlib import Path
import importlib.util
import tempfile
import unittest


ROOT = Path(__file__).resolve().parents[1]
MODULE_PATH = ROOT / "tools" / "build_artifact_manifest.py"
SPEC = importlib.util.spec_from_file_location("build_artifact_manifest", MODULE_PATH)
MODULE = importlib.util.module_from_spec(SPEC)
assert SPEC.loader is not None
SPEC.loader.exec_module(MODULE)


class ArtifactManifestTests(unittest.TestCase):
    def test_sha256_is_stable(self):
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / "artifact.txt"
            path.write_text("atlas\n", encoding="utf-8")
            self.assertEqual(
                MODULE.sha256(path),
                "e7764dedc66e4378732a0f96ef9df5235dd40c8c2348dc07acb92008564c3761",
            )

    def test_records_capture_hash_and_size(self):
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / "artifact.txt"
            path.write_bytes(b"abc")
            record = MODULE.records([path])[0]
            self.assertEqual(record["path"], str(path))
            self.assertEqual(record["size_bytes"], 3)
            self.assertEqual(
                record["sha256"],
                "ba7816bf8f01cfea414140de5dae2223b00361a396177a9cb410ff61f20015ad",
            )

    def test_key_values_require_explicit_key(self):
        self.assertEqual(
            MODULE.key_values(["snap_tolerance_m=10000"], "--param"),
            {"snap_tolerance_m": "10000"},
        )
        with self.assertRaises(SystemExit):
            MODULE.key_values(["missing-separator"], "--param")


if __name__ == "__main__":
    unittest.main()
