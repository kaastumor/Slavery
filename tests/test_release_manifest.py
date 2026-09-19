from pathlib import Path
import sys
import tempfile
import unittest

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "experiments" / "release_artifacts"))

from manifest import (  # noqa: E402
    artifact_entry,
    membership_digest,
    membership_entry,
    validate_manifest,
    verify_artifact,
)


class ReleaseManifestProofTests(unittest.TestCase):
    def test_membership_digest_is_order_independent_and_deduplicated(self):
        self.assertEqual(
            membership_digest(["b", "a", "a"]),
            membership_digest(["a", "b"]),
        )

    def test_artifact_verification_detects_byte_change(self):
        with tempfile.TemporaryDirectory() as td:
            path = Path(td) / "release.bin"
            path.write_bytes(b"canonical bytes")
            entry = artifact_entry(
                path,
                role="canonical_input",
                media_type="application/octet-stream",
            )
            self.assertEqual(verify_artifact(path, entry), [])
            path.write_bytes(b"changed bytes")
            errors = verify_artifact(path, entry)
            self.assertTrue(any("size mismatch" in x or "sha256 mismatch" in x for x in errors))

    def test_manifest_validation(self):
        with tempfile.TemporaryDirectory() as td:
            path = Path(td) / "release.bin"
            path.write_bytes(b"example")
            manifest = {
                "release_version": "test-1",
                "status": "draft",
                "artifacts": [
                    artifact_entry(
                        path,
                        role="canonical_input",
                        media_type="application/octet-stream",
                    )
                ],
                "database_membership": [
                    membership_entry("claim", ["claim-2", "claim-1"]),
                    membership_entry("geometry", []),
                ],
            }
            self.assertEqual(validate_manifest(manifest), [])


if __name__ == "__main__":
    unittest.main()
