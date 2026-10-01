#!/usr/bin/env python3
"""Export the bounded #374 transaction for the connected SQL executor.

No connection or execution occurs here. Default exports fail before any insert.
Insertion statements come from the reviewed Python helpers, not a second importer.
"""
from __future__ import annotations

import argparse
import json
from pathlib import Path
import sys
from uuid import NAMESPACE_URL, uuid5

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from psycopg import sql
from tools import apply_geometry_closure_tranche_02 as production
from tools import rehearse_geometry_closure_tranche_02 as rehearsal
from tools.rehearse_geometry_closure_tranche_01 import ClosureError

HRW_ID = "43eaef18-4b5e-489c-84a5-5c035d433cfc"
HRW_URL = "https://www.hrw.org/report/2003/01/22/small-change/bonded-child-labor-indias-silk-industry"
PROTECTED = ("atlas.claim", "atlas.territorial_practice_claim",
             "audit.research_case_ingest", "audit.release_claim", "audit.release_channel")


def literal(value):
    return sql.Literal(value).as_string(None)


def require(condition: str, message: str) -> str:
    return f"IF NOT ({condition}) THEN RAISE EXCEPTION {literal(message)}; END IF;"


class InsertCollector:
    """Exercise the helpers' fresh-insert branch and collect its parameterized SQL.

    SELECTs are permitted only for the exact helper lookups. Corresponding absence
    guards are emitted under table locks before the collected INSERTs can run.
    Symbolic UUIDs exist only during generation and never enter exported SQL.
    """
    def __init__(self):
        self.variables = {}
        self.statements = []
        self.rows = []

    def __enter__(self):
        return self

    def __exit__(self, *args):
        return False

    def cursor(self):
        return self

    def execute(self, query, params=()):
        compact = " ".join(query.split())
        self.rows = []
        if compact.startswith("select "):
            allowed = (
                "select spatial_entity_id::text,entity_type_code from atlas.spatial_entity where canonical_name=%s",
                "select spatial_entity_id, entity_type_code from atlas.spatial_entity where canonical_name = %s",
                "select sv.source_version_id from atlas.source_version sv where sv.url_or_identifier = %s",
            )
            if compact in allowed:
                if params == (HRW_URL,):
                    self.rows = [(HRW_ID,)]
                return self
            if compact.startswith("select geometry_id::text, from_year, to_year, accuracy_status::text,"):
                return self
            if compact.startswith("select role_text, notes from atlas.claim_evidence_locus "):
                return self
            if compact.startswith("select evidence_role,independence_group,directness,direction::text,"):
                return self
            raise ClosureError(f"unrecognized helper lookup: {compact}")
        if not compact.startswith("insert into "):
            raise ClosureError("export only supports helper inserts")
        parts = query.split("%s")
        if len(parts) != len(params) + 1:
            raise ClosureError("parameter arity drift")
        rendered = parts[0]
        for value, suffix in zip(params, parts[1:]):
            rendered += self.variables.get(str(value), literal(value)) + suffix
        if " returning " in compact:
            name = f"generated_{len(self.variables)}"
            symbolic = str(uuid5(NAMESPACE_URL, f"atlas/374/export/{name}"))
            self.variables[symbolic] = name
            self.rows = [(symbolic,)]
            rendered += f" INTO {name}"
        self.statements.append(rendered.strip() + ";")
        return self

    def fetchone(self):
        return self.rows[0] if self.rows else None

    def fetchall(self):
        return self.rows


def count_expression():
    return "jsonb_build_object(" + ",".join(
        f"{literal(table)},(select count(*) from {table})"
        for table in rehearsal.STRICT_DELTA
    ) + ")"


def snapshot_expression(table):
    # Sorting full row JSON also detects same-count changes, including serving moves.
    return f"(select coalesce(jsonb_agg(to_jsonb(t) order by to_jsonb(t)::text),'[]'::jsonb) from {table} t)"


def render(review, *, authorized=False, revision, expected=None, hrw_id=HRW_ID):
    expected = expected or production.EXPECTED_PRODUCTION
    resolved = {
        key: {"claim_id": item["claim_id"],
              "target_spatial_entity_id": item["spatial_entity_id"],
              "target_canonical_name": item["canonical_name"]}
        for key, item in expected.items()
    }
    collector = InsertCollector()
    first = rehearsal.apply_once(collector, review, resolved)
    declarations = ["before_counts jsonb;", "after_counts jsonb;", "receipt jsonb;"]
    declarations += [f"{name} uuid;" for name in collector.variables.values()]
    declarations += [f"protected_{i} jsonb;" for i in range(len(PROTECTED))]
    body = [require("true" if authorized else "false", "#374 explicit production authorization absent")]
    tables = tuple(dict.fromkeys((*rehearsal.STRICT_DELTA, *PROTECTED)))
    body += [f"LOCK TABLE {','.join(tables)} IN SHARE ROW EXCLUSIVE MODE;"]
    for key, item in expected.items():
        identity = f"""(select count(*)=1 from audit.research_case_ingest r
          join atlas.claim c using(claim_id)
          join atlas.territorial_practice_claim t using(claim_id)
          join atlas.spatial_entity se using(spatial_entity_id)
          where r.case_key={literal(key)} and r.claim_id={literal(item['claim_id'])}::uuid
          and t.spatial_entity_id={literal(item['spatial_entity_id'])}::uuid
          and se.canonical_name={literal(item['canonical_name'])}
          and c.review_status::text='reviewed' and c.publication_status::text='unpublished'
          and t.practice_level is null)"""
        body.append(require(identity, f"live identity/state drift: {key}"))
    names = literal(list(production.NEW_IDENTITIES))
    urls = literal(list(production.NEW_SOURCE_URLS))
    claims = literal([item["claim_id"] for item in expected.values()])
    body += [require(f"not exists(select 1 from atlas.spatial_entity where canonical_name=any({names}::text[]))", "locus identity collision"),
             require(f"not exists(select 1 from atlas.source_version where url_or_identifier=any({urls}::text[]))", "new source URL collision"),
             require(f"not exists(select 1 from atlas.claim_evidence_locus where claim_id=any({claims}::uuid[]))", "existing locus links"),
             require(f"not exists(select 1 from audit.release_claim where claim_id=any({claims}::uuid[]))", "unexpected release membership"),
             require(f"(select count(*)=1 and min(source_version_id::text)={literal(hrw_id)} from atlas.source_version where url_or_identifier={literal(HRW_URL)})", "India HRW reuse drift"),
             require(f"""(select count(*)=1 from audit.research_case_ingest r
                 join atlas.claim c using(claim_id) join atlas.territorial_practice_claim t using(claim_id)
                 where r.case_key={literal(rehearsal.BRAZIL_HOLD)}
                 and c.review_status::text='reviewed' and c.publication_status::text='unpublished'
                 and t.practice_level is null
                 and not exists(select 1 from atlas.claim_evidence_locus cel where cel.claim_id=c.claim_id))""", "Brazil HOLD drift")]
    for i, table in enumerate(PROTECTED):
        body.append(f"protected_{i} := {snapshot_expression(table)};")
    body.append(f"before_counts := {count_expression()};")
    body.extend(collector.statements)
    body.append(f"after_counts := {count_expression()};")
    for table, delta in rehearsal.STRICT_DELTA.items():
        body.append(require(f"(after_counts->>{literal(table)})::bigint - (before_counts->>{literal(table)})::bigint = {delta}", f"unexpected delta: {table}"))
    for i, table in enumerate(PROTECTED):
        body.append(require(f"protected_{i} = {snapshot_expression(table)}", f"protected rows changed: {table}"))
    accepted = [r for r in review["candidates"] if r["case_key"] in expected]
    for row in accepted:
        result = first[row["case_key"]]
        entity = collector.variables[result["locus_spatial_entity_id"]]
        geometry = row["geometry"]
        body.append(require(f"""(select count(*)=1 from atlas.geometry g
          join atlas.claim_evidence_locus cel using(spatial_entity_id)
          where cel.claim_id={literal(result['claim_id'])}::uuid and g.spatial_entity_id={entity}
          and cel.role_text={literal(row['locus_link']['role_text'])}
          and g.geometry_source_native_id={literal(geometry['source_native_id'])}
          and g.accuracy_status::text={literal(geometry['accuracy_status'])}
          and GeometryType(g.geom)='POINT' and ST_SRID(g.geom)=4326
          and ST_Equals(g.geom,ST_SetSRID(ST_GeomFromGeoJSON({literal(json.dumps(geometry['geojson']))}),4326)))""", "case-linked point semantics drift"))
    result_sql = []
    for key, result in first.items():
        fields = []
        for name, value in result.items():
            fields += [literal(name), collector.variables.get(str(value), literal(value))]
        result_sql += [literal(key), "jsonb_build_object(" + ",".join(fields) + ")"]
    body.append(f"""receipt := jsonb_build_object(
      'issue',374,'git_revision',{literal(revision)},'transport','connected_sql',
      'checked_at',clock_timestamp(),'before_counts',before_counts,'after_counts',after_counts,
      'first_pass',jsonb_build_object({','.join(result_sql)}),
      'held_cases_unchanged',jsonb_build_array({literal(rehearsal.BRAZIL_HOLD)}));""")
    body.append("PERFORM set_config('atlas.issue374_receipt',receipt::text,true);")
    return "-- #374 only. Review and explicit sponsor authorization required.\n" + \
        "DO $atlas374$\nDECLARE\n" + "\n".join(declarations) + \
        "\nBEGIN\nSET LOCAL lock_timeout = '10s';\nSET LOCAL statement_timeout = '60s';\n" + \
        "\n".join(body) + "\nEND\n$atlas374$;\n" + \
        "SELECT current_setting('atlas.issue374_receipt')::jsonb AS receipt;\n"


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--output', type=Path)
    parser.add_argument('--production-write-authorized')
    parser.add_argument('--expected-main-sha')
    args = parser.parse_args()
    review = rehearsal.load_review()
    production.load_plan()
    production.load_receipt()
    revision = production.git_head()
    authorized = args.production_write_authorized is not None
    if authorized:
        production.require_authority(args)
    if args.output:
        args.output.write_text(render(review, authorized=authorized, revision=revision), encoding='utf-8')
    print(json.dumps({'issue': 374, 'mode': 'export_only', 'production_authorized': authorized,
                      'database_connected': False, 'git_revision': revision,
                      'output': str(args.output) if args.output else None}))
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
