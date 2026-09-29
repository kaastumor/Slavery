import json
from pathlib import Path
import unittest

from tools.add_legal_event_case import content_sha256 as legal_hash, load_spec as load_legal, plan as legal_plan
from tools.add_research_case import load_spec as load_territorial, plan as territorial_plan

ROOT = Path(__file__).resolve().parents[1]
CAND = ROOT / "data/research/recovery/production_batch_2026_09_29/candidates"


class ProductionBatchCandidateTests(unittest.TestCase):
    def test_goryeo_is_reviewed_legal_event_not_territorial_practice(self):
        spec = load_legal(CAND / "01_goryeo_0956_legal_event.json", require_case_key=True)
        plan = legal_plan(spec)
        self.assertEqual(plan["claim_kind"], "legal_event")
        self.assertTrue(plan["internally_admitted"])
        self.assertEqual(plan["claim_interval"], [956, 956])
        self.assertNotIn("territorial_practice", spec["claim"])
        self.assertEqual(spec["research_target"]["result"]["category_mapping_status"],
                         "broader_nobi_slavery_mapping_held")
        self.assertEqual(len(legal_hash(spec)), 64)

    def test_dahomey_is_bounded_reviewed_process_with_unresolved_geometry(self):
        spec = load_territorial(CAND / "02_dahomey_1727_sale_process.json", require_case_key=True)
        plan = territorial_plan(spec)
        self.assertEqual(plan["claim_interval"], [1727, 1727])
        self.assertEqual(plan["practice_type"], "slave_trade_sale_purchase")
        self.assertIsNone(plan["practice_level"])
        self.assertEqual(plan["review_status"], "reviewed")
        self.assertEqual(plan["geometry_accuracy"], "unresolved")
        self.assertIn("sold-versus-retained split", spec["claim"]["notes"].lower())

    def test_mexica_stays_draft_until_time_identity_and_category_review(self):
        spec = load_territorial(CAND / "03_mexica_exchangeable_tlacotli.json", require_case_key=True)
        plan = territorial_plan(spec)
        self.assertEqual(plan["review_status"], "draft")
        self.assertEqual(plan["coverage_state"], "source_identified")
        self.assertIsNone(plan["claim_interval"][0])
        self.assertIsNone(plan["claim_interval"][1])
        self.assertEqual(plan["geometry_accuracy"], "unresolved")
        self.assertIn("tlacotli", spec["claim"]["summary"])

    def test_angkor_is_bounded_reviewed_site_claim_with_modern_proxy_point(self):
        spec = load_territorial(CAND / "04_angkor_1296_1297_household_slavery.json", require_case_key=True)
        plan = territorial_plan(spec)
        self.assertEqual(plan["claim_interval"], [1296, 1297])
        self.assertEqual(plan["practice_type"], "slavery_enslavement")
        self.assertIsNone(plan["practice_level"])
        self.assertEqual(plan["review_status"], "reviewed")
        self.assertEqual(plan["geometry_accuracy"], "modern_proxy")
        self.assertEqual(spec["geometry"]["geojson"]["type"], "Point")
        self.assertIn("not the historical practice extent", spec["geometry"]["resolution_method"])
        self.assertIn("empire-wide prevalence", spec["claim"]["summary"])

    def test_asante_is_polity_level_slavery_with_navigation_proxy_only(self):
        spec = load_territorial(CAND / "05_asante_1807_1895_slavery.json", require_case_key=True)
        plan = territorial_plan(spec)
        self.assertEqual(plan["claim_interval"], [1807, 1895])
        self.assertEqual(plan["practice_type"], "slavery_enslavement")
        self.assertIsNone(plan["practice_level"])
        self.assertEqual(plan["review_status"], "reviewed")
        self.assertEqual(plan["geometry_accuracy"], "modern_proxy")
        self.assertEqual(spec["geometry"]["geojson"]["type"], "Point")
        self.assertIn("navigation proxy", spec["geometry"]["resolution_method"])
        self.assertIn("pawnship", spec["claim"]["notes"].lower())

    def test_sitka_is_bounded_case_with_navigation_proxy_only(self):
        spec = load_territorial(CAND / "06_sitka_sah_quah_1886_slavery.json", require_case_key=True)
        plan = territorial_plan(spec)
        self.assertEqual(plan["claim_interval"], [1886, 1886])
        self.assertEqual(plan["practice_type"], "slavery_enslavement")
        self.assertIsNone(plan["practice_level"])
        self.assertEqual(plan["review_status"], "reviewed")
        self.assertEqual(plan["geometry_accuracy"], "modern_proxy")
        self.assertEqual(spec["geometry"]["geojson"]["type"], "Point")
        self.assertIn("not the 1886 courtroom", spec["geometry"]["resolution_method"])
        self.assertIn("test case", spec["claim"]["notes"].lower())

    def test_bukhara_is_bounded_1820_claim_with_navigation_proxy(self):
        spec = load_territorial(CAND / "07_bukhara_persian_slavery_1820.json", require_case_key=True)
        plan = territorial_plan(spec)
        self.assertEqual(plan["claim_interval"], [1820, 1820])
        self.assertEqual(plan["practice_type"], "slavery_enslavement")
        self.assertIsNone(plan["practice_level"])
        self.assertEqual(plan["geometry_accuracy"], "modern_proxy")
        self.assertEqual(spec["geometry"]["geojson"]["type"], "Point")
        self.assertIn("not the 1820 slave market", spec["geometry"]["resolution_method"])
        self.assertIn("not converted into prevalence", spec["claim"]["notes"].lower())

    def test_taghaza_is_bounded_1352_site_claim_with_no_geometry(self):
        spec = load_territorial(CAND / "08_taghaza_slave_salt_mining_1352.json", require_case_key=True)
        plan = territorial_plan(spec)
        self.assertEqual(plan["claim_interval"], [1352, 1352])
        self.assertEqual(plan["practice_type"], "slavery_enslavement")
        self.assertIsNone(plan["practice_level"])
        self.assertIsNone(plan["geometry_accuracy"])
        self.assertNotIn("geometry", spec)
        self.assertIn("single", spec["claim"]["territorial_practice"]["notes"].lower())

    def test_candidate_case_keys_are_unique(self):
        specs = [
            json.loads(p.read_text(encoding="utf-8"))
            for p in sorted(CAND.glob("*.json"))
        ]
        keys = [s["case_key"] for s in specs]
        self.assertEqual(len(keys), len(set(keys)))

    def test_accepted_subset_manifest_matches_candidate_hashes_and_zero_map_delta(self):
        manifest = json.loads(
            (ROOT / "data/research/recovery/production_batch_2026_09_29/accepted_subset_manifest.json")
            .read_text(encoding="utf-8")
        )
        self.assertEqual(
            [row["case_key"] for row in manifest["accepted"]],
            [
                "production-batch-2026-09-29/goryeo/nobi-status-review-0956-v1",
                "production-batch-2026-09-29/dahomey/royal-captive-allocation-sale-1727-v1",
                "production-batch-2026-09-29/angkor/household-slavery-1296-1297-v1",
                "production-batch-2026-09-29/asante/slavery-1807-1895-v1",
                "production-batch-2026-09-29/sitka/sah-quah-slavery-1886-v1",
                "production-batch-2026-09-29/bukhara/persian-slavery-1820-v1",
                "production-batch-2026-09-29/taghaza/slave-salt-mining-1352-v1",
            ],
        )
        goryeo = load_legal(CAND / "01_goryeo_0956_legal_event.json", require_case_key=True)
        dahomey = load_territorial(CAND / "02_dahomey_1727_sale_process.json", require_case_key=True)
        self.assertEqual(manifest["accepted"][0]["content_sha256"], legal_hash(goryeo))
        from tools.add_research_case import case_content_sha256
        self.assertEqual(manifest["accepted"][1]["content_sha256"], case_content_sha256(dahomey))
        angkor = load_territorial(CAND / "04_angkor_1296_1297_household_slavery.json", require_case_key=True)
        self.assertEqual(manifest["accepted"][2]["content_sha256"], case_content_sha256(angkor))
        asante = load_territorial(CAND / "05_asante_1807_1895_slavery.json", require_case_key=True)
        self.assertEqual(manifest["accepted"][3]["content_sha256"], case_content_sha256(asante))
        sitka = load_territorial(CAND / "06_sitka_sah_quah_1886_slavery.json", require_case_key=True)
        self.assertEqual(manifest["accepted"][4]["content_sha256"], case_content_sha256(sitka))
        bukhara = load_territorial(CAND / "07_bukhara_persian_slavery_1820.json", require_case_key=True)
        taghaza = load_territorial(CAND / "08_taghaza_slave_salt_mining_1352.json", require_case_key=True)
        self.assertEqual(manifest["accepted"][5]["content_sha256"], case_content_sha256(bukhara))
        self.assertEqual(manifest["accepted"][6]["content_sha256"], case_content_sha256(taghaza))
        self.assertEqual(manifest["expected_database_delta_if_explicitly_ingested"]["claim"], 7)
        self.assertEqual(manifest["expected_database_delta_if_explicitly_ingested"]["source_version"], 18)
        self.assertEqual(manifest["expected_database_delta_if_explicitly_ingested"]["release_claim"], 0)
        self.assertEqual(manifest["map_coverage_effect"]["visible_geometry_additions"], 4)
        self.assertEqual(manifest["map_coverage_effect"]["visible_targets"], ["Angkor", "Asante", "Sitka", "Bukhara"])
        self.assertEqual(len(manifest["held_exclusions"]), 3)


if __name__ == "__main__":
    unittest.main()
