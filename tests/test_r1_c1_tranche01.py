import json
import importlib.util
import unittest
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]
FINAL=ROOT/"programmes"/"r1"/"c1_tranche_01_final.json"
SEL=ROOT/"programmes"/"r1"/"c1_tranche_01_selection.json"
VALIDATOR=ROOT/"programmes"/"r1"/"validate_core_contract.py"

spec=importlib.util.spec_from_file_location("r1core",VALIDATOR)
m=importlib.util.module_from_spec(spec);spec.loader.exec_module(m)

class Tranche01Tests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.final=json.loads(FINAL.read_text(encoding="utf-8"))
        cls.sel=json.loads(SEL.read_text(encoding="utf-8"))

    def test_exact_frozen_membership(self):
        self.assertEqual(
            {r["target_id"] for r in self.final["rows"]},
            {r["target_id"] for r in self.sel},
        )
        self.assertEqual(len(self.final["rows"]),10)

    def test_all_rows_pass_core_contract_validator(self):
        for row in self.final["rows"]:
            self.assertEqual(m.validate_row(row),[],msg=row["target_id"])

    def test_every_row_was_adversarially_reviewed(self):
        for row in self.final["rows"]:
            self.assertEqual(row["review_state"],"internally_adversarially_reviewed")
            self.assertTrue(row.get("adversarial_corrections"))

    def test_no_unresolved_c2(self):
        for row in self.final["rows"]:
            self.assertFalse(row.get("c2_required",False))
        self.assertEqual(sum(bool(r.get("c2_completed")) for r in self.final["rows"]),2)

    def test_temporal_guard_rows_remain_unknown_at_selected_year(self):
        ids={"R1:P:500:A:r1","R1:N:inuit_arctic_1800","R1:L:cahokia_1200"}
        found={r["target_id"]:r for r in self.final["rows"] if r["target_id"] in ids}
        self.assertEqual(set(found),ids)
        for row in found.values():
            self.assertEqual(row["temporal_selected_year_truth"],"unknown")

    def test_aggregate_has_no_territorial_selected_year_truth(self):
        row=next(r for r in self.final["rows"] if r["target_id"]=="R1:L:1800:F")
        self.assertEqual(row["temporal_selected_year_truth"],"not_applicable_to_aggregate_territorial_claim")
        self.assertEqual(row["classification_outcome"],"inconclusive")

    def test_cahokia_not_disputed_or_positive(self):
        row=next(r for r in self.final["rows"] if r["target_id"]=="R1:L:cahokia_1200")
        self.assertEqual(row["classification_outcome"],"inconclusive")
        self.assertIn("does not securely establish slave status",row["bounded_proposition"])

if __name__=="__main__":
    unittest.main()
