from pathlib import Path
import json
import sys
import tempfile
import unittest

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "tools"))

from publish_release import PublishError, artifact_sha256, load_manifest  # noqa: E402


def artifact():
    data = {
        "release_version": "preview-1",
        "schema_version": "0025",
        "claim_ids": ["00000000-0000-0000-0000-000000000001"],
        "spatial_entity_ids": ["00000000-0000-0000-0000-000000000002"],
        "geometry_ids": ["00000000-0000-0000-0000-000000000003"],
        "source_version_ids": ["00000000-0000-0000-0000-000000000004"],
        "changelog": "test",
        "qc_summary": "test",
        "unresolved_issues": "test",
        "canonical": False,
    }
    data["artifact_sha256"] = artifact_sha256(data)
    return data


def write_and_load(data):
    with tempfile.TemporaryDirectory() as td:
        path = Path(td) / "artifact.json"
        path.write_text(json.dumps(data), encoding="utf-8")
        return load_manifest(path)


class PublishManifestTests(unittest.TestCase):
    def test_accepts_exact_noncanonical_artifact(self):
        loaded = write_and_load(artifact())
        self.assertFalse(loaded["canonical"])
        self.assertEqual(loaded["artifact_sha256"], artifact_sha256(loaded))

    def test_rejects_canonical_switch(self):
        data = artifact()
        data["canonical"] = True
        data["artifact_sha256"] = artifact_sha256(data)
        with self.assertRaises(PublishError):
            write_and_load(data)

    def test_rejects_duplicate_membership(self):
        data = artifact()
        data["claim_ids"].append(data["claim_ids"][0])
        data["artifact_sha256"] = artifact_sha256(data)
        with self.assertRaises(PublishError):
            write_and_load(data)

    def test_rejects_unsorted_membership(self):
        data = artifact()
        data["geometry_ids"] = [
            "00000000-0000-0000-0000-000000000009",
            "00000000-0000-0000-0000-000000000003",
        ]
        data["artifact_sha256"] = artifact_sha256(data)
        with self.assertRaises(PublishError):
            write_and_load(data)

    def test_rejects_tampered_artifact(self):
        data = artifact()
        data["changelog"] = "changed after review"
        with self.assertRaises(PublishError):
            write_and_load(data)

    def test_requires_precomputed_membership(self):
        data = artifact()
        del data["geometry_ids"]
        data["artifact_sha256"] = artifact_sha256(data)
        with self.assertRaises(PublishError):
            write_and_load(data)


if __name__ == "__main__":
    unittest.main()
