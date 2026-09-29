import json
from pathlib import Path
import unittest

from tools.ingest_population_subset import (
    EXPECTED_ACCEPTED,
    EXPECTED_HELD,
    IngestError,
    MANIFEST,
    load_candidates,
    load_manifest,
    plan,
)


class PopulationIngestPlanTests(unittest.TestCase):
    def test_manifest_and_candidate_hashes_are_exact(self):
        manifest = load_manifest()
        rows = load_candidates(manifest)
        self.assertEqual(len(rows), EXPECTED_ACCEPTED)
        self.assertEqual(len(manifest["held_exclusions"]), EXPECTED_HELD)
        self.assertEqual(
            [r["case_key"] for r in manifest["accepted"]],
            [r["case_key"] for r, _, _ in rows],
        )

    def test_plan_is_nonpublishing_and_complete(self):
        p = plan(load_manifest())
        self.assertEqual(p["accepted_cases"], 12)
        self.assertEqual(p["held_exclusions"], 11)
        self.assertEqual(p["claim_kinds"], {"legal_event": 1, "territorial_practice": 11})
        self.assertEqual(p["release_membership_change"], 0)
        self.assertEqual(p["publication_change"], 0)
        self.assertEqual(p["serving_channel_change"], 0)
        self.assertFalse(p["production_write_authorized"])

    def test_manifest_accounts_for_all_23_targets(self):
        manifest = load_manifest()
        accounting = manifest["register_accounting"]
        self.assertEqual(accounting["planning_targets"], 23)
        self.assertEqual(accounting["accepted_staging"], 12)
        self.assertEqual(accounting["held_exclusions"], 11)
        self.assertEqual(accounting["unaccounted_targets"], 0)

    def test_live_expected_delta_keeps_release_separate(self):
        manifest = load_manifest()
        delta = manifest["expected_database_delta_if_explicitly_ingested"]
        self.assertEqual(delta["claim"], 12)
        self.assertEqual(delta["legal_event"], 1)
        self.assertEqual(delta["territorial_practice_claim"], 11)
        self.assertEqual(delta["geometry_rows"], 10)
        self.assertEqual(delta["resolved_geometry"], 9)
        self.assertEqual(delta["release_claim"], 0)
        self.assertEqual(delta["publication_status_changes"], 0)


if __name__ == "__main__":
    unittest.main()
