#!/usr/bin/env python3
"""Verify pilot connected SQL in disposable PostGIS; always roll back."""
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
from tools import rehearse_100_100_pilot_batch as pilot
from tools import export_100_100_pilot_sql as exporter
from tools.test_geometry_closure_tranche_02_sql import execute_block

def rejection(conn, statement, message):
    before = pilot.counts(conn)
    try:
        with conn.transaction():
            execute_block(conn, statement)
    except psycopg.Error as exc:
        if message not in str(exc):
            raise
    else:
        raise pilot.RehearsalError('negative control did not reject: ' + message)
    if pilot.counts(conn) != before:
        raise pilot.RehearsalError('negative control did not roll back')

def run(conn):
    original = pilot.counts(conn)
    _, candidates = exporter.inputs()
    urls = list(exporter.inventory(candidates))
    reused = {url: str(sv) for url, sv in conn.execute(
        'select url_or_identifier,source_version_id from atlas.source_version where url_or_identifier=any(%s)', (urls,)).fetchall()}
    controls = []
    try:
        statement = exporter.render(revision='DISPOSABLE_PILOT_SQL', authorized=True, reused=reused)
        rejection(conn, exporter.render(revision='DISPOSABLE_PILOT_SQL', reused=reused), '#369 pilot explicit authorization absent')
        controls.append('unauthorized_rejected')
        bad = statement.replace("(before_counts->>'atlas.claim')::bigint = 5", "(before_counts->>'atlas.claim')::bigint = 999")
        if bad == statement:
            raise pilot.RehearsalError('late-failure injection did not change SQL')
        rejection(conn, bad, 'pilot delta drift: atlas.claim')
        controls.append('late_failure_atomic_rollback')
        bad = statement.replace('after_counts := ', "UPDATE atlas.claim SET notes=coalesce(notes,'') || ' altered' WHERE claim_id not in (SELECT claim_id FROM audit.research_case_ingest WHERE case_key LIKE 'atlas-100x100/%');\nafter_counts := ")
        rejection(conn, bad, 'pilot existing claims changed: atlas.claim')
        controls.append('same_count_existing_claim_mutation_rejected')
        receipt = execute_block(conn, statement)
        pilot.assert_delta(original, pilot.counts(conn))
        pilot.semantic_checks(conn, [r['case_key'] for r, _, _ in candidates])
        after = pilot.counts(conn)
        for row, spec, kind in candidates:
            helper = pilot.insert_territorial_case if kind == 'territorial_practice' else pilot.insert_external_case
            claim_id, inserted = helper(conn, spec, source_path=row['path'], git_revision='DISPOSABLE_PILOT_SQL')
            if inserted or str(claim_id) != receipt['claim_ids'][row['case_key']]:
                raise pilot.RehearsalError('Python replay / generated identity drift')
        if after != pilot.counts(conn):
            raise pilot.RehearsalError('replay changed counts')
        controls.append('reviewed_python_exact_noop_and_receipt_ids')
        rejection(conn, statement, 'pilot case-key collision')
        controls.append('retry_rejected')
    finally:
        conn.rollback()
    if original != pilot.counts(conn):
        raise pilot.RehearsalError('outer rollback changed counts')
    conn.rollback()
    return {'status': 'PASS', 'controls': controls, 'rollback_restored_counts': True}

def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--disposable-test-db', action='store_true')
    args = parser.parse_args()
    if not args.disposable_test_db or os.environ.get('CI') != 'true':
        raise SystemExit('requires disposable test DB and CI=true')
    dsn = os.environ.get('DATABASE_URL', '')
    pilot.require_disposable_dsn(dsn)
    with psycopg.connect(dsn, autocommit=False) as conn:
        print(json.dumps(run(conn), sort_keys=True))
    return 0

if __name__ == '__main__':
    raise SystemExit(main())
