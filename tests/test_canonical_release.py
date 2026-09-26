from __future__ import annotations

import json
import shutil
from collections import Counter
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
FINGERPRINT = (
    ROOT
    / "reviews"
    / "db-canonicalization"
    / "gate3"
    / "gate3-cartography-recovery-fingerprint.json"
)
RELEASE = ROOT / "data" / "releases" / "v0.7.0"


class CanonicalReleaseTests(unittest.TestCase):
    def test_committed_v070_package_rebuilds_exactly(self) -> None:
        verify_package(SPEC, AUTHORITY, FINGERPRINT, RELEASE)

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
                verify_package(SPEC, AUTHORITY, FINGERPRINT, candidate)


    def test_release_preserves_gate4_evidence_boundaries(self) -> None:
        authority = json.loads(
            (RELEASE / "authority-state.json").read_text(encoding="utf-8")
        )
        results = authority["objects"]["research_target_results"].values()
        stages = Counter(item["result"]["research_stage"] for item in results)
        self.assertEqual(stages, Counter({"researched_internal": 21, "under_review": 5}))

        outcomes = [
            item["result"]["research_outcome"].lower()
            for item in authority["objects"]["research_target_results"].values()
        ]
        self.assertEqual(sum("inconclusive" in value for value in outcomes), 6)

        kinds = Counter(
            item["claim"]["claim_kind_code"]
            for item in authority["objects"]["claims"].values()
        )
        self.assertEqual(
            kinds,
            Counter(
                {
                    "territorial_practice": 18,
                    "voyage_owner": 12,
                    "actor_attribute": 6,
                    "external_participation": 3,
                    "legal_event": 1,
                }
            ),
        )
        self.assertEqual(authority["membership"]["geometry_ids"], [])

    def test_portable_cartography_fingerprint_is_shipped_exactly(self) -> None:
        self.assertEqual(
            (RELEASE / "cartography-recovery-fingerprint.json").read_bytes(),
            FINGERPRINT.read_bytes(),
        )


if __name__ == "__main__":
    unittest.main()
