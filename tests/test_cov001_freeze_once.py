import json
import tempfile
import unittest
import urllib.request
from pathlib import Path
import importlib.util

ROOT = Path(__file__).resolve().parents[1]
SELECTOR_PATH = ROOT / "experiments" / "coverage-value" / "select_sample.py"
SOURCE_URL = "https://raw.githubusercontent.com/Seshat-Global-History-Databank/cliopatria/ad28a691b7c07c1fca89d0e0636d324667d2a258/cliopatria.geojson.zip"

spec = importlib.util.spec_from_file_location("cov001_selector_freeze", SELECTOR_PATH)
selector = importlib.util.module_from_spec(spec)
assert spec.loader is not None
spec.loader.exec_module(selector)


class Cov001OneOffFreezeProbe(unittest.TestCase):
    def test_generate_exact_sample_and_emit_to_ci_log(self):
        with tempfile.TemporaryDirectory() as tmp:
            source = Path(tmp) / "cliopatria.geojson.zip"
            urllib.request.urlretrieve(SOURCE_URL, source)
            data = selector.load_geojson(source)
            sample = selector.build_sample(data)

            self.assertTrue(sample["viable"], sample)
            self.assertGreaterEqual(sample["valid_cells"], 18)

            print("COV001_SAMPLE_JSON_BEGIN")
            print(json.dumps(sample, indent=2, ensure_ascii=False))
            print("COV001_SAMPLE_JSON_END")


if __name__ == "__main__":
    unittest.main()
