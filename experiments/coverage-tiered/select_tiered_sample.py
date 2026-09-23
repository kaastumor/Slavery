#!/usr/bin/env python3
"""Freeze COV-003's tiered 24-target sample from pinned Cliopatria."""

from __future__ import annotations
import argparse, hashlib, json, zipfile
from pathlib import Path
from typing import Any, Iterable

EXPECTED_SHA256="d01ae3a20d358cc5d54f69d9d725d390767d9c8759ac89ad6f90c58d106f3370"
EXPECTED_FEATURES=13765
COV1_SEED="COV-001|ac73a560|cliopatria-ad28a691|2026-09-23"
ANCHORS=(-500,500,1300,1800)

def sha256_file(path:Path)->str:
    h=hashlib.sha256()
    with path.open("rb") as fh:
        for chunk in iter(lambda:fh.read(1024*1024),b""): h.update(chunk)
    return h.hexdigest()

def iter_positions(coords:Any)->Iterable[tuple[float,float]]:
    if not isinstance(coords,list): return
    if len(coords)>=2 and isinstance(coords[0],(int,float)) and isinstance(coords[1],(int,float)):
        yield float(coords[0]),float(coords[1]); return
    for item in coords: yield from iter_positions(item)

def midpoint(geometry:dict[str,Any])->tuple[float,float]|None:
    pts=list(iter_positions(geometry.get("coordinates")))
    if not pts: return None
    xs=[p[0] for p in pts]; ys=[p[1] for p in pts]
    return ((min(xs)+max(xs))/2,(min(ys)+max(ys))/2)

def sector(lon:float,lat:float)->str:
    if lon < -30: return "A" if lat>=0 else "B"
    if lon < 60: return "C" if lat<30 else "D"
    if lon < 100: return "E"
    return "F"

def active(p:dict[str,Any],year:int)->bool:
    try: return int(p["FromYear"])<=year<=int(p["ToYear"])
    except (KeyError,TypeError,ValueError): return False

def eligible(f:dict[str,Any],year:int)->bool:
    p=f.get("properties") or {}; name=str(p.get("Name") or "")
    return p.get("Type")=="POLITY" and not str(p.get("Components") or "").strip() and not name.startswith("(") and active(p,year) and bool(f.get("geometry"))

def cov1_digest(year:int,sec:str,ordinal:int,p:dict[str,Any])->str:
    raw="|".join([COV1_SEED,str(year),sec,str(ordinal),str(p.get("Name") or ""),str(p.get("FromYear") or ""),str(p.get("ToYear") or "")])
    return hashlib.sha256(raw.encode()).hexdigest()

def load(path:Path)->dict[str,Any]:
    got=sha256_file(path)
    if got!=EXPECTED_SHA256: raise SystemExit(f"source SHA mismatch: {got}")
    with zipfile.ZipFile(path) as z:
        members=[n for n in z.namelist() if n.lower().endswith((".geojson",".json")) and not n.startswith("__MACOSX/")]
        if len(members)!=1: raise SystemExit(f"expected one data member: {members}")
        data=json.loads(z.read(members[0]))
    if len(data.get("features") or [])!=EXPECTED_FEATURES: raise SystemExit("feature count mismatch")
    return data

def build(data:dict[str,Any])->dict[str,Any]:
    strata={}
    for year in ANCHORS:
        for sec in "ABCDEF":
            cand=[]
            for ordinal,f in enumerate(data["features"]):
                if not eligible(f,year): continue
                mid=midpoint(f["geometry"])
                if mid is None or sector(*mid)!=sec: continue
                p=f["properties"]
                cand.append((cov1_digest(year,sec,ordinal,p),ordinal,p,mid))
            cand.sort(key=lambda x:x[0])
            if len(cand)>=10: strata[f"{year}:{sec}"]=cand

    ordered=sorted(strata,key=lambda cell:hashlib.sha256(f"COV-003-BATCH|{cell}".encode()).hexdigest())
    selected=ordered[:3]
    batches=[]
    for cell in selected:
        year_s,sec=cell.split(":"); year=int(year_s); cand=strata[cell]
        targets=[]
        for rank in range(3,11):
            digest,ordinal,p,mid=cand[rank-1]
            tier="C1" if rank<=6 else "C0"
            targets.append({
                "target_id":f"COV3:{cell}:r{rank}",
                "stratum":cell,
                "anchor_source_year":year,
                "sector":sec,
                "candidate_count":len(cand),
                "selection_rank":rank,
                "selection_digest":digest,
                "tier_assignment":tier,
                "source_row_ordinal":ordinal,
                "source_name":p.get("Name"),
                "source_type":p.get("Type"),
                "source_from_year":p.get("FromYear"),
                "source_to_year":p.get("ToYear"),
                "source_seshat_id":p.get("SeshatID"),
                "source_wikidata":p.get("Wikidata"),
                "sampling_bbox_midpoint":list(mid),
                "identity_validation_state":"identity_unreviewed",
                "research_state":"research_not_performed" if tier=="C0" else "research_planned",
                "reviewed_through":None,
                "release_id":"COV-003-exp-v0"
            })
        ranked_identity=sorted(targets,key=lambda t:hashlib.sha256(f"COV-003-IDENTITY|{t['source_row_ordinal']}".encode()).hexdigest())
        identity_ids={t["target_id"] for t in ranked_identity[:2]}
        for t in targets: t["identity_validation_selected"]=t["target_id"] in identity_ids
        batches.append({"stratum":cell,"batch_digest":hashlib.sha256(f"COV-003-BATCH|{cell}".encode()).hexdigest(),"targets":targets})

    flat=[t for b in batches for t in b["targets"]]
    return {
        "experiment":"COV-003",
        "purpose":"tiered completeness architecture sample; neutral to slavery evidence",
        "source_sha256":EXPECTED_SHA256,
        "eligible_strata_with_10_plus":len(strata),
        "selected_batches":selected,
        "target_count":len(flat),
        "c0_only_count":sum(t["tier_assignment"]=="C0" for t in flat),
        "c1_count":sum(t["tier_assignment"]=="C1" for t in flat),
        "identity_validation_sample_count":sum(t["identity_validation_selected"] for t in flat),
        "viable":len(selected)==3 and len(flat)==24,
        "batches":batches
    }

def main()->None:
    ap=argparse.ArgumentParser()
    ap.add_argument("source_zip",type=Path)
    ap.add_argument("--output",type=Path,required=True)
    a=ap.parse_args()
    out=build(load(a.source_zip))
    a.output.parent.mkdir(parents=True,exist_ok=True)
    a.output.write_text(json.dumps(out,indent=2,ensure_ascii=False)+"\n",encoding="utf-8")
    print(json.dumps({"selected_batches":out["selected_batches"],"target_count":out["target_count"],"c1_count":out["c1_count"],"identity_validation_sample_count":out["identity_validation_sample_count"],"viable":out["viable"]},indent=2))

if __name__=="__main__": main()
