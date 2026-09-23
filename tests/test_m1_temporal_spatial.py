from pathlib import Path
import json
import unittest

ROOT = Path(__file__).resolve().parents[1]
FIXTURE = ROOT / "tests" / "fixtures" / "methodology" / "m1_temporal_spatial_prototype.json"


def active_at(case, year):
    query_window = case.get("query_window")
    if query_window and not (query_window[0] <= year <= query_window[1]):
        return False
    mode = case.get("applicability_mode")
    intervals = case.get("asserted_intervals", [])
    if mode in {"continuous_interval", "bounded_occurrence", "alternative_dates"}:
        return any(start <= year <= end for start, end in intervals)
    return False


class M1TemporalSpatialPrototypeTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.fixture = json.loads(FIXTURE.read_text(encoding="utf-8"))
        cls.cases = {item["id"]: item for item in cls.fixture["cases"]}

    def test_prototype_is_noncanonical_and_preserves_release(self):
        self.assertEqual(self.fixture["status"], "experimental_not_canonical")
        self.assertEqual(self.fixture["legacy_release"], "v0.6.1")
        self.assertNotIn("approximate_period", self.fixture["applicability_modes"])
        self.assertIn("approximate", self.fixture["temporal_precision_values"])

    def test_silla_outer_window_does_not_become_continuous_validity(self):
        case = self.cases["silla-alternative-dates"]
        source = json.loads((ROOT / case["source_case"]).read_text(encoding="utf-8"))
        self.assertEqual(source["claim"]["from_year"], 695)
        self.assertEqual(source["claim"]["to_year"], 819)
        for year in case["positive_years"]:
            self.assertTrue(active_at(case, year))
        for year in case["negative_probe_years"]:
            self.assertFalse(active_at(case, year))

    def test_period_level_synthesis_can_assert_continuity_with_broad_precision(self):
        case = self.cases["hittite-period-synthesis"]
        self.assertEqual(case["applicability_mode"], "continuous_interval")
        self.assertEqual(case["temporal_precision"], "broad_range")
        for year in case["positive_probe_years"]:
            self.assertTrue(active_at(case, year))
        for year in case["negative_probe_years"]:
            self.assertFalse(active_at(case, year))

    def test_temporal_precision_does_not_change_applicability_truth(self):
        exact = self.cases["synthetic-continuous-exact"]
        approximate = self.cases["synthetic-continuous-approximate"]
        self.assertNotEqual(exact["temporal_precision"], approximate["temporal_precision"])
        for year in range(-505, -444):
            self.assertEqual(active_at(exact, year), active_at(approximate, year))

    def test_approximation_alone_does_not_fill_query_window(self):
        case = self.cases["synthetic-approximate-bounded-occurrence"]
        self.assertEqual(case["temporal_precision"], "approximate")
        for year in case["positive_probe_years"]:
            self.assertTrue(active_at(case, year))
        for year in case["negative_probe_years"]:
            self.assertFalse(active_at(case, year))

    def test_geometry_does_not_enlarge_local_inference(self):
        case = self.cases["synthetic-local-to-polity-rejected"]
        self.assertNotEqual(case["containing_polity"], case["inference_extent"])
        self.assertFalse(case["whole_polity_fill_allowed"])

    def test_broader_inference_requires_reviewed_basis_and_rationale(self):
        case = self.cases["synthetic-reviewed-generalization"]
        self.assertNotEqual(case["evidence_locus"], case["inference_extent"])
        self.assertNotEqual(case["generalization_basis"], "none")
        self.assertTrue(case["generalization_rationale"].strip())
        self.assertTrue(case["whole_polity_fill_allowed"])

    def test_bce_signed_year_convention_survives(self):
        case = self.cases["synthetic-continuous-exact"]
        self.assertLess(case["query_window"][0], 0)
        self.assertTrue(active_at(case, -475))


if __name__ == "__main__":
    unittest.main()
