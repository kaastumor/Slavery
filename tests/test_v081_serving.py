from __future__ import annotations
import hashlib
import json
import re
from pathlib import Path
import unittest

ROOT=Path(__file__).resolve().parents[1]
MAT=ROOT/"data"/"serving"/"v0.8.1-public-mvp-v1"
ASSET=ROOT/"web"/"public"/"release-geometries"/"v0.8.1-public-mvp-v1"/"b3066705-616e-42c7-a50d-656c6926813c.json"
INDEX=ROOT/"web"/"public"/"release-geometries"/"v0.8.1-public-mvp-v1"/"manifest.json"
AUDIT=ROOT/"data"/"research"/"geometry_reviews"/"v081_corpus_render_alignment_audit.json"

class V081ServingTests(unittest.TestCase):
    def test_payload_and_materialization(self):
        payload_bytes=(MAT/"atlas-data.json").read_bytes()
        payload=json.loads(payload_bytes)
        manifest=json.loads((MAT/"materialization-manifest.json").read_text())
        self.assertEqual(payload["release_version"],"v0.8.1")
        self.assertEqual(payload["serving_materialization_id"],"v0.8.1-public-mvp-v1")
        self.assertEqual(manifest["payload_sha256"],hashlib.sha256(payload_bytes).hexdigest())
        self.assertEqual(manifest["rollback_release"],"v0.8.0-public-mvp-v2")
        self.assertEqual(sum(len(p["claims"]) for p in payload["places"]),53)
        self.assertEqual(sum(len(p["geometries"]) for p in payload["places"]),46)

    def test_rome_replacement_and_asset_lineage(self):
        payload=json.loads((MAT/"atlas-data.json").read_text())
        rome=next(p for p in payload["places"] if p["spatial_entity_id"]=="ae1111c0-98bf-4bef-a1b2-98736f618aa3")
        ids={g["geometry_id"] for g in rome["geometries"]}
        self.assertIn("b3066705-616e-42c7-a50d-656c6926813c",ids)
        self.assertNotIn("b7c31528-ff4c-49cf-a95b-c662afab4339",ids)
        new=next(g for g in rome["geometries"] if g["geometry_id"]=="b3066705-616e-42c7-a50d-656c6926813c")
        self.assertEqual(new["geometry_asset_materialization_id"],"v0.8.1-public-mvp-v1")
        self.assertEqual(new["render_transform"],"land_clip")
        for p in payload["places"]:
            for g in p["geometries"]:
                if g["geometry_id"]!="b3066705-616e-42c7-a50d-656c6926813c":
                    self.assertEqual(g["geometry_asset_materialization_id"],"v0.8.0-public-mvp-v2")

    def test_new_asset_and_index(self):
        asset=json.loads(ASSET.read_text())
        idx=json.loads(INDEX.read_text())
        self.assertEqual(asset["materialization_id"],"v0.8.1-public-mvp-v1")
        self.assertEqual(asset["geometry_id"],"b3066705-616e-42c7-a50d-656c6926813c")
        self.assertEqual(asset["render_land_mask_id"],"natural-earth-ne_10m_land-v5.1.1-ca96624")
        self.assertEqual(len(idx["assets"]),46)
        self.assertEqual(sum(1 for x in idx["assets"] if x["asset_materialization_id"]=="v0.8.1-public-mvp-v1"),1)
        self.assertEqual(sum(1 for x in idx["assets"] if x["asset_materialization_id"]=="v0.8.0-public-mvp-v2"),45)

    def test_corpus_alignment(self):
        audit=json.loads(AUDIT.read_text())
        self.assertTrue(audit["pass"])
        self.assertEqual(audit["geometry_count"],46)
        for row in audit["rows"]:
            if "POLYGON" in row["geometry_type"].upper():
                self.assertLessEqual(float(row["render_outside_land_pct"]),0.0001)
                self.assertEqual(row["render_land_mask_id"],audit["canonical_land_mask_id"])

    def test_edge_and_client_contract(self):
        payload_bytes=(MAT/"atlas-data.json").read_bytes()
        module=(ROOT/"supabase"/"functions"/"atlas-data"/"v081_payload.ts").read_text()
        match=re.search(r"export const V081_PAYLOAD = (.+);\n?$",module,re.DOTALL)
        self.assertIsNotNone(match)
        self.assertEqual(json.loads(match.group(1)).encode(),payload_bytes)
        self.assertIn("56cb29dfd8fcb968d08ae3a7fa0bd8b11af44e15c03facc7ee2c6b27cae49347",module)
        edge=(ROOT/"supabase"/"functions"/"atlas-data"/"index.ts").read_text()
        self.assertIn("V081_MATERIALIZATION_ID",edge)
        client=(ROOT/"web"/"src"/"main.ts").read_text()
        self.assertIn("geometry_asset_materialization_id",client)

if __name__=="__main__":
    unittest.main()
