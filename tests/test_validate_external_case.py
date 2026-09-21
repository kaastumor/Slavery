from pathlib import Path
import copy
import json
import sys
import unittest

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "tools"))

from validate_external_case import SpecError, validate  # noqa: E402

CASE_PATH = ROOT / "data" / "research" / "external_cases" / "global_04_zaghawa_captive_export.json"

class ExternalParticipationValidationTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.case = json.loads(CASE_PATH.read_text(encoding="utf-8"))

    def test_staged_zaghawa_case_is_valid(self):
        validate(copy.deepcopy(self.case))

    def test_rejects_territorial_practice_leakage(self):
        case = copy.deepcopy(self.case)
        case["claim"]["territorial_practice"] = {"practice_level": "P2"}
        with self.assertRaises(SpecError):
            validate(case)

    def test_rejects_p_level_on_external_claim(self):
        case = copy.deepcopy(self.case)
        case["claim"]["practice_level"] = "P1"
        with self.assertRaises(SpecError):
            validate(case)

    def test_rejects_nationality_inference_guardrail(self):
        case = copy.deepcopy(self.case)
        case["guardrails"]["nationality_inferred"] = True
        with self.assertRaises(SpecError):
            validate(case)

    def test_rejects_published_research_staging(self):
        case = copy.deepcopy(self.case)
        case["claim"]["publication_status"] = "published"
        with self.assertRaises(SpecError):
            validate(case)

    def test_rejects_geometry_for_unresolved_case(self):
        case = copy.deepcopy(self.case)
        case["geometry"]["geojson"] = {"type": "Point", "coordinates": [0, 0]}
        with self.assertRaises(SpecError):
            validate(case)

if __name__ == "__main__":
    unittest.main()
