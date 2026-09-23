import io
import json
import unittest
import zipfile

from tools.profile_cliopatria import git_blob_sha1, load_features, profile, semantic_diagnostics


def fixture_bytes():
    obj = {
        "type": "FeatureCollection",
        "features": [
            {
                "type": "Feature",
                "properties": {"Name": "A", "Type": "POLITY", "FromYear": -10, "ToYear": -1, "Extra": "x", "MemberOf": "", "Components": ""},
                "geometry": {"type": "Polygon", "coordinates": []},
            },
            {
                "type": "Feature",
                "properties": {"Name": "B", "Type": "RELATION", "FromYear": -2, "ToYear": 3, "MemberOf": "", "Components": "A;C"},
                "geometry": {"type": "MultiPolygon", "coordinates": []},
            },
            {
                "type": "Feature",
                "properties": {"Name": "Composite", "Type": "POLITY, RELATION", "FromYear": 4, "ToYear": 2, "MemberOf": "", "Components": ""},
                "geometry": None,
            },
            {
                "type": "Feature",
                "properties": {"Name": "Zero", "Type": "POLITY", "FromYear": 0, "ToYear": 1, "MemberOf": "(Group)", "Components": ""},
                "geometry": {"type": "Polygon", "coordinates": []},
            },
        ],
    }
    buf = io.BytesIO()
    with zipfile.ZipFile(buf, "w") as z:
        z.writestr("cliopatria.geojson", json.dumps(obj))
        z.writestr("__MACOSX/._cliopatria.geojson", "finder metadata")
    return buf.getvalue()


def semantic_features():
    def feature(name, typ, start, end, member="", components=""):
        return {
            "type": "Feature",
            "properties": {
                "Name": name,
                "Type": typ,
                "FromYear": start,
                "ToYear": end,
                "MemberOf": member,
                "Components": components,
                "SeshatID": "",
                "Wikidata": "",
                "Wikipedia": "",
            },
            "geometry": {"type": "Polygon", "coordinates": []},
        }

    return [
        feature("Polity A", "POLITY", -3, -1, "(Union)", ""),
        feature("Polity A", "POLITY", 0, 2, "(Union)", ""),
        feature("(Union)", "RELATION", -3, 2, "", "Polity A, Polity B"),
        feature("Polity B", "POLITY", -3, 2, "(Union)", ""),
        feature("Gap Polity", "POLITY", 10, 12),
        feature("Gap Polity", "POLITY", 15, 20),
        feature("Overlap Polity", "POLITY", 30, 35),
        feature("Overlap Polity", "POLITY", 35, 40),
    ]


class CliopatriaProfileTests(unittest.TestCase):
    def test_profile_preserves_source_semantics_and_counts_property_presence(self):
        data = fixture_bytes()
        features = load_features(data)
        p = profile(features)
        self.assertEqual(p["feature_count"], 4)
        self.assertEqual(p["type_counts"], {"POLITY": 2, "POLITY, RELATION": 1, "RELATION": 1})
        self.assertEqual(p["source_native_years"]["minimum"], -10)
        self.assertEqual(p["source_native_years"]["maximum"], 3)
        self.assertEqual(p["source_native_years"]["rows_crossing_numeric_zero"], 1)
        self.assertEqual(p["source_native_years"]["invalid_from_to_ranges"], 1)
        self.assertEqual(p["source_native_years"]["rows_with_zero_endpoint"], 1)
        self.assertEqual(p["property_presence_counts"]["Extra"], 1)
        self.assertEqual(p["property_presence_counts"]["Name"], 4)
        self.assertEqual(p["property_presence_counts"]["Type"], 4)

    def test_semantic_diagnostics_preserve_zero_row_and_membership(self):
        d = semantic_diagnostics(semantic_features())
        self.assertEqual(len(d["zero_endpoint_rows"]), 1)
        zero = d["zero_endpoint_rows"][0]
        self.assertEqual(zero["row"]["Name"], "Polity A")
        self.assertEqual(zero["row"]["FromYear"], 0)
        self.assertEqual(zero["previous_same_name"]["ToYear"], -1)
        self.assertEqual(d["membership"]["rows_with_member_of"], 3)
        self.assertEqual(d["membership"]["relation_rows_with_components"], 1)
        self.assertEqual(d["relation_name_parenthesized_count"], 1)
        self.assertEqual(d["member_of_arity_counts"], {1: 3})
        self.assertEqual(d["component_arity_counts"], {2: 1})
        self.assertEqual(d["nested_composite_samples"], [])

    def test_semantic_diagnostics_surface_interval_overlap_and_gap(self):
        d = semantic_diagnostics(semantic_features())
        adjacency = d["same_name_interval_adjacency"]
        self.assertEqual(adjacency["integer_contiguous"], 1)
        self.assertEqual(adjacency["gap_more_than_one_integer"], 1)
        self.assertEqual(adjacency["inclusive_overlap_or_parallel"], 1)
        self.assertEqual(d["same_name_overlap_examples"][0]["name"], "Overlap Polity")
        self.assertEqual(d["same_name_gap_examples"][0]["name"], "Gap Polity")

    def test_git_blob_identity_is_content_sensitive(self):
        data = fixture_bytes()
        self.assertNotEqual(git_blob_sha1(data), git_blob_sha1(data + b"x"))


if __name__ == "__main__":
    unittest.main()
