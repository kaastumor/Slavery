#!/usr/bin/env python3
"""Rollback-only replay of the 11 existing population packets in disposable CI DB.

Never a production admission command: requires the explicit disposable-test flag,
CI identity, and the local Compose database host/user/name. There is no commit path.
"""
from __future__ import annotations

import argparse
import copy
import json
import os
from pathlib import Path
import sys
from urllib.parse import urlparse

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
from tools.verify_population_packets import PREFLIGHT, PacketError, entries, verify_one

TABLES = ('atlas.claim', 'atlas.territorial_practice_claim', 'atlas.spatial_entity',
          'atlas.source', 'atlas.source_version', 'atlas.claim_source',
          'atlas.geometry', 'audit.research_case_ingest', 'audit.release_channel',
          'audit.release_claim')


def check_disposable_dsn(dsn: str, flag: bool, ci: str | None) -> None:
    parsed = urlparse(dsn)
    if not flag or ci != 'true':
        raise PacketError('requires --disposable-test-db and CI=true')
    if parsed.scheme not in ('postgres', 'postgresql') or parsed.hostname != 'db':
        raise PacketError('only the local Compose host db is allowed')
    if parsed.username != 'atlas' or parsed.path != '/slavery_atlas':
        raise PacketError('unexpected disposable DB identity')
    if parsed.query or parsed.fragment:
        raise PacketError('DSN overrides are not allowed')


def counts(conn):
    with conn.cursor() as cur:
        return {table: cur.execute(f'SELECT count(*) FROM {table}').fetchone()[0]
                for table in TABLES}


def assert_persisted(conn, claim_id, spec):
    claim = spec['claim']
    expected = tuple(claim.get(k) for k in (
        'from_year', 'to_year', 'date_text_original', 'temporal_precision',
        'temporal_certainty', 'spatial_precision', 'summary', 'confidence', 'notes'))
    with conn.cursor() as cur:
        actual = cur.execute('''SELECT from_year, to_year, date_text_original,
          temporal_precision, temporal_certainty, spatial_precision, summary,
          confidence, notes FROM atlas.claim WHERE claim_id=%s''', (claim_id,)).fetchone()
        if actual != expected:
            raise PacketError('claim fields failed lossless import roundtrip')
        status = cur.execute('''SELECT c.review_status::text, c.publication_status::text,
          t.practice_level::text, s.canonical_name
          FROM atlas.claim c JOIN atlas.territorial_practice_claim t USING(claim_id)
          JOIN atlas.spatial_entity s USING(spatial_entity_id) WHERE c.claim_id=%s''',
          (claim_id,)).fetchone()
        if status != ('reviewed', 'unpublished', None, spec['spatial_entity']['canonical_name']):
            raise PacketError('review/publication/P-level/identity roundtrip failed')
        source_rows = cur.execute('''SELECT sv.url_or_identifier, cs.evidence_role,
          cs.independence_group, cs.directness, cs.direction::text, cs.locator, cs.notes
          FROM atlas.claim_source cs JOIN atlas.source_version sv USING(source_version_id)
          WHERE cs.claim_id=%s''', (claim_id,)).fetchall()
        wanted = [(e['version']['url_or_identifier'], e.get('evidence_role'),
                   e.get('independence_group'), e.get('directness'), e.get('direction', 'supports'),
                   e.get('locator'), e.get('notes')) for e in spec['evidence']]
        sorter = lambda r: json.dumps(r, ensure_ascii=False)
        if sorted(source_rows, key=sorter) != sorted(wanted, key=sorter):
            raise PacketError('evidence links failed lossless import roundtrip')


def run(conn, root: Path) -> dict:
    from tools.add_research_case import insert_case, validate_case_spec
    preflight = json.loads((root / PREFLIGHT).read_text(encoding='utf-8'))
    batch = []
    for entry in entries(preflight):
        _, spec = verify_one(entry, (root / entry['path']).read_bytes())
        validate_case_spec(spec, require_case_key=True)
        batch.append((entry, spec))
    before = counts(conn)
    inserted, replayed, changed_rejected = [], [], False
    after_import = None
    try:
        with conn.cursor() as cur:
            keys = [s['case_key'] for _, s in batch]
            prior = cur.execute('SELECT count(*) FROM audit.research_case_ingest WHERE case_key=ANY(%s)',
                                (keys,)).fetchone()[0]
            if prior:
                raise PacketError('test requires a clean disposable fixture for these case keys')
        for entry, spec in batch:
            claim_id, is_new = insert_case(conn, spec, source_path=entry['path'], git_revision=entry['revision'])
            if not is_new:
                raise PacketError('unexpected no-op on first disposable insertion')
            assert_persisted(conn, claim_id, spec)
            inserted.append(claim_id)
        after_import = counts(conn)
        for table in ('atlas.claim', 'atlas.territorial_practice_claim', 'audit.research_case_ingest'):
            if after_import[table] - before[table] != len(batch):
                raise PacketError(f'unexpected first-pass delta: {table}')
        for index, (entry, spec) in enumerate(batch):
            claim_id, is_new = insert_case(conn, spec, source_path=entry['path'], git_revision=entry['revision'])
            if is_new or claim_id != inserted[index]:
                raise PacketError('replay created a duplicate or returned a different ID')
            replayed.append(claim_id)
        if counts(conn) != after_import:
            raise PacketError('replay changed database counts')
        changed = copy.deepcopy(batch[0][1])
        changed['claim']['summary'] += ' TEST_ONLY mutation to verify rejection.'
        try:
            insert_case(conn, changed)
        except RuntimeError as exc:
            if 'different content' not in str(exc):
                raise
            changed_rejected = True
        if not changed_rejected or counts(conn) != after_import:
            raise PacketError('changed-content same-key replay was not fail-closed')
        if after_import['audit.release_channel'] != before['audit.release_channel']:
            raise PacketError('unexpected serving channel count change')
        if after_import['audit.release_claim'] != before['audit.release_claim']:
            raise PacketError('unexpected release membership count change')
    finally:
        conn.rollback()
    after_rollback = counts(conn)
    conn.rollback()
    if before != after_rollback:
        raise PacketError('rollback did not restore database table counts')
    return {
        'record_kind': 'population_disposable_replay_result', 'version': 1,
        'issue': 360, 'scope': 'DISPOSABLE_CI_DATABASE_NOT_PRODUCTION',
        'verified_input_packets': len(batch), 'first_pass_inserted': len(inserted),
        'second_pass_noops': len(replayed), 'changed_content_rejected': changed_rejected,
        'claim_and_evidence_field_roundtrip': True, 'rollback_restored_counts': True,
        'temporary_table_deltas': {k: after_import[k] - before[k] for k in TABLES},
        'production_writes': 0, 'release_ready': False,
        'limits': ['Tests validate import mechanics, not historical acceptance.',
                   'Extended post-M1 semantic annotations and mapped-locus readiness remain separately gated.',
                   'Existing production claims must be reused, not reinserted.'],
    }


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--dsn', default=os.environ.get('DATABASE_URL', ''))
    parser.add_argument('--disposable-test-db', action='store_true')
    args = parser.parse_args()
    check_disposable_dsn(args.dsn, args.disposable_test_db, os.environ.get('CI'))
    import psycopg
    with psycopg.connect(args.dsn, autocommit=False) as conn:
        result = run(conn, ROOT)
    print('POPULATION_REPLAY_BEGIN')
    print(json.dumps(result, indent=2, sort_keys=True))
    print('POPULATION_REPLAY_END')
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
