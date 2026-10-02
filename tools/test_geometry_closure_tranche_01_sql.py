#!/usr/bin/env python3
"""Disposable #370 connected-transport parity/rollback test; no commit path."""
from __future__ import annotations

import argparse
import copy
import json
import os
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

import psycopg
from tools import rehearse_geometry_closure_tranche_01 as rehearsal
from tools import export_geometry_closure_tranche_01_sql as exporter
from tools.test_geometry_closure_tranche_02_sql import execute_block, expect_rejection


def run(conn):
    original = rehearsal.counts(conn)
    controls = []
    try:
        review, plan, _ = exporter.load_inputs()
        resolved = rehearsal.verify_claims(conn)
        plan = copy.deepcopy(plan)
        for row in plan['production_cases']:
            row['production_claim_id'] = resolved[row['case_key']]['claim_id']
            row['production_spatial_entity_id'] = resolved[row['case_key']]['spatial_entity_id']
        dahomey = next(v for k, v in resolved.items() if '/dahomey/' in k)
        unresolved_id = conn.execute("select geometry_id::text from atlas.geometry where spatial_entity_id=%s and geom is null and accuracy_status='unresolved'",
                                     (dahomey['spatial_entity_id'],)).fetchone()[0]
        statement = exporter.render(review, plan, revision='DISPOSABLE_SQL_FIXTURE',
                                    authorized=True, unresolved_id=unresolved_id,
                                    expected_release_memberships=[])
        inert = exporter.render(review, plan, revision='DISPOSABLE_SQL_FIXTURE',
                                unresolved_id=unresolved_id,
                                expected_release_memberships=[])
        expect_rejection(conn, inert, '#370 explicit production authorization absent')
        controls.append('unauthorized_export_rejected')
        wrong_id = statement.replace(resolved[next(iter(resolved))]['claim_id'],
                                     '00000000-0000-0000-0000-000000000000')
        expect_rejection(conn, wrong_id, 'live identity/state drift')
        controls.append('wrong_claim_identity_rejected')
        wrong_unresolved = statement.replace(unresolved_id, '00000000-0000-0000-0000-000000000000')
        expect_rejection(conn, wrong_unresolved, 'Dahomey unresolved geometry drift')
        controls.append('wrong_unresolved_geometry_identity_rejected')
        wrong_delta = statement.replace("(before_counts->>'atlas.geometry')::bigint = 3",
                                        "(before_counts->>'atlas.geometry')::bigint = 999")
        if wrong_delta == statement:
            raise rehearsal.ClosureError('late delta failure did not modify SQL')
        expect_rejection(conn, wrong_delta, 'unexpected delta: atlas.geometry')
        controls.append('late_guard_failure_atomic_rollback')
        marker = 'after_counts := '
        mutation = f"UPDATE atlas.geometry SET notes=coalesce(notes,'') || ' altered' WHERE geometry_id='{unresolved_id}'::uuid;\n"
        changed_unresolved = statement.replace(marker, mutation + marker)
        expect_rejection(conn, changed_unresolved, 'Dahomey unresolved geometry changed')
        controls.append('same_count_unresolved_row_mutation_rejected_and_rolled_back')
        legal_mutation = "UPDATE atlas.legal_event SET notes=coalesce(notes,'') || ' altered';\n"
        expect_rejection(conn, statement.replace(marker, legal_mutation + marker),
                         'protected rows changed: atlas.legal_event')
        controls.append('same_count_legal_event_mutation_rejected_and_rolled_back')
        before = rehearsal.counts(conn)
        receipt = execute_block(conn, statement)
        after = rehearsal.counts(conn)
        rehearsal.assert_delta(before, after)
        rehearsal.verify_semantics(conn, resolved)
        second = rehearsal.apply_once(conn, review, resolved)
        if rehearsal.counts(conn) != after or any(v.get(k) for v in second.values()
          for k in ('geometry_inserted', 'claim_source_inserted', 'locus_link_inserted')):
            raise rehearsal.ClosureError('SQL rows fail exact reviewed Python no-op replay')
        controls.append('reviewed_python_replay_exact_noop')
        for key, value in second.items():
            for field in ('geometry_id', 'locus_spatial_entity_id'):
                if value.get(field) != receipt['first_pass'][key].get(field):
                    raise rehearsal.ClosureError(f'generated identity mismatch: {key}/{field}')
        if receipt['before_counts'] != before or receipt['after_counts'] != after or len(receipt['sources']) != 4:
            raise rehearsal.ClosureError('receipt counts/source identities differ')
        controls.append('generated_ids_independently_verified')
        expect_rejection(conn, statement, 'existing target geometry')
        controls.append('transport_retry_fail_closed')
    finally:
        conn.rollback()
    if rehearsal.counts(conn) != original:
        raise rehearsal.ClosureError('disposable rollback failed to restore original counts')
    conn.rollback()
    return {'issue': 370, 'mode': 'DISPOSABLE_SQL_TRANSPORT_ROLLBACK', 'status': 'PASS',
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
