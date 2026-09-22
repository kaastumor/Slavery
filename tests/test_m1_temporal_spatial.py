from pathlib import Path
import json
import unittest

ROOT = Path(__file__).resolve().parents[1]
FIXTURE = ROOT / "tests" / "fixtures" / "methodology" / "m1_temporal_spatial_prototype.json"


def active_at(case, year):
    if not (case["query_window"][0] <= year <= case["query_window"][1]):
        return False
    mode = case["time_mode"]
    intervals = case.get("asserted_intervals", [])
    if mode in {"continuous_interval", "bounded_occurrence", "approximate_period"}:
        return any(start <= year <= end for start, end in intervals)
    if mode == "alternative_dates":
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

    def test_silla_outer_window_does_not_become_continuous_validity(self):
        case = self.cases["silla-alternative-dates"]
        source = json.loads((ROOT / case["source_case"]).read_text(encoding="utf-8"))
        self.assertEqual(source["claim"]["from_year"], 695)
        self.assertEqual(source["claim"]["to_year"], 819)
        for year in case["positive_years"]:
            self.assertTrue(active_at(case, year))
        for year in case["negative_probe_years"]:
            self.assertFalse(active_at(case, year))

    def test_continuous_interval_has_positive_interior(self):
        case = self.cases["synthetic-continuous"]
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
        case = self.cases["synthetic-continuous"]
        self.assertLess(case["query_window"][0], 0)
        self.assertTrue(active_at(case, -475))


if __name__ == "__main__":
    unittest.main()
