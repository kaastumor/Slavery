from __future__ import annotations

import shutil
import sys
from pathlib import Path
import tempfile
import unittest

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "tools"))

from build_canonical_release import ReleaseError, verify_package  # noqa: E402


SPEC = ROOT / "release" / "specs" / "v0.7.0.json"
AUTHORITY = (
    ROOT
    / "reviews"
    / "db-canonicalization"
    / "gate3"
    / "gate3-live-full-state-bundle.json"
)
RELEASE = ROOT / "data" / "releases" / "v0.7.0"


class CanonicalReleaseTests(unittest.TestCase):
    def test_committed_v070_package_rebuilds_exactly(self) -> None:
        verify_package(SPEC, AUTHORITY, RELEASE)

    def test_release_tamper_is_rejected(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            candidate = Path(tmp) / "v0.7.0"
            shutil.copytree(RELEASE, candidate)
            release_md = candidate / "RELEASE.md"
            release_md.write_text(
                release_md.read_text(encoding="utf-8") + "\nTAMPER\n",
                encoding="utf-8",
            )
            with self.assertRaises(ReleaseError):
                verify_package(SPEC, AUTHORITY, candidate)


if __name__ == "__main__":
    unittest.main()
