import importlib.util
import unittest
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]
PATH=ROOT/"experiments"/"coverage-scale"/"select_expansion.py"
spec=importlib.util.spec_from_file_location("cov002",PATH)
mod=importlib.util.module_from_spec(spec)
assert spec.loader is not None
spec.loader.exec_module(mod)

def square(lon,lat):
    return {"type":"Polygon","coordinates":[[[lon-1,lat-1],[lon+1,lat-1],[lon+1,lat+1],[lon-1,lat+1],[lon-1,lat-1]]]}

def feat(name,lon,lat,ordhint):
    return {"type":"Feature","properties":{"Name":name,"Type":"POLITY","FromYear":-500,"ToYear":1800,"Components":"","SeshatID":str(ordhint),"Wikidata":""},"geometry":square(lon,lat)}

class Cov002Tests(unittest.TestCase):
    def test_sector(self):
        self.assertEqual(mod.sector(-100,40),"A")
        self.assertEqual(mod.sector(-70,-20),"B")
        self.assertEqual(mod.sector(20,0),"C")
        self.assertEqual(mod.sector(20,50),"D")
        self.assertEqual(mod.sector(80,20),"E")
        self.assertEqual(mod.sector(130,20),"F")

    def test_rank2_selection_is_deterministic(self):
        pts={"A":(-100,40),"B":(-70,-20),"C":(20,0),"D":(20,50),"E":(80,20),"F":(130,20)}
        features=[]
        n=0
        for sec,(lon,lat) in pts.items():
            for i in range(3):
                features.append(feat(f"{sec}-{i}",lon,lat,n)); n+=1
        data={"features":features}
        a=mod.build(data); b=mod.build(data)
        self.assertEqual(a,b)
        self.assertEqual(a["selected_cells"],12)
        self.assertTrue(a["viable"])
        self.assertTrue(all(x["selection_rank"]==2 for x in a["cells"]))

if __name__=="__main__":
    unittest.main()
