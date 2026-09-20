from pathlib import Path
import json
import tempfile
import unittest

from tools.build_public_snapshot import SnapshotError, build_snapshot


def payload():
    return {
        "status": "published_preview",
        "release_version": "mvp-preview-test",
        "schema_version": "db-foundation-v0.2",
        "canonical": False,
        "data_boundary": "release_manifest_plus_publish_views",
        "date_model": "astronomical_year_numbering",
        "cartography": {
            "fabric_id": "fabric-test",
            "source_url": "https://example.test/land.geojson",
            "content_sha256": "a" * 64,
        },
        "places": [
            {
                "spatial_entity_id": "place-1",
                "name": "Test",
                "display_name": "Test",
                "entity_type_code": "polity",
                "notes": None,
                "claims": [{"claim_id": "claim-1", "sources": []}],
                "geometries": [{"geometry_id": "geometry-1", "geometry": {"type": "Point", "coordinates": [1, 2]}}],
            }
        ],
    }


class PublicSnapshotTests(unittest.TestCase):
    def test_snapshot_is_deterministic_and_checksummed(self):
        with tempfile.TemporaryDirectory() as tmp:
            first = build_snapshot(
                payload(),
                Path(tmp) / "one",
                source_url="https://example.test/api",
                source_git_sha="abc123",
            )
            scrambled = dict(reversed(list(payload().items())))
            second = build_snapshot(
                scrambled,
                Path(tmp) / "two",
                source_url="https://example.test/api",
                source_git_sha="abc123",
            )
            self.assertEqual(first["payload_sha256"], second["payload_sha256"])
            self.assertEqual(first["place_count"], 1)
            self.assertEqual(first["claim_count"], 1)
            self.assertEqual(first["geometry_record_count"], 1)
            self.assertEqual(first["mapped_geometry_count"], 1)

            body = (Path(tmp) / "one" / "atlas-data.json").read_text(encoding="utf-8")
            self.assertEqual(json.loads(body)["release_version"], "mvp-preview-test")

    def test_snapshot_rejects_missing_cartography(self):
        bad = payload()
        bad["cartography"] = None
        with tempfile.TemporaryDirectory() as tmp:
            with self.assertRaises(SnapshotError):
                build_snapshot(
                    bad,
                    Path(tmp),
                    source_url="https://example.test/api",
                    source_git_sha="abc123",
                )


if __name__ == "__main__":
    unittest.main()
