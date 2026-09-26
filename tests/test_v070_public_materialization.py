from __future__ import annotations

import json
from pathlib import Path
import sys
import unittest

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "tools"))

from build_v070_public_materialization import (  # noqa: E402
    MATERIALIZATION_ID,
    verify_materialization,
)


RELEASE = ROOT / "data" / "releases" / "v0.7.0"
FINGERPRINT = RELEASE / "cartography-recovery-fingerprint.json"
MATERIALIZATION = ROOT / "data" / "serving" / MATERIALIZATION_ID


class V070PublicMaterializationTests(unittest.TestCase):
    def test_committed_materialization_rebuilds_exactly(self) -> None:
        verify_materialization(RELEASE, FINGERPRINT, MATERIALIZATION)

    def test_materialization_is_bounded_and_truthful(self) -> None:
        payload = json.loads(
            (MATERIALIZATION / "atlas-data.json").read_text(encoding="utf-8")
        )
        manifest = json.loads(
            (MATERIALIZATION / "materialization-manifest.json").read_text(
                encoding="utf-8"
            )
        )

        self.assertEqual(payload["release_version"], "v0.7.0")
        self.assertTrue(payload["canonical"])
        self.assertEqual(payload["serving_materialization_id"], MATERIALIZATION_ID)
        self.assertEqual(payload["display_scope"], "territorial_practice_only")
        self.assertEqual(len(payload["places"]), 16)
        self.assertEqual(
            sum(len(place["claims"]) for place in payload["places"]),
            18,
        )
        self.assertTrue(all(place["geometries"] == [] for place in payload["places"]))

        self.assertEqual(
            payload["release_dimensions"]["claim_kind_counts"],
            {
                "actor_attribute": 6,
                "external_participation": 3,
                "legal_event": 1,
                "territorial_practice": 18,
                "voyage_owner": 12,
            },
        )
        self.assertEqual(
            payload["release_dimensions"]["research_stage_counts"],
            {"researched_internal": 21, "under_review": 5},
        )
        self.assertEqual(
            payload["release_dimensions"]["researched_inconclusive_count"], 6
        )
        self.assertEqual(
            payload["release_dimensions"]["independent_historical_reviews"], 0
        )
        self.assertEqual(
            payload["release_dimensions"]["reviewed_historical_geometry_count"], 0
        )

        self.assertFalse(manifest["canonical"])
        self.assertEqual(manifest["purpose"], "public_mvp_preview")
        self.assertEqual(manifest["canonical_source_release"], "v0.7.0")
        self.assertEqual(manifest["rollback_release"], "mvp-preview-ancient-v2")

    def test_displayed_claims_are_exact_release_projection(self) -> None:
        authority = json.loads(
            (RELEASE / "authority-state.json").read_text(encoding="utf-8")
        )
        payload = json.loads(
            (MATERIALIZATION / "atlas-data.json").read_text(encoding="utf-8")
        )

        expected = {
            claim_id: obj
            for claim_id, obj in authority["objects"]["claims"].items()
            if obj["claim"]["claim_kind_code"] == "territorial_practice"
        }
        displayed = {
            claim["claim_id"]: claim
            for place in payload["places"]
            for claim in place["claims"]
        }
        self.assertEqual(set(displayed), set(expected))

        allowed_source_versions = set(authority["membership"]["source_version_ids"])
        for claim_id, row in displayed.items():
            frozen = expected[claim_id]
            self.assertEqual(
                row["practice_level"],
                frozen["territorial_practice"]["practice_level"],
            )
            self.assertEqual(
                row["coverage_state"],
                frozen["territorial_practice"]["coverage_state_code"],
            )
            self.assertEqual(
                row["classification_status"],
                frozen["territorial_practice"]["classification_status"],
            )
            self.assertEqual(
                row["publication_status"],
                frozen["claim"]["publication_status"],
            )
            expected_source_versions = {
                source["source_version_id"]
                for source in frozen.get("claim_sources", [])
            }
            actual_source_versions = {
                source["source_version_id"] for source in row["sources"]
            }
            self.assertEqual(actual_source_versions, expected_source_versions)
            self.assertTrue(actual_source_versions <= allowed_source_versions)


if __name__ == "__main__":
    unittest.main()
