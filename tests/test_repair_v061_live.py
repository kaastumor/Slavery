from pathlib import Path
import os
import sys
import unittest
import uuid

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "tools"))

from repair_v061_live import build_plan, stable_uuid  # noqa: E402


class RepairV061LiveTests(unittest.TestCase):
    def test_stable_uuid_is_deterministic_and_kind_scoped(self):
        a = stable_uuid("claim", "v0.4.9 Evidence!10:1:territorial_practice")
        b = stable_uuid("claim", "v0.4.9 Evidence!10:1:territorial_practice")
        c = stable_uuid("spatial", "v0.4.9 Evidence!10:1:territorial_practice")
        self.assertIsInstance(a, uuid.UUID)
        self.assertEqual(a, b)
        self.assertNotEqual(a, c)

    def test_canonical_workbook_repair_plan(self):
        workbook = os.environ.get("HSA_V061_WORKBOOK")
        if not workbook:
            self.skipTest("HSA_V061_WORKBOOK not set")
        plan, _ = build_plan(Path(workbook))
        self.assertEqual(plan.raw_rows.__len__(), 288)
        self.assertEqual(plan.global_rows.__len__(), 36)
        self.assertEqual(plan.unique_urls.__len__(), 29)
        self.assertEqual(plan.positive_rows, 18)
        self.assertEqual(plan.claim_targets, 22)
        self.assertEqual(
            plan.target_kind_counts,
            {
                "territorial_practice": 18,
                "external_participation": 3,
                "legal_event": 1,
            },
        )


if __name__ == "__main__":
    unittest.main()
