from pathlib import Path
import unittest

ROOT = Path(__file__).resolve().parents[1]
WRAPPER = (ROOT / "tools" / "qgis_render_pipeline_adaptive.sh").read_text(encoding="utf-8")
SELECTOR = (ROOT / "tools" / "select_adaptive_qgis_coastal_candidate.py").read_text(encoding="utf-8")


class QgisAdaptiveCoastalPipelineTests(unittest.TestCase):
    def test_standard_qgis_pipeline_remains_geometry_generator(self) -> None:
        self.assertIn("qgis_render_pipeline.sh", WRAPPER)
        self.assertIn("25000", WRAPPER)
        self.assertIn("50000", WRAPPER)
        self.assertNotIn("ST_Buffer", WRAPPER)
        self.assertNotIn("normalize_coastal_polygon", WRAPPER)

    def test_adaptive_selection_is_area_bounded(self) -> None:
        self.assertIn("--max-extra-pct 2.0", WRAPPER)
        self.assertIn("extra_vs_baseline_pct", SELECTOR)
        self.assertIn("<= args.max_extra_pct", SELECTOR)
        self.assertIn("max(safe", SELECTOR)

    def test_source_geometry_is_never_overwritten(self) -> None:
        self.assertIn("Source geometry is never overwritten", WRAPPER)
        self.assertNotIn("atlas.geometry", WRAPPER)
        self.assertNotIn("publish.geometry", WRAPPER)


if __name__ == "__main__":
    unittest.main()
