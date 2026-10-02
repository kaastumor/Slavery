#!/usr/bin/env python3
"""Build a typed immutable public adapter for the exact D-125 case selection."""
from __future__ import annotations
import argparse
import copy
import hashlib
import json
from pathlib import Path
import sys
sys.path.insert(0,str(Path(__file__).resolve().parent))
from build_v070_public_materialization import build_payload, source_ref, canonical_bytes
from full_state_release_bundle import validate_bundle
from shapely import from_wkb
from shapely.geometry import mapping

ROOT=Path(__file__).resolve().parents[1]
ID='v0.8.2-public-mvp-v1'

def load(p):return json.loads(p.read_text(encoding='utf-8'))
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()

def build(release_dir,output_dir):
    authority=load(release_dir/'authority-state.json');validate_bundle(authority)
    release=load(release_dir/'manifest.json')
    if release['release_version']!='v0.8.2' or release['authority']['membership']!=authority['membership']:
        raise ValueError('canonical source mismatch')
    selection=load(ROOT/'release/selections/v0.8.2-requested-corpus.json')
    payload=build_payload(release,authority)
    payload.update(serving_materialization_id=ID,data_boundary='immutable_v082_release_materialization',display_scope='territorial_practice_with_separate_legal_and_external_cases',case_count=65)
    payload['release_dimensions']['case_counts']=selection['expected_dimensions']
    payload['release_dimensions']['non_absence_note']='Unresolved or withheld geometry is not historical absence. Legal and external/network evidence is separate from territorial practice; modern site points establish no territorial extent.'
    places={p['spatial_entity_id']:p for p in payload['places']}
    for p in places.values():
        for c in p['claims']:c['claim_kind']='territorial_practice'
    selected_additions={r['claim_id'] for r in selection['research_claims']}|set(selection['pilot_claim_ids'].values())
    for cid in sorted(selected_additions):
        obj=authority['objects']['claims'][cid];c=obj['claim'];kind=c['claim_kind_code']
        if kind=='territorial_practice':continue
        subtype=obj[kind]
        sid=subtype.get('spatial_entity_id') or subtype['jurisdiction_spatial_entity_id']
        entity=authority['objects']['spatial_entities'][sid]['spatial_entity']
        claim={'claim_id':cid,'claim_kind':kind,'from_year':c['from_year'],'to_year':c['to_year'],'summary':c['summary'],'review_status':c['review_status'],'publication_status':c['publication_status'],
            'practice_type':subtype.get('participation_type_code') or subtype.get('event_type'),'practice_level':None,'coverage_state':'reviewed','classification_status':None,'dimension_details':subtype,
            'sources':[source_ref(r,authority['objects']['source_versions']) for r in obj['claim_sources']]}
        places[sid]={'spatial_entity_id':sid,'name':entity['canonical_name'],'display_name':entity['display_name'],'entity_type_code':entity['entity_type_code'],'notes':entity['notes'],'claims':[claim],'geometries':[]}
    old=load(ROOT/'data/serving/v0.8.1-public-mvp-v2/atlas-data.json')
    render={g['geometry_id']:g for p in old['places'] for g in p['geometries']}
    for sid,p in places.items():
        linked_loci={l['spatial_entity_id'] for c in p['claims'] for l in authority['objects']['claims'][c['claim_id']]['evidence_loci']}
        for gid,g in authority['objects']['geometries'].items():
            if g['spatial_entity_id']!=sid and g['spatial_entity_id'] not in linked_loci:continue
            if gid in render:
                p['geometries'].append(copy.deepcopy(render[gid]));continue
            sv=authority['objects']['source_versions'].get(g['geometry_source_version_id'],{})
            geometry=mapping(from_wkb(bytes.fromhex(g['geom_ewkb_hex']))) if g['geom_ewkb_hex'] else None
            if geometry and geometry['type']!='Point':raise ValueError('new non-point geometry has no reviewed render asset')
            p['geometries'].append({'geometry_id':gid,'from_year':g['from_year'],'to_year':g['to_year'],'accuracy_status':g['accuracy_status'],'resolution_method':g['resolution_method'],
                'source_native_id':g['geometry_source_native_id'],'geometry':geometry,'source_title':sv.get('source',{}).get('title'),'source_version':sv.get('source_version',{}).get('version_label'),
                'source_url':sv.get('source_version',{}).get('url_or_identifier'),'geometry_role':'evidence_locus' if g['spatial_entity_id'] in linked_loci else 'site_navigation_locator',
                'render_transform':'source_geometry' if geometry else 'none','notes':'Site/navigation or evidence locator only; not a territorial practice extent.'})
    payload['places']=sorted(places.values(),key=lambda p:(p['name'],p['spatial_entity_id']))
    if len(payload['places'])!=65:raise ValueError('requested case count mismatch')
    expected_claims={cid for group in selection['inherited_case_groups'] for cid in group['claim_ids']}|selected_additions
    shown={c['claim_id'] for p in payload['places'] for c in p['claims']}
    if shown!=expected_claims:raise ValueError('public exact claim membership differs')
    output_dir.mkdir(parents=True,exist_ok=True)
    (output_dir/'atlas-data.json').write_bytes(canonical_bytes(payload))
    manifest={'materialization_schema':'historical-slavery-atlas-public-materialization-v1','materialization_id':ID,'purpose':'public_mvp_preview','canonical':False,'canonical_source_release':'v0.8.2',
        'canonical_source_release_manifest_sha256':sha(release_dir/'manifest.json'),'canonical_source_authority_sha256':sha(release_dir/'authority-state.json'),
        'payload_file':'atlas-data.json','payload_sha256':sha(output_dir/'atlas-data.json'),'payload_bytes':(output_dir/'atlas-data.json').stat().st_size,'place_count':65,
        'displayed_claim_count':len(shown),'case_counts':selection['expected_dimensions'],'rollback_materialization':'v0.8.1-public-mvp-v2',
        'render_geometry_source':'unchanged accepted v0.8.1 v2 assets for verified inherited geometry, plus reviewed source-native point locators; unresolved geometry retained',
        'withheld_inherited_geometry_ids':selection['geometry_selection']['withheld_inherited_geometry_ids'],'source_membership_sha256':authority['membership_sha256'],'source_database_state_sha256':authority['database_state_sha256']}
    (output_dir/'materialization-manifest.json').write_bytes(canonical_bytes(manifest))
    module='export const V082_MATERIALIZATION_ID = '+json.dumps(ID)+';\nexport const V082_PAYLOAD_SHA256 = '+json.dumps(manifest['payload_sha256'])+';\nexport const V082_PAYLOAD = '+json.dumps((output_dir/'atlas-data.json').read_text(encoding='utf-8'),ensure_ascii=False)+';\n'
    (ROOT/'supabase/functions/atlas-data/v082_payload.ts').write_text(module,encoding='utf-8',newline='\n')
    return manifest

if __name__=='__main__':
    p=argparse.ArgumentParser(description=__doc__);p.add_argument('release_dir',type=Path);p.add_argument('output_dir',type=Path);a=p.parse_args()
    print(json.dumps(build(a.release_dir,a.output_dir)))
