#!/usr/bin/env python3
"""Profile a pinned Cliopatria corpus without promoting geometry into atlas state."""
from __future__ import annotations
import argparse, hashlib, io, json, urllib.request, zipfile
from collections import Counter, defaultdict
from pathlib import Path

UPSTREAM_REPO="Seshat-Global-History-Databank/cliopatria"
UPSTREAM_RELEASE="v0.2.0-duplicate"
UPSTREAM_COMMIT="ad28a691b7c07c1fca89d0e0636d324667d2a258"
UPSTREAM_PATH="cliopatria.geojson.zip"
UPSTREAM_URL=f"https://raw.githubusercontent.com/{UPSTREAM_REPO}/{UPSTREAM_COMMIT}/{UPSTREAM_PATH}"
UPSTREAM_GIT_BLOB_SHA1="cefab0f4b622e2e7fb3daf68d4f461f83991204c"

def git_blob_sha1(data):
    return hashlib.sha1(f"blob {len(data)}\0".encode()+data).hexdigest()

def load_features(data):
    with zipfile.ZipFile(io.BytesIO(data)) as z:
        names=[n for n in z.namelist() if n.lower().endswith('.geojson') and not n.startswith('__MACOSX/') and not Path(n).name.startswith('._')]
        if len(names)!=1:
            raise ValueError(f"expected one data GeoJSON member after metadata filtering, found {names}")
        obj=json.loads(z.read(names[0]))
    if obj.get('type')!='FeatureCollection':
        raise ValueError('not a FeatureCollection')
    return obj['features']

def _present(value):
    return value not in (None, "", [], {})

def _row_summary(feature):
    p=feature.get("properties") or {}
    return {
        key:p.get(key)
        for key in ("Name","Type","FromYear","ToYear","MemberOf","Components","SeshatID","Wikidata","Wikipedia")
    }

def semantic_diagnostics(features):
    rows=[_row_summary(f) for f in features]
    by_name=defaultdict(list)
    for row in rows:
        by_name[str(row.get("Name"))].append(row)

    zero_rows=[]
    for row in rows:
        if row.get("FromYear")==0 or row.get("ToYear")==0:
            ordered=sorted(
                by_name[str(row.get("Name"))],
                key=lambda r:(
                    r.get("FromYear") if isinstance(r.get("FromYear"),int) else 10**9,
                    r.get("ToYear") if isinstance(r.get("ToYear"),int) else 10**9,
                    str(r.get("Type")),
                )
            )
            idx=ordered.index(row)
            zero_rows.append({
                "row":row,
                "previous_same_name":ordered[idx-1] if idx>0 else None,
                "next_same_name":ordered[idx+1] if idx+1<len(ordered) else None,
            })

    relations=[r for r in rows if r.get("Type")=="RELATION"]
    membership={
        "rows_with_member_of":sum(_present(r.get("MemberOf")) for r in rows),
        "rows_with_components":sum(_present(r.get("Components")) for r in rows),
        "rows_with_both":sum(_present(r.get("MemberOf")) and _present(r.get("Components")) for r in rows),
        "top_level_rows_member_of_empty":sum(not _present(r.get("MemberOf")) for r in rows),
        "leaf_rows_components_empty":sum(not _present(r.get("Components")) for r in rows),
        "relation_rows_with_member_of":sum(_present(r.get("MemberOf")) for r in relations),
        "relation_rows_with_components":sum(_present(r.get("Components")) for r in relations),
        "relation_rows_with_both":sum(_present(r.get("MemberOf")) and _present(r.get("Components")) for r in relations),
    }

    relation_value_types={
        "MemberOf":dict(sorted(Counter(type(r.get("MemberOf")).__name__ for r in relations).items())),
        "Components":dict(sorted(Counter(type(r.get("Components")).__name__ for r in relations).items())),
    }

    def split_semicolon(value):
        if not _present(value):
            return []
        return [part.strip() for part in str(value).split(";") if part.strip()]

    member_of_arities=Counter(len(split_semicolon(r.get("MemberOf"))) for r in rows if _present(r.get("MemberOf")))
    component_arities=Counter(len(split_semicolon(r.get("Components"))) for r in rows if _present(r.get("Components")))
    nested_composite_samples=[
        r for r in rows
        if _present(r.get("MemberOf")) and _present(r.get("Components"))
    ][:20]

    adjacency=Counter()
    overlap_examples=[]
    gap_examples=[]
    for name,name_rows in by_name.items():
        comparable=[r for r in name_rows if isinstance(r.get("FromYear"),int) and isinstance(r.get("ToYear"),int)]
        comparable.sort(key=lambda r:(r["FromYear"],r["ToYear"],str(r.get("Type")),str(r.get("MemberOf")),str(r.get("Components"))))
        for left,right in zip(comparable,comparable[1:]):
            if right["FromYear"]<=left["ToYear"]:
                adjacency["inclusive_overlap_or_parallel"]+=1
                if len(overlap_examples)<20:
                    overlap_examples.append({"name":name,"left":left,"right":right})
            elif right["FromYear"]==left["ToYear"]+1:
                adjacency["integer_contiguous"]+=1
            else:
                adjacency["gap_more_than_one_integer"]+=1
                if len(gap_examples)<20:
                    gap_examples.append({"name":name,"left":left,"right":right})

    relation_samples=sorted(
        relations,
        key=lambda r:(str(r.get("Name")),r.get("FromYear") if isinstance(r.get("FromYear"),int) else 10**9,r.get("ToYear") if isinstance(r.get("ToYear"),int) else 10**9)
    )[:20]

    return {
        "zero_endpoint_rows":sorted(
            zero_rows,
            key=lambda x:(
                x["row"].get("FromYear") if isinstance(x["row"].get("FromYear"),int) else 10**9,
                x["row"].get("ToYear") if isinstance(x["row"].get("ToYear"),int) else 10**9,
                str(x["row"].get("Name")),
            )
        ),
        "membership":membership,
        "relation_value_types":relation_value_types,
        "relation_name_parenthesized_count":sum(
            str(r.get("Name","")).startswith("(") and str(r.get("Name","")).endswith(")")
            for r in relations
        ),
        "member_of_arity_counts":dict(sorted(member_of_arities.items())),
        "component_arity_counts":dict(sorted(component_arities.items())),
        "nested_composite_samples":nested_composite_samples,
        "relation_samples":relation_samples,
        "same_name_interval_adjacency":dict(sorted(adjacency.items())),
        "same_name_overlap_examples":overlap_examples,
        "same_name_gap_examples":gap_examples,
    }

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
    return {
        'feature_count':len(features),
        'distinct_names':len(names),
        'type_counts':dict(sorted(types.items())),
        'geometry_type_counts':dict(sorted(geoms.items())),
        'property_presence_counts':dict(sorted(keys.items())),
        'source_native_years':{
            'minimum':lo,
            'maximum':hi,
            'rows_with_negative_year':neg,
            'rows_crossing_numeric_zero':cross,
            'rows_with_zero_endpoint':zero_endpoint,
            'invalid_from_to_ranges':bad,
            'interpretation':'preserved source-native signed integers; negative=BCE, positive=CE; no atlas normalization performed'
        },
        'semantic_diagnostics':semantic_diagnostics(features),
    }

def main():
    ap=argparse.ArgumentParser()
    ap.add_argument('--input',type=Path)
    ap.add_argument('--output',type=Path)
    a=ap.parse_args()
    data=a.input.read_bytes() if a.input else urllib.request.urlopen(UPSTREAM_URL,timeout=60).read()
    blob=git_blob_sha1(data)
    if blob!=UPSTREAM_GIT_BLOB_SHA1:
        raise SystemExit(f"upstream blob mismatch: expected {UPSTREAM_GIT_BLOB_SHA1}, got {blob}")
    out={
        'source':{
            'repository':UPSTREAM_REPO,
            'release':UPSTREAM_RELEASE,
            'commit':UPSTREAM_COMMIT,
            'path':UPSTREAM_PATH,
            'url':UPSTREAM_URL,
            'git_blob_sha1':blob,
            'sha256':hashlib.sha256(data).hexdigest()
        },
        'profile':profile(load_features(data)),
        'promotion':'none; raw geography profile only'
    }
    text=json.dumps(out,indent=2,sort_keys=True)+'\n'
    a.output.write_text(text,encoding='utf-8') if a.output else print(text,end='')

if __name__=='__main__':
    main()
