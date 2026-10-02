#!/usr/bin/env python3
"""Exercise exact D-125 registration, drift rejection, replay and rollback in CI only."""
import json
import os
from pathlib import Path
import psycopg
import export_v082_requested_publication_sql as exporter
from publish_canonical_release import verify_published, MEMBERSHIP_TABLES

def verify_serving(cur,data):
    version=data['spec']['release_version']
    cur.execute('SELECT schema_version,status,manifest FROM audit.release_manifest WHERE release_version=%s',(version,))
    if cur.fetchone()!=('0034','published',data['manifest']):raise RuntimeError('serving manifest differs')
    for key,(table,col,group) in MEMBERSHIP_TABLES.items():
        cur.execute(f'SELECT {col}::text,object_sha256,capture_status FROM {table} WHERE release_version=%s',(version,))
        actual={r[0]:(r[1],r[2]) for r in cur.fetchall()}
        expected={oid:(data['authority']['object_digests'][group][oid],'captured_at_release') for oid in data['authority']['membership'][key]}
        if actual!=expected:raise RuntimeError('serving typed membership differs '+key)
    cur.execute("SELECT filename,sha256,size_bytes,storage_locator,capture_status FROM audit.release_artifact WHERE release_version=%s AND artifact_role='public_serving_materialization'",(version,))
    actual={r[0]:(r[1],r[2],r[3],r[4]) for r in cur.fetchall()}
    expected={r['filename']:(r['sha256'],r['size_bytes'],r['storage_locator'],'captured_at_release') for r in data['artifacts']}
    if actual!=expected:raise RuntimeError('serving artifact registry differs')

def main():
    if os.environ.get('CI')!='true':raise SystemExit('disposable CI only')
    dsn=os.environ['DATABASE_URL']
    if psycopg.conninfo.conninfo_to_dict(dsn)['dbname']!='slavery_atlas_d125_rehearsal':
        raise SystemExit('exact disposable database name required')
    canonical,serving=exporter.inputs('CI_REHEARSAL')
    authority=canonical['authority']
    with psycopg.connect(dsn) as conn:
        with conn.cursor() as cur:
            cur.execute("INSERT INTO audit.release_manifest(release_version,schema_version,status,changelog,qc_summary,unresolved_issues,manifest) VALUES ('v0.8.1-public-mvp-v2','0034','published','CI predecessor fixture','CI fixture','CI fixture','{\"purpose\":\"public_mvp_preview\"}'::jsonb)")
            cur.execute("INSERT INTO audit.release_channel(channel_code,release_version,updated_by,note) VALUES ('public_mvp_preview','v0.8.1-public-mvp-v2','CI','disposable predecessor fixture')")
        conn.commit()
        groups={}
        with conn.cursor() as cur:
            for key,q in exporter.preflight_queries(authority).items():
                cur.execute(q);count,match,hashes=cur.fetchone()
                if not match:raise RuntimeError('restored preflight mismatch '+key)
                groups[key]={'matched_count':count,'exact_match':match,'database_hashes':hashes}
        preflight={'authority_sha256':exporter.sha256_file(exporter.ROOT/'data/releases/v0.8.2/authority-state.json'),'groups':groups}
        authorized=exporter.render(preflight,'CI_REHEARSAL',True)
        inert=exporter.render(preflight,'CI_REHEARSAL')
        def rejects(sql,reason):
            try:
                with conn.transaction():
                    with conn.cursor() as cur:cur.execute(sql)
            except psycopg.errors.RaiseException as exc:
                if reason not in str(exc):raise
            else:raise RuntimeError('expected fail-closed rejection '+reason)
        rejects(inert,'authorization absent')
        class IntentionalRollback(Exception):pass
        try:
            with conn.transaction():
                with conn.cursor() as cur:
                    cur.execute("UPDATE atlas.claim SET summary='CI unsupported replacement' WHERE claim_id='c3084bb0-f281-4f59-93c4-a4672c9b272b'")
                rejects(authorized,'frozen governed state drift: claim_ids')
                raise IntentionalRollback()
        except IntentionalRollback:pass
        try:
            with conn.transaction():
                with conn.cursor() as cur:
                    cur.execute(authorized)
                    verify_published(cur,canonical)
                    verify_serving(cur,serving)
                    cur.execute("SELECT release_version FROM audit.release_channel WHERE channel_code='public_mvp_preview'")
                    if cur.fetchone()[0]!='v0.8.1-public-mvp-v2':raise RuntimeError('registration moved channel')
                rejects(authorized,'release replay/collision')
                raise IntentionalRollback()
        except IntentionalRollback:pass
        try:
            with conn.transaction():
                with conn.cursor() as cur:
                    cur.execute(exporter.render(preflight,'CI_REHEARSAL',True,True))
                    verify_published(cur,canonical);verify_serving(cur,serving)
                    cur.execute("SELECT release_version FROM audit.release_channel WHERE channel_code='public_mvp_preview'")
                    if cur.fetchone()[0]!=exporter.SERVING:raise RuntimeError('cutover compare-and-set failed')
                raise IntentionalRollback()
        except IntentionalRollback:pass
        with conn.cursor() as cur:
            cur.execute("SELECT count(*) FROM audit.release_manifest WHERE release_version IN ('v0.8.2','v0.8.2-public-mvp-v1')")
            if cur.fetchone()[0]!=0:raise RuntimeError('rollback left release rows')
            for key,(table,col,group) in MEMBERSHIP_TABLES.items():
                cur.execute(f"SELECT count(*) FROM {table} WHERE release_version IN ('v0.8.2','v0.8.2-public-mvp-v1')")
                if cur.fetchone()[0]!=0:raise RuntimeError('rollback left typed membership '+key)
            for key,q in exporter.preflight_queries(authority).items():
                cur.execute(q)
                if cur.fetchone()[1] is not True:raise RuntimeError('rollback changed governed state '+key)
    print(json.dumps({'status':'PASS','canonical_claims':92,'case_slots':65,'controls':['inert_default','object_drift_rejection','exact_canonical_and_serving_registration','registration_channel_unchanged','explicit_cutover_compare_and_set','replay_rejection','full_rollback']}))

if __name__=='__main__':main()
