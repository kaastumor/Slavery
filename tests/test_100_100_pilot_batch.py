from pathlib import Path
import sys
import unittest

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from tools.rehearse_100_100_pilot_batch import (  # noqa: E402
    EXPECTED_MEMBERS,
    load_candidates,
    load_manifest,
    plan,
)


class PilotBatchManifestTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.manifest = load_manifest()
        cls.loaded = load_candidates(cls.manifest)

    def test_manifest_is_exact_first_d124_batch(self):
        self.assertEqual(len(self.loaded), EXPECTED_MEMBERS)
        self.assertEqual(len(self.loaded), 5)
        self.assertFalse(
            self.manifest["authority"]["production_write_authorized"]
        )
        self.assertEqual(
            self.manifest["status"],
            "READY_FOR_DISPOSABLE_REHEARSAL_ONLY_NOT_PRODUCTION_AUTHORIZED",
        )

    def test_packet_blob_bindings_and_claim_kind_mix_validate(self):
        result = plan(self.manifest)
        self.assertEqual(
            result["claim_kinds"],
            {"territorial_practice": 2, "external_participation": 3},
        )
        self.assertEqual(len(result["packet_blobs"]), 5)
        self.assertFalse(result["production_write_authorized"])

    def test_no_member_has_p_level_or_publication(self):
        for _, spec, kind in self.loaded:
            self.assertEqual(spec["claim"]["review_status"], "reviewed")
            self.assertEqual(spec["claim"]["publication_status"], "unpublished")
            if kind == "territorial_practice":
                self.assertIsNone(
                    spec["claim"]["territorial_practice"]["practice_level"]
                )
            else:
                self.assertNotIn("territorial_practice", spec["claim"])
                self.assertNotIn("practice_level", spec["claim"])

    def test_geometry_composition_is_two_resolved_three_unresolved(self):
        resolved = 0
        unresolved = 0
        for _, spec, _ in self.loaded:
            geometry = spec["geometry"]
            if geometry["accuracy_status"] == "unresolved":
                unresolved += 1
                self.assertIsNone(geometry["geojson"])
            else:
                resolved += 1
                self.assertEqual(geometry["accuracy_status"], "modern_proxy")
                self.assertEqual(geometry["geojson"]["type"], "Point")
        self.assertEqual((resolved, unresolved), (2, 3))


if __name__ == "__main__":
    unittest.main()
