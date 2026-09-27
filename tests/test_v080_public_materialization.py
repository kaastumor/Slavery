from __future__ import annotations

import hashlib
import json
import re
from pathlib import Path
import unittest

ROOT = Path(__file__).resolve().parents[1]
RELEASE = ROOT / "data" / "releases" / "v0.8.0"
MATERIALIZATION = ROOT / "data" / "serving" / "v0.8.0-public-mvp-v1"


class V080PublicMaterializationTests(unittest.TestCase):
    def test_materialization_is_exact_release_projection(self) -> None:
        authority = json.loads((RELEASE / "authority-state.json").read_text(encoding="utf-8"))
        payload_bytes = (MATERIALIZATION / "atlas-data.json").read_bytes()
        payload = json.loads(payload_bytes)
        manifest = json.loads((MATERIALIZATION / "materialization-manifest.json").read_text(encoding="utf-8"))
        expected_claims = {cid for cid,obj in authority["objects"]["claims"].items() if obj["claim"]["claim_kind_code"] == "territorial_practice"}
        displayed = {claim["claim_id"] for place in payload["places"] for claim in place["claims"]}
        self.assertEqual(displayed, expected_claims)
        self.assertEqual(len(displayed), 53)
        self.assertEqual(len(payload["places"]), 48)
        self.assertEqual(sum(len(p["geometries"]) for p in payload["places"]), 46)
        self.assertEqual(payload["release_version"], "v0.8.0")
        self.assertTrue(payload["canonical"])
        self.assertEqual(payload["serving_materialization_id"], "v0.8.0-public-mvp-v1")
        self.assertEqual(manifest["payload_sha256"], hashlib.sha256(payload_bytes).hexdigest())
        self.assertEqual(manifest["canonical_source_release"], "v0.8.0")
        self.assertEqual(manifest["rollback_release"], "v0.7.0-public-mvp-v1")

    def test_post_m1_null_levels_and_reviewed_disputes_survive(self) -> None:
        payload = json.loads((MATERIALIZATION / "atlas-data.json").read_text(encoding="utf-8"))
        claims = {c["claim_id"]:c for p in payload["places"] for c in p["claims"]}
        for claim_id in {
            "04cdf6ea-5b43-4f44-94a4-04b720ac7a2a","4897a70a-0286-4281-9b65-68901135c993",
            "53405178-e879-4ef2-a12d-3cfcc0ad55f6","60f28ab3-2f20-4490-843b-c03a727d2c1d",
            "687bed4f-281e-4821-bc23-1e75cb65dd99","8077abf3-f506-4bb1-908a-4aa5abd12369",
            "a0e592c2-aa47-4e55-8b62-c4923f7de6f2","abf43c9e-4689-4620-8418-fbf92e7725cc",
            "bcd7f1d7-a192-4bcd-880d-16a899dc11ff","dde79d87-898c-4c57-902a-b3d3fd65c9bb",
            "e66638b2-f022-4bca-b173-5c128f3a3739",
        }:
            self.assertIsNone(claims[claim_id]["practice_level"])
        self.assertEqual(claims["cfd709dd-55ad-4f92-a6ec-f6c7910b3fe1"]["classification_status"], "disputed")
        self.assertEqual(claims["dac1fdbe-8a72-411e-a43c-6180e3d24298"]["classification_status"], "reviewed_with_date_dispute")

    def test_edge_embeds_exact_payload(self) -> None:
        payload_bytes=(MATERIALIZATION / "atlas-data.json").read_bytes()
        module=(ROOT / "supabase" / "functions" / "atlas-data" / "v080_payload.ts").read_text(encoding="utf-8")
        match=re.search(r"export const V080_PAYLOAD = (.+);\n?$",module,flags=re.DOTALL)
        self.assertIsNotNone(match)
        self.assertEqual(json.loads(match.group(1)).encode("utf-8"),payload_bytes)
        self.assertIn('b49eee6c843dc1a8dcc0aabdb71e88600c452262d83903b4b443f07cac77bcbd',module)
        index=(ROOT / "supabase" / "functions" / "atlas-data" / "index.ts").read_text(encoding="utf-8")
        self.assertIn("V080_MATERIALIZATION_ID",index)
        self.assertIn("audit.release_channel",index)


if __name__ == "__main__":
    unittest.main()
