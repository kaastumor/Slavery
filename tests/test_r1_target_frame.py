import importlib.util
import json
import tempfile
import unittest
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]
P=ROOT/"programmes"/"r1"/"select_target_frame.py"
spec=importlib.util.spec_from_file_location("r1frame",P)
m=importlib.util.module_from_spec(spec);spec.loader.exec_module(m)

def square(lon,lat):
    return {"type":"Polygon","coordinates":[[[lon-1,lat-1],[lon+1,lat-1],[lon+1,lat+1],[lon-1,lat+1],[lon-1,lat-1]]]}

def feat(name,lon,lat,n):
    return {"type":"Feature","properties":{"Name":name,"Type":"POLITY","FromYear":-3000,"ToYear":1900,"Components":"","SeshatID":str(n),"Wikidata":""},"geometry":square(lon,lat)}

class R1FrameTests(unittest.TestCase):
    def test_calendar_inverse(self):
        self.assertEqual(m.atlas_year_from_source(-500),-499)
        self.assertEqual(m.atlas_year_from_source(-1),0)
        self.assertEqual(m.atlas_year_from_source(1),1)
        self.assertEqual(m.display_year(-2000),"2000 BCE")

    def test_sector(self):
        self.assertEqual(m.sector(-100,40),"A")
        self.assertEqual(m.sector(-70,-20),"B")
        self.assertEqual(m.sector(20,0),"C")
        self.assertEqual(m.sector(20,50),"D")
        self.assertEqual(m.sector(80,20),"E")
        self.assertEqual(m.sector(130,20),"F")

    def test_polity_selection_balances_cells(self):
        # Synthetic repo-root with no prior selections.
        with tempfile.TemporaryDirectory() as td:
            root=Path(td)
            for p in ["experiments/coverage-value","experiments/coverage-scale","experiments/coverage-tiered",
                      "experiments/falsification-atlas"]:
                (root/p).mkdir(parents=True,exist_ok=True)
            (root/"experiments/coverage-value/sample.json").write_text(json.dumps({"cells":[]}))
            (root/"experiments/coverage-scale/expansion_sample.json").write_text(json.dumps({"cells":[]}))
            (root/"experiments/coverage-tiered/tiered_sample.json").write_text(json.dumps({"batches":[]}))
            pool={"classes":{c:[[f"{c}{i}",f"{c}-{i}",1000+i] for i in range(8)] for c in ["node_site","institution_estate","mobile_network","region_community"]}}
            (root/"experiments/falsification-atlas/06_NONPOLITY_CANDIDATE_POOL.json").write_text(json.dumps(pool))
            prev=[]
            for c,items in pool["classes"].items():
                for x in items[:2]:prev.append({"id":x[0],"tier":"C1"})
            (root/"experiments/falsification-atlas/07_NONPOLITY_SELECTION.json").write_text(json.dumps(prev))
            full=[]
            for i in range(8):full.append({"cell_id":f"P{i}","target_label":f"P{i}","anchor_year":500,"coverage_outcome":"bounded_supported"})
            for i in range(8):full.append({"cell_id":f"I{i}","target_label":f"I{i}","anchor_year":500,"coverage_outcome":"researched_inconclusive"})
            (root/"experiments/coverage-scale/full_37.json").write_text(json.dumps(full))
            np=[{"target_id":f"N{i}","target_label":f"N{i}","anchor_year":1000,"coverage_outcome":"bounded_supported"} for i in range(8)]
            (root/"experiments/falsification-atlas/11_ARM_B_C1.json").write_text(json.dumps({"rows":np}))

            pts={"A":(-100,40),"B":(-70,-20),"C":(20,0),"D":(20,50),"E":(80,20),"F":(130,20)}
            features=[];n=0
            for sec,(lon,lat) in pts.items():
                for i in range(15):
                    features.append(feat(f"{sec}-{i}",lon,lat,n));n+=1
            cells,c1=m.polity_frame({"features":features},root)
            self.assertEqual(len(c1),16)
            self.assertEqual({x["sampling_sector"] for x in c1},set("ABCDEF"))
            self.assertEqual({x["source_anchor_year"] for x in c1},set(m.SOURCE_ANCHORS))

if __name__=="__main__":unittest.main()
