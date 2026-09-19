from pathlib import Path
import os
import sys
import unittest

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "tools"))
from import_v061 import validate_and_normalize, parse_claim_period  # noqa: E402
from v061_global_evidence import EXPECTED_GLOBAL_COUNTS, POSITIVE_PLAN  # noqa: E402


class ImportV061Tests(unittest.TestCase):
    def test_period_parser(self):
        self.assertEqual(parse_claim_period("1824"), (1824, 1824, "exact_year"))
        self.assertEqual(parse_claim_period("1751–1753"), (1751, 1753, "year_range"))
        self.assertEqual(parse_claim_period("c. 1747–1777"), (1747, 1777, "approximate_range"))
        self.assertEqual(parse_claim_period("18th century"), (1700, 1799, "century"))

    def test_global_evidence_plan_is_explicit_and_bounded(self):
        self.assertEqual(len(POSITIVE_PLAN), 18)
        self.assertEqual(
            sum(len(item["targets"]) for item in POSITIVE_PLAN.values()),
            EXPECTED_GLOBAL_COUNTS["claim_targets"],
        )
        self.assertEqual(EXPECTED_GLOBAL_COUNTS["claim_targets"], 22)
        self.assertEqual(EXPECTED_GLOBAL_COUNTS["RI"], 18)

        territorial = [
            target
            for item in POSITIVE_PLAN.values()
            for target in item["targets"]
            if target["kind"] == "territorial_practice"
        ]
        self.assertTrue(territorial)
        self.assertTrue(all("practice_level" not in target for target in territorial))
        self.assertEqual(POSITIVE_PLAN["v0.4.9 Evidence!6"]["targets"][0]["kind"], "external_participation")

    def test_canonical_workbook_dry_run(self):
        workbook = os.environ.get("HSA_V061_WORKBOOK")
        if not workbook:
            self.skipTest("HSA_V061_WORKBOOK not set")
        result = validate_and_normalize(Path(workbook))
        self.assertTrue(result["report"]["ok"], result["report"]["errors"])
        self.assertEqual(result["report"]["counts"]["voyages"], 8)
        self.assertEqual(result["report"]["counts"]["real_actors"], 11)
        self.assertEqual(result["report"]["counts"]["workbook_sheets"], 18)
        self.assertEqual(result["report"]["counts"]["workbook_nonempty_rows"], 288)
        self.assertEqual(result["report"]["sha256"], "0a38e4eb6f63c3bb4ce9543be379605d24dd9ff1c1cea1e0a49c0c3db7ba17d4")
        self.assertEqual(result["report"]["raw_sheet_row_counts"]["v0.4.7 Evidence"], 13)
        self.assertEqual(result["report"]["raw_sheet_row_counts"]["v0.4.8 Evidence"], 9)
        self.assertEqual(result["report"]["raw_sheet_row_counts"]["v0.4.9 Evidence"], 12)
        self.assertEqual(result["report"]["raw_sheet_row_counts"]["v0.5.0 Evidence"], 14)
        self.assertEqual(result["report"]["evidence_mapping_rows"], 17)
        self.assertEqual(result["report"]["global_evidence"]["rows"], 36)
        self.assertEqual(result["report"]["global_evidence"]["unique_source_urls"], 29)
        self.assertEqual(result["report"]["global_evidence"]["claim_targets"], 22)
        self.assertEqual(result["report"]["global_evidence"]["counts"]["RI"], 18)
        self.assertIn("https://www.slavevoyages.org/voyage/35181/variables", result["report"]["source_registry_gaps"])


if __name__ == "__main__":
    unittest.main()
