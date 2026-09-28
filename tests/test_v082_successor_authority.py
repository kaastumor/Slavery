from __future__ import annotations

import copy
import json
from pathlib import Path
import sys
import tempfile
import unittest

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "tools"))

from build_successor_authority import (  # noqa: E402
    SuccessorAuthorityError,
    load_predecessor,
    load_selection,
    verify_predecessor_objects_preserved,
)

SELECTION = ROOT / "release" / "selections" / "v0.8.2-post-overnight-claims.json"
PREDECESSOR = (
    ROOT
    / "data"
    / "release_candidates"
    / "v0.8.1-rome-geometry-authority.bundle.json"
)


class V082SuccessorAuthorityContractTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.selection = load_selection(SELECTION)
        cls.predecessor = load_predecessor(cls.selection, PREDECESSOR)

    def test_frozen_selection_is_release_ready_and_explicit(self) -> None:
        self.assertEqual(len(self.selection["claim_additions"]), 11)
        self.assertEqual(
            self.selection["expected_claim_state"]["successor_claims"], 86
        )
        self.assertEqual(
            self.selection["expected_claim_state"]["successor_spatial_entities"], 63
        )
        self.assertEqual(
            self.selection["geometry_policy"][
                "expected_successor_geometry_membership"
            ],
            48,
        )
        self.assertEqual(
            self.selection["geometry_policy"]["new_practice_extent_geometry_ids"],
            [],
        )

    def test_predecessor_authority_is_exact_v081(self) -> None:
        self.assertEqual(
            self.predecessor["release"]["release_version"],
            "v0.8.1-rome-geometry-authority-v1",
        )
        self.assertEqual(len(self.predecessor["membership"]["claim_ids"]), 75)
        self.assertEqual(len(self.predecessor["membership"]["spatial_entity_ids"]), 50)
        self.assertEqual(len(self.predecessor["membership"]["geometry_ids"]), 46)

    def test_load_selection_rejects_reviewed_row_discovery(self) -> None:
        candidate = copy.deepcopy(self.selection)
        candidate["rules"]["reviewed_row_discovery_forbidden"] = False
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / "selection.json"
            path.write_text(json.dumps(candidate), encoding="utf-8")
            with self.assertRaises(SuccessorAuthorityError):
                load_selection(path)

    def test_load_selection_rejects_proxy_practice_extent(self) -> None:
        candidate = copy.deepcopy(self.selection)
        candidate["geometry_policy"]["new_practice_extent_geometry_ids"] = [
            "00000000-0000-0000-0000-000000000001"
        ]
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / "selection.json"
            path.write_text(json.dumps(candidate), encoding="utf-8")
            with self.assertRaises(SuccessorAuthorityError):
                load_selection(path)

    def test_bounded_mycenaean_augmentation_allows_only_locus_delta(self) -> None:
        correction = self.selection["predecessor_object_correction_required"]
        claim_id = correction["claim_id"]
        objects = copy.deepcopy(self.predecessor["objects"])
        objects["claims"][claim_id]["evidence_loci"] = [
            {
                "claim_id": claim_id,
                "spatial_entity_id": row["spatial_entity_id"],
                "role_text": "archaeological evidence locus",
                "notes": None,
            }
            for row in correction["current_evidence_loci"]
        ]
        verify_predecessor_objects_preserved(
            self.predecessor, objects, self.selection
        )

        drifted = copy.deepcopy(objects)
        drifted["claims"][claim_id]["claim"]["summary"] = "unauthorized drift"
        with self.assertRaises(SuccessorAuthorityError):
            verify_predecessor_objects_preserved(
                self.predecessor, drifted, self.selection
            )

    def test_unrelated_predecessor_drift_is_rejected(self) -> None:
        objects = copy.deepcopy(self.predecessor["objects"])
        first_id = sorted(objects["spatial_entities"])[0]
        objects["spatial_entities"][first_id]["spatial_entity"]["notes"] = (
            "unauthorized drift"
        )
        with self.assertRaises(SuccessorAuthorityError):
            verify_predecessor_objects_preserved(
                self.predecessor, objects, self.selection
            )


if __name__ == "__main__":
    unittest.main()
