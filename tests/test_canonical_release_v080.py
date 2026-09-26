from pathlib import Path
import json
import shutil
import sys
import tempfile
import unittest

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "tools"))

from build_canonical_release import build_package, verify_package  # noqa: E402

SPEC = ROOT / "release" / "specs" / "v0.8.0.json"
AUTHORITY = ROOT / "data" / "release_candidates" / "v0.8.0-expansion-02-authority.bundle.json"
FINGERPRINT = (
    ROOT
    / "reviews"
    / "db-canonicalization"
    / "gate3"
    / "gate3-cartography-recovery-fingerprint.json"
)
RELEASE = ROOT / "data" / "releases" / "v0.8.0"


class CanonicalReleaseV080Tests(unittest.TestCase):
    def test_committed_package_verifies(self) -> None:
        verify_package(SPEC, AUTHORITY, FINGERPRINT, RELEASE)

    def test_committed_package_rebuilds_byte_exactly(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            rebuilt = Path(tmp) / "v0.8.0"
            build_package(SPEC, AUTHORITY, FINGERPRINT, rebuilt)
            expected = sorted(p.name for p in RELEASE.iterdir() if p.is_file())
            actual = sorted(p.name for p in rebuilt.iterdir() if p.is_file())
            self.assertEqual(actual, expected)
            for name in expected:
                self.assertEqual(
                    (rebuilt / name).read_bytes(),
                    (RELEASE / name).read_bytes(),
                    name,
                )

    def test_release_boundaries_are_explicit(self) -> None:
        manifest = json.loads((RELEASE / "manifest.json").read_text(encoding="utf-8"))
        membership = manifest["authority"]["membership"]
        self.assertTrue(manifest["canonical"])
        self.assertEqual(manifest["release_version"], "v0.8.0")
        self.assertEqual(len(membership["claim_ids"]), 75)
        self.assertEqual(len(membership["spatial_entity_ids"]), 50)
        self.assertEqual(len(membership["geometry_ids"]), 46)
        self.assertEqual(len(membership["source_version_ids"]), 294)
        self.assertEqual(manifest["authority"]["decision"], "D-115")
        self.assertFalse(manifest["public_channel"]["moved_by_release"])
        self.assertEqual(
            manifest["public_channel"]["current_release"],
            "v0.7.0-public-mvp-v1",
        )

    def test_authority_copy_is_exact(self) -> None:
        self.assertEqual(
            (RELEASE / "authority-state.json").read_bytes(),
            AUTHORITY.read_bytes(),
        )


if __name__ == "__main__":
    unittest.main()
