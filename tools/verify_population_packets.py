#!/usr/bin/env python3
"""Verify #360's existing packets, without connecting to or writing a database.

The ingestion ledger hashes parsed canonical JSON, NOT the formatted file bytes.
Keep the two fingerprints separate. A verified packet is not release approval.
"""
from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path, PurePosixPath
import re
import subprocess
from typing import Any, Callable

ROOT = Path(__file__).resolve().parents[1]
PREFLIGHT = Path('data/research/recovery/production_batch_2026_09_29/preflight.json')
SHA = re.compile(r'^[0-9a-f]{40}$')
SHA256 = re.compile(r'^[0-9a-f]{64}$')


class PacketError(ValueError):
    """Missing, mismatched or ambiguous packet input."""


def canonical_hash(value: dict[str, Any]) -> str:
    encoded = json.dumps(value, ensure_ascii=False, sort_keys=True,
                         separators=(',', ':')).encode('utf-8')
    return hashlib.sha256(encoded).hexdigest()


def unique_object(pairs):
    result = {}
    for key, value in pairs:
        if key in result:
            raise PacketError(f'duplicate JSON key: {key}')
        result[key] = value
    return result


def parse_packet(raw: bytes) -> dict[str, Any]:
    value = json.loads(raw.decode('utf-8'), object_pairs_hook=unique_object)
    if not isinstance(value, dict):
        raise PacketError('packet must be a JSON object')
    return value


def entries(preflight: dict[str, Any]) -> list[dict[str, Any]]:
    columns = preflight['existing_claim_columns']
    rows = []
    seen_ids = set()
    seen_paths = set()
    for values in preflight['existing_claims']:
        if len(values) != len(columns):
            raise PacketError('preflight column count mismatch')
        row = dict(zip(columns, values))
        rule = preflight['packet_path_rule']
        override = rule.get(row['name'], {})
        row['path'] = override.get('prefix', rule['default_prefix']) + row['packet_filename']
        row['revision'] = override.get('recorded_git_revision', rule['default_recorded_git_revision'])
        path = PurePosixPath(row['path'])
        if path.is_absolute() or '..' in path.parts or not str(path).startswith('data/research/'):
            raise PacketError('unsafe packet path')
        if not SHA.fullmatch(row['revision']):
            raise PacketError('packet revision must be a full commit SHA')
        if not SHA256.fullmatch(row['recorded_ingest_content_sha256']):
            raise PacketError('invalid recorded content SHA-256')
        if row['claim_id'] in seen_ids or row['path'] in seen_paths:
            raise PacketError('duplicate claim ID or packet path in preflight')
        seen_ids.add(row['claim_id'])
        seen_paths.add(row['path'])
        rows.append(row)
    if len(rows) != preflight['existing_claims_contract']['observed_count']:
        raise PacketError('preflight observed count mismatch')
    return rows


def git_read(root: Path, revision: str, path: str) -> bytes:
    result = subprocess.run(['git', 'show', f'{revision}:{path}'], cwd=root,
                            capture_output=True, timeout=30, check=False)
    if result.returncode:
        raise PacketError(f'exact committed packet unavailable: {revision}:{path}')
    return result.stdout


def verify_one(entry: dict[str, Any], raw: bytes) -> tuple[dict[str, Any], dict[str, Any]]:
    spec = parse_packet(raw)
    actual = canonical_hash(spec)
    if actual != entry['recorded_ingest_content_sha256']:
        raise PacketError(f"{entry['name']}: canonical ingestion-content hash mismatch")
    claim = spec['claim']
    if [claim.get('from_year'), claim.get('to_year')] != [entry['from_year'], entry['to_year']]:
        raise PacketError(f"{entry['name']}: temporal scope differs from observed ledger")
    if spec['spatial_entity']['canonical_name'] != entry['name']:
        raise PacketError(f"{entry['name']}: target identity differs")
    if claim['territorial_practice'].get('practice_level') is not None:
        raise PacketError('post-M1 input has a P-level')
    if claim.get('review_status') != 'reviewed' or claim.get('publication_status') != 'unpublished':
        raise PacketError('unexpected input review/publication state')
    if not spec.get('case_key') or not spec.get('evidence'):
        raise PacketError('missing case key or evidence')
    raw_hash = hashlib.sha256(raw).hexdigest()
    row = {
        'name': entry['name'], 'existing_claim_id': entry['claim_id'],
        'case_key': spec['case_key'], 'path': entry['path'], 'revision': entry['revision'],
        'raw_file_sha256': raw_hash, 'raw_file_bytes': len(raw),
        'git_blob_sha1': hashlib.sha1(f'blob {len(raw)}\0'.encode() + raw).hexdigest(),
        'canonical_ingest_content_sha256': actual,
        'recorded_ingest_content_sha256': entry['recorded_ingest_content_sha256'],
        'canonical_hash_match': True,
        'raw_hash_equals_ingest_hash': raw_hash == actual,
        'claim_interval': [claim.get('from_year'), claim.get('to_year')],
        'evidence_source_count': len(spec['evidence']),
        'packet_blank_locator_count': sum(not str(e.get('locator') or '').strip() for e in spec['evidence']),
        'observed_db_blank_locator_count': entry['missing_locator_count'],
        'sources': [{'url': e['version']['url_or_identifier'], 'locator': e.get('locator'),
                     'direction': e.get('direction', 'supports'),
                     'independence_group': e.get('independence_group')} for e in spec['evidence']],
        'production_action': 'REUSE_EXISTING_CLAIM_DO_NOT_REINSERT',
        'release_ready': False,
    }
    return row, spec


def audit(root: Path, preflight: dict[str, Any],
          reader: Callable[[Path, str, str], bytes] = git_read) -> dict[str, Any]:
    rows, failures = [], []
    for entry in entries(preflight):
        try:
            row, _ = verify_one(entry, reader(root, entry['revision'], entry['path']))
            current = root / entry['path']
            row['current_checkout_matches_recorded_content'] = (
                canonical_hash(parse_packet(current.read_bytes())) == row['canonical_ingest_content_sha256']
                if current.is_file() else None
            )
            rows.append(row)
        except (PacketError, OSError, ValueError, KeyError) as exc:
            failures.append({'name': entry['name'], 'error': str(exc)})
    return {
        'record_kind': 'population_packet_integrity_verification', 'version': 1,
        'issue': 360, 'input_preflight_repository_commit': preflight['input_repository_commit'],
        'hash_contract': 'tools/add_research_case.py: json.dumps(ensure_ascii=False, sort_keys=True, separators=(comma,colon)); UTF-8; SHA-256',
        'expected_packet_count': len(preflight['existing_claims']),
        'verified_packet_count': len(rows), 'failures': failures, 'packets': rows,
        'production_claim_insert_count': 0, 'database_contacted': False,
        'release_ready': False,
        'remaining_gates': ['Live field-by-field reconciliation', 'Claim-specific locator and source review',
                            'Defensible temporal applicability and geometry role',
                            'Governed successor dependency closure and publication'],
    }


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--root', type=Path, default=ROOT)
    parser.add_argument('--preflight', type=Path, default=PREFLIGHT)
    parser.add_argument('--output', type=Path)
    args = parser.parse_args()
    report = audit(args.root, json.loads((args.root / args.preflight).read_text(encoding='utf-8')))
    text = json.dumps(report, ensure_ascii=False, indent=2, sort_keys=True) + '\n'
    if args.output:
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(text, encoding='utf-8')
    print(text, end='')
    return int(bool(report['failures']))


if __name__ == '__main__':
    raise SystemExit(main())
