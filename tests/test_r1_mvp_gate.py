import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
R1 = ROOT / "programmes" / "r1"
WEB = ROOT / "web"
sys.path.insert(0, str(R1))

import build_mvp_candidate_bundle as bundle_builder  # noqa: E402


class R1TechnicalMVPGateTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.bundle = bundle_builder.build()
        cls.index = (WEB / "index.html").read_text(encoding="utf-8")
        cls.mvp = (WEB / "src" / "mvp.ts").read_text(encoding="utf-8")
        cls.release_check = (ROOT / "docs" / "mvp" / "v0.1-release-check.md").read_text(encoding="utf-8")

    def test_candidate_boundary_is_static_and_noncanonical(self):
        self.assertEqual(self.bundle["publication_state"], "candidate_not_published_not_canonical")
        self.assertEqual(self.bundle["canonical_historical_release"], "v0.6.1")
        self.assertEqual(self.bundle["review_scope"], "internal_adversarial_review_only_not_independent_review")
        self.assertEqual(self.bundle["counts"]["targets"], 77)
        self.assertEqual(self.bundle["counts"]["reviewed_c1"], 19)

    def test_candidate_generation_is_byte_deterministic(self):
        first = bundle_builder.canonical_bytes(bundle_builder.build())
        second = bundle_builder.canonical_bytes(bundle_builder.build())
        self.assertEqual(first, second)

    def test_default_web_path_is_candidate_not_live_api(self):
        self.assertIn('src="/src/mvp.ts"', self.index)
        self.assertIn('./data/r1-mvp-candidate.json', self.mvp)
        self.assertNotIn("VITE_ATLAS_API_URL", self.mvp)
        self.assertNotIn("/v1/atlas", self.mvp)
        self.assertNotIn("supabase", self.mvp.lower())

    def test_mvp_surface_preserves_core_safety_boundaries(self):
        self.assertIn("No historical absence inference.", self.mvp)
        self.assertIn("Required abstention", self.mvp)
        self.assertIn("Source family:", self.mvp)
        self.assertIn("Temporal rendering guard", self.mvp)
        self.assertIn("No reviewed target geometry is materialized", self.mvp)
        self.assertNotIn("P1", self.mvp)
        self.assertNotIn("P4", self.mvp)

    def test_accessibility_smoke_is_semantic_and_keyboard_reachable(self):
        self.assertIn('class="skip-link" href="#panel"', self.index)
        self.assertIn('id="panel"', self.index)
        self.assertIn('tabindex="-1"', self.index)
        self.assertIn('class="place-card" type="button"', self.mvp)
        self.assertIn('id="register-back" type="button"', self.mvp)
        self.assertIn('aria-label="Frozen research anchor"', self.index)

    def test_locked_frontend_dependency_graph_exists(self):
        lock = WEB / "package-lock.json"
        self.assertTrue(lock.exists())
        self.assertGreater(lock.stat().st_size, 0)

    def test_known_external_land_dependency_is_not_hidden(self):
        self.assertIn("raw.githubusercontent.com/nvkelso/natural-earth-vector", self.mvp)
        self.assertIn("External neutral-land asset", self.release_check)
        self.assertIn("TECHNICAL_MVP_CANDIDATE", self.release_check)
        self.assertIn("Sponsor/browser usability acceptance remains pending", self.release_check)


if __name__ == "__main__":
    unittest.main()
