from pathlib import Path
import copy
import json
import subprocess
import sys
import tempfile
import unittest

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "tools"))

from add_external_participation_case import plan  # noqa: E402
from add_research_case import case_content_sha256  # noqa: E402
from validate_external_case import load as load_external_spec, validate  # noqa: E402


def valid_external_case():
    return {
        "case_key": "test/example-network-v1",
        "claim_kind": "external_participation",
        "spatial_entity": {
            "canonical_name": "Example analytical network",
            "entity_type_code": "region",
        },
        "claim": {
            "from_year": 900,
            "to_year": 910,
            "summary": "Bounded example network participation claim.",
            "review_status": "reviewed",
            "publication_status": "unpublished",
            "external_participation": {
                "participation_type_code": "slave_trade_network",
                "role_text": "Example bounded network role.",
            },
        },
        "evidence": [
            {
                "source": {"title": "Example source"},
                "version": {"url_or_identifier": "https://example.org/external-source"},
                "direction": "supports",
            }
        ],
        "geometry": {
            "from_year": 900,
            "to_year": 910,
            "accuracy_status": "unresolved",
            "resolution_method": "No defensible network geometry.",
            "geojson": None,
        },
        "guardrails": {
            "territorial_practice_inferred": False,
            "practice_level_assigned": False,
            "nationality_inferred": False,
            "absence_inferred": False,
        },
    }


class ExternalParticipationImporterTests(unittest.TestCase):
    def test_plan_preserves_external_kind_and_null_p_level(self):
        spec = valid_external_case()
        validate(copy.deepcopy(spec))
        result = plan(spec)
        self.assertEqual(result["claim_kind"], "external_participation")
        self.assertEqual(result["participation_type"], "slave_trade_network")
        self.assertIsNone(result["practice_level"])
        self.assertEqual(result["publication_status"], "unpublished")
        self.assertEqual(result["geometry_accuracy"], "unresolved")

    def test_content_hash_is_stable(self):
        spec = valid_external_case()
        first = case_content_sha256(spec)
        second = case_content_sha256(json.loads(json.dumps(spec)))
        self.assertEqual(first, second)
        self.assertEqual(len(first), 64)

    def test_loads_current_andaman_packet(self):
        path = (
            ROOT
            / "data/research/recovery/population_100_100_intake_2026_10_01/candidates"
            / "05_andaman_colonial_captivity_c1789_1796.json"
        )
        spec = load_external_spec(path)
        result = plan(spec)
        self.assertEqual(result["claim_kind"], "external_participation")
        self.assertEqual(result["participation_type"], "other")

    def test_loads_json_file(self):
        with tempfile.TemporaryDirectory() as td:
            path = Path(td) / "case.json"
            path.write_text(json.dumps(valid_external_case()), encoding="utf-8")
            loaded = load_external_spec(path)
            self.assertEqual(loaded["case_key"], "test/example-network-v1")

    def test_standalone_apply_is_rejected_before_database_access(self):
        case_path = (
            ROOT
            / "data/research/recovery/population_100_100_intake_2026_10_01/candidates"
            / "05_andaman_colonial_captivity_c1789_1796.json"
        )
        result = subprocess.run(
            [
                sys.executable,
                str(ROOT / "tools/add_external_participation_case.py"),
                str(case_path),
                "--apply",
            ],
            cwd=ROOT,
            capture_output=True,
            text=True,
            check=False,
        )
        self.assertNotEqual(result.returncode, 0)
        self.assertIn(
            "standalone external participation importer has no database commit path",
            result.stdout + result.stderr,
        )



if __name__ == "__main__":
    unittest.main()
