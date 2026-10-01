#!/usr/bin/env python3
"""Export #370 for connected SQL; default is inert and never executes a query."""
from __future__ import annotations

import argparse
import json
from pathlib import Path
import subprocess
import sys

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from tools import apply_geometry_closure_tranche_01 as production
from tools import rehearse_geometry_closure_tranche_01 as rehearsal
from tools.export_geometry_closure_tranche_02_sql import (
    InsertCollector, PROTECTED, count_expression, literal, require, snapshot_expression,
)

PINNED_INPUTS = {
    rehearsal.REVIEW: '2a63035c0ed670a69194a00e03dd3a45feeff3e8',
    production.PLAN: '3db5c88ae0ccd6adfa25e01cce36803071ae91af',
    production.RECEIPT: '62cde2de0e6d334b6b9d4855a18e0e90e613e27e',
}
UNRESOLVED_ID = 'bdab64f1-cc36-4771-8224-00b199d16c15'


class ClosureCollector(InsertCollector):
    def execute(self, query, params=()):
        compact = ' '.join(query.split())
        if compact == ('select evidence_role, direction::text, locator, claim_fitness '
                       'from atlas.claim_source where claim_id=%s and source_version_id=%s and evidence_role=%s'):
            self.rows = []
            return self
        return super().execute(query, params)


def load_inputs():
    for path, expected in PINNED_INPUTS.items():
        actual = subprocess.check_output(['git', 'hash-object', str(path.relative_to(ROOT))],
                                         cwd=ROOT, text=True).strip()
        if actual != expected:
            raise rehearsal.ClosureError(f'pinned #370 input drift: {path.name}')
    return rehearsal.load_review(), production.load_plan(), production.load_rehearsal_receipt()


def render(review, plan, *, revision, authorized=False, unresolved_id=UNRESOLVED_ID):
    resolved = {r['case_key']: {'claim_id': r['production_claim_id'],
                               'spatial_entity_id': r['production_spatial_entity_id']}
                for r in plan['production_cases']}
    if set(resolved) != set(rehearsal.EXPECTED):
        raise rehearsal.ClosureError('production membership drift')
    collector = ClosureCollector()
    first = rehearsal.apply_once(collector, review, resolved)
    protected = (*PROTECTED, 'atlas.legal_event')
    declarations = ['before_counts jsonb;', 'after_counts jsonb;', 'original_unresolved jsonb;', 'receipt jsonb;']
    declarations += [f'{name} uuid;' for name in collector.variables.values()]
    declarations += [f'protected_{i} jsonb;' for i in range(len(protected))]
    body = [require('true' if authorized else 'false', '#370 explicit production authorization absent')]
    body += [f"LOCK TABLE {','.join(dict.fromkeys((*rehearsal.TRACKED, *protected)))} IN SHARE ROW EXCLUSIVE MODE;"]
    for key, identity in resolved.items():
        expected = rehearsal.EXPECTED[key]
        body.append(require(f"""(select count(*)=1 from audit.research_case_ingest r
          join atlas.claim c using(claim_id)
          left join atlas.territorial_practice_claim t using(claim_id)
          left join atlas.legal_event le using(claim_id)
          join atlas.spatial_entity se on se.spatial_entity_id=coalesce(t.spatial_entity_id,le.jurisdiction_spatial_entity_id)
          where r.case_key={literal(key)} and c.claim_id={literal(identity['claim_id'])}::uuid
          and se.spatial_entity_id={literal(identity['spatial_entity_id'])}::uuid
          and se.canonical_name={literal(expected['canonical_name'])}
          and c.claim_kind_code={literal(expected['claim_kind'])}
          and c.review_status::text='reviewed' and c.publication_status::text='unpublished'
          and t.practice_level is null)""", f'live identity/state drift: {key}'))
        if expected['canonical_name'] != 'Dahomey':
            body.append(require(f"not exists(select 1 from atlas.geometry where spatial_entity_id={literal(identity['spatial_entity_id'])}::uuid)", 'existing target geometry'))
    dahomey = next(v for k, v in resolved.items() if '/dahomey/' in k)
    claim_ids = literal([r['claim_id'] for r in resolved.values()])
    urls = literal(list(production.CLOSURE_SOURCE_URLS))
    body += [require("not exists(select 1 from atlas.spatial_entity where canonical_name='Jakin (Godomey)')", 'Jakin identity collision'),
             require(f'not exists(select 1 from atlas.source_version where url_or_identifier=any({urls}::text[]))', 'new source URL collision'),
             require(f'not exists(select 1 from atlas.claim_evidence_locus where claim_id=any({claim_ids}::uuid[]))', 'existing locus links'),
             require(f'not exists(select 1 from audit.release_claim where claim_id=any({claim_ids}::uuid[]))', 'unexpected release membership'),
             require(f"""(select count(*)=1 from atlas.geometry where spatial_entity_id={literal(dahomey['spatial_entity_id'])}::uuid)
               and exists(select 1 from atlas.geometry where geometry_id={literal(unresolved_id)}::uuid
                 and spatial_entity_id={literal(dahomey['spatial_entity_id'])}::uuid
                 and geom is null and accuracy_status::text='unresolved' and review_status::text='reviewed')""", 'Dahomey unresolved geometry drift')]
    original_geometry = f"(select to_jsonb(g) from atlas.geometry g where geometry_id={literal(unresolved_id)}::uuid)"
    body.append(f'original_unresolved := {original_geometry};')
    for i, table in enumerate(protected):
        body.append(f'protected_{i} := {snapshot_expression(table)};')
    body.append(f'before_counts := {count_expression()};')
    body.extend(collector.statements)
    body.append(f'after_counts := {count_expression()};')
    for table, delta in rehearsal.STRICT_DELTA.items():
        body.append(require(f'(after_counts->>{literal(table)})::bigint - (before_counts->>{literal(table)})::bigint = {delta}', f'unexpected delta: {table}'))
    for i, table in enumerate(protected):
        body.append(require(f'protected_{i} = {snapshot_expression(table)}', f'protected rows changed: {table}'))
    body.append(require(f'original_unresolved = {original_geometry}', 'Dahomey unresolved geometry changed'))
    result_sql = []
    for row in review['candidates']:
        result = first[row['case_key']]
        geometry_id = collector.variables[result['geometry_id']]
        spatial_id = collector.variables.get(result.get('locus_spatial_entity_id'),
                                               literal(resolved[row['case_key']]['spatial_entity_id']) + '::uuid')
        geom = row['geometry']
        body.append(require(f"""(select count(*)=1 from atlas.geometry where geometry_id={geometry_id}
          and spatial_entity_id={spatial_id} and geometry_source_native_id={literal(geom['source_native_id'])}
          and accuracy_status::text='modern_proxy' and review_status::text='reviewed'
          and from_year={geom['from_year']} and to_year={geom['to_year']}
          and ST_SRID(geom)=4326 and GeometryType(geom)='POINT' and ST_IsValid(geom)
          and ST_Equals(geom,ST_SetSRID(ST_GeomFromGeoJSON({literal(json.dumps(geom['geojson']))}),4326)))""", 'navigation point semantics drift'))
        if row.get('locus_link'):
            body.append(require(f"""(select count(*)=1 from atlas.claim_evidence_locus
              where claim_id={literal(resolved[row['case_key']]['claim_id'])}::uuid
              and spatial_entity_id={spatial_id} and role_text={literal(row['locus_link']['role_text'])}
              and notes={literal(row['locus_link']['notes'])})""", 'transaction locus drift'))
        fields = []
        for name, value in result.items():
            fields += [literal(name), collector.variables.get(str(value), literal(value))]
        fields += ["'claim_id'", literal(resolved[row['case_key']]['claim_id']),
                   "'mapped_spatial_entity_id'", spatial_id]
        result_sql += [literal(row['case_key']), 'jsonb_build_object(' + ','.join(fields) + ')']
    body.append(f"""receipt := jsonb_build_object('issue',370,'git_revision',{literal(revision)},
      'transport','connected_sql','checked_at',clock_timestamp(),'before_counts',before_counts,
      'after_counts',after_counts,'first_pass',jsonb_build_object({','.join(result_sql)}),
      'sources',(select jsonb_agg(jsonb_build_object('source_id',source_id,'source_version_id',source_version_id,
        'url_or_identifier',url_or_identifier) order by url_or_identifier) from atlas.source_version
        where url_or_identifier=any({urls}::text[])),
      'preserved_unresolved_geometry_id',{literal(unresolved_id)});""")
    body.append("PERFORM set_config('atlas.issue370_receipt',receipt::text,true);")
    return '-- #370 only; explicit sponsor authority required.\nDO $atlas370$\nDECLARE\n' + \
        '\n'.join(declarations) + "\nBEGIN\nSET LOCAL lock_timeout = '10s';\nSET LOCAL statement_timeout = '60s';\n" + \
        '\n'.join(body) + "\nEND\n$atlas370$;\nSELECT current_setting('atlas.issue370_receipt')::jsonb AS receipt;\n"


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--output', type=Path)
    parser.add_argument('--production-write-authorized')
    parser.add_argument('--expected-main-sha')
    args = parser.parse_args()
    review, plan, _ = load_inputs()
    revision = production.git_head()
    authorized = args.production_write_authorized is not None
    if authorized:
        production.require_authority(args)
    if args.output:
        args.output.write_text(render(review, plan, revision=revision, authorized=authorized), encoding='utf-8')
    print(json.dumps({'issue': 370, 'mode': 'export_only', 'production_authorized': authorized,
                      'database_connected': False, 'git_revision': revision}))
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
