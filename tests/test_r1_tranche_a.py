import json, unittest
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]
P=ROOT/"programmes"/"r1"/"tranche_a_selection.json"

class TrancheASelectionTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.s=json.loads(P.read_text(encoding="utf-8"))

    def test_size_and_uniqueness(self):
        rows=self.s["rows"]
        self.assertEqual(len(rows),12)
        self.assertEqual(len({r["target_id"] for r in rows}),12)
        self.assertFalse(self.s["replacement_allowed"])

    def test_bucket_shape(self):
        from collections import Counter
        c=Counter(r["bucket"].replace("_extra","") for r in self.s["rows"])
        self.assertEqual(c["new_polity"],6)
        self.assertEqual(c["new_nonpolity"],2)
        self.assertEqual(c["legacy_polity"],2)
        self.assertEqual(c["legacy_nonpolity"],2)

    def test_all_five_new_polity_anchor_bands_present(self):
        anchors={r["anchor"] for r in self.s["rows"] if r["bucket"].startswith("new_polity")}
        self.assertTrue({"2000 BCE","500 BCE","500 CE","1300 CE","1800 CE"} <= anchors)

    def test_nonpolity_frames_are_distinct(self):
        frames=[r["effective_frame_class"] for r in self.s["rows"] if r["bucket"]=="new_nonpolity"]
        self.assertEqual(len(frames),len(set(frames)))
        legacy=[r["effective_frame_class"] for r in self.s["rows"] if r["bucket"]=="legacy_nonpolity"]
        self.assertEqual(len(legacy),len(set(legacy)))

if __name__=="__main__":unittest.main()
