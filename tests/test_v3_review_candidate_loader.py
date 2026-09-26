import json
from pathlib import Path
import sys
import unittest

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "tools"))

from load_v3_review_candidate import (  # noqa: E402
    load_payload,
    parse_anchor_year,
    stable_uuid,
    target_content_sha,
)

PAYLOAD = ROOT / "reviews" / "db-canonicalization" / "gate2-v3-ingest-payload.json"


class Gate2V3PayloadTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.payload = load_payload(PAYLOAD)

    def test_exact_candidate_counts(self):
        self.assertEqual(
            self.payload["counts"],
            {"targets": 26, "admitted": 21, "holds": 5, "source_relations": 166},
        )

    def test_target_membership_unique_and_reviewed(self):
        ids = [t["data"]["target_id"] for t in self.payload["targets"]]
        self.assertEqual(len(ids), len(set(ids)))
        self.assertEqual(len(ids), 26)
        self.assertEqual(sum(t["review"]["admitted"] == "true" for t in self.payload["targets"]), 21)
        self.assertEqual(sum(t["review"]["admitted"] != "true" for t in self.payload["targets"]), 5)

    def test_all_sources_are_claim_specific_and_versioned(self):
        for relation in self.payload["source_relations"]:
            row = relation["data"]
            self.assertTrue(row["source_version_ref"])
            self.assertTrue(row["independence_group"])
            self.assertTrue(row["claim_fitness"])

    def test_historical_freeze_is_preserved(self):
        frozen = [
            t for t in self.payload["targets"]
            if t["lineage"]["stage"] == "v1_frozen"
        ]
        self.assertEqual(len(frozen), 17)
        self.assertTrue(all(t["lineage"]["git_ref"] == "7448a94a38fdb5c4380b3adf91bcedbf7ac84dd5" for t in frozen))

    def test_content_hash_and_uuid_are_stable(self):
        target = self.payload["targets"][0]
        self.assertEqual(target_content_sha(target), target_content_sha(target))
        self.assertEqual(stable_uuid("x", "y"), stable_uuid("x", "y"))

    def test_anchor_year_parser(self):
        self.assertEqual(parse_anchor_year("2000 BCE"), -2000)
        self.assertEqual(parse_anchor_year("800 CE"), 800)
        self.assertEqual(parse_anchor_year("1300"), 1300)

    def test_payload_json_roundtrip(self):
        data = json.loads(PAYLOAD.read_text(encoding="utf-8"))
        self.assertEqual(data["candidate_id"], "post-r1-cumulative-review-v3-cross-frame")


if __name__ == "__main__":
    unittest.main()
