from pathlib import Path
import json
import sys
import tempfile
import unittest

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "tools"))

from add_research_case import (  # noqa: E402\n    SpecError,\n    case_content_sha256,\n    load_spec,\n    plan,\n    validate_case_spec,\n)


def valid_case():
    return {
        "spatial_entity": {
            "canonical_name": "Example ancient site",
            "entity_type_code": "site",
        },
        "claim": {
            "from_year": -999,
            "to_year": -950,
            "summary": "Bounded example claim.",
            "territorial_practice": {
                "practice_type_code": "slavery_enslavement",
                "practice_level": None,
                "coverage_state_code": "reviewed",
            },
        },
        "evidence": [
            {
                "source": {
                    "title": "Example publication",
                    "source_classification": "secondary",
                },
                "version": {"url_or_identifier": "https://example.org/source"},
                "direction": "supports",
            }
        ],
        "geometry": {
            "from_year": -999,
            "to_year": -950,
            "accuracy_status": "unresolved",
            "resolution_method": "No defensible geometry yet.",
            "geojson": None,
        },
    }


class ResearchCaseValidationTests(unittest.TestCase):
    def test_valid_case_defaults_to_unpublished(self):
        spec = valid_case()
        validate_case_spec(spec)
        self.assertEqual(plan(spec)["publication_status"], "unpublished")
        self.assertEqual(plan(spec)["practice_level"], None)


    def test_case_key_is_required_and_stable(self):
        spec = valid_case()
        validate_case_spec(spec)
        first = case_content_sha256(spec)
        second = case_content_sha256(json.loads(json.dumps(spec)))
        self.assertEqual(first, second)
        self.assertEqual(len(first), 64)

        del spec["case_key"]
        with self.assertRaises(SpecError):
            validate_case_spec(spec)

    def test_case_key_rejects_unstable_display_text(self):
        spec = valid_case()
        spec["case_key"] = "Bad Key With Spaces"
        with self.assertRaises(SpecError):
            validate_case_spec(spec)
\n    def test_rejects_direct_publication(self):
        spec = valid_case()
        spec["claim"]["publication_status"] = "published"
        with self.assertRaises(SpecError):
            validate_case_spec(spec)

    def test_rejects_false_year_order(self):
        spec = valid_case()
        spec["claim"]["from_year"] = 100
        spec["claim"]["to_year"] = 50
        with self.assertRaises(SpecError):
            validate_case_spec(spec)

    def test_unresolved_geometry_cannot_have_shape(self):
        spec = valid_case()
        spec["geometry"]["geojson"] = {"type": "Point", "coordinates": [0, 0]}
        with self.assertRaises(SpecError):
            validate_case_spec(spec)

    def test_loads_json_file(self):
        with tempfile.TemporaryDirectory() as td:
            path = Path(td) / "case.json"
            path.write_text(json.dumps(valid_case()), encoding="utf-8")
            loaded = load_spec(path)
            self.assertEqual(loaded["spatial_entity"]["canonical_name"], "Example ancient site")


if __name__ == "__main__":
    unittest.main()
