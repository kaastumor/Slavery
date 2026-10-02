# 100/100 released geo recovery tranche 5 — Nineveh

**Owner:** #369  
**Reviewed against main:** `494ea31f1d259653c02b14ac64890eaa561de4e0`  
**Result:** `ACCEPTED_STAGING` — review-only; governed DB preflight still required

## Released identity preserved

- spatial entity: `6b3fd57f-4d30-44d2-9d15-427e41b6cd47` — Neo-Assyrian Nineveh
- claim: `8077abf3-f506-4bb1-908a-4aa5abd12369`
- claim kind: `territorial_practice`
- interval: 695 BCE (`-695` in atlas astronomical year numbering)
- practice type: `slavery_enslavement`
- practice level: `NULL`
- current released geometry count: 0
- immutable membership: v0.8.2

The existing claim is unchanged. Its bounded proposition rests on SAA 06 128 and Karen Radner's specialist legal interpretation. The geometry source below identifies Nineveh as a historical city site; it is independent of those historical-evidence sources.

## Proposed geometry

Use the Pleiades source-native **DARE Location** for Nineveh/Ninos:

- Pleiades place: `874621`
- location: `dare-location`
- point: **[43.155403, 36.366841]**
- source-native interval: **750 BCE–640 CE** (`-750..640`)
- published accuracy value: **10 m** (`dare-3`)
- proposed atlas interval: **-695..-695**, clipped to the released claim
- role: `site_navigation_locator`
- accuracy status: `specialist`

The proposal is pinned to `isawnyu/pleiades.datasets` commit `a7b17570094a6544017290cbb6d780d2769dd112`, path `data/json/8/7/4/6/874621.json`, blob `646d909e88c4913213eb2d00fdf70188a1c67ca8`. Pleiades data is distributed under CC BY 3.0.

## Explicit abstentions

This point is not:

- a Nineveh city boundary or territorial-practice polygon;
- an exact findspot, archive room, household or transaction locus for SAA 06 128;
- evidence for prevalence, intensity or a P-level;
- a publication, release-membership or serving-channel change.

The Pleiades place-level representative point is not selected because it is derived across published locations. The OpenStreetMap-derived archaeological perimeter is rejected as a modern feature without a historical interval. The CIGS point remains corroborating only because the selected DARE location provides the stronger explicit temporal pin.

## Gate

Governed PostgreSQL/PostGIS read access was unavailable in this runtime. Before any disposable rehearsal, a fresh fail-closed preflight must confirm the exact released IDs and zero collisions for target geometry and the Pleiades source/version. Production admission, immutable-release mutation, serving movement and merge remain separately gated.
