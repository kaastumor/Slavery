import copy
import gzip
import json
import unittest
from tools import export_100_100_pilot_sql as exporter
from tools import audit_successor_source_bindings as bindings

class PilotTransportTests(unittest.TestCase):
    def test_default_inert_and_five_distinct_claims(self):
        sql = exporter.render(revision='UNIT_TEST')
        self.assertIn("IF NOT (false) THEN RAISE EXCEPTION", sql)
        self.assertLess(sql.index('authorization absent'), sql.index('insert into'))
        self.assertEqual(sql.count('insert into atlas.claim('), 5)
        self.assertEqual(sql.count('insert into atlas.territorial_practice_claim('), 2)
        self.assertEqual(sql.count('insert into atlas.external_participation_claim('), 3)
        self.assertIn('pilot existing claims changed: atlas.claim', sql)
        self.assertNotIn('COMMIT', sql)

    def test_exact_preflight_source_reuse_remains_visible(self):
        path = exporter.pilot.MANIFEST.parent / 'production_source_reuse_preflight.json'
        data = json.loads(path.read_text(encoding='utf-8'))
        reused = {r['url_or_identifier']:r['source_version_id'] for r in data['sources']}
        sql = exporter.render(revision='UNIT_TEST', reused=reused)
        self.assertEqual(sql.count('insert into atlas.source('), 10)
        self.assertIn('pilot source reuse drift', sql)
        for identity in reused.values():
            self.assertIn(identity, sql)

    def test_frozen_upstream_bindings_reject_tampered_native_time(self):
        audit = json.loads(gzip.decompress((exporter.ROOT / 'data/research/geometry_reviews/v082_exact_api_source_bindings.json.gz').read_bytes()))
        bundle = json.loads((exporter.ROOT / 'data/releases/v0.8.1/authority-state.json').read_text(encoding='utf-8'))
        self.assertTrue(bindings.verify_bindings(audit, bundle))
        bad = copy.deepcopy(audit)
        bad['rows'][0]['source_record']['start_year'] += 1
        with self.assertRaisesRegex(ValueError, 'fingerprint'):
            bindings.verify_bindings(bad, bundle)

if __name__ == '__main__':
    unittest.main()
