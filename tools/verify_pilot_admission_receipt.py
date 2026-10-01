#!/usr/bin/env python3
"""Compare an independent live readback with every reviewed pilot packet."""
from __future__ import annotations
import argparse
import json
from pathlib import Path
import sys
ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))
from tools import export_100_100_pilot_sql as exporter

RECEIPT = exporter.pilot.MANIFEST.parent / 'production_admission_receipt.json'

def verify(receipt):
    checks = 0
    def equal(actual, expected, label):
        nonlocal checks
        checks += 1
        if actual != expected:
            raise ValueError(f'{label}: readback mismatch')
    rb = receipt['independent_readback']
    equal(rb['serving'], 'v0.8.1-public-mvp-v2', 'serving')
    _, candidates = exporter.inputs()
    equal(len(rb['cases']), 5, 'case count')
    cases = {row['case_key']: row for row in rb['cases']}
    sources = {row['source_version_id']: row for row in rb['sources']}
    preflight = json.loads((exporter.pilot.MANIFEST.parent / 'production_source_reuse_preflight.json').read_text(encoding='utf-8'))
    for old in preflight['sources']:
        for field, value in old.items():
            equal(sources[old['source_version_id']].get(field), value, 'reused source/' + field)
    for member, spec, kind in candidates:
        actual = cases[member['case_key']]
        equal(actual['claim']['claim_id'], receipt['transaction']['claim_ids'][member['case_key']], 'claim identity')
        equal(actual['ingest']['content_sha256'], exporter.pilot.case_content_sha256(spec), 'content lineage')
        equal(actual['ingest']['source_path'], member['path'], 'source path')
        equal(actual['claim']['claim_kind_code'], kind, 'claim kind')
        equal(actual['claim']['review_status'], 'reviewed', 'review')
        equal(actual['claim']['publication_status'], 'unpublished', 'publication')
        subtype = 'territorial' if kind == 'territorial_practice' else 'external'
        for field, value in spec['claim'].items():
            if field in ('territorial_practice', 'external_participation'):
                for key, expected in value.items():
                    equal(actual[subtype].get(key), expected, field + '/' + key)
            else:
                equal(actual['claim'].get(field), value, 'claim/' + field)
        for field, value in spec['spatial_entity'].items():
            equal(actual['spatial'].get(field), value, 'spatial/' + field)
        equal(actual['territorial'] is None, kind == 'external_participation', 'dimension separation')
        equal(len(actual['evidence']), len(spec['evidence']), 'evidence count')
        for expected in spec['evidence']:
            hits = [row for row in actual['evidence'] if sources[row['source_version_id']]['url_or_identifier'] == expected['version']['url_or_identifier']
                    and row['locator'] == expected.get('locator')]
            equal(len(hits), 1, 'source/locator binding')
            for key, value in expected.items():
                if key not in ('source', 'version'):
                    equal(hits[0].get(key), value, 'evidence/' + key)
        equal(len(actual['geometries']), 1, 'geometry count')
        geometry = actual['geometries'][0]
        for key, value in spec['geometry'].items():
            if key in ('source', 'version', 'geojson'):
                continue
            equal(geometry.get('geometry_source_native_id' if key == 'source_native_id' else key), value, 'geometry/' + key)
        expected_geojson = spec['geometry'].get('geojson')
        if expected_geojson is None:
            equal(geometry['geojson'], None, 'unresolved geometry')
        else:
            equal(geometry['geojson']['type'], 'Point', 'point type')
            checks += 1
            if any(abs(a-b) > 1e-9 for a,b in zip(geometry['geojson']['coordinates'], expected_geojson['coordinates'])):
                raise ValueError('point coordinate drift')
            equal(sources[geometry['geometry_source_version_id']]['url_or_identifier'], spec['geometry']['version']['url_or_identifier'], 'geometry source')
    for table, delta in exporter.pilot.STRICT_DELTAS.items():
        equal(receipt['transaction']['after_counts'][table]-receipt['transaction']['before_counts'][table], delta, 'transaction delta/' + table)
    return checks

def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--record-validation', action='store_true')
    args = parser.parse_args()
    data = json.loads(RECEIPT.read_text(encoding='utf-8'))
    checks = verify(data)
    if args.record_validation:
        data['status'] = 'COMMITTED_INDEPENDENT_READBACK_VERIFIED'
        data['readback_assertions'] = checks
        RECEIPT.write_text(json.dumps(data, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
    print(json.dumps({'status':'PASS','field_assertions':checks,'cases':5}))
    return 0

if __name__ == '__main__':
    raise SystemExit(main())
