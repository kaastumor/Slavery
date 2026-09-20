from pathlib import Path
import importlib.util
import json
import tempfile
import unittest


ROOT = Path(__file__).resolve().parents[1]
MODULE_PATH = ROOT / "tools" / "build_geometry_visual_review.py"
SPEC = importlib.util.spec_from_file_location("build_geometry_visual_review", MODULE_PATH)
MODULE = importlib.util.module_from_spec(SPEC)
assert SPEC.loader is not None
SPEC.loader.exec_module(MODULE)


class GeometryVisualReviewTests(unittest.TestCase):
    def test_generates_review_sheet_and_index(self):
        source = {
            "type": "FeatureCollection",
            "features": [{
                "type": "Feature",
                "properties": {"geometry_id": "g-1", "name": "Synthetic"},
                "geometry": {"type": "Polygon", "coordinates": [[[0,0],[1,0],[1,1],[0,1],[0,0]]]},
            }],
        }
        candidate = {
            "type": "FeatureCollection",
            "features": [{
                "type": "Feature",
                "properties": {"geometry_id": "g-1", "name": "Synthetic"},
                "geometry": {
                    "type": "MultiPolygon",
                    "coordinates": [
                        [[[0,0],[0.9,0],[0.9,1],[0,1],[0,0]]],
                        [[[0.2,0.2],[0.3,0.2],[0.3,0.3],[0.2,0.3],[0.2,0.2]]],
                    ],
                },
            }],
        }
        land = {
            "type": "FeatureCollection",
            "features": [{
                "type": "Feature",
                "properties": {},
                "geometry": {"type": "Polygon", "coordinates": [[[-1,-1],[2,-1],[2,2],[-1,2],[-1,-1]]]},
            }],
        }
        decision = {
            "features": [{
                "geometry_id": "g-1",
                "status": "qc_passed",
                "reasons": [],
                "metrics": {
                    "area_delta_pct": -1.0,
                    "symmetric_difference_pct": 1.0,
                    "hausdorff_m": 1000
                },
            }],
        }
        with tempfile.TemporaryDirectory() as td:
            root = Path(td)
            for name, payload in [
                ("source.json", source),
                ("candidate.json", candidate),
                ("land.json", land),
                ("decision.json", decision),
            ]:
                (root / name).write_text(json.dumps(payload), encoding="utf-8")

            out = root / "out"
            old_argv = __import__("sys").argv
            try:
                __import__("sys").argv = [
                    "build_geometry_visual_review.py",
                    str(root / "source.json"),
                    str(root / "candidate.json"),
                    str(root / "land.json"),
                    str(root / "decision.json"),
                    str(out),
                ]
                self.assertEqual(MODULE.main(), 0)
            finally:
                __import__("sys").argv = old_argv

            sheets = list(out.glob("*.svg"))
            self.assertEqual(len(sheets), 1)
            svg = sheets[0].read_text(encoding="utf-8")
            self.assertIn("Synthetic", svg)
            self.assertIn("qc_passed", svg)
            self.assertIn("Candidate + source outline + canonical land", svg)
            self.assertEqual(svg.count('class="candidate"'), 2)
            index = (out / "index.html").read_text(encoding="utf-8")
            self.assertIn("open SVG", index)


if __name__ == "__main__":
    unittest.main()
