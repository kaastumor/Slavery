from pathlib import Path
import re
import unittest

ROOT = Path(__file__).resolve().parents[1]
MAIN = (ROOT / "web" / "src" / "main.ts").read_text(encoding="utf-8")


class MapBorderAlignmentTests(unittest.TestCase):
    def _source_block(self, source_id: str) -> str:
        match = re.search(
            rf'map\.addSource\("{re.escape(source_id)}", \{{(?P<body>.*?)\n    \}}\);',
            MAIN,
            flags=re.DOTALL,
        )
        self.assertIsNotNone(match, f"source {source_id} not found")
        return match.group("body")

    def test_land_and_evidence_polygons_disable_independent_simplification(self):
        for source_id in ("land", "evidence-polygons"):
            with self.subTest(source_id=source_id):
                block = self._source_block(source_id)
                self.assertRegex(block, r"tolerance:\s*0")

    def test_land_still_uses_api_selected_canonical_fabric(self):
        block = self._source_block("land")
        self.assertIn("apiResponse.cartography.source_url", block)


if __name__ == "__main__":
    unittest.main()
