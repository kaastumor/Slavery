from __future__ import annotations

import json
from pathlib import Path
import tempfile
import unittest

ROOT = Path(__file__).resolve().parents[1]

import sys
sys.path.insert(0, str(ROOT / "tools"))

from build_canonical_release import build_package, verify_package  # noqa: E402

SPEC = ROOT / "release" / "specs" / "v0.8.1.json"
AUTHORITY = ROOT / "data" / "release_candidates" / "v0.8.1-rome-geometry-authority.bundle.json"
FINGERPRINT = (
    ROOT
    / "reviews"
    / "db-canonicalization"
    / "gate3"
    / "gate3-cartography-recovery-fingerprint.json"
)
RELEASE = ROOT / "data" / "releases" / "v0.8.1"


class CanonicalReleaseV081Tests(unittest.TestCase):
    def test_committed_package_verifies(self) -> None:
        verify_package(SPEC, AUTHORITY, FINGERPRINT, RELEASE)

    def test_committed_package_rebuilds_byte_exactly(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            rebuilt = Path(tmp) / "v0.8.1"
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

    def test_geometry_only_membership_correction(self) -> None:
        current = json.loads((RELEASE / "authority-state.json").read_text(encoding="utf-8"))
        previous = json.loads(
            (ROOT / "data" / "releases" / "v0.8.0" / "authority-state.json").read_text(
                encoding="utf-8"
            )
        )
        self.assertEqual(len(current["membership"]["claim_ids"]), 75)
        self.assertEqual(current["membership"]["claim_ids"], previous["membership"]["claim_ids"])
        self.assertEqual(
            current["membership"]["spatial_entity_ids"],
            previous["membership"]["spatial_entity_ids"],
        )
        self.assertIn(
            "b3066705-616e-42c7-a50d-656c6926813c",
            current["membership"]["geometry_ids"],
        )
        self.assertNotIn(
            "b7c31528-ff4c-49cf-a95b-c662afab4339",
            current["membership"]["geometry_ids"],
        )
        geometry = current["objects"]["geometries"][
            "b3066705-616e-42c7-a50d-656c6926813c"
        ]
        self.assertEqual(geometry["accuracy_status"], "approximate_historical")
        source = current["objects"]["source_versions"][
            "8041c6c9-52cb-4979-a2ea-c191128f047a"
        ]
        self.assertIn("CC-BY-NC", source["source_version"]["license_status"])


if __name__ == "__main__":
    unittest.main()
