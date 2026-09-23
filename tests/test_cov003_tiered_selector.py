import importlib.util, unittest
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
PATH=ROOT/"experiments"/"coverage-tiered"/"select_tiered_sample.py"
spec=importlib.util.spec_from_file_location("cov003",PATH)
mod=importlib.util.module_from_spec(spec); spec.loader.exec_module(mod)

def square(lon,lat):
    return {"type":"Polygon","coordinates":[[[lon-1,lat-1],[lon+1,lat-1],[lon+1,lat+1],[lon-1,lat+1],[lon-1,lat-1]]]}

def feat(name,lon,lat,n):
    return {"type":"Feature","properties":{"Name":name,"Type":"POLITY","FromYear":-500,"ToYear":1800,"Components":"","SeshatID":str(n),"Wikidata":""},"geometry":square(lon,lat)}

class Tests(unittest.TestCase):
    def test_sector(self):
        self.assertEqual(mod.sector(-100,40),"A"); self.assertEqual(mod.sector(-70,-20),"B")
        self.assertEqual(mod.sector(20,0),"C"); self.assertEqual(mod.sector(20,50),"D")
        self.assertEqual(mod.sector(80,20),"E"); self.assertEqual(mod.sector(130,20),"F")

    def test_tiered_selection(self):
        pts={"A":(-100,40),"B":(-70,-20),"C":(20,0),"D":(20,50),"E":(80,20),"F":(130,20)}
        features=[]; n=0
        for sec,(lon,lat) in pts.items():
            for i in range(12):
                features.append(feat(f"{sec}-{i}",lon,lat,n)); n+=1
        out=mod.build({"features":features})
        self.assertTrue(out["viable"])
        self.assertEqual(out["target_count"],24)
        self.assertEqual(out["c1_count"],12)
        self.assertEqual(out["c0_only_count"],12)
        self.assertEqual(out["identity_validation_sample_count"],6)
        for b in out["batches"]:
            ranks=[t["selection_rank"] for t in b["targets"]]
            self.assertEqual(ranks,list(range(3,11)))

if __name__=="__main__": unittest.main()
