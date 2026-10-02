#!/usr/bin/env python3
"""Export exact, inert-by-default D-125 release registration; never execute SQL."""
from __future__ import annotations
import argparse
import copy
import hashlib
import json
from pathlib import Path
import sys
sys.path.insert(0,str(Path(__file__).resolve().parent))
from full_state_release_bundle import snapshot_objects, OBJECT_GROUPS
from export_geometry_closure_tranche_02_sql import literal,snapshot_expression
from publish_canonical_release import load_publication_inputs,insert_membership,insert_artifacts
from build_canonical_release import sha256_file

ROOT=Path(__file__).resolve().parents[1]
SERVING='v0.8.2-public-mvp-v1'

def load(p):return json.loads(p.read_text(encoding='utf-8'))

def require(condition,message):
    return f'IF NOT coalesce(({condition}),false) THEN RAISE EXCEPTION {literal(message)}; END IF;'

def inputs(revision):
    release=ROOT/'data/releases/v0.8.2'
    data=load_publication_inputs(ROOT/'release/specs/v0.8.2.json',release/'authority-state.json',release/'cartography-recovery-fingerprint.json',release,source_git_sha=revision)
    directory=ROOT/'data/serving'/SERVING
    payload=load(directory/'atlas-data.json');manifest=load(directory/'materialization-manifest.json')
    if sha256_file(directory/'atlas-data.json')!=manifest['payload_sha256'] or manifest['canonical_source_authority_sha256']!=sha256_file(release/'authority-state.json'):
        raise ValueError('serving payload/source checksum drift')
    claims=sorted({c['claim_id'] for p in payload['places'] for c in p['claims']})
    spatial=sorted({p['spatial_entity_id'] for p in payload['places']})
    geometry=sorted({g['geometry_id'] for p in payload['places'] for g in p['geometries']})
    sources=sorted({s['source_version_id'] for p in payload['places'] for c in p['claims'] for s in c['sources']}|{data['authority']['objects']['geometries'][gid]['geometry_source_version_id'] for gid in geometry if data['authority']['objects']['geometries'][gid]['geometry_source_version_id']})
    membership={k:[] for k in data['authority']['membership']}
    membership.update(claim_ids=claims,spatial_entity_ids=spatial,geometry_ids=geometry,source_version_ids=sources)
    if len(spatial)!=65 or len(claims)!=70 or any(not set(ids)<=set(data['authority']['membership'][key]) for key,ids in membership.items()):
        raise ValueError('serving exact membership mismatch')
    dbmanifest={'purpose':'public_mvp_preview','canonical':False,'canonical_source_release':'v0.8.2','display_scope':payload['display_scope'],**membership,'source_membership_sha256':data['authority']['membership_sha256'],
        'serving_materialization':{'materialization_id':SERVING,'canonical_source_release':'v0.8.2','canonical_source_release_manifest_sha256':manifest['canonical_source_release_manifest_sha256'],'payload_sha256':manifest['payload_sha256'],'payload_bytes':manifest['payload_bytes'],'materialization_manifest_sha256':sha256_file(directory/'materialization-manifest.json')},'release_dimensions':payload['release_dimensions']}
    serving={'spec':{'release_version':SERVING,'schema_version':'0034'},'authority':copy.deepcopy(data['authority']),'manifest':dbmanifest,
        'artifacts':[{'filename':name,'sha256':sha256_file(directory/name),'size_bytes':(directory/name).stat().st_size,'media_type':'application/json','storage_status':'repository','storage_locator':f'git:{revision}:data/serving/{SERVING}/{name}'} for name in ['atlas-data.json','materialization-manifest.json']]}
    serving['authority']['membership']=membership
    return data,serving

def snapshot_queries(authority):
    queries={}
    class Collector:
        def execute(self,q,params=()):
            if params:
                self.ids=params[0]
                self.key=next(k for k,ids in authority['membership'].items() if ids==self.ids)
                q=q.replace('%s',literal(self.ids))
                if self.key=='geometry_ids':
                    q=q.replace("'geom_ewkb_hex',case when g.geom is null then null else encode(st_asewkb(g.geom),'hex') end","'geom_ewkb_sha256',case when g.geom is null then null else encode(digest(st_asewkb(g.geom),'sha256'),'hex') end")
                queries[self.key]=q
            else:
                # D-108 portable shape invariant; raw union serialization can differ between PostGIS/GEOS builds.
                queries['cartography']=q.replace("'geom_ewkb_sha256',encode(digest(st_asewkb(f.geom),'sha256'),'hex')","'normalized_wkb_sha256',encode(digest(st_asbinary(st_normalize(f.geom)),'sha256'),'hex')").replace("'geom_ewkb_bytes',octet_length(st_asewkb(f.geom))","'normalized_wkb_bytes',octet_length(st_asbinary(st_normalize(f.geom)))")
        def fetchall(self):return [(oid,None) for oid in self.ids]
        def fetchone(self):return ('land_fabric','stub',{})
    snapshot_objects(Collector(),authority['membership'])
    return queries

def expected_rows(authority,key):
    if key=='cartography':
        payload=copy.deepcopy(authority['cartography']['payload'])
        payload.pop('geom_ewkb_sha256');payload.pop('geom_ewkb_bytes')
        fingerprint=load(ROOT/'data/releases/v0.8.2/cartography-recovery-fingerprint.json')
        payload.update(normalized_wkb_sha256=fingerprint['normalized_wkb_sha256'],normalized_wkb_bytes=fingerprint['normalized_wkb_bytes'])
        return {authority['cartography']['id']:payload}
    group=next(group for group,k in OBJECT_GROUPS.items() if k==key)
    expected=copy.deepcopy(authority['objects'][group])
    if key=='geometry_ids':
        for g in expected.values():
            ewkb=g.pop('geom_ewkb_hex');g['geom_ewkb_sha256']=hashlib.sha256(bytes.fromhex(ewkb)).hexdigest() if ewkb else None
    return expected

def snapshot_sql(q,key):
    if key=='cartography':return 'SELECT id,payload FROM ('+q+') AS cartography(kind,id,payload)'
    return q

def preflight_queries(authority):
    output={}
    for key,q in snapshot_queries(authority).items():
        expected=expected_rows(authority,key)
        output[key]="WITH actual AS ("+snapshot_sql(q,key)+"), expected AS (SELECT key AS id,value AS payload FROM jsonb_each("+literal(json.dumps(expected,ensure_ascii=False,separators=(',',':')))+"::jsonb)) SELECT count(*)::int AS matched_count,bool_and(a.payload=e.payload) AS exact_match,jsonb_object_agg(a.id,encode(digest(a.payload::text,'sha256'),'hex')) AS database_hashes FROM actual a(id,payload) JOIN expected e USING(id)"
    return output

def guard(q,key,hashes):
    live="(SELECT coalesce(jsonb_object_agg(id,encode(digest(payload::text,'sha256'),'hex')),'{}'::jsonb) FROM ("+snapshot_sql(q,key)+") AS live(id,payload))"
    return require(live+'='+literal(json.dumps(hashes,separators=(',',':')))+'::jsonb','D125 frozen governed state drift: '+key)

class Collector:
    def __init__(self):self.statements=[]
    def execute(self,q,params=()):
        parts=q.split('%s')
        if len(parts)!=len(params)+1:raise ValueError('publication parameter arity drift')
        out=parts[0]
        for v,suffix in zip(params,parts[1:]):out+=literal(v)+suffix
        self.statements.append(out.strip()+';')

def render(preflight,revision,authorized=False,cutover=False):
    canonical,serving=inputs(revision);authority=canonical['authority']
    if preflight['authority_sha256']!=sha256_file(ROOT/'data/releases/v0.8.2/authority-state.json'):
        raise ValueError('preflight authority checksum differs')
    queries=snapshot_queries(authority)
    if set(preflight['groups'])!=set(queries):raise ValueError('preflight group membership differs')
    guards=[]
    for key,q in queries.items():
        checked=preflight['groups'][key]
        if checked['exact_match'] is not True or checked['matched_count']!=len(expected_rows(authority,key)):
            raise ValueError('preflight mismatch: '+key)
        guards.append(guard(q,key,checked['database_hashes']))
    collector=Collector()
    for data in [canonical,serving]:
        version=data['spec']['release_version']
        collector.execute("INSERT INTO audit.release_manifest(release_version,schema_version,status,changelog,qc_summary,unresolved_issues,manifest) VALUES (%s,'0034','validated',%s,%s,%s,%s::jsonb)",
            (version,data.get('changelog','D-125 typed immutable public serving materialization.'),data.get('qc_summary','Exact 65-case adapter with separate territorial, legal and external evidence.'),data.get('unresolved_issues','Three inherited points withheld under D-121; unresolved geometry is not absence. Independent historical reviews remain zero.'),json.dumps(data['manifest'],ensure_ascii=False,separators=(',',':'))))
        insert_membership(collector,data)
        insert_artifacts(collector,data)
        if version==SERVING:collector.statements[-2:]=[s.replace("'canonical_release_file'","'public_serving_materialization'") for s in collector.statements[-2:]]
        collector.execute("UPDATE audit.release_manifest SET status='published' WHERE release_version=%s AND status='validated'",(version,))
    body=[require('true' if authorized else 'false','D125 explicit registration authorization absent'),
        'LOCK TABLE atlas.claim,atlas.claim_source,atlas.territorial_practice_claim,atlas.external_participation_claim,atlas.legal_event,atlas.claim_evidence_locus,atlas.source,atlas.source_version,atlas.source_asset,atlas.spatial_entity,atlas.geometry,audit.release_manifest,audit.release_claim,audit.release_geometry,audit.release_artifact,audit.release_channel IN SHARE ROW EXCLUSIVE MODE;',
        require("(SELECT migration_name LIKE '0034_%' FROM atlas_meta.schema_migration ORDER BY migration_name DESC LIMIT 1)",'schema head drift'),
        require("(SELECT release_version='v0.8.1-public-mvp-v2' FROM audit.release_channel WHERE channel_code='public_mvp_preview')",'serving predecessor drift'),
        require("NOT EXISTS(SELECT 1 FROM audit.release_manifest WHERE release_version IN ('v0.8.2','v0.8.2-public-mvp-v1'))",'release replay/collision'),
        "old_releases := (SELECT jsonb_agg(to_jsonb(r) ORDER BY release_version) FROM audit.release_manifest r);",
        'old_channel := '+snapshot_expression('audit.release_channel')+';',*guards,*collector.statements,*guards,
        require("(SELECT jsonb_agg(to_jsonb(r) ORDER BY release_version) FROM audit.release_manifest r WHERE release_version NOT IN ('v0.8.2','v0.8.2-public-mvp-v1'))=old_releases",'predecessor releases changed'),
        require(snapshot_expression('audit.release_channel')+'=old_channel','registration moved public channel'),
        "RAISE NOTICE 'D125 registration complete: canonical v0.8.2, serving v0.8.2-public-mvp-v1; registration itself left channel unchanged';"]
    if cutover:
        body.extend([
            require("EXISTS(SELECT 1 FROM audit.release_manifest WHERE release_version='v0.8.2-public-mvp-v1' AND status='published' AND manifest->>'purpose'='public_mvp_preview' AND manifest->'serving_materialization'->>'payload_sha256'="+literal(serving['manifest']['serving_materialization']['payload_sha256'])+")",'cutover target metadata drift'),
            "UPDATE audit.release_channel SET release_version='v0.8.2-public-mvp-v1',updated_by='sponsor-authorized D125 release integration',note='Exact 65 requested cases; verified immutable v0.8.2 payload; rollback v0.8.1-public-mvp-v2' WHERE channel_code='public_mvp_preview' AND release_version='v0.8.1-public-mvp-v2';",
            require('FOUND','cutover compare-and-set affected no row'),
            require("(SELECT release_version='v0.8.2-public-mvp-v1' FROM audit.release_channel WHERE channel_code='public_mvp_preview')",'cutover readback mismatch')])
    return 'DO $atlas_d125_registration$\nDECLARE old_releases jsonb; old_channel jsonb;\nBEGIN\n'+'\n'.join(body)+'\nEND\n$atlas_d125_registration$;\n'

if __name__=='__main__':
    p=argparse.ArgumentParser(description=__doc__);p.add_argument('--preflight',type=Path,required=True);p.add_argument('--revision',required=True);p.add_argument('--authorized',action='store_true');p.add_argument('--cutover',action='store_true');p.add_argument('--output',type=Path,required=True);a=p.parse_args()
    a.output.write_text(render(load(a.preflight),a.revision,a.authorized,a.cutover),encoding='utf-8',newline='\n')
