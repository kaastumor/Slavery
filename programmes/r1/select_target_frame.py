#!/usr/bin/env python3
"""Freeze R1's neutral target frame before slavery/coercion research.

This script selects:
- new polity C0/C1 targets from the exact pinned Cliopatria corpus;
- new non-polity C0/C1 targets from the frozen COV-004 neutral candidate universe,
  excluding targets already researched in COV-004;
- a legacy C1 promotion cohort from prior experimental rows for Core Contract re-review.

Selection uses no slavery/coercion evidence.
"""

from __future__ import annotations
import argparse, hashlib, json, zipfile
from collections import Counter
from pathlib import Path
from typing import Any, Iterable

EXPECTED_SHA256="d01ae3a20d358cc5d54f69d9d725d390767d9c8759ac89ad6f90c58d106f3370"
EXPECTED_FEATURES=13765
SOURCE_COMMIT="ad28a691b7c07c1fca89d0e0636d324667d2a258"
SEED="R1|core-v1|cliopatria-ad28a691|2026-09-23"
SOURCE_ANCHORS=(-2000,-500,500,1300,1800)
NEW_POLITY_C1=16
NEW_NONPOLITY_C1_PER_CLASS=2
LEGACY_POLITY_POSITIVE=4
LEGACY_POLITY_INCONCLUSIVE=4
LEGACY_NONPOLITY=4

STRUCTURALLY_INVALID_LEGACY={
    "1300:C",          # Mahdids anchor/identity mismatch
    "COV2:1800:A",     # New Netherland at 1800
    "COV2:1800:D",     # medieval Kingdom of Georgia at 1800
    "COV2:500:E",      # Western Regions protectorate at 500
}

def sha(text:str)->str:
    return hashlib.sha256(text.encode("utf-8")).hexdigest()

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

def midpoint(g:dict[str,Any])->tuple[float,float]|None:
    pts=list(iter_positions(g.get("coordinates")))
    if not pts:return None
    xs=[p[0] for p in pts];ys=[p[1] for p in pts]
    return ((min(xs)+max(xs))/2,(min(ys)+max(ys))/2)

def sector(lon:float,lat:float)->str:
    if lon < -30: return "A" if lat>=0 else "B"
    if lon < 60: return "C" if lat<30 else "D"
    if lon < 100: return "E"
    return "F"

def active(p:dict[str,Any],year:int)->bool:
    try:return int(p["FromYear"])<=year<=int(p["ToYear"])
    except (KeyError,TypeError,ValueError):return False

def eligible(f:dict[str,Any],year:int)->bool:
    p=f.get("properties") or {};name=str(p.get("Name") or "")
    return p.get("Type")=="POLITY" and not str(p.get("Components") or "").strip() and not name.startswith("(") and active(p,year) and bool(f.get("geometry"))

def atlas_year_from_source(source_year:int)->int:
    # D-059: atlas y<=0 queries source y-1. Inverse for negative source years.
    return source_year+1 if source_year<0 else source_year

def display_year(source_year:int)->str:
    return f"{abs(source_year)} BCE" if source_year<0 else f"{source_year} CE"

def load_cliopatria(path:Path)->dict[str,Any]:
    got=sha256_file(path)
    if got!=EXPECTED_SHA256: raise SystemExit(f"source SHA mismatch: {got}")
    with zipfile.ZipFile(path) as z:
        members=[n for n in z.namelist() if n.lower().endswith((".geojson",".json")) and not n.startswith("__MACOSX/")]
        if len(members)!=1:raise SystemExit(f"expected one data member: {members}")
        data=json.loads(z.read(members[0]))
    if len(data.get("features") or [])!=EXPECTED_FEATURES:raise SystemExit("feature count mismatch")
    return data

def prior_ordinals(repo_root:Path)->dict[str,set[int]]:
    out:dict[str,set[int]]={}
    def add(cell,ordinal):
        if cell is None or ordinal is None:return
        out.setdefault(str(cell),set()).add(int(ordinal))

    p=json.loads((repo_root/"experiments/coverage-value/sample.json").read_text(encoding="utf-8"))
    for r in p["cells"]:
        if r.get("status")=="selected":add(r["cell_id"],r.get("source_row_ordinal"))

    p=json.loads((repo_root/"experiments/coverage-scale/expansion_sample.json").read_text(encoding="utf-8"))
    for r in p["cells"]:
        add(r.get("cell_id"),r.get("source_row_ordinal"))

    p=json.loads((repo_root/"experiments/coverage-tiered/tiered_sample.json").read_text(encoding="utf-8"))
    for b in p["batches"]:
        for r in b["targets"]:
            add(r.get("stratum"),r.get("source_row_ordinal"))
    return out

def polity_frame(data:dict[str,Any],repo_root:Path)->tuple[list[dict[str,Any]],list[dict[str,Any]]]:
    used=prior_ordinals(repo_root)
    cells=[]
    features=data["features"]
    for year in SOURCE_ANCHORS:
        for sec in "ABCDEF":
            candidates=[]
            for ordinal,f in enumerate(features):
                if not eligible(f,year):continue
                m=midpoint(f["geometry"])
                if m is None or sector(*m)!=sec:continue
                if ordinal in used.get(f"{year}:{sec}",set()):continue
                p=f["properties"]
                digest=sha("|".join([SEED,"POLITY",str(year),sec,str(ordinal),str(p.get("Name") or ""),str(p.get("FromYear") or ""),str(p.get("ToYear") or "")]))
                candidates.append((digest,ordinal,p,m))
            candidates.sort(key=lambda x:x[0])
            picks=[]
            for rank,x in enumerate(candidates[:2],start=1):
                digest,ordinal,p,m=x
                picks.append({
                    "target_id":f"R1:P:{year}:{sec}:r{rank}",
                    "frame_origin":"new_systematic_polity",
                    "tier":"C0",
                    "cell_id":f"{year}:{sec}",
                    "source_anchor_year":year,
                    "atlas_anchor_year":atlas_year_from_source(year),
                    "display_anchor":display_year(year),
                    "sampling_sector":sec,
                    "candidate_count_after_prior_exclusion":len(candidates),
                    "selection_rank":rank,
                    "selection_digest":digest,
                    "source_row_ordinal":ordinal,
                    "source_name":p.get("Name"),
                    "source_from_year":p.get("FromYear"),
                    "source_to_year":p.get("ToYear"),
                    "source_seshat_id":p.get("SeshatID"),
                    "source_wikidata":p.get("Wikidata"),
                    "sampling_bbox_midpoint":list(m),
                    "research_stage":"not_researched",
                    "classification_outcome":"unassessed",
                    "interpretation":"Registered target; historical slavery/coercion research not yet performed."
                })
            cells.append({
                "cell_id":f"{year}:{sec}","source_anchor_year":year,"sector":sec,
                "candidate_count_after_prior_exclusion":len(candidates),
                "status":"selected" if picks else "sampling_gap",
                "targets":picks
            })

    eligible_cells=[c for c in cells if c["targets"]]
    # Deterministic balanced cell choice for 16 new polity C1 rows.
    cell_digest={c["cell_id"]:sha(f"{SEED}|C1CELL|{c['cell_id']}") for c in eligible_cells}
    chosen=[]
    ac=Counter();sc=Counter()
    def can(c):
        return ac[c["source_anchor_year"]]<4 and sc[c["sector"]]<4
    def add(c):
        if c["cell_id"] in {x["cell_id"] for x in chosen}:return False
        if not can(c):return False
        chosen.append(c);ac[c["source_anchor_year"]]+=1;sc[c["sector"]]+=1;return True

    # Cover every anchor that has candidates.
    for year in SOURCE_ANCHORS:
        opts=sorted([c for c in eligible_cells if c["source_anchor_year"]==year],key=lambda c:cell_digest[c["cell_id"]])
        for c in opts:
            if add(c):break
    # Cover every sector that has candidates.
    for sec in "ABCDEF":
        if sc[sec]:continue
        opts=sorted([c for c in eligible_cells if c["sector"]==sec],key=lambda c:cell_digest[c["cell_id"]])
        for c in opts:
            if add(c):break
    # Fill to target under caps.
    for c in sorted(eligible_cells,key=lambda c:cell_digest[c["cell_id"]]):
        if len(chosen)>=NEW_POLITY_C1:break
        add(c)

    if len(chosen)<NEW_POLITY_C1:
        raise SystemExit(f"could select only {len(chosen)} balanced polity C1 cells")

    c1ids=set()
    for c in chosen:
        t=c["targets"][0]
        t["tier"]="C1"
        t["research_stage"]="not_researched"
        t["classification_outcome"]="unassessed"
        t["c1_selection_digest"]=cell_digest[c["cell_id"]]
        c1ids.add(t["target_id"])

    flat=[t for c in cells for t in c["targets"]]
    return cells,[t for t in flat if t["target_id"] in c1ids]

def nonpolity_frame(repo_root:Path)->tuple[list[dict[str,Any]],list[dict[str,Any]]]:
    pool=json.loads((repo_root/"experiments/falsification-atlas/06_NONPOLITY_CANDIDATE_POOL.json").read_text(encoding="utf-8"))
    prev=json.loads((repo_root/"experiments/falsification-atlas/07_NONPOLITY_SELECTION.json").read_text(encoding="utf-8"))
    researched={x["id"] for x in prev if x.get("tier")=="C1"}
    c0=[];c1=[]
    for cls,items in pool["classes"].items():
        available=[x for x in items if x[0] not in researched]
        if len(available)<6:raise SystemExit(f"{cls}: expected >=6 unresearched candidates, got {len(available)}")
        # All six unresearched candidates form R1 C0 frame.
        rows=[]
        for candidate_id,name,year in available:
            row={
                "target_id":f"R1:N:{candidate_id}",
                "source_candidate_id":candidate_id,
                "target_label":name,
                "anchor_year":year,
                "frame_class":cls,
                "frame_origin":"new_systematic_nonpolity",
                "tier":"C0",
                "selection_digest":sha(f"{SEED}|NONPOLITY|{cls}|{candidate_id}"),
                "research_stage":"not_researched",
                "classification_outcome":"unassessed",
                "interpretation":"Registered target; historical slavery/coercion research not yet performed."
            }
            rows.append(row)
        rows.sort(key=lambda r:r["selection_digest"])
        c0.extend(rows)
        for row in sorted(rows,key=lambda r:sha(f"{SEED}|NONPOLITY-C1|{r['source_candidate_id']}"))[:NEW_NONPOLITY_C1_PER_CLASS]:
            row["tier"]="C1"
            row["c1_selection_digest"]=sha(f"{SEED}|NONPOLITY-C1|{row['source_candidate_id']}")
            c1.append(row)
    return c0,c1

def legacy_cohort(repo_root:Path)->list[dict[str,Any]]:
    full=json.loads((repo_root/"experiments/coverage-scale/full_37.json").read_text(encoding="utf-8"))
    np=json.loads((repo_root/"experiments/falsification-atlas/11_ARM_B_C1.json").read_text(encoding="utf-8"))["rows"]

    polity=[r for r in full if r.get("cell_id") not in STRUCTURALLY_INVALID_LEGACY and not str(r.get("cell_id","")).startswith("NP-")]
    positive=[r for r in polity if r.get("coverage_outcome") in {"bounded_supported","materially_disputed"}]
    inconclusive=[r for r in polity if r.get("coverage_outcome")=="researched_inconclusive"]
    positive=sorted(positive,key=lambda r:sha(f"{SEED}|LEGACY-POS|{r['cell_id']}"))[:LEGACY_POLITY_POSITIVE]
    inconclusive=sorted(inconclusive,key=lambda r:sha(f"{SEED}|LEGACY-INC|{r['cell_id']}"))[:LEGACY_POLITY_INCONCLUSIVE]
    nonpolity=sorted(np,key=lambda r:sha(f"{SEED}|LEGACY-NP|{r['target_id']}"))[:LEGACY_NONPOLITY]
    out=[]
    for r in positive+inconclusive:
        out.append({
            "legacy_ref":r["cell_id"],"target_label":r["target_label"],"anchor_year":r["anchor_year"],
            "legacy_outcome":r["coverage_outcome"],"frame_origin":"legacy_promotion_polity",
            "sampling_sector":(r.get("source_sample") or {}).get("sampling_sector"),
            "tier":"C1","promotion_state":"requires_core_v1_rereview",
            "selection_digest":sha(f"{SEED}|LEGACY|{r['cell_id']}")
        })
    for r in nonpolity:
        out.append({
            "legacy_ref":r["target_id"],"target_label":r["target_label"],"anchor_year":r["anchor_year"],
            "legacy_outcome":r["coverage_outcome"],"frame_origin":"legacy_promotion_nonpolity",
            "tier":"C1","promotion_state":"requires_core_v1_rereview",
            "selection_digest":sha(f"{SEED}|LEGACY|{r['target_id']}")
        })
    return out

def build(data:dict[str,Any],repo_root:Path)->dict[str,Any]:
    polity_cells,polity_c1=polity_frame(data,repo_root)
    polity_c0=[t for c in polity_cells for t in c["targets"]]
    non_c0,non_c1=nonpolity_frame(repo_root)
    legacy=legacy_cohort(repo_root)
    c1_new=polity_c1+non_c1

    anchors=sorted({x.get("source_anchor_year",x.get("anchor_year")) for x in c1_new})
    new_polity_sectors=sorted({x["sampling_sector"] for x in polity_c1})
    legacy_polity_sectors=[x.get("sampling_sector") for x in legacy if x.get("frame_origin")=="legacy_promotion_polity" and x.get("sampling_sector")]
    release_polity_sectors=sorted(set(new_polity_sectors)|set(legacy_polity_sectors))
    release_sector_counts=Counter([x["sampling_sector"] for x in polity_c1] + legacy_polity_sectors)
    frame_classes=sorted({"polity"}|{x["frame_class"] for x in non_c1})
    polity_sampling_gaps=[c["cell_id"] for c in polity_cells if not c["targets"]]

    required_balance_gates={
        "all_five_source_anchor_bands_represented":all(y in anchors for y in SOURCE_ANCHORS),
        "all_six_release_polity_sampling_sectors_represented":all(s in release_polity_sectors for s in "ABCDEF"),
        "at_least_three_frame_classes":len(frame_classes)>=3,
        "no_release_polity_sector_exceeds_25pct_of_planned_c1":all(n/(len(c1_new)+len(legacy))<=0.25 for n in release_sector_counts.values()),
    }

    result={
      "programme":"R1",
      "purpose":"target-frame freeze before slavery/coercion research",
      "source":{
        "cliopatria_commit":SOURCE_COMMIT,"cliopatria_sha256":EXPECTED_SHA256,
        "cliopatria_features":EXPECTED_FEATURES,
        "nonpolity_candidate_source":"experiments/falsification-atlas/06_NONPOLITY_CANDIDATE_POOL.json"
      },
      "calendar_note":"Negative Cliopatria source-native anchors are converted to Atlas astronomical internal years; source -500 = display 500 BCE = Atlas internal -499.",
      "source_anchor_years":list(SOURCE_ANCHORS),
      "polity_cells":polity_cells,
      "new_polity_c0":polity_c0,
      "new_polity_c1_ids":[x["target_id"] for x in polity_c1],
      "new_nonpolity_c0":non_c0,
      "new_nonpolity_c1_ids":[x["target_id"] for x in non_c1],
      "legacy_promotion_c1":legacy,
      "counts":{
        "new_polity_c0":len(polity_c0),
        "new_nonpolity_c0":len(non_c0),
        "new_c0_total":len(polity_c0)+len(non_c0),
        "new_polity_c1":len(polity_c1),
        "new_nonpolity_c1":len(non_c1),
        "new_c1_total":len(c1_new),
        "legacy_c1":len(legacy),
        "planned_c1_total":len(c1_new)+len(legacy)
      },
      "balance_check":{
        "new_c1_source_anchors":anchors,
        "new_polity_c1_sectors":new_polity_sectors,
        "legacy_polity_c1_sectors":sorted(set(legacy_polity_sectors)),
        "release_polity_c1_sectors":release_polity_sectors,
        "release_polity_sector_counts":dict(sorted(release_sector_counts.items())),
        "new_c1_frame_classes":frame_classes,
        "new_polity_sampling_gaps":polity_sampling_gaps,
        "new_polity_sector_b_gap_preserved":"B" not in new_polity_sectors,
        "required_gates":required_balance_gates
      },
      "hard_rule":"No target substitution after slavery/coercion evidence is inspected. Sampling gaps remain gaps."
    }
    if result["counts"]["planned_c1_total"]>36:raise SystemExit("C1 ceiling exceeded")
    if result["counts"]["new_c0_total"]>120:raise SystemExit("C0 ceiling exceeded")
    return result

def main():
    ap=argparse.ArgumentParser()
    ap.add_argument("source_zip",type=Path)
    ap.add_argument("--repo-root",type=Path,default=Path("."))
    ap.add_argument("--output",type=Path,required=True)
    a=ap.parse_args()
    out=build(load_cliopatria(a.source_zip),a.repo_root)
    a.output.parent.mkdir(parents=True,exist_ok=True)
    a.output.write_text(json.dumps(out,indent=2,ensure_ascii=False)+"\n",encoding="utf-8")
    print(json.dumps({
        "counts":out["counts"],
        "balance":out["balance_check"],
        "polity_cell_diagnostics":[
            {
                "cell_id":c["cell_id"],
                "source_anchor_year":c["source_anchor_year"],
                "sector":c["sector"],
                "candidate_count_after_prior_exclusion":c["candidate_count_after_prior_exclusion"],
                "status":c["status"],
                "selected_c1_target_ids":[t["target_id"] for t in c["targets"] if t["tier"]=="C1"],
                "c0_target_ids":[t["target_id"] for t in c["targets"] if t["tier"]=="C0"],
                "target_names":[t["source_name"] for t in c["targets"]],
            }
            for c in out["polity_cells"]
        ],
    },indent=2))
    if not all(out["balance_check"]["required_gates"].values()):
        raise SystemExit(f"balance failed: {out['balance_check']}")

if __name__=="__main__":main()
