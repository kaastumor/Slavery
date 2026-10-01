#!/usr/bin/env python3
"""Collect the reviewed D-124 pilot helpers into one inert-by-default SQL block."""
from __future__ import annotations
import argparse
import json
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))
from tools import rehearse_100_100_pilot_batch as pilot
from tools.export_geometry_closure_tranche_02_sql import InsertCollector, literal, require, snapshot_expression

class PilotCollector(InsertCollector):
    def __init__(self, reused=None):
        super().__init__()
        self.sources = dict(reused or {})

    def execute(self, query, params=()):
        compact = ' '.join(query.split())
        if compact == 'select content_sha256, claim_id::text from audit.research_case_ingest where case_key = %s':
            self.rows = []
            return self
        if compact == 'select sv.source_version_id from atlas.source_version sv where sv.url_or_identifier = %s':
            self.rows = [(self.sources[params[0]],)] if params[0] in self.sources else []
            return self
        result = super().execute(query, params)
        if compact.startswith('insert into atlas.source_version('):
            self.sources[params[5]] = str(self.fetchone()[0])
        return result

def inputs():
    manifest = pilot.load_manifest()
    return manifest, pilot.load_candidates(manifest)

def inventory(candidates):
    versions = {}
    for _, spec, _ in candidates:
        for evidence in spec['evidence']:
            versions[evidence['version']['url_or_identifier']] = evidence['version']
        geometry = spec.get('geometry') or {}
        if geometry.get('version'):
            versions[geometry['version']['url_or_identifier']] = geometry['version']
    return versions

def render(*, revision, authorized=False, reused=None):
    _, candidates = inputs()
    keys = [row['case_key'] for row, _, _ in candidates]
    names = [spec['spatial_entity']['canonical_name'] for _, spec, _ in candidates]
    collector = PilotCollector(reused)
    results = []
    for row, spec, kind in candidates:
        helper = pilot.insert_territorial_case if kind == 'territorial_practice' else pilot.insert_external_case
        claim_id, inserted = helper(collector, spec, source_path=row['path'], git_revision=revision)
        if not inserted:
            raise pilot.RehearsalError('collector did not select fresh insertion')
        results.append((row['case_key'], claim_id))
    tables = pilot.TRACKED_TABLES
    counts = 'jsonb_build_object(' + ','.join(f'{literal(t)},(select count(*) from {t})' for t in tables) + ')'
    declarations = ['before_counts jsonb;', 'after_counts jsonb;', 'receipt jsonb;']
    declarations += [f'{v} uuid;' for v in collector.variables.values()]
    protected = ('audit.release_manifest', 'audit.release_claim', 'audit.release_geometry', 'audit.release_channel', 'atlas.legal_event')
    declarations += [f'protected_{i} jsonb;' for i in range(len(protected))]
    claim_tables = ('atlas.claim', 'atlas.territorial_practice_claim', 'atlas.external_participation_claim', 'atlas.claim_source', 'audit.research_case_ingest')
    declarations += [f'old_claim_rows_{i} jsonb;' for i in range(len(claim_tables))]
    body = [require('true' if authorized else 'false', '#369 pilot explicit authorization absent'),
            'LOCK TABLE ' + ','.join(dict.fromkeys((*tables, *protected))) + ' IN SHARE ROW EXCLUSIVE MODE;',
            require(f'not exists(select 1 from audit.research_case_ingest where case_key=any({literal(keys)}::text[]))', 'pilot case-key collision'),
            require(f'not exists(select 1 from atlas.spatial_entity where canonical_name=any({literal(names)}::text[]))', 'pilot spatial identity collision')]
    for url in inventory(candidates):
        if url in (reused or {}):
            body.append(require(f"(select count(*)=1 and min(source_version_id::text)={literal(reused[url])} from atlas.source_version where url_or_identifier={literal(url)})", 'pilot source reuse drift'))
        else:
            body.append(require(f'not exists(select 1 from atlas.source_version where url_or_identifier={literal(url)})', 'pilot source collision'))
    for i, table in enumerate(protected):
        body.append(f'protected_{i} := {snapshot_expression(table)};')
    for i, table in enumerate(claim_tables):
        body.append(f'old_claim_rows_{i} := {snapshot_expression(table)};')
    body.append('before_counts := ' + counts + ';')
    body.extend(collector.statements)
    body.append('after_counts := ' + counts + ';')
    deltas = dict(pilot.STRICT_DELTAS)
    for table in ('atlas.source', 'atlas.source_version'):
        deltas[table] = sum(' '.join(s.split()).startswith(f'insert into {table}(') for s in collector.statements)
    for table, delta in deltas.items():
        body.append(require(f'(after_counts->>{literal(table)})::bigint - (before_counts->>{literal(table)})::bigint = {delta}', f'pilot delta drift: {table}'))
    for i, table in enumerate(protected):
        body.append(require(f'protected_{i} = {snapshot_expression(table)}', f'pilot protected rows changed: {table}'))
    claim_vars = ','.join(collector.variables[cid] for _, cid in results)
    for i, table in enumerate(claim_tables):
        filtered = f"(select coalesce(jsonb_agg(to_jsonb(t) order by to_jsonb(t)::text),'[]'::jsonb) from {table} t where claim_id<>all(ARRAY[{claim_vars}]::uuid[]))"
        body.append(require(f'old_claim_rows_{i} = {filtered}', f'pilot existing claims changed: {table}'))
    body.append(require(f"(select count(*)=5 from atlas.claim where claim_id=any(ARRAY[{claim_vars}]::uuid[]) and review_status='reviewed' and publication_status='unpublished')", 'pilot review/publication drift'))
    body.append(require(f'not exists(select 1 from atlas.territorial_practice_claim where claim_id=any(ARRAY[{claim_vars}]::uuid[]) and practice_level is not null)', 'pilot P-level assigned'))
    fields = ','.join(literal(key) + ',' + collector.variables[cid] for key, cid in results)
    body.append(f"receipt := jsonb_build_object('issue',369,'scope','exact_five_case_pilot','revision',{literal(revision)},'checked_at',clock_timestamp(),'before_counts',before_counts,'after_counts',after_counts,'claim_ids',jsonb_build_object({fields}));")
    body.append("PERFORM set_config('atlas.issue369_pilot_receipt',receipt::text,true);")
    return 'DO $atlas369$\nDECLARE\n' + '\n'.join(declarations) + "\nBEGIN\nSET LOCAL lock_timeout='10s';\nSET LOCAL statement_timeout='60s';\n" + '\n'.join(body) + "\nEND\n$atlas369$;\nSELECT current_setting('atlas.issue369_pilot_receipt')::jsonb AS receipt;\n"

def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--output', type=Path)
    args = parser.parse_args()
    if args.output:
        args.output.write_text(render(revision='INERT_EXPORT'), encoding='utf-8')
    _, candidates = inputs()
    print(json.dumps({'mode':'inert_export_only','keys':[r['case_key'] for r,_,_ in candidates],
                      'names':[s['spatial_entity']['canonical_name'] for _,s,_ in candidates],
                      'source_urls':list(inventory(candidates))}))
    return 0

if __name__ == '__main__':
    raise SystemExit(main())
