import json, tempfile, unittest, urllib.request, importlib.util
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]
SELECTOR=ROOT/"experiments"/"coverage-tiered"/"select_tiered_sample.py"
SOURCE_URL="https://raw.githubusercontent.com/Seshat-Global-History-Databank/cliopatria/ad28a691b7c07c1fca89d0e0636d324667d2a258/cliopatria.geojson.zip"

spec=importlib.util.spec_from_file_location("cov003_freeze",SELECTOR)
mod=importlib.util.module_from_spec(spec); spec.loader.exec_module(mod)

class Freeze(unittest.TestCase):
    def test_emit(self):
        with tempfile.TemporaryDirectory() as tmp:
            p=Path(tmp)/"cliopatria.geojson.zip"
            urllib.request.urlretrieve(SOURCE_URL,p)
            out=mod.build(mod.load(p))
            self.assertTrue(out["viable"],out)
            print("COV003_SAMPLE_JSON_BEGIN")
            print(json.dumps(out,indent=2,ensure_ascii=False))
            print("COV003_SAMPLE_JSON_END")

if __name__=="__main__": unittest.main()
