import json, unittest
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]
R1=ROOT/"programmes"/"r1"

class R1IdentityQATests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.c0=json.loads((R1/"c0_register.json").read_text(encoding="utf-8"))
        cls.qa=json.loads((R1/"identity_qa.json").read_text(encoding="utf-8"))
        cls.queue=json.loads((R1/"subject_research_queue.json").read_text(encoding="utf-8"))

    def test_c0_shape_and_no_claims(self):
        self.assertEqual(len(self.c0),65)
        for r in self.c0:
            self.assertEqual(r["research_stage"],"not_researched")
            self.assertEqual(r["classification_outcome"],"unassessed")
            self.assertTrue(r["absence_inference_prohibited"])
            self.assertEqual(r["interpretation"],"Registered target; historical slavery/coercion research not yet performed.")

    def test_all_planned_c1_have_qa(self):
        self.assertEqual(self.qa["planned_c1_total"],36)
        self.assertEqual(len(self.qa["rows"]),36)
        self.assertEqual(len({r["target_id"] for r in self.qa["rows"]}),36)

    def test_two_holds_are_not_replaced(self):
        self.assertEqual(set(self.qa["holds"]),{"R1:P:1800:A:r1","R1:P:1800:D:r1"})
        q={r["target_id"] for r in self.queue}
        self.assertNotIn("R1:P:1800:A:r1",q)
        self.assertNotIn("R1:P:1800:D:r1",q)
        self.assertEqual(len(self.queue),34)
        self.assertTrue(all(not r["replacement_allowed"] for r in self.queue))

    def test_queue_contains_only_safe_qa_states(self):
        safe={"validated","validated_with_frame_limitation"}
        self.assertTrue(all(r["qa_state"] in safe for r in self.queue))

if __name__=="__main__":unittest.main()
