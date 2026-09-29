import copy
import json
from pathlib import Path
import unittest

from tools.verify_population_packets import PacketError, audit, canonical_hash, entries, parse_packet, verify_one
from tools.test_population_replay import check_disposable_dsn

ROOT = Path(__file__).resolve().parents[1]
PREFLIGHT = ROOT / 'data/research/recovery/production_batch_2026_09_29/preflight.json'


class PopulationPacketTests(unittest.TestCase):
    def fixture(self):
        spec = {'case_key': 'test/population/one',
                'spatial_entity': {'canonical_name': 'Example'},
                'claim': {'from_year': 2000, 'to_year': 2000, 'review_status': 'reviewed',
                          'publication_status': 'unpublished',
                          'territorial_practice': {'practice_level': None}},
                'evidence': [{'source': {'title': 'Example'},
                              'version': {'url_or_identifier': 'urn:example:one'},
                              'locator': 'section 1'}]}
        entry = {'name': 'Example', 'from_year': 2000, 'to_year': 2000,
                 'recorded_ingest_content_sha256': canonical_hash(spec), 'claim_id': 'test-id',
                 'revision': 'a' * 40, 'path': 'data/research/test.json', 'missing_locator_count': 0}
        return entry, spec

    def test_formatted_bytes_are_not_the_ingestion_digest(self):
        entry, spec = self.fixture()
        a, _ = verify_one(entry, json.dumps(spec, indent=2).encode())
        b, _ = verify_one(entry, json.dumps(spec, separators=(',', ':')).encode())
        self.assertEqual(a['canonical_ingest_content_sha256'], b['canonical_ingest_content_sha256'])
        self.assertNotEqual(a['raw_file_sha256'], b['raw_file_sha256'])
        self.assertFalse(a['release_ready'])

    def test_changed_content_fails(self):
        entry, spec = self.fixture()
        spec['claim']['to_year'] = 2001
        with self.assertRaises(PacketError):
            verify_one(entry, json.dumps(spec).encode())

    def test_duplicate_json_keys_rejected(self):
        with self.assertRaises(PacketError):
            parse_packet(b'{"a":1,"a":2}')

    def test_production_dsn_is_rejected(self):
        for dsn, flag, ci in [
            ('postgresql://atlas:password@prod.example/slavery_atlas', True, 'true'),
            ('postgresql://atlas:password@db/slavery_atlas?host=prod.example', True, 'true'),
            ('postgresql://atlas:password@db/slavery_atlas', False, 'true'),
            ('postgresql://atlas:password@db/slavery_atlas', True, None),
        ]:
            with self.assertRaises(PacketError):
                check_disposable_dsn(dsn, flag, ci)
        check_disposable_dsn('postgresql://atlas:password@db:5432/slavery_atlas', True, 'true')

    def test_all_eleven_recorded_packets_and_importer_hash_agree(self):
        from tools.add_research_case import case_content_sha256, validate_case_spec, plan
        preflight = json.loads(PREFLIGHT.read_text(encoding='utf-8'))
        report = audit(ROOT, preflight)
        self.assertEqual(report['failures'], [])
        self.assertEqual(report['verified_packet_count'], 11)
        for row in report['packets']:
            spec = parse_packet((ROOT / row['path']).read_bytes())
            validate_case_spec(spec, require_case_key=True)
            self.assertEqual(case_content_sha256(spec), row['canonical_ingest_content_sha256'])
            self.assertEqual(plan(spec)['content_sha256'], row['canonical_ingest_content_sha256'])
            self.assertTrue(row['current_checkout_matches_recorded_content'])
        print('POPULATION_PACKET_AUDIT_BEGIN')
        print(json.dumps(report, ensure_ascii=False, sort_keys=True))
        print('POPULATION_PACKET_AUDIT_END')

    def test_inventory_duplicate_and_unsafe_path_fail(self):
        p = json.loads(PREFLIGHT.read_text(encoding='utf-8'))
        p['existing_claims'].append(copy.deepcopy(p['existing_claims'][0]))
        with self.assertRaises(PacketError):
            entries(p)
        p = json.loads(PREFLIGHT.read_text(encoding='utf-8'))
        p['packet_path_rule']['default_prefix'] = '../'
        with self.assertRaises(PacketError):
            entries(p)
