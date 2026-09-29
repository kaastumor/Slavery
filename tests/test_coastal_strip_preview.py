"""Geometric acceptance checks for the presentation preview, in planar metres."""
import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "tools"))
from shapely.geometry import box
from build_coastal_strip_preview import fit_coastal_strip


class CoastalStripTests(unittest.TestCase):
    def test_inward_coast_gap_is_filled_but_inland_border_stays(self):
        land = box(0, 0, 100, 100)
        source = box(3, -5, 60, 105)
        result, _ = fit_coastal_strip(source, land, 5)
        self.assertTrue(result.covers(box(0, 20, 3, 80)))
        self.assertTrue(result.intersection(box(6, 6, 94, 94)).equals(
            source.intersection(box(6, 6, 94, 94))))
        self.assertLess(result.difference(land).area, 1e-9)
        self.assertLess(source.intersection(land).difference(result).area, 1e-9)

    def test_distant_island_and_inland_hole_are_retained(self):
        land = box(0, 0, 100, 100).union(box(110, 0, 120, 10))
        source = box(-2, -2, 102, 102).difference(box(40, 40, 60, 60))
        result, _ = fit_coastal_strip(source, land, 5)
        self.assertLess(result.intersection(box(110, 0, 120, 10)).area, 1e-9)
        self.assertLess(result.intersection(box(40, 40, 60, 60)).area, 1e-9)


if __name__ == "__main__":
    unittest.main()
