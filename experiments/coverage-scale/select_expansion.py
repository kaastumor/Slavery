#!/usr/bin/env python3
"""Freeze COV-002's 12-cell rank-2 expansion cohort from pinned Cliopatria."""

from __future__ import annotations

import argparse
import hashlib
import json
import zipfile
from pathlib import Path
from typing import Any, Iterable

EXPECTED_SHA256 = "d01ae3a20d358cc5d54f69d9d725d390767d9c8759ac89ad6f90c58d106f3370"
EXPECTED_FEATURES = 13_765
COV1_SEED = "COV-001|ac73a560|cliopatria-ad28a691|2026-09-23"
ANCHORS = (-500, 500, 1300, 1800)


def sha256_file(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as fh:
        for chunk in iter(lambda: fh.read(1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest()


def iter_positions(coords: Any) -> Iterable[tuple[float, float]]:
    if not isinstance(coords, list):
        return
    if len(coords) >= 2 and isinstance(coords[0], (int, float)) and isinstance(coords[1], (int, float)):
        yield float(coords[0]), float(coords[1])
        return
    for item in coords:
        yield from iter_positions(item)


def midpoint(geometry: dict[str, Any]) -> tuple[float, float] | None:
    pts = list(iter_positions(geometry.get("coordinates")))
    if not pts:
        return None
    xs=[p[0] for p in pts]; ys=[p[1] for p in pts]
    return ((min(xs)+max(xs))/2.0,(min(ys)+max(ys))/2.0)


def sector(lon: float, lat: float) -> str:
    if lon < -30:
        return "A" if lat >= 0 else "B"
    if lon < 60:
        return "C" if lat < 30 else "D"
    if lon < 100:
        return "E"
    return "F"


def active(props: dict[str, Any], year: int) -> bool:
    try:
        return int(props["FromYear"]) <= year <= int(props["ToYear"])
    except (KeyError,TypeError,ValueError):
        return False


def eligible(feature: dict[str, Any], year: int) -> bool:
    p=feature.get("properties") or {}
    name=str(p.get("Name") or "")
    return (
        p.get("Type")=="POLITY"
        and not str(p.get("Components") or "").strip()
        and not name.startswith("(")
        and active(p,year)
        and bool(feature.get("geometry"))
    )


def cov1_digest(year:int, sec:str, ordinal:int, p:dict[str,Any])->str:
    raw="|".join([COV1_SEED,str(year),sec,str(ordinal),str(p.get("Name") or ""),str(p.get("FromYear") or ""),str(p.get("ToYear") or "")])
    return hashlib.sha256(raw.encode()).hexdigest()


def load(path:Path)->dict[str,Any]:
    got=sha256_file(path)
    if got!=EXPECTED_SHA256:
        raise SystemExit(f"source SHA mismatch: {got}")
    with zipfile.ZipFile(path) as z:
        members=[n for n in z.namelist() if n.lower().endswith((".geojson",".json")) and not n.startswith("__MACOSX/")]
        if len(members)!=1:
            raise SystemExit(f"expected one geojson/json member: {members}")
        data=json.loads(z.read(members[0]))
    if len(data.get("features") or [])!=EXPECTED_FEATURES:
        raise SystemExit("feature count mismatch")
    return data


def build(data:dict[str,Any])->dict[str,Any]:
    by_cell={}
    for year in ANCHORS:
        for sec in "ABCDEF":
            cand=[]
            for ordinal,f in enumerate(data["features"]):
                if not eligible(f,year):
                    continue
                mid=midpoint(f["geometry"])
                if mid is None or sector(*mid)!=sec:
                    continue
                p=f["properties"]
                cand.append((cov1_digest(year,sec,ordinal,p),ordinal,p,mid))
            cand.sort(key=lambda x:x[0])
            if len(cand)>=2:
                by_cell[f"{year}:{sec}"]=cand

    strata=sorted(by_cell, key=lambda cell: hashlib.sha256(f"COV-002-STRATUM|{cell}".encode()).hexdigest())
    chosen=strata[:12]
    rows=[]
    for cell in chosen:
        year_s,sec=cell.split(":"); year=int(year_s)
        cand=by_cell[cell]
        digest,ordinal,p,mid=cand[1]
        rows.append({
            "cell_id":cell,
            "anchor_source_year":year,
            "sector":sec,
            "candidate_count":len(cand),
            "selection_rank":2,
            "selection_digest":digest,
            "source_row_ordinal":ordinal,
            "source_name":p.get("Name"),
            "source_type":p.get("Type"),
            "source_from_year":p.get("FromYear"),
            "source_to_year":p.get("ToYear"),
            "source_seshat_id":p.get("SeshatID"),
            "source_wikidata":p.get("Wikidata"),
            "sampling_bbox_midpoint":list(mid)
        })
    return {
        "experiment":"COV-002",
        "purpose":"rank-2 scale cohort; neutral to slavery evidence",
        "source_sha256":EXPECTED_SHA256,
        "valid_rank2_strata":len(strata),
        "requested_cells":12,
        "selected_cells":len(rows),
        "viable":len(rows)==12,
        "cells":rows
    }


def main()->None:
    ap=argparse.ArgumentParser()
    ap.add_argument("source_zip",type=Path)
    ap.add_argument("--output",type=Path,required=True)
    a=ap.parse_args()
    out=build(load(a.source_zip))
    a.output.parent.mkdir(parents=True,exist_ok=True)
    a.output.write_text(json.dumps(out,indent=2,ensure_ascii=False)+"\n",encoding="utf-8")
    print(json.dumps({"selected_cells":out["selected_cells"],"valid_rank2_strata":out["valid_rank2_strata"],"viable":out["viable"]},indent=2))


if __name__=="__main__":
    main()
