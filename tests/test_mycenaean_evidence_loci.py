from pathlib import Path
import json
import unittest

ROOT=Path(__file__).resolve().parents[1]
PATH=ROOT/"data"/"research"/"geometry_reviews"/"mycenaean_pylos_knossos_evidence_loci_v1.json"

class MycenaeanEvidenceLociTests(unittest.TestCase):
    def test_loci_are_points_only(self):
        d=json.loads(PATH.read_text(encoding="utf-8"))
        self.assertFalse(d["semantic_scope"]["territorial_extent"])
        self.assertFalse(d["semantic_scope"]["inference_extent"])
        self.assertEqual(len(d["loci"]),2)
        for row in d["loci"]:
            self.assertEqual(row["geometry"]["type"],"Point")
            self.assertEqual(row["accuracy_status"],"modern_proxy")
            self.assertIn("CC0",row["version"]["license_status"])

    def test_exact_wikidata_versions_are_frozen(self):
        d=json.loads(PATH.read_text(encoding="utf-8"))
        versions={x["source_native_id"]:x["version"]["version_label"] for x in d["loci"]}
        self.assertEqual(versions["Q2047396"],"Wikidata Q2047396 revision 2485117208")
        self.assertEqual(versions["Q173527"],"Wikidata Q173527 revision 2522185606")

    def test_knossos_is_not_mainland_geometry(self):
        d=json.loads(PATH.read_text(encoding="utf-8"))
        self.assertIn("Do not attach",d["qc"]["mainland_warning"])

if __name__=="__main__":
    unittest.main()
