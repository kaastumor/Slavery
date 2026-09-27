from pathlib import Path
import json
import sys
import unittest

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "tools"))
from add_research_case import load_spec  # noqa: E402

DIR = ROOT / "data" / "research" / "recovery" / "overnight_2026_09_27"


class OvernightEvidenceReconciliationTests(unittest.TestCase):
    def test_all_completed_packets_are_valid_current_method_cases(self) -> None:
        paths = sorted(DIR.glob("[0-9][0-9]_*.json"))
        self.assertEqual(len(paths), 10)
        for path in paths:
            with self.subTest(path=path.name):
                spec = load_spec(path, require_case_key=True)
                claim = spec["claim"]
                tp = claim["territorial_practice"]
                self.assertEqual(claim["review_status"], "reviewed")
                self.assertEqual(claim["publication_status"], "unpublished")
                self.assertIsNone(tp["practice_level"])
                self.assertEqual(
                    tp["classification_status"], "reviewed_reconciled_post_m1"
                )
                self.assertNotIn("geometry", spec)

    def test_legacy_modern_country_proxies_are_not_successor_extent(self) -> None:
        inv = json.loads(
            (DIR / "reconciliation_inventory.json").read_text(encoding="utf-8")
        )
        self.assertEqual(len(inv["completed_packets"]), 10)
        for row in inv["completed_packets"]:
            self.assertTrue(row["legacy_proxy_geometry_id"])
        self.assertEqual(
            inv["geometry_disposition"]["all_successor_claims_geometry_state"],
            "unresolved_pending_bounded_geometry",
        )

    def test_unfinished_legacy_claims_remain_explicit(self) -> None:
        inv = json.loads(
            (DIR / "reconciliation_inventory.json").read_text(encoding="utf-8")
        )
        remaining = {
            row["legacy_claim_id"] for row in inv["unprocessed_legacy_prototypes"]
        }
        self.assertEqual(
            remaining,
            {
                "df374145-bfd5-414b-ba9f-2d85819b7626",
                "ab1f826b-aecf-4f2b-a88a-bccf1eea4f9a",
            },
        )

    def test_brazil_and_uzbekistan_do_not_turn_counts_into_prevalence(self) -> None:
        brazil = json.loads(
            (DIR / "10_brazil_rural_debt_bondage_v2.json").read_text(
                encoding="utf-8"
            )
        )
        uzbek = json.loads(
            (DIR / "09_uzbekistan_cotton_forced_labour_v2.json").read_text(
                encoding="utf-8"
            )
        )
        self.assertIn("not prevalence", brazil["evidence"][1]["locator"])
        self.assertIn(
            "not a country-wide prevalence rate",
            uzbek["evidence"][0]["source"]["reliability_limitations"],
        )


if __name__ == "__main__":
    unittest.main()
