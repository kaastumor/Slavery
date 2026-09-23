#!/usr/bin/env python3
"""Profile a pinned Cliopatria corpus without promoting geometry into atlas state."""
from __future__ import annotations
import argparse, hashlib, io, json, urllib.request, zipfile
from collections import Counter
from pathlib import Path
UPSTREAM_REPO="Seshat-Global-History-Databank/cliopatria"
UPSTREAM_RELEASE="v0.2.0-duplicate"
UPSTREAM_COMMIT="ad28a691b7c07c1fca89d0e0636d324667d2a258"
UPSTREAM_PATH="cliopatria.geojson.zip"
UPSTREAM_URL=f"https://raw.githubusercontent.com/{UPSTREAM_REPO}/{UPSTREAM_COMMIT}/{UPSTREAM_PATH}"
UPSTREAM_GIT_BLOB_SHA1="cefab0f4b622e2e7fb3daf68d4f461f83991204c"
def git_blob_sha1(data): return hashlib.sha1(f"blob {len(data)}\0".encode()+data).hexdigest()
def load_features(data):
    with zipfile.ZipFile(io.BytesIO(data)) as z:
        names=[n for n in z.namelist() if n.lower().endswith('.geojson') and not n.startswith('__MACOSX/') and not Path(n).name.startswith('._')]
        if len(names)!=1: raise ValueError(f"expected one data GeoJSON member after metadata filtering, found {names}")
        obj=json.loads(z.read(names[0]))
    if obj.get('type')!='FeatureCollection': raise ValueError('not a FeatureCollection')
    return obj['features']
def profile(features):
    types=Counter(); geoms=Counter(); keys=Counter(); names=set(); lo=hi=None; neg=cross=zero_endpoint=bad=0
    for f in features:
        p=f.get('properties') or {}; keys.update(p.keys()); types[str(p.get('Type','<missing>'))]+=1
        geoms[str((f.get('geometry') or {}).get('type','<missing>'))]+=1
        if p.get('Name') is not None: names.add(str(p['Name']))
        a,b=p.get('FromYear'),p.get('ToYear')
        if isinstance(a,int) and isinstance(b,int):
            lo=a if lo is None else min(lo,a); hi=b if hi is None else max(hi,b)
            neg+=int(a<0 or b<0); cross+=int(a<0<b); zero_endpoint+=int(a==0 or b==0); bad+=int(a>b)
    return {'feature_count':len(features),'distinct_names':len(names),'type_counts':dict(sorted(types.items())),
      'geometry_type_counts':dict(sorted(geoms.items())),'property_presence_counts':dict(sorted(keys.items())),
      'source_native_years':{'minimum':lo,'maximum':hi,'rows_with_negative_year':neg,'rows_crossing_numeric_zero':cross,
      'rows_with_zero_endpoint':zero_endpoint,'invalid_from_to_ranges':bad,'interpretation':'preserved source-native signed integers; negative=BCE, positive=CE; no atlas normalization performed'}}
def main():
    ap=argparse.ArgumentParser(); ap.add_argument('--input',type=Path); ap.add_argument('--output',type=Path); a=ap.parse_args()
    data=a.input.read_bytes() if a.input else urllib.request.urlopen(UPSTREAM_URL,timeout=60).read()
    blob=git_blob_sha1(data)
    if blob!=UPSTREAM_GIT_BLOB_SHA1: raise SystemExit(f"upstream blob mismatch: expected {UPSTREAM_GIT_BLOB_SHA1}, got {blob}")
    out={'source':{'repository':UPSTREAM_REPO,'release':UPSTREAM_RELEASE,'commit':UPSTREAM_COMMIT,'path':UPSTREAM_PATH,'url':UPSTREAM_URL,
      'git_blob_sha1':blob,'sha256':hashlib.sha256(data).hexdigest()},'profile':profile(load_features(data)),'promotion':'none; raw geography profile only'}
    text=json.dumps(out,indent=2,sort_keys=True)+'\n'
    a.output.write_text(text,encoding='utf-8') if a.output else print(text,end='')
if __name__=='__main__': main()
