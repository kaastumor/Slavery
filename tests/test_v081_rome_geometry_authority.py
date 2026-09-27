from __future__ import annotations

import json
from pathlib import Path
import unittest

ROOT = Path(__file__).resolve().parents[1]
AUTHORITY = ROOT / "data" / "release_candidates" / "v0.8.1-rome-geometry-authority.bundle.json"
PREDECESSOR = ROOT / "data" / "releases" / "v0.8.0" / "authority-state.json"
SELECTION = ROOT / "release" / "selections" / "v0.8.1-rome-geometry-correction.json"

import sys
sys.path.insert(0, str(ROOT / "tools"))
from full_state_release_bundle import validate_bundle  # noqa: E402


class V081RomeGeometryAuthorityTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.bundle = json.loads(AUTHORITY.read_text(encoding="utf-8"))
        cls.predecessor = json.loads(PREDECESSOR.read_text(encoding="utf-8"))
        cls.selection = json.loads(SELECTION.read_text(encoding="utf-8"))

    def test_bundle_validates(self) -> None:
        validate_bundle(self.bundle)

    def test_counts_do_not_change(self) -> None:
        membership = self.bundle["membership"]
        expected = self.selection["expected_counts"]
        for key, count in expected.items():
            self.assertEqual(len(membership[key]), count, key)

    def test_only_geometry_and_geometry_source_are_substituted(self) -> None:
        correction = self.selection["correction"]
        new_membership = self.bundle["membership"]
        old_membership = self.predecessor["membership"]

        for key in old_membership:
            if key not in {"geometry_ids", "source_version_ids"}:
                self.assertEqual(new_membership[key], old_membership[key], key)

        self.assertEqual(
            set(new_membership["geometry_ids"]),
            (set(old_membership["geometry_ids"]) - {correction["remove_geometry_id"]})
            | {correction["add_geometry_id"]},
        )
        self.assertEqual(
            set(new_membership["source_version_ids"]),
            (
                set(old_membership["source_version_ids"])
                - {correction["remove_source_version_id"]}
            )
            | {correction["add_source_version_id"]},
        )

    def test_all_other_predecessor_objects_are_identical(self) -> None:
        correction = self.selection["correction"]
        exceptions = {
            ("geometries", correction["remove_geometry_id"]),
            ("source_versions", correction["remove_source_version_id"]),
        }
        for group, objects in self.predecessor["objects"].items():
            for object_id, payload in objects.items():
                if (group, object_id) in exceptions:
                    continue
                self.assertEqual(
                    self.bundle["objects"][group][object_id],
                    payload,
                    f"unexpected predecessor drift {group}:{object_id}",
                )

    def test_new_geometry_is_bounded_and_approximate(self) -> None:
        correction = self.selection["correction"]
        geometry = self.bundle["objects"]["geometries"][correction["add_geometry_id"]]
        self.assertEqual(geometry["from_year"], 14)
        self.assertEqual(geometry["to_year"], 22)
        self.assertEqual(geometry["accuracy_status"], "approximate_historical")
        self.assertEqual(
            geometry["geometry_source_version_id"],
            correction["add_source_version_id"],
        )


if __name__ == "__main__":
    unittest.main()
