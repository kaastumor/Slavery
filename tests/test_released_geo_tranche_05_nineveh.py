from pathlib import Path
import json
import unittest


ROOT = Path(__file__).resolve().parents[1]
REVIEW = (
    ROOT
    / "data"
    / "research"
    / "geometry_reviews"
    / "population_100_100_released_geo_tranche_05_nineveh.json"
)


class NinevehReleasedGeometryReviewTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.review = json.loads(REVIEW.read_text(encoding="utf-8"))

    def test_exact_released_identity_is_preserved(self) -> None:
        case = self.review["released_case"]
        self.assertEqual(
            case["spatial_entity_id"], "6b3fd57f-4d30-44d2-9d15-427e41b6cd47"
        )
        self.assertEqual(case["claim_id"], "8077abf3-f506-4bb1-908a-4aa5abd12369")
        self.assertEqual(case["claim_kind"], "territorial_practice")
        self.assertEqual((case["from_year"], case["to_year"]), (-695, -695))
        self.assertIsNone(case["practice_level"])
        self.assertEqual(case["current_geometry_count"], 0)

    def test_candidate_is_a_source_pinned_point_only(self) -> None:
        candidate = self.review["candidate"]
        geometry = candidate["geometry"]
        source = candidate["geometry_source"]
        self.assertEqual(candidate["disposition"], "ACCEPTED_STAGING")
        self.assertEqual(geometry["geometry_role"], "site_navigation_locator")
        self.assertEqual(geometry["accuracy_status"], "specialist")
        self.assertEqual(geometry["geojson"]["type"], "Point")
        self.assertEqual(geometry["geojson"]["coordinates"], [43.155403, 36.366841])
        self.assertEqual(source["source_native_place_id"], "874621")
        self.assertEqual(source["source_native_location_id"], "dare-location")
        self.assertEqual(
            source["snapshot_commit"], "a7b17570094a6544017290cbb6d780d2769dd112"
        )
        self.assertEqual(
            source["snapshot_blob_sha"], "646d909e88c4913213eb2d00fdf70188a1c67ca8"
        )
        self.assertEqual(source["source_native_interval"], {"start": -750, "end": 640})

    def test_review_is_fail_closed_and_has_no_release_effect(self) -> None:
        self.assertEqual(
            self.review["governed_db_preflight"]["status"],
            "NOT_RUN_RUNTIME_ACCESS_UNAVAILABLE",
        )
        qc = self.review["qc"]
        self.assertEqual(qc["historical_practice_polygons_added"], 0)
        self.assertEqual(qc["historical_claim_delta"], 0)
        self.assertEqual(qc["p_level_changes"], 0)
        self.assertEqual(qc["release_membership_delta"], 0)
        self.assertEqual(qc["serving_channel_delta"], 0)
        self.assertIn("none", self.review["release_effect"])


if __name__ == "__main__":
    unittest.main()
