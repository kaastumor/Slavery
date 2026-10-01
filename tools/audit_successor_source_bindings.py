#!/usr/bin/env python3
"""Read-only D-121 audit of exact upstream API features; no DB mutation."""
from __future__ import annotations
import argparse
from concurrent.futures import ThreadPoolExecutor
from datetime import datetime, timezone
import hashlib
import gzip
import json
from pathlib import Path
import urllib.request
from shapely import from_wkb, make_valid
from shapely.geometry import shape

ROOT = Path(__file__).resolve().parents[1]
API = 'https://seshat-db.com/api/core/cliopatria-shapefiles/'

def verify_bindings(audit, bundle):
    rows = audit['rows']
    if len(rows) != 38 or len({r['geometry_id'] for r in rows}) != 38:
        raise ValueError('source binding membership differs')
    for row in rows:
        record = row['source_record']
        stored = bundle['objects']['geometries'][row['geometry_id']]
        if str(record['id']) != stored['geometry_source_native_id']:
            raise ValueError('native identity differs')
        if hashlib.sha256(canonical(record)).hexdigest() != row['source_record_sha256']:
            raise ValueError('source record fingerprint differs')
        if hashlib.sha256(canonical(record['geom'])).hexdigest() != row['source_feature_sha256']:
            raise ValueError('source feature fingerprint differs')
        if [atlas_year(record['start_year']), atlas_year(record['end_year'])] != [stored['from_year'], stored['to_year']]:
            raise ValueError('source native temporal translation differs')
        if not make_valid(shape(record['geom'])).equals(make_valid(from_wkb(bytes.fromhex(stored['geom_ewkb_hex'])))):
            raise ValueError('upstream source geometry differs')
    return True

def canonical(value):
    return json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(',', ':')).encode('utf-8')

def atlas_year(native):
    return native + 1 if native < 0 else native

def inspect_record(item):
    gid, geometry = item
    native_id = geometry['geometry_source_native_id']
    url = API + native_id + '/'
    req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0', 'Accept': 'application/json'})
    with urllib.request.urlopen(req, timeout=45) as response:
        raw = response.read()
    record = json.loads(raw)
    if str(record['id']) != native_id:
        raise ValueError(f'{gid}: upstream returned the wrong native ID')
    stored = from_wkb(bytes.fromhex(geometry['geom_ewkb_hex']))
    upstream = shape(record['geom'])
    exact = upstream.equals_exact(stored, 0)
    repaired_equal = make_valid(upstream).equals(make_valid(stored))
    translated = [atlas_year(record['start_year']), atlas_year(record['end_year'])]
    interval_equal = translated == [geometry['from_year'], geometry['to_year']]
    return {
        'geometry_id': gid, 'source_native_id': native_id, 'upstream_url': url,
        'source_response_sha256': hashlib.sha256(raw).hexdigest(),
        'source_record_sha256': hashlib.sha256(canonical(record)).hexdigest(),
        'source_feature_sha256': hashlib.sha256(canonical(record['geom'])).hexdigest(),
        'source_native_from': record['start_year'], 'source_native_to': record['end_year'],
        'source_native_convention': 'signed historical years; BCE excludes year zero',
        'translation_rule': 'negative source year + 1; nonnegative source year unchanged',
        'translated_interval': translated, 'stored_interval': [geometry['from_year'], geometry['to_year']],
        'coordinates_exact': exact, 'make_valid_topology_equal': repaired_equal,
        'interval_equal': interval_equal, 'source_record': record,
        'status': 'PASS' if repaired_equal and interval_equal else 'HOLD',
    }

def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--output', type=Path, required=True)
    args = parser.parse_args()
    predecessor = ROOT / 'data/releases/v0.8.1/authority-state.json'
    bundle = json.loads(predecessor.read_text(encoding='utf-8'))
    selected = [(gid, g) for gid, g in bundle['objects']['geometries'].items()
                if str(g.get('geometry_source_native_id', '')).isdigit()
                and 'cliopatria' in bundle['objects']['source_versions'].get(
                    str(g.get('geometry_source_version_id')), {}).get('source_version', {}).get('url_or_identifier', '').lower()]
    if len(selected) != 38:
        raise ValueError(f'expected 38 exact predecessor Cliopatria records, got {len(selected)}')
    with ThreadPoolExecutor(max_workers=4) as pool:
        rows = list(pool.map(inspect_record, selected))
    result = {'audit_schema': 'atlas-successor-exact-api-feature-bindings-v1',
              'decision': 'D-121', 'checked_at': datetime.now(timezone.utc).isoformat(),
              'predecessor_sha256': hashlib.sha256(predecessor.read_bytes()).hexdigest(),
              'api_feature_count': len(rows), 'passed': sum(r['status'] == 'PASS' for r in rows),
              'remaining_non_api_geometries': sorted(set(bundle['objects']['geometries']) - {r['geometry_id'] for r in rows}),
              'rows': sorted(rows, key=lambda r: r['geometry_id'])}
    args.output.write_text(json.dumps(result, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
    print(json.dumps({'count': len(rows), 'passed': result['passed'],
                     'holds': [{k: r[k] for k in ('geometry_id', 'source_native_id', 'coordinates_exact',
                                'make_valid_topology_equal', 'stored_interval', 'translated_interval')}
                               for r in rows if r['status'] == 'HOLD']}))
    return 0 if result['passed'] == 38 else 1

if __name__ == '__main__':
    raise SystemExit(main())
