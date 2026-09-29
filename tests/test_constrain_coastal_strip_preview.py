"""Acceptance checks for supported land and neighboring-source exclusions."""
import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "tools"))
from shapely.geometry import box
from constrain_coastal_strip_preview import constrain_additions


class ConstrainedCoastalStripTests(unittest.TestCase):
    def test_source_land_survives_and_new_overlap_and_island_do_not(self):
        land = box(0, 0, 100, 100).union(box(105, 0, 110, 5))
        source = box(5, 0, 50, 100)
        fitted = box(0, 0, 55, 100).union(box(105, 0, 110, 5))
        neighbor = box(52, 20, 60, 80)
        result, _, accepted, _, _ = constrain_additions(source, fitted, land, [neighbor])
        self.assertLess(source.intersection(land).difference(result).area, 1e-9)
        self.assertLess(accepted.intersection(neighbor).area, 1e-9)
        self.assertLess(result.intersection(box(105, 0, 110, 5)).area, 1e-9)
        self.assertGreater(accepted.intersection(box(0, 0, 5, 100)).area, 0)


if __name__ == "__main__":
    unittest.main()
