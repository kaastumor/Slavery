import json
from pathlib import Path
import sys
import tempfile
import unittest

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "tools"))

from ingest_cliopatria import (  # noqa: E402
    UPSTREAM_COMMIT,
    UPSTREAM_GIT_BLOB_SHA1,
    UPSTREAM_SHA256,
    canonical_json,
    feature_checksum,
    feature_projection,
    raw_record_id,
    verify_expected_profile,
)
from profile_cliopatria import profile  # noqa: E402


def feature(
    name="Polity A",
    typ="POLITY",
    start=-1,
    end=0,
    member="(Composite)",
    components="",
    feature_id=None,
):
    value = {
        "type": "Feature",
        "properties": {
            "Name": name,
            "Type": typ,
            "FromYear": start,
            "ToYear": end,
            "MemberOf": member,
            "Components": components,
            "SeshatID": "Ses-1",
            "Wikidata": "Q1",
            "Wikipedia": "Polity_A",
            "Area": 12.5,
        },
        "geometry": {
            "type": "Polygon",
            "coordinates": [[[0, 0], [1, 0], [1, 1], [0, 0]]],
        },
    }
    if feature_id is not None:
        value["id"] = feature_id
    return value


class CliopatriaIngestUnitTests(unittest.TestCase):
    def test_projection_preserves_source_native_year_zero_and_hierarchy(self):
        row = feature_projection(feature(), 7)
        self.assertEqual(row[0], 7)
        self.assertEqual(row[5], "Polity A")
        self.assertEqual(row[6], "POLITY")
        self.assertEqual(row[7], -1)
        self.assertEqual(row[8], 0)
        self.assertEqual(row[9], "(Composite)")
        self.assertEqual(row[10], "")
        self.assertEqual(row[11], "Ses-1")
        self.assertEqual(row[12], "Q1")
        self.assertEqual(row[13], "Polity_A")
        self.assertIsNone(row[2], "missing upstream feature id must remain unknown")

    def test_upstream_feature_id_is_separate_from_import_ordinal(self):
        first = feature_projection(feature(feature_id=123), 1)
        second = feature_projection(feature(feature_id=123), 2)
        self.assertEqual(first[2], "123")
        self.assertEqual(second[2], "123")
        self.assertNotEqual(first[1], second[1])
        self.assertNotEqual(raw_record_id(1), raw_record_id(2))

    def test_feature_checksum_is_canonical_but_content_sensitive(self):
        original = feature()
        reordered = json.loads(canonical_json(original))
        self.assertEqual(feature_checksum(original), feature_checksum(reordered))
        changed = feature(end=1)
        self.assertNotEqual(feature_checksum(original), feature_checksum(changed))

    def test_expected_profile_comparison_does_not_normalize_source_values(self):
        features = [
            feature(name="A", start=-1, end=0, member="(Union)"),
            feature(
                name="(Union)",
                typ="RELATION",
                start=-1,
                end=1,
                member="",
                components="A;B",
            ),
        ]
        expected = {
            "source": {
                "commit": UPSTREAM_COMMIT,
                "git_blob_sha1": UPSTREAM_GIT_BLOB_SHA1,
                "sha256": UPSTREAM_SHA256,
            },
            "profile": profile(features),
        }
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / "expected.json"
            path.write_text(json.dumps(expected), encoding="utf-8")
            verify_expected_profile(features, path)

    def test_expected_profile_mismatch_fails_closed(self):
        features = [feature()]
        expected = {
            "source": {
                "commit": UPSTREAM_COMMIT,
                "git_blob_sha1": UPSTREAM_GIT_BLOB_SHA1,
                "sha256": UPSTREAM_SHA256,
            },
            "profile": {**profile(features), "feature_count": 999},
        }
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / "expected.json"
            path.write_text(json.dumps(expected), encoding="utf-8")
            with self.assertRaises(ValueError):
                verify_expected_profile(features, path)


if __name__ == "__main__":
    unittest.main()
