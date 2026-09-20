from pathlib import Path
import json
import sys
import tempfile
import unittest

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "tools"))

from publish_release import PublishError, load_manifest  # noqa: E402


class PublishManifestTests(unittest.TestCase):
    def test_manifest_is_noncanonical(self):
        manifest = {
            "release_version": "preview-1",
            "schema_version": "0011",
            "claim_ids": ["00000000-0000-0000-0000-000000000001"],
            "changelog": "test",
            "qc_summary": "test",
            "unresolved_issues": "test",
            "canonical": False,
        }
        with tempfile.TemporaryDirectory() as td:
            path = Path(td) / "manifest.json"
            path.write_text(json.dumps(manifest), encoding="utf-8")
            self.assertFalse(load_manifest(path).get("canonical"))

    def test_rejects_canonical_switch(self):
        manifest = {
            "release_version": "bad",
            "schema_version": "0011",
            "claim_ids": ["00000000-0000-0000-0000-000000000001"],
            "changelog": "test",
            "qc_summary": "test",
            "unresolved_issues": "test",
            "canonical": True,
        }
        with tempfile.TemporaryDirectory() as td:
            path = Path(td) / "manifest.json"
            path.write_text(json.dumps(manifest), encoding="utf-8")
            with self.assertRaises(PublishError):
                load_manifest(path)

    def test_direct_apply_path_is_disabled_in_source(self):
        source = (ROOT / "tools" / "publish_release.py").read_text(encoding="utf-8")
        self.assertIn("direct --apply is disabled by D-054", source)

    def test_rejects_duplicate_claim_ids(self):
        manifest = {
            "release_version": "bad",
            "schema_version": "0011",
            "claim_ids": ["x", "x"],
            "changelog": "test",
            "qc_summary": "test",
            "unresolved_issues": "test",
        }
        with tempfile.TemporaryDirectory() as td:
            path = Path(td) / "manifest.json"
            path.write_text(json.dumps(manifest), encoding="utf-8")
            with self.assertRaises(PublishError):
                load_manifest(path)


if __name__ == "__main__":
    unittest.main()
