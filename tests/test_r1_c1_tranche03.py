import json
import importlib.util
import unittest
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]
FINAL=ROOT/"programmes"/"r1"/"c1_tranche_03_final.json"
SEL=ROOT/"programmes"/"r1"/"c1_tranche_03_selection.json"
VALIDATOR=ROOT/"programmes"/"r1"/"validate_core_contract.py"

spec=importlib.util.spec_from_file_location("r1core",VALIDATOR)
m=importlib.util.module_from_spec(spec);spec.loader.exec_module(m)

class Tranche03Tests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.final=json.loads(FINAL.read_text(encoding="utf-8"))
        cls.sel=json.loads(SEL.read_text(encoding="utf-8"))
        cls.rows={r["target_id"]:r for r in cls.final["rows"]}

    def test_exact_frozen_membership(self):
        self.assertEqual(set(self.rows),{r["target_id"] for r in self.sel})
        self.assertEqual(len(self.rows),3)

    def test_all_rows_pass_core_contract_validator(self):
        for row in self.rows.values():
            self.assertEqual(m.validate_row(row),[],msg=row["target_id"])

    def test_every_row_was_adversarially_reviewed(self):
        for row in self.rows.values():
            self.assertEqual(row["research_stage"],"review_complete")
            self.assertEqual(row["review_state"],"internally_adversarially_reviewed")
            self.assertTrue(row.get("adversarial_corrections"))

    def test_final_outcomes(self):
        outcomes=[r["classification_outcome"] for r in self.rows.values()]
        self.assertEqual(outcomes.count("classified"),1)
        self.assertEqual(outcomes.count("inconclusive"),2)

    def test_selected_year_truth(self):
        self.assertEqual(self.rows["R1:P:500:F:r1"]["temporal_selected_year_truth"],"unknown")
        self.assertEqual(self.rows["R1:L:COV2:1300:E"]["temporal_selected_year_truth"],"unknown")
        self.assertEqual(self.rows["R1:L:COV2:1300:B"]["temporal_selected_year_truth"],"supported")

    def test_pandya_c2_completed_without_positive_inference(self):
        row=self.rows["R1:L:COV2:1300:E"]
        self.assertFalse(row.get("c2_required",False))
        self.assertTrue(row.get("c2_completed",False))
        self.assertEqual(row["classification_outcome"],"inconclusive")
        self.assertIn("spatial",row["c2_resolution"])

    def test_chimu_is_corvee_not_slavery(self):
        row=self.rows["R1:L:COV2:1300:B"]
        self.assertEqual(row["classification_outcome"],"classified")
        self.assertEqual(row["release_summary"],"bounded_supported_corvee_labor")
        self.assertIn("corv",row["bounded_proposition"].lower())
        self.assertIn("do not relabel",row["required_abstention"].lower())

    def test_mackey_source_fitness_is_limited(self):
        row=self.rows["R1:L:COV2:1300:B"]
        src=next(s for s in row["sources"] if s["source_version_ref"]=="Mackey-1987-Chimu-administration-provinces")
        self.assertEqual(src["claim_fitness"],"usable_with_limitation")

    def test_no_absence_or_network_shortcuts(self):
        for row in self.rows.values():
            self.assertIsNot(row.get("territorial_practice_inferred_from_network"),True)
            self.assertIsNot(row.get("absence_inferred_from_missing_evidence"),True)

if __name__=="__main__":
    unittest.main()
