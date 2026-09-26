from pathlib import Path
import json
import sys
import unittest

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "tools"))

from add_research_case import load_spec  # noqa: E402


INTAKE = ROOT / "data" / "research" / "intake" / "atlas_expansion_01"
RECOVERY = ROOT / "data" / "research" / "recovery" / "atlas_expansion_01"


class AtlasExpansion01Tests(unittest.TestCase):
    def test_all_new_claim_packages_are_valid_post_m1_cases(self) -> None:
        paths = sorted(INTAKE.glob("*.json")) + sorted(RECOVERY.glob("*_v2.json"))
        self.assertEqual(len(paths), 11)
        for path in paths:
            with self.subTest(path=path.name):
                spec = load_spec(path, require_case_key=True)
                practice = spec["claim"]["territorial_practice"]
                self.assertIsNone(
                    practice.get("practice_level"),
                    f"{path.name} assigns a new post-M1 P-level",
                )
                self.assertEqual(spec["claim"]["review_status"], "reviewed")
                self.assertEqual(spec["claim"]["publication_status"], "unpublished")

    def test_unresolved_geometry_never_contains_geojson(self) -> None:
        for path in sorted(INTAKE.glob("*.json")):
            spec = json.loads(path.read_text(encoding="utf-8"))
            geometry = spec.get("geometry")
            if geometry and geometry["accuracy_status"] == "unresolved":
                self.assertIsNone(geometry.get("geojson"), path.name)

    def test_todaiji_is_mapped_as_institutional_locus_only(self) -> None:
        spec = json.loads(
            (INTAKE / "05_todaiji_nuhi_status.json").read_text(encoding="utf-8")
        )
        geometry = spec["geometry"]
        self.assertEqual(geometry["geojson"]["type"], "Point")
        self.assertEqual(geometry["source_native_id"], "UNESCO-WHC-870-001")
        self.assertIn("institutional/evidence site only", geometry["resolution_method"])
        self.assertIn("not a practice polygon", geometry["notes"].lower())
        self.assertIsNone(spec["claim"]["territorial_practice"]["practice_level"])

    def test_songo_mnara_is_a_locus_not_a_practice_polygon(self) -> None:
        spec = json.loads(
            (INTAKE / "04_songo_mnara_slavery.json").read_text(encoding="utf-8")
        )
        geometry = spec["geometry"]
        self.assertEqual(geometry["accuracy_status"], "specialist")
        self.assertEqual(geometry["geojson"]["type"], "Point")
        self.assertEqual(geometry["source_native_id"], "UNESCO-WHC-144-002")
        self.assertIn("site/evidence locus", geometry["resolution_method"])
        self.assertIn("not a slavery-practice extent", geometry["resolution_method"])

    def test_recovery_inventory_keeps_disputed_separate(self) -> None:
        inventory = json.loads(
            (RECOVERY / "recovery_inventory.json").read_text(encoding="utf-8")
        )
        self.assertEqual(len(inventory["tiers"]["R0_direct_recovery"]["entities"]), 7)
        self.assertEqual(len(inventory["tiers"]["R1_prototype_reconcile"]["entities"]), 6)
        self.assertEqual(len(inventory["tiers"]["R2_special_review"]["entities"]), 2)
        disputed_names = {
            item["name"]
            for item in inventory["tiers"]["R2_special_review"]["entities"]
        }
        self.assertIn("Achaemenid Persis/Elam royal economy", disputed_names)
        self.assertIn("Zhengzhou Shang City (Early Shang)", disputed_names)

    def test_zhengzhou_captive_claim_stays_separate_from_disputed_slavery(self) -> None:
        spec = json.loads(
            (RECOVERY / "zhengzhou_captive_taking_v2.json").read_text(
                encoding="utf-8"
            )
        )
        practice = spec["claim"]["territorial_practice"]
        self.assertEqual(
            practice["practice_type_code"], "captive_taking_incorporation"
        )
        self.assertIsNone(practice["practice_level"])
        self.assertIn(
            "896a3720-d871-495e-b23e-c24d7dde3039",
            spec["claim"]["notes"],
        )
        self.assertIn("remains separate", spec["claim"]["notes"])

    def test_rome_reconciliation_does_not_copy_legacy_p4(self) -> None:
        spec = json.loads(
            (RECOVERY / "roman_early_principate_slavery_v2.json").read_text(
                encoding="utf-8"
            )
        )
        self.assertIsNone(spec["claim"]["territorial_practice"]["practice_level"])
        self.assertEqual(
            spec["claim"]["territorial_practice"]["classification_status"],
            "reviewed_reconciled_post_m1",
        )
        self.assertIn(
            "ce2feb0a-917f-4bf1-9561-3d1f1f9887d4",
            spec["claim"]["notes"],
        )


if __name__ == "__main__":
    unittest.main()
