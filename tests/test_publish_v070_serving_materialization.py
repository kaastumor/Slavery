from __future__ import annotations

from pathlib import Path
import sys
import unittest

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "tools"))

from publish_v070_serving_materialization import (  # noqa: E402
    MATERIALIZATION_ID,
    prepare,
)


RELEASE = ROOT / "data" / "releases" / "v0.7.0"
FINGERPRINT = RELEASE / "cartography-recovery-fingerprint.json"
MATERIALIZATION = ROOT / "data" / "serving" / MATERIALIZATION_ID


class V070ServingPublicationTests(unittest.TestCase):
    def test_plan_is_subset_of_canonical_release_and_channel_neutral(self) -> None:
        data = prepare(
            RELEASE,
            FINGERPRINT,
            MATERIALIZATION,
            source_git_sha="test-git-sha",
        )
        membership = data["membership"]
        self.assertEqual(len(membership["claim_ids"]), 18)
        self.assertEqual(len(membership["spatial_entity_ids"]), 16)
        self.assertEqual(len(membership["source_version_ids"]), 16)
        self.assertEqual(membership["geometry_ids"], [])
        self.assertEqual(membership["actor_ids"], [])
        self.assertEqual(membership["voyage_ids"], [])
        self.assertEqual(membership["coverage_assessment_ids"], [])
        self.assertEqual(membership["research_target_result_ids"], [])
        self.assertEqual(len(data["artifacts"]), 2)

        db_manifest = data["db_manifest"]
        self.assertFalse(db_manifest["canonical"])
        self.assertEqual(db_manifest["purpose"], "public_mvp_preview")
        self.assertEqual(db_manifest["canonical_source_release"], "v0.7.0")
        self.assertEqual(
            db_manifest["serving_materialization"]["materialization_id"],
            MATERIALIZATION_ID,
        )
        self.assertEqual(
            db_manifest["serving_materialization"]["payload_sha256"],
            "2a04787a2ee0e42a97f273621eebbf32ddc6a1b2e903239a626eb41d72c29786",
        )
        self.assertEqual(
            db_manifest["serving_materialization"][
                "reviewed_historical_geometry_count"
            ],
            0,
        )

    def test_artifact_locators_are_commit_pinned(self) -> None:
        data = prepare(
            RELEASE,
            FINGERPRINT,
            MATERIALIZATION,
            source_git_sha="abc123",
        )
        self.assertEqual(
            {row["filename"] for row in data["artifacts"]},
            {"atlas-data.json", "materialization-manifest.json"},
        )
        for row in data["artifacts"]:
            self.assertEqual(row["storage_status"], "repository")
            self.assertTrue(
                row["storage_locator"].startswith(
                    "git:abc123:data/serving/v0.7.0-public-mvp-v1/"
                )
            )


if __name__ == "__main__":
    unittest.main()
