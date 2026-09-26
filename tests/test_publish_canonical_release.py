from __future__ import annotations

from pathlib import Path
import sys
import unittest

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "tools"))

from publish_canonical_release import load_publication_inputs  # noqa: E402


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
SOURCE_GIT_SHA = "1cc7c227de9559a4659058d38327befdfdec6b5b"


class CanonicalReleasePublicationTests(unittest.TestCase):
    def test_publication_plan_is_exact_and_channel_neutral(self) -> None:
        data = load_publication_inputs(
            SPEC,
            AUTHORITY,
            FINGERPRINT,
            RELEASE,
            source_git_sha=SOURCE_GIT_SHA,
        )
        membership = data["authority"]["membership"]
        self.assertEqual(
            {key: len(value) for key, value in membership.items()},
            {
                "actor_ids": 11,
                "claim_ids": 40,
                "coverage_assessment_ids": 99,
                "geometry_ids": 0,
                "research_target_result_ids": 26,
                "source_version_ids": 211,
                "spatial_entity_ids": 18,
                "voyage_ids": 8,
            },
        )
        self.assertEqual(len(data["artifacts"]), 9)
        self.assertFalse(data["manifest"]["public_channel"]["moved_by_release"])
        self.assertEqual(
            data["manifest"]["public_channel"]["current_release"],
            "mvp-preview-ancient-v2",
        )
        self.assertTrue(data["manifest"]["canonical"])

    def test_artifact_locators_pin_exact_release_commit(self) -> None:
        data = load_publication_inputs(
            SPEC,
            AUTHORITY,
            FINGERPRINT,
            RELEASE,
            source_git_sha=SOURCE_GIT_SHA,
        )
        expected_prefix = f"git:{SOURCE_GIT_SHA}:data/releases/v0.7.0/"
        self.assertEqual(
            {item["filename"] for item in data["artifacts"]},
            {
                "CHANGELOG.md",
                "MIGRATION_RECONCILIATION.md",
                "QC_SUMMARY.md",
                "RELEASE.md",
                "SHA256SUMS.txt",
                "UNRESOLVED_ISSUES.md",
                "authority-state.json",
                "cartography-recovery-fingerprint.json",
                "manifest.json",
            },
        )
        for artifact in data["artifacts"]:
            self.assertTrue(artifact["storage_locator"].startswith(expected_prefix))


if __name__ == "__main__":
    unittest.main()
