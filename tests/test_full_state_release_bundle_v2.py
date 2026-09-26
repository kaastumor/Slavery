import json
from pathlib import Path
import sys
import tempfile
import unittest

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "tools"))

from full_state_release_bundle import (  # noqa: E402
    BUNDLE_SCHEMA,
    CANDIDATE_SCHEMA,
    BundleError,
    canonical_bytes,
    load_candidate,
    sha256_value,
)


class FullStateBundleV2Tests(unittest.TestCase):
    def _candidate(self):
        membership = {
            "claim_ids": ["a"],
            "actor_ids": [],
            "spatial_entity_ids": [],
            "geometry_ids": [],
            "voyage_ids": [],
            "coverage_assessment_ids": [],
            "source_version_ids": ["b"],
            "research_target_result_ids": ["c"],
        }
        return {
            "candidate_schema": CANDIDATE_SCHEMA,
            "release_version": "test",
            "schema_version": "0033",
            "purpose": "canonical_research_state_proof",
            "canonical": False,
            "canonical_predecessor_version": "v0.6.1",
            "predecessor_manifest_version": "pred",
            "reviewed_candidate_id": "reviewed",
            "workbook_sha256": "a" * 64,
            "changelog": "test",
            "qc_summary": "test",
            "unresolved_issues": "none",
            "seed": {
                "predecessor_manifest_version": "pred",
                "reviewed_candidate_id": "reviewed",
            },
            "membership": membership,
            "membership_sha256": sha256_value(membership),
        }

    def test_canonical_bytes_are_key_order_independent(self):
        self.assertEqual(canonical_bytes({"b": 1, "a": 2}), canonical_bytes({"a": 2, "b": 1}))

    def test_candidate_roundtrip(self):
        data=self._candidate()
        with tempfile.TemporaryDirectory() as tmp:
            path=Path(tmp)/"candidate.json"
            path.write_bytes(canonical_bytes(data))
            loaded=load_candidate(path)
        self.assertEqual(loaded["membership"], data["membership"])

    def test_unsorted_membership_rejected(self):
        data=self._candidate()
        data["membership"]["claim_ids"]=["z","a"]
        data["membership_sha256"]=sha256_value(data["membership"])
        with tempfile.TemporaryDirectory() as tmp:
            path=Path(tmp)/"candidate.json"
            path.write_text(json.dumps(data),encoding="utf-8")
            with self.assertRaises(BundleError):
                load_candidate(path)

    def test_membership_digest_mismatch_rejected(self):
        data=self._candidate()
        data["membership_sha256"]="0"*64
        with tempfile.TemporaryDirectory() as tmp:
            path=Path(tmp)/"candidate.json"
            path.write_text(json.dumps(data),encoding="utf-8")
            with self.assertRaises(BundleError):
                load_candidate(path)

    def test_bundle_schema_constant(self):
        self.assertEqual(BUNDLE_SCHEMA, "historical-slavery-atlas-full-state-bundle-v2")


if __name__ == "__main__":
    unittest.main()
