import copy
import unittest
from tools import build_requested_corpus_authority as builder


class RequestedCorpusSourceTests(unittest.TestCase):
    def test_native_source_bindings_and_tampered_coordinate(self):
        old=builder.load(builder.ROOT/'data/releases/v0.8.1/authority-state.json')
        audit=builder.load(builder.ROOT/'data/research/geometry_reviews/v082_non_api_source_bindings.json')
        builder.verify_source_bindings(old,audit)
        bad=copy.deepcopy(audit)
        bad['rows'][0]['source_record']['longitude_dms'][0]+=1
        with self.assertRaisesRegex(ValueError,'fingerprint'):
            builder.verify_source_bindings(old,bad)

    def test_unknown_legacy_geometry_cannot_be_declared_closed(self):
        old=builder.load(builder.ROOT/'data/releases/v0.8.1/authority-state.json')
        audit=builder.load(builder.ROOT/'data/research/geometry_reviews/v082_non_api_source_bindings.json')
        audit['held'].pop()
        with self.assertRaisesRegex(ValueError,'membership drift'):
            builder.verify_source_bindings(old,audit)
