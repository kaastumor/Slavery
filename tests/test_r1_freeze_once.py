import json, tempfile, unittest, urllib.request, importlib.util
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]
SELECTOR=ROOT/"programmes"/"r1"/"select_target_frame.py"
SOURCE_URL="https://raw.githubusercontent.com/Seshat-Global-History-Databank/cliopatria/ad28a691b7c07c1fca89d0e0636d324667d2a258/cliopatria.geojson.zip"

spec=importlib.util.spec_from_file_location("r1_freeze",SELECTOR)
m=importlib.util.module_from_spec(spec);spec.loader.exec_module(m)

class Freeze(unittest.TestCase):
    def test_emit(self):
        with tempfile.TemporaryDirectory() as tmp:
            p=Path(tmp)/"cliopatria.geojson.zip"
            urllib.request.urlretrieve(SOURCE_URL,p)
            out=m.build(m.load_cliopatria(p),ROOT)
            print("R1_TARGET_FRAME_JSON_BEGIN")
            print(json.dumps(out,indent=2,ensure_ascii=False))
            print("R1_TARGET_FRAME_JSON_END")
            self.assertLessEqual(out["counts"]["new_c0_total"],120)
            self.assertLessEqual(out["counts"]["planned_c1_total"],36)
            self.assertTrue(all(out["balance_check"].values()))

if __name__=="__main__":unittest.main()
