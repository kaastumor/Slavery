from __future__ import annotations
import hashlib,json,re
from pathlib import Path
import unittest
ROOT=Path(__file__).resolve().parents[1]
V1=ROOT/"data/serving/v0.8.0-public-mvp-v1"
V2=ROOT/"data/serving/v0.8.0-public-mvp-v2"
ASSETS=ROOT/"web/public/release-geometries/v0.8.0-public-mvp-v2"
class V080RenderAssetTests(unittest.TestCase):
 @classmethod
 def setUpClass(cls):
  cls.v1=json.loads((V1/"atlas-data.json").read_text(encoding="utf-8"));cls.v2_bytes=(V2/"atlas-data.json").read_bytes();cls.v2=json.loads(cls.v2_bytes);cls.manifest=json.loads((V2/"materialization-manifest.json").read_text(encoding="utf-8"));cls.index=json.loads((ASSETS/"manifest.json").read_text(encoding="utf-8"))
 def test_claim_projection_unchanged(self):
  def claims(p):return {c["claim_id"]:c for place in p["places"] for c in place["claims"]}
  self.assertEqual(claims(self.v2),claims(self.v1));self.assertEqual(len(claims(self.v2)),53)
 def test_every_mapped_geometry_is_versioned_asset(self):
  gs=[g for p in self.v2["places"] for g in p["geometries"]];self.assertEqual(len(gs),46);self.assertEqual(len(self.index["assets"]),46);fabric=self.v2["cartography"]["fabric_id"]
  for g in gs:
   self.assertIsNone(g["geometry"]);self.assertTrue(g["geometry_asset"].startswith("release-geometries/v0.8.0-public-mvp-v2/"));self.assertEqual(g["render_land_mask_id"],fabric);asset_path=ROOT/"web/public"/g["geometry_asset"];self.assertTrue(asset_path.is_file());asset=json.loads(asset_path.read_text(encoding="utf-8"));self.assertEqual(asset["geometry_id"],g["geometry_id"]);self.assertEqual(asset["render_ewkb_sha256"],g["render_ewkb_sha256"]);self.assertEqual(asset["render_land_mask_id"],fabric);self.assertIsNotNone(asset["geometry"])
 def test_roman_12ce_regression(self):
  old_place=next(p for p in self.v1["places"] if p["name"]=="Roman Empire — early Principate");old=next(g for g in old_place["geometries"] if g["from_year"]==9 and g["to_year"]==13);new_place=next(p for p in self.v2["places"] if p["name"]=="Roman Empire — early Principate");new=next(g for g in new_place["geometries"] if g["from_year"]==9 and g["to_year"]==13);asset=json.loads((ROOT/"web/public"/new["geometry_asset"]).read_text(encoding="utf-8"));self.assertNotEqual(old["geometry"],asset["geometry"]);self.assertIsNone(old.get("render_transform"));self.assertEqual(asset["render_transform"],"boundary_normalized_cache");self.assertEqual(asset["render_policy_id"],"cliopatria-boundary-normalization-v3")
 def test_manifest_and_edge_freeze_v2(self):
  self.assertEqual(self.manifest["materialization_id"],"v0.8.0-public-mvp-v2");self.assertFalse(self.manifest["raw_atlas_geometry_served"]);self.assertEqual(self.manifest["payload_sha256"],hashlib.sha256(self.v2_bytes).hexdigest());module=(ROOT/"supabase/functions/atlas-data/v080_v2_payload.ts").read_text(encoding="utf-8");m=re.search(r"export const V080_V2_PAYLOAD = (.+);\n?$",module,flags=re.DOTALL);self.assertIsNotNone(m);self.assertEqual(json.loads(m.group(1)).encode("utf-8"),self.v2_bytes)
 def test_client_lazy_loads_and_validates_assets(self):
  src=(ROOT/"web/src/main.ts").read_text(encoding="utf-8");self.assertIn("ensureGeometryAssetsForYear",src);self.assertIn("render geometry fingerprint mismatch",src);self.assertIn("render geometry land-fabric mismatch",src)
if __name__=="__main__":unittest.main()
