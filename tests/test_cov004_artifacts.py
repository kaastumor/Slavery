import json
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
EXP = ROOT / "experiments" / "falsification-atlas"

class Cov004ArtifactTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.data = json.loads((EXP / "arm_d_data.json").read_text(encoding="utf-8"))
        cls.baseline = (EXP / "21_ARM_D_BASELINE.html").read_text(encoding="utf-8")
        cls.atlas = (EXP / "22_ARM_D_ATLAS.html").read_text(encoding="utf-8")

    def test_arm_d_frozen_target_counts(self):
        targets = self.data["targets"]
        self.assertEqual(len(targets), 12)
        self.assertEqual(sum(t["tier"] == "C1" for t in targets), 8)
        self.assertEqual(sum(t["tier"] == "C0" for t in targets), 4)
        self.assertEqual(len({t["id"] for t in targets}), 12)

    def test_c0_never_contains_subject_claim(self):
        for t in self.data["targets"]:
            if t["tier"] == "C0":
                self.assertFalse(t["practice"])
                self.assertFalse(t["legal"])
                self.assertFalse(t["network"])
                self.assertIn("research not performed", t["research"])

    def test_nonpolity_geometry_types_remain_explicit(self):
        allowed = {"point", "route", "fuzzy"}
        for t in self.data["targets"]:
            self.assertIn(t["geometry"]["type"], allowed)
            self.assertTrue(t["geometry"]["precision"])
        self.assertEqual(next(t for t in self.data["targets"] if t["id"] == "silk_road_700")["geometry"]["type"], "route")
        self.assertEqual(next(t for t in self.data["targets"] if t["id"] == "samoa_1700")["geometry"]["type"], "fuzzy")

    def test_baseline_and_atlas_embed_same_target_set(self):
        for t in self.data["targets"]:
            self.assertIn(t["id"], self.baseline)
            self.assertIn(t["id"], self.atlas)
        self.assertIn("const DATA=", self.baseline)
        self.assertIn("const DATA=", self.atlas)

    def test_atlas_layers_do_not_replace_baseline_data(self):
        for layer in ["practice", "legal", "network", "research", "geometry"]:
            self.assertIn(f'data-layer="{layer}"', self.atlas)
        self.assertIn("COV-004 Baseline B", self.baseline)
        self.assertIn("COV-004 Atlas A", self.atlas)

if __name__ == "__main__":
    unittest.main()
