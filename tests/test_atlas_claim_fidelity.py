from __future__ import annotations

import json
from pathlib import Path
import sys
import unittest

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "tools"))
from build_v070_public_materialization import build_payload, temporal_fields_for_serving  # noqa: E402

INTAKE = ROOT / "data" / "research" / "intake" / "atlas_expansion_01"


class ClaimFidelityTests(unittest.TestCase):
    def test_null_level_proposals_do_not_assign_legacy_ordinals_in_prose(self) -> None:
        for name in (
            "01_funan_enslavement.json",
            "02_hawaii_kauwa_dependency.json",
            "03_late_classic_maya_captive_dependency.json",
        ):
            with self.subTest(name=name):
                claim = json.loads((INTAKE / name).read_text(encoding="utf-8"))["claim"]
                self.assertIsNone(claim["territorial_practice"]["practice_level"])
                text = claim["summary"] + " " + claim["territorial_practice"]["notes"]
                self.assertNotRegex(text, r"\bP[1-4]\b")
                self.assertIn("P-level", claim["summary"])

    def test_payload_projection_retains_distinct_exact_and_broad_claims(self) -> None:
        broad = json.loads((INTAKE / "01_funan_enslavement.json").read_text())["claim"]
        exact = {
            "date_text_original": "22 June 1633", "temporal_precision": "exact_event",
            "temporal_certainty": "high",
        }
        def entry(claim_id: str, fields: dict[str, object]) -> dict[str, object]:
            return {
                "claim": {
                    "claim_id": claim_id, "claim_kind_code": "territorial_practice",
                    "from_year": 228, "to_year": 500, "summary": "fixture",
                    **fields,
                },
                "territorial_practice": {"spatial_entity_id": "place", "practice_level": None},
                "claim_sources": [{"source_version_id": "source"}],
            }
        authority = {
            "objects": {
                "claims": {"broad": entry("broad", broad), "exact": entry("exact", exact)},
                "source_versions": {"source": {"source": {}, "source_version": {}}},
                "spatial_entities": {"place": {"spatial_entity": {"canonical_name": "Fixture"}}},
                "research_target_results": {},
            },
            "membership": {
                "spatial_entity_ids": ["place"], "geometry_ids": [],
                "coverage_assessment_ids": [], "source_version_ids": ["source"],
            },
            "cartography": {"id": "fixture", "payload": {}},
        }
        rows = build_payload({"release_version": "v0.8.2", "schema_version": "fixture"}, authority)["places"][0]["claims"]
        by_id = {row["claim_id"]: row for row in rows}
        self.assertEqual(by_id["broad"]["temporal_precision"], "source_context_only")
        self.assertEqual(by_id["broad"]["date_text_original"], broad["date_text_original"])
        self.assertEqual(by_id["exact"]["temporal_precision"], "exact_event")
        old = build_payload({"release_version": "v0.7.0", "schema_version": "fixture"}, authority)["places"][0]["claims"]
        self.assertTrue(all("temporal_precision" not in row for row in old))

    def test_funan_does_not_invent_event_or_geometry_interval(self) -> None:
        spec = json.loads((INTAKE / "01_funan_enslavement.json").read_text(encoding="utf-8"))
        self.assertIsNone(spec["claim"]["from_year"])
        self.assertIsNone(spec["claim"]["to_year"])
        self.assertEqual(spec["claim"]["temporal_precision"], "source_context_only")
        self.assertIsNone(spec["geometry"]["from_year"])
        self.assertIsNone(spec["geometry"]["to_year"])
        self.assertIsNone(spec["geometry"]["geojson"])

    def test_future_projection_preserves_source_date_meaning_without_changing_v070(self) -> None:
        broad = json.loads((INTAKE / "01_funan_enslavement.json").read_text())["claim"]
        expected = {
            "date_text_original": (
                "Enslavement description preserved in Nan Qi Shu (History of the Southern Qi), "
                "compiled in the early sixth century; in the Funan biography the description "
                "follows Jayavarman's 484 CE embassy material, but the underlying observation "
                "date of the passage is not securely recoverable."
            ),
            "temporal_precision": "source_context_only",
            "temporal_certainty": "uncertain",
        }
        self.assertEqual(temporal_fields_for_serving(broad, "v0.8.2"), expected)
        self.assertEqual(temporal_fields_for_serving(broad, "v0.7.0"), {})
        exact = {"date_text_original": "22 June 1633", "temporal_precision": "exact_event", "temporal_certainty": "high"}
        self.assertEqual(temporal_fields_for_serving(exact, "successor"), exact)
        self.assertEqual(temporal_fields_for_serving({}, "successor"), dict.fromkeys(expected))


if __name__ == "__main__":
    unittest.main()
