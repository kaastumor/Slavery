import json
import importlib.util
import unittest
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]
FINAL=ROOT/"programmes"/"r1"/"c1_tranche_02_final.json"
SEL=ROOT/"programmes"/"r1"/"c1_tranche_02_selection.json"
VALIDATOR=ROOT/"programmes"/"r1"/"validate_core_contract.py"

spec=importlib.util.spec_from_file_location("r1core",VALIDATOR)
m=importlib.util.module_from_spec(spec);spec.loader.exec_module(m)

class Tranche02Tests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.final=json.loads(FINAL.read_text(encoding="utf-8"))
        cls.sel=json.loads(SEL.read_text(encoding="utf-8"))
        cls.rows={r["target_id"]:r for r in cls.final["rows"]}

    def test_exact_frozen_membership(self):
        self.assertEqual(
            set(self.rows),
            {r["target_id"] for r in self.sel},
        )
        self.assertEqual(len(self.rows),6)

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
        self.assertEqual(outcomes.count("inconclusive"),5)
        self.assertEqual(outcomes.count("disputed"),0)

    def test_selected_year_guards(self):
        usa=self.rows["R1:L:1800:A"]
        self.assertEqual(usa["temporal_selected_year_truth"],"supported")
        for tid in (
            "R1:P:-500:C:r1",
            "R1:P:-500:F:r1",
            "R1:P:500:D:r1",
            "R1:N:nalanda_700",
            "R1:P:1300:C:r1",
        ):
            self.assertEqual(self.rows[tid]["temporal_selected_year_truth"],"unknown")

    def test_mali_c2_completed(self):
        row=self.rows["R1:P:1300:C:r1"]
        self.assertFalse(row.get("c2_required",False))
        self.assertTrue(row.get("c2_completed",False))
        self.assertEqual(row["classification_outcome"],"inconclusive")

    def test_dependency_groups_are_not_false_independence(self):
        lazica=self.rows["R1:P:500:D:r1"]
        groups={s["source_version_ref"]:s["independence_group"] for s in lazica["sources"]}
        self.assertEqual(
            groups["Procopius-Wars-II.15.4-5-Dewing"],
            groups["doi:10.1017/S0009838800003682"],
        )

        nalanda=self.rows["R1:N:nalanda_700"]
        self.assertEqual(len({s["independence_group"] for s in nalanda["sources"]}),1)

        usa=self.rows["R1:L:1800:A"]
        self.assertEqual(len({s["independence_group"] for s in usa["sources"]}),1)

    def test_no_network_to_territorial_shortcut(self):
        for row in self.rows.values():
            self.assertIsNot(row.get("territorial_practice_inferred_from_network"),True)

if __name__=="__main__":
    unittest.main()
