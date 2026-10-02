#!/usr/bin/env python3
"""Freeze the sponsor's exact 48 + 12 + 5 corpus from independent governed snapshots."""
from __future__ import annotations
import argparse
import copy
import hashlib
import gzip
import json
from pathlib import Path
import sys
sys.path.insert(0, str(Path(__file__).resolve().parent))
from full_state_release_bundle import BUNDLE_SCHEMA, OBJECT_GROUPS, canonical_bytes, object_digests, sha256_value, validate_bundle
from audit_successor_source_bindings import verify_bindings, canonical
from shapely import from_wkb, make_valid
from shapely.geometry import shape
from shapely.ops import unary_union

ROOT = Path(__file__).resolve().parents[1]
HELD_GEOMETRIES = {
    '21c9c493-14f8-4c13-9845-0e8a738c9110',
    '65f31d95-3e05-49f6-9f74-43f2a3717728',
    'b81dd8d2-3956-4060-856c-7ab2ca72fde7',
}
LOCUS_AUGMENTATIONS = {
    '8691d038-1683-5331-bccb-e7a189cdd229': {
        '9d0106e0-1ee1-4d29-996d-aff760af7e59', '572179ca-bb9c-4dd9-90d8-df4dcf8c41a4'},
    '63dda32b-6c3e-4b3e-9c5a-36596e6cdc1b': {'d8918150-bedc-4a02-a037-2b02b9376b83'},
}

def load(path):
    return json.loads(path.read_text(encoding='utf-8'))

def verify_source_bindings(old, audit=None):
    verify_bindings(json.loads(gzip.decompress((ROOT/'data/research/geometry_reviews/v082_exact_api_source_bindings.json.gz').read_bytes())),old)
    audit=audit if audit is not None else load(ROOT/'data/research/geometry_reviews/v082_non_api_source_bindings.json')
    if {r['geometry_id'] for r in audit['held']} != HELD_GEOMETRIES or len(audit['rows'])!=5:
        raise ValueError('non-API source audit membership drift')
    for row in audit['rows']:
        stored=make_valid(from_wkb(bytes.fromhex(old['objects']['geometries'][row['geometry_id']]['geom_ewkb_hex'])))
        if 'source_record' in row:
            record=row['source_record']
            if hashlib.sha256(canonical(record)).hexdigest()!=row['source_record_sha256']:
                raise ValueError('source record fingerprint drift')
            if 'latitude_dms' in record:
                def dms(v):return (1 if v[0]>=0 else -1)*(abs(v[0])+v[1]/60+v[2]/3600)
                coords=[round(dms(record['longitude_dms']),10),round(dms(record['latitude_dms']),10)]
            elif 'statement' in record:
                native=record['statement']['mainsnak']['datavalue']['value']
                coords=[round(native['longitude'],4),round(native['latitude'],4)]
            else:
                coords=[record['longitude_wgs1984'],record['latitude_wgs1984']]
            if any(abs(a-b)>1e-9 for a,b in zip(coords,list(stored.coords)[0])):
                raise ValueError('native point translation differs')
        else:
            native=unary_union([make_valid(shape(f['geometry'])) for f in row['source_asset']['features']])
            if native.hausdorff_distance(stored)>1e-8 or native.symmetric_difference(stored).area>1e-8:
                raise ValueError('Rome pinned source geometry differs')
            if [row['source_native_from'],row['source_native_to'],row['atlas_interval']] != [14,14,[14,22]]:
                raise ValueError('Rome native time differs')

def build(snapshot_dir, source_git_sha):
    old = load(ROOT/'data/releases/v0.8.1/authority-state.json')
    verify_source_bindings(old)
    selection = load(ROOT/'release/selections/v0.8.2-requested-corpus.json')
    objects = {}
    for group, key in OBJECT_GROUPS.items():
        rows = load(snapshot_dir/f'atlas-snapshot-{key}.json')
        objects[group] = {r['id']: r['payload'] for r in rows}
        if len(objects[group]) != len(rows):
            raise ValueError('duplicate snapshot identity')
    for gid, g in objects['geometries'].items():
        digest = g.pop('live_ewkb_sha256')
        if gid in old['objects']['geometries']:
            expected = old['objects']['geometries'][gid]
            ewkb = expected['geom_ewkb_hex']
            if digest != (hashlib.sha256(bytes.fromhex(ewkb)).hexdigest() if ewkb else None):
                raise ValueError('inherited geometry bytes drifted: '+gid)
            g['geom_ewkb_hex'] = ewkb
        elif digest != (hashlib.sha256(bytes.fromhex(g['geom_ewkb_hex'])).hexdigest() if g['geom_ewkb_hex'] else None):
            raise ValueError('new geometry bytes drifted: '+gid)
    pinned=selection['geometry_selection']
    if set(pinned['withheld_inherited_geometry_ids'])!=HELD_GEOMETRIES or set(objects['geometries'])!=(set(old['membership']['geometry_ids'])-HELD_GEOMETRIES)|set(pinned['exact_additions']):
        raise ValueError('exact geometry selection differs')
    for group, previous in old['objects'].items():
        for oid, expected in previous.items():
            if group == 'geometries' and oid in HELD_GEOMETRIES:
                if oid in objects[group]:
                    raise ValueError('unbound geometry reused')
                continue
            actual = objects[group].get(oid)
            if group == 'claims' and oid in LOCUS_AUGMENTATIONS:
                bounded = copy.deepcopy(actual)
                if {r['spatial_entity_id'] for r in bounded['evidence_loci']} != LOCUS_AUGMENTATIONS[oid]:
                    raise ValueError('evidence-locus membership drift')
                bounded['evidence_loci'] = expected['evidence_loci']
                actual = bounded
            if actual != expected:
                changed = [k for k in set(actual or {})|set(expected) if (actual or {}).get(k) != expected.get(k)]
                raise ValueError(f'predecessor drift {group}:{oid}: {changed}')
    additions = {r['claim_id'] for r in selection['research_claims']}|set(selection['pilot_claim_ids'].values())
    if len(additions)!=17 or set(objects['claims']) != set(old['membership']['claim_ids'])|additions:
        raise ValueError('exact requested claim membership differs')
    counts = {'territorial_practice':0,'legal_event':0,'external_participation':0}
    for cid in additions:
        c = objects['claims'][cid]
        if c['claim']['review_status']!='reviewed' or not c['claim_sources']:
            raise ValueError('addition lacks reviewed evidence')
        if c['claim']['publication_status']!='unpublished':
            raise ValueError('addition publication drift')
        kind = c['claim']['claim_kind_code']
        counts[kind]+=1
        if kind=='territorial_practice' and c['territorial_practice']['practice_level'] is not None:
            raise ValueError('new P-level forbidden')
    if counts!={'territorial_practice':13,'legal_event':1,'external_participation':3}:
        raise ValueError('dimension counts differ')
    source_ids=set(old['membership']['source_version_ids'])
    source_ids.update(r['source_version_id'] for c in objects['claims'].values() for r in c['claim_sources'])
    source_ids.update(g['geometry_source_version_id'] for g in objects['geometries'].values() if g['geometry_source_version_id'])
    objects['source_versions']={sid:objects['source_versions'][sid] for sid in sorted(source_ids)}
    membership={key:sorted(objects[group]) for group,key in OBJECT_GROUPS.items()}
    rows=load(snapshot_dir/'atlas-snapshot-cartography.json')
    cartography=rows[0]
    if cartography!=old['cartography']:
        raise ValueError('canonical neutral cartography drift')
    digests=object_digests(objects)
    state={'bundle_schema':BUNDLE_SCHEMA,'schema_version':'0034','membership':membership,'object_digests':digests,'cartography_sha256':sha256_value(cartography)}
    result={'bundle_schema':BUNDLE_SCHEMA,'candidate_sha256':sha256_value(selection),'source_git_sha':source_git_sha,
        'release':{'release_version':'v0.8.2-requested-corpus-authority-v1','schema_version':'0034','canonical':False,'purpose':'canonical_research_state_proof',
        'canonical_predecessor_version':'v0.8.1','canonical_predecessor_artifact_sha256':hashlib.sha256((ROOT/'data/releases/v0.8.1/manifest.json').read_bytes().replace(b'\r\n',b'\n')).hexdigest(),
        'reviewed_candidate_id':'v0.8.2-requested-48-12-5',
        'changelog':'Exact requested corpus: preserve 75 predecessor claims; add 17 reviewed claims representing 13 territorial, one legal and three external cases. Preserve bounded Mycenaean and Sogdiana evidence-locus augmentations.',
        'qc_summary':'65 requested case slots (61 territorial, one legal, three external); exact IDs and source closure; no new P-levels; verified predecessor objects and geometry bytes; neutral cartography unchanged.',
        'unresolved_issues':'Three legacy Pleiades-labelled points withheld from successor geometry reuse under D-121. Case evidence remains included. Unresolved geometry is not absence. Independent historical reviews remain zero.'},
        'membership':membership,'membership_sha256':sha256_value(membership),'cartography':cartography,'cartography_sha256':sha256_value(cartography),
        'objects':objects,'object_digests':digests,'database_state_sha256':sha256_value(state)}
    validate_bundle(result)
    return result

def main():
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument('--snapshot-dir',type=Path,required=True)
    p.add_argument('--source-git-sha',required=True)
    p.add_argument('--output',type=Path,required=True)
    a=p.parse_args()
    result=build(a.snapshot_dir,a.source_git_sha)
    a.output.parent.mkdir(parents=True,exist_ok=True)
    a.output.write_bytes(canonical_bytes(result))
    print(json.dumps({'status':'PASS','counts':{k:len(v) for k,v in result['membership'].items()},'database_state_sha256':result['database_state_sha256']}))

if __name__=='__main__':
    main()
