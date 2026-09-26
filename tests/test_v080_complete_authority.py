from pathlib import Path
import hashlib
import json
import unittest

ROOT = Path(__file__).resolve().parents[1]
AUTHORITY = ROOT / "data" / "release_candidates" / "v0.8.0-expansion-02-authority.bundle.json"
SELECTION = ROOT / "release" / "selections" / "v0.8.0-expansion-02.json"
PREDECESSOR = ROOT / "data" / "releases" / "v0.7.0" / "authority-state.json"

import sys
sys.path.insert(0, str(ROOT / "tools"))
from full_state_release_bundle import sha256_value, validate_bundle  # noqa: E402


class V080CompleteAuthorityTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.authority = json.loads(AUTHORITY.read_text(encoding="utf-8"))
        cls.selection = json.loads(SELECTION.read_text(encoding="utf-8"))
        cls.predecessor = json.loads(PREDECESSOR.read_text(encoding="utf-8"))

    def test_preservation_bundle_is_valid(self) -> None:
        validate_bundle(self.authority)

    def test_exact_complete_entry_membership(self) -> None:
        membership = self.authority["membership"]
        self.assertEqual(len(membership["claim_ids"]), 75)
        self.assertEqual(len(membership["spatial_entity_ids"]), 50)
        self.assertEqual(len(membership["geometry_ids"]), 46)
        self.assertEqual(len(membership["source_version_ids"]), 294)
        self.assertEqual(len(membership["actor_ids"]), 11)
        self.assertEqual(len(membership["voyage_ids"]), 8)
        self.assertEqual(len(membership["coverage_assessment_ids"]), 99)
        self.assertEqual(len(membership["research_target_result_ids"]), 26)

    def test_selection_bytes_are_exact_authority_input(self) -> None:
        self.assertEqual(
            self.authority["candidate_sha256"],
            hashlib.sha256(SELECTION.read_bytes()).hexdigest(),
        )
        self.assertEqual(
            self.authority["membership_sha256"],
            sha256_value(self.authority["membership"]),
        )

    def test_predecessor_membership_and_objects_are_preserved(self) -> None:
        for key, ids in self.predecessor["membership"].items():
            self.assertTrue(set(ids).issubset(self.authority["membership"][key]))
        for group, objects in self.predecessor["objects"].items():
            for object_id, payload in objects.items():
                self.assertEqual(
                    self.authority["objects"][group][object_id],
                    payload,
                    f"predecessor drift {group}:{object_id}",
                )

    def test_unresolved_geometry_rows_are_not_mapped_membership(self) -> None:
        unresolved = {
            "136c0f0b-537f-4a39-a5ec-7117edfadbfb",
            "2a11ccf8-06c4-495a-85e2-214cd8d164ba",
            "3cffa01a-740b-4195-a992-e4e4a96837da",
        }
        self.assertTrue(unresolved.isdisjoint(self.authority["membership"]["geometry_ids"]))

    def test_reviewed_disputes_are_preserved_as_claim_state(self) -> None:
        reviewed_state = set(self.selection["additions"]["reviewed_state_claim_ids"])
        self.assertTrue(reviewed_state.issubset(self.authority["membership"]["claim_ids"]))
        for claim_id in reviewed_state:
            status = self.authority["objects"]["claims"][claim_id]["territorial_practice"][
                "classification_status"
            ]
            self.assertIn(status, {"disputed", "reviewed_with_date_dispute"})


if __name__ == "__main__":
    unittest.main()
