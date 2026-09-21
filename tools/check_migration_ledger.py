#!/usr/bin/env python3
"""Compare repository migrations with a Supabase migration-history export."""
from __future__ import annotations
import argparse, json
from collections import Counter
from pathlib import Path
import sys
ROOT = Path(__file__).resolve().parents[1]
MIGRATIONS = ROOT / "db" / "migrations"

def repository_names(): return [p.stem for p in sorted(MIGRATIONS.glob("[0-9][0-9][0-9][0-9]_*.sql"))]
def remote_names(payload):
    if isinstance(payload, dict): payload = payload.get("migrations", payload.get("data", payload))
    if not isinstance(payload, list): raise ValueError("remote JSON must contain a migration list")
    out=[]
    for row in payload:
        if isinstance(row,str): out.append(row)
        elif isinstance(row,dict) and isinstance(row.get("name"),str): out.append(row["name"])
        else: raise ValueError("each remote migration needs a name")
    return out

def compare(repo, remote):
    counts=Counter(remote); rs=set(repo); ms=set(remote)
    return {"repository_count":len(repo),"remote_entry_count":len(remote),"missing_remote":[n for n in repo if n not in ms],"duplicate_remote":{n:c for n,c in sorted(counts.items()) if c>1},"unknown_remote":sorted(ms-rs)}

def main():
    p=argparse.ArgumentParser(); p.add_argument("remote_json",type=Path); a=p.parse_args()
    result=compare(repository_names(),remote_names(json.loads(a.remote_json.read_text(encoding="utf-8"))))
    print(json.dumps(result,indent=2,sort_keys=True))
    return 2 if result["missing_remote"] or result["duplicate_remote"] or result["unknown_remote"] else 0
if __name__ == "__main__": sys.exit(main())
