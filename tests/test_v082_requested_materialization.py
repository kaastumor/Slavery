import copy
import unittest
from tools import export_v082_requested_publication_sql as exporter
from tools import build_v082_requested_materialization as materializer
from tools.full_state_release_bundle import validate_bundle

class RequestedMaterializationTests(unittest.TestCase):
    def test_frozen_cases_dimensions_and_geometry_hold(self):
        authority=exporter.load(exporter.ROOT/'data/releases/v0.8.2/authority-state.json')
        validate_bundle(authority)
        payload=exporter.load(exporter.ROOT/'data/serving/v0.8.2-public-mvp-v1/atlas-data.json')
        self.assertEqual(len(payload['places']),65)
        kinds=[c['claim_kind'] for p in payload['places'] for c in p['claims']]
        self.assertEqual(kinds.count('territorial_practice'),66)
        self.assertEqual(kinds.count('legal_event'),1)
        self.assertEqual(kinds.count('external_participation'),3)
        for p in payload['places']:
            for c in p['claims']:
                if c['claim_kind']!='territorial_practice':self.assertIsNone(c['practice_level'])
        geometry_ids={g['geometry_id'] for p in payload['places'] for g in p['geometries']}
        selection=exporter.load(exporter.ROOT/'release/selections/v0.8.2-requested-corpus.json')
        self.assertTrue(geometry_ids.isdisjoint(selection['geometry_selection']['withheld_inherited_geometry_ids']))
        self.assertEqual(geometry_ids,set(authority['membership']['geometry_ids']))

    def test_export_is_inert_and_preflight_mismatch_rejected(self):
        receipt=exporter.load(exporter.ROOT/'data/research/release_candidates/v082_requested_publication_preflight.json')
        sql=exporter.render(receipt,'UNIT_TEST')
        self.assertLess(sql.index('authorization absent'),sql.index('INSERT INTO audit.release_manifest'))
        self.assertIn('release replay/collision',sql)
        self.assertIn('registration moved public channel',sql)
        self.assertIn('st_normalize',sql)
        bad=copy.deepcopy(receipt);bad['groups']['claim_ids']['exact_match']=False
        with self.assertRaisesRegex(ValueError,'preflight mismatch'):
            exporter.render(bad,'UNIT_TEST',True)
