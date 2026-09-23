import io
import json
import unittest
import zipfile

from tools.profile_cliopatria import git_blob_sha1, load_features, profile


def fixture_bytes():
    obj = {
        "type": "FeatureCollection",
        "features": [
            {
                "type": "Feature",
                "properties": {"Name": "A", "Type": "POLITY", "FromYear": -10, "ToYear": -1, "Extra": "x"},
                "geometry": {"type": "Polygon", "coordinates": []},
            },
            {
                "type": "Feature",
                "properties": {"Name": "B", "Type": "RELATION", "FromYear": -2, "ToYear": 3},
                "geometry": {"type": "MultiPolygon", "coordinates": []},
            },
            {
                "type": "Feature",
                "properties": {"Name": "Composite", "Type": "POLITY, RELATION", "FromYear": 4, "ToYear": 2},
                "geometry": None,
            },
        ],
    }
    buf = io.BytesIO()
    with zipfile.ZipFile(buf, "w") as z:
        z.writestr("cliopatria.geojson", json.dumps(obj))
        z.writestr("__MACOSX/._cliopatria.geojson", "finder metadata")
    return buf.getvalue()


class CliopatriaProfileTests(unittest.TestCase):
    def test_profile_preserves_source_semantics_and_counts_property_presence(self):
        data = fixture_bytes()
        features = load_features(data)
        p = profile(features)
        self.assertEqual(p["feature_count"], 3)
        self.assertEqual(p["type_counts"], {"POLITY": 1, "POLITY, RELATION": 1, "RELATION": 1})
        self.assertEqual(p["source_native_years"]["minimum"], -10)
        self.assertEqual(p["source_native_years"]["maximum"], 3)
        self.assertEqual(p["source_native_years"]["rows_crossing_numeric_zero"], 1)
        self.assertEqual(p["source_native_years"]["invalid_from_to_ranges"], 1)
        self.assertEqual(p["property_presence_counts"]["Extra"], 1)
        self.assertEqual(p["property_presence_counts"]["Name"], 3)
        self.assertEqual(p["property_presence_counts"]["Type"], 3)

    def test_git_blob_identity_is_content_sensitive(self):
        data = fixture_bytes()
        self.assertNotEqual(git_blob_sha1(data), git_blob_sha1(data + b"x"))


if __name__ == "__main__":
    unittest.main()
