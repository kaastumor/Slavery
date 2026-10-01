#!/usr/bin/env python3
"""Test #374 SQL transport against disposable PostGIS; always roll back."""
from __future__ import annotations

import argparse
import json
import os
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

import psycopg
from tools import rehearse_geometry_closure_tranche_02 as rehearsal
from tools import export_geometry_closure_tranche_02_sql as exporter
from tools.add_research_case import insert_case, load_spec
from tools.rehearse_geometry_closure_tranche_01 import ClosureError, counts


def execute_block(conn, statement):
    # Use the exact DO block sent to the connector. Read the final SELECT separately
    # because psycopg's extended protocol cannot prepare multiple commands.
    block, select = statement.rsplit("SELECT current_setting", 1)
    conn.execute(block)
    return conn.execute("SELECT current_setting" + select).fetchone()[0]


def expect_rejection(conn, statement, message):
    before = counts(conn)
    rejected = False
    try:
        with conn.transaction():
            execute_block(conn, statement)
    except psycopg.Error as exc:
        if message not in str(exc):
            raise
        rejected = True
    if not rejected or counts(conn) != before:
        raise ClosureError(f"negative control failed: {message}")


def run(conn):
    original = counts(conn)
    controls = []
    try:
        review = rehearsal.load_review()
        resolved = rehearsal.insert_prerequisites(conn)
        brazil = ROOT / 'data/research/recovery/overnight_2026_09_27/08_brazil_debt_bondage_v2.json'
        # Locate by case key rather than relying on the packet's ordinal filename.
        matches = [path for path in brazil.parent.glob('*.json')
                   if json.loads(path.read_text(encoding='utf-8')).get('case_key') == rehearsal.BRAZIL_HOLD]
        if len(matches) != 1:
            raise ClosureError('Brazil fixture packet is not unique')
        insert_case(conn, load_spec(matches[0], require_case_key=True),
                    source_path=str(matches[0].relative_to(ROOT)), git_revision='DISPOSABLE_SQL_FIXTURE')
        expected = {key: {'claim_id': value['claim_id'],
                         'spatial_entity_id': value['target_spatial_entity_id'],
                         'canonical_name': value['target_canonical_name']}
                    for key, value in resolved.items()}
        hrw_id = conn.execute('select source_version_id::text from atlas.source_version where url_or_identifier=%s',
                             (exporter.HRW_URL,)).fetchone()[0]
        statement = exporter.render(review, authorized=True, revision='DISPOSABLE_SQL_FIXTURE',
                                    expected=expected, hrw_id=hrw_id)
        inert = exporter.render(review, revision='DISPOSABLE_SQL_FIXTURE', expected=expected, hrw_id=hrw_id)
        expect_rejection(conn, inert, '#374 explicit production authorization absent')
        controls.append('unauthorized_export_rejected')
        wrong_identity = statement.replace(expected[rehearsal.ACCEPTED[0]]['claim_id'],
                                           '00000000-0000-0000-0000-000000000000')
        expect_rejection(conn, wrong_identity, 'live identity/state drift')
        controls.append('wrong_claim_identity_rejected')
        wrong_reuse = statement.replace(hrw_id, '00000000-0000-0000-0000-000000000000')
        expect_rejection(conn, wrong_reuse, 'India HRW reuse drift')
        controls.append('wrong_source_reuse_rejected')
        # This failure occurs after all INSERTs: the DO block must unwind every row.
        wrong_delta = statement.replace("(before_counts->>'atlas.spatial_entity')::bigint = 4",
                                        "(before_counts->>'atlas.spatial_entity')::bigint = 999")
        if wrong_delta == statement:
            raise ClosureError('late failure control did not modify the SQL')
        expect_rejection(conn, wrong_delta, 'unexpected delta: atlas.spatial_entity')
        controls.append('late_guard_failure_atomic_rollback')
        before = counts(conn)
        receipt = execute_block(conn, statement)
        after = counts(conn)
        rehearsal.assert_delta(before, after)
        rehearsal.verify_semantics(conn, review, resolved)
        second = rehearsal.apply_once(conn, review, resolved)
        if counts(conn) != after or not rehearsal.replay_is_noop(second):
            raise ClosureError('SQL rows fail the reviewed Python exact no-op replay')
        controls.append('reviewed_python_replay_exact_noop')
        # A transport retry must abort rather than make another set of rows.
        expect_rejection(conn, statement, 'locus identity collision')
        controls.append('transport_retry_fail_closed')
        if receipt['before_counts'] != before or receipt['after_counts'] != after:
            raise ClosureError('returned SQL receipt does not match independent counts')
        if set(receipt['first_pass']) != set(rehearsal.ACCEPTED):
            raise ClosureError('receipt membership drift')
        for key, result in receipt['first_pass'].items():
            for field in ('claim_id', 'locus_spatial_entity_id', 'geometry_id', 'geometry_source_version_id',
                          'context_source_version_id'):
                if result[field] != second[key][field]:
                    raise ClosureError(f'receipt/replay identity drift: {key}/{field}')
        controls.append('generated_ids_independently_verified')
    finally:
        conn.rollback()
    if counts(conn) != original:
        raise ClosureError('disposable rollback failed to restore counts')
    conn.rollback()
    return {'issue': 374, 'mode': 'DISPOSABLE_SQL_TRANSPORT_ROLLBACK', 'status': 'PASS',
            'controls': controls, 'rollback_restored_counts': True}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--disposable-test-db', action='store_true')
    args = parser.parse_args()
    if not args.disposable_test_db or os.environ.get('CI') != 'true':
        raise SystemExit('SQL transport rehearsal requires --disposable-test-db and CI=true')
    dsn = os.environ.get('DATABASE_URL', '')
    rehearsal.require_disposable_dsn(dsn)
    with psycopg.connect(dsn, autocommit=False) as conn:
        print(json.dumps(run(conn), indent=2, sort_keys=True))
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
