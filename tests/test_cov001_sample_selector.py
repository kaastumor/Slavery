import importlib.util
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
MODULE_PATH = ROOT / "experiments" / "coverage-value" / "select_sample.py"

spec = importlib.util.spec_from_file_location("cov001_selector", MODULE_PATH)
selector = importlib.util.module_from_spec(spec)
assert spec.loader is not None
spec.loader.exec_module(selector)


def square(lon: float, lat: float):
    return {
        "type": "Polygon",
        "coordinates": [[
            [lon - 1, lat - 1],
            [lon + 1, lat - 1],
            [lon + 1, lat + 1],
            [lon - 1, lat + 1],
            [lon - 1, lat - 1],
        ]],
    }


def feature(name: str, lon: float, lat: float):
    return {
        "type": "Feature",
        "properties": {
            "Name": name,
            "Type": "POLITY",
            "FromYear": -500,
            "ToYear": 1800,
            "Components": "",
            "MemberOf": "",
            "SeshatID": "",
            "Wikidata": "",
        },
        "geometry": square(lon, lat),
    }


class CoverageValueSamplerTests(unittest.TestCase):
    def test_sector_assignment_is_disjoint_for_representative_points(self):
        examples = {
            "A": (-100, 40),
            "B": (-70, -20),
            "C": (20, 0),
            "D": (20, 50),
            "E": (80, 20),
            "F": (130, 20),
        }
        for expected, (lon, lat) in examples.items():
            self.assertEqual(selector.sector(lon, lat), expected)

    def test_bbox_midpoint_is_sampling_only_and_deterministic(self):
        self.assertEqual(selector.bbox_midpoint(square(20, 10)), (20.0, 10.0))

    def test_inclusive_anchor_year_filter(self):
        props = {"FromYear": 500, "ToYear": 1300}
        self.assertTrue(selector.active(props, 500))
        self.assertTrue(selector.active(props, 1300))
        self.assertFalse(selector.active(props, 499))
        self.assertFalse(selector.active(props, 1301))

    def test_six_sector_fixture_produces_all_24_cells(self):
        data = {
            "features": [
                feature("A-polity", -100, 40),
                feature("B-polity", -70, -20),
                feature("C-polity", 20, 0),
                feature("D-polity", 20, 50),
                feature("E-polity", 80, 20),
                feature("F-polity", 130, 20),
            ]
        }
        first = selector.build_sample(data)
        second = selector.build_sample(data)

        self.assertEqual(first, second)
        self.assertEqual(first["valid_cells"], 24)
        self.assertEqual(first["sampling_gaps"], 0)
        self.assertTrue(first["viable"])
        self.assertEqual(len(first["cells"]), 24)

    def test_composites_are_not_sample_targets(self):
        f = feature("(Composite)", 20, 50)
        f["properties"]["Components"] = "Child A;Child B"
        self.assertFalse(selector.eligible(f, 500))


if __name__ == "__main__":
    unittest.main()
