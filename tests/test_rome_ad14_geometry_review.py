from __future__ import annotations

import json
from pathlib import Path
import unittest

ROOT = Path(__file__).resolve().parents[1]
CANDIDATE = (
    ROOT
    / "data"
    / "research"
    / "geometry_reviews"
    / "rome_early_principate_ad14_awmc_v1.json"
)


def point_in_ring(point: tuple[float, float], ring: list[list[float]]) -> bool:
    x, y = point
    inside = False
    j = len(ring) - 1
    for i in range(len(ring)):
        xi, yi = ring[i]
        xj, yj = ring[j]
        crosses = (yi > y) != (yj > y)
        if crosses and x < (xj - xi) * (y - yi) / (yj - yi) + xi:
            inside = not inside
        j = i
    return inside


def point_in_polygon(point: tuple[float, float], polygon: list[list[list[float]]]) -> bool:
    if not point_in_ring(point, polygon[0]):
        return False
    return not any(point_in_ring(point, hole) for hole in polygon[1:])


def covers(point: tuple[float, float], geometry: dict) -> bool:
    if geometry["type"] == "Polygon":
        return point_in_polygon(point, geometry["coordinates"])
    if geometry["type"] == "MultiPolygon":
        return any(point_in_polygon(point, p) for p in geometry["coordinates"])
    raise AssertionError(f"unexpected geometry type {geometry['type']}")


class RomeAd14GeometryReviewTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.review = json.loads(CANDIDATE.read_text(encoding="utf-8"))
        cls.geometry = cls.review["proposed_geometry"]["geojson"]

    def test_candidate_is_bounded_approximate_historical_replacement(self) -> None:
        self.assertEqual(
            self.review["candidate_id"],
            "rome-early-principate-ad14-awmc-v1",
        )
        self.assertEqual(
            self.review["proposed_geometry"]["accuracy_status"],
            "approximate_historical",
        )
        self.assertEqual(self.review["spatial_entity"]["target_from_year"], 14)
        self.assertEqual(self.review["spatial_entity"]["target_to_year"], 22)
        self.assertEqual(
            self.review["spatial_entity"]["incumbent_geometry_id"],
            "b7c31528-ff4c-49cf-a95b-c662afab4339",
        )

    def test_source_identity_and_license_are_explicit(self) -> None:
        source = self.review["source"]
        self.assertEqual(
            source["source_file_sha256"],
            "fddb933ecf9dce7e2a56c1ecbe051f81287890d21676e2cdbf6b47c2556bf85c",
        )
        self.assertIn("CC-BY-NC", source["license_status"])
        self.assertIn(
            "33a41a0bd16fc159a19b294c5cf3072a56c77eb7",
            source["version_label"],
        )
        self.assertIn(
            "1229c07850753cc28dec1e222469201728c5af46",
            source["version_label"],
        )

    def test_quantitative_review_is_material_but_bounded(self) -> None:
        metrics = self.review["quantitative_review"]
        self.assertEqual(metrics["source_feature_count"], 109)
        self.assertEqual(metrics["source_points"], 6741)
        self.assertLess(metrics["source_outside_canonical_land_pct"], 1.0)
        self.assertGreater(metrics["land_clipped_vs_incumbent_render_symdiff_pct"], 10.0)
        self.assertLess(metrics["land_clipped_vs_incumbent_render_symdiff_pct"], 25.0)

    def test_frontier_sanity(self) -> None:
        expected = {
            "Rome": ((12.4964, 41.9028), True),
            "Lutetia": ((2.3522, 48.8566), True),
            "Cologne": ((6.9603, 50.9375), True),
            "Alexandria": ((29.9187, 31.2001), True),
            "Antioch": ((36.1600, 36.2000), True),
            "London": ((-0.1276, 51.5072), False),
            "Central Germania": ((10.0, 51.0), False),
            "Armenia interior": ((44.5, 40.2), False),
            "Central Arabia": ((42.0, 25.0), False),
            "Central Sahara": ((10.0, 25.0), False),
        }
        for name, (point, wanted) in expected.items():
            with self.subTest(name=name):
                self.assertEqual(covers(point, self.geometry), wanted)

    def test_rejected_incremental_alternative_stays_rejected(self) -> None:
        rejected = self.review["rejected_alternatives"]
        self.assertTrue(
            any(
                "incremental expansion layers" in item["reason"]
                for item in rejected
                if "siriusbontea" in item["source"]
            )
        )


if __name__ == "__main__":
    unittest.main()
