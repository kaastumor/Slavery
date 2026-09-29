# Population successor preparation — post-ingest checkpoint

**Issue:** #360  
**PR:** #367  
**Strategic successor milestone:** #369 (100 release-qualified cases / 100 defensible case-linked map representations)

## Production ingest

The sponsor explicitly authorized the #367 production write. The 12-case transaction committed successfully against live PostgreSQL/PostGIS.

Exact input authority:
- main: `09f5d77fb21f451d855c5df4a0b442469eaf422b`
- reviewed PR head: `4465b2606f4b8f4cae4ad8c8fe769446b68b66f4`
- exact-head foundation CI: run `36627780153` = PASS
- schema head after write: `0034_release_manifest_immutability`

Observed atomic delta:
- +12 spatial entities
- +12 claims: 1 legal event + 11 territorial-practice claims
- +28 sources / +28 source versions, with one pre-existing Angkor source version reused
- +20 claim-source links
- +10 geometry rows / 9 non-null reviewed modern-proxy navigation/context points
- +1 research target/result/claim/review package and +2 research-target-source rows
- +12 research-case-ingest ledger rows
- +0 release membership
- +0 serving-channel rows
- +0 publication-status changes

All 12 claims remain reviewed/unpublished. All 11 territorial-practice claims retain NULL practice level.

## Geometry interpretation

The nine resolved geometries are navigation/context modern proxies, not historical practice extents. Dahomey and Taghaza remain unresolved. Goryeo is a bounded legal event and has no practice geometry.

No new shaded historical-practice polygon is implied by this transaction.

## Successor lineage

Do not create a competing version number.

The existing successor lane remains:
`release/selections/v0.8.2-post-overnight-claims.json`

Its D-121 inherited-geometry provenance HOLD is still binding. The new batch's source/geometry IDs are now captured, but that does not cure D-121 for inherited structured geometry.

The public channel remains:
`public_mvp_preview` → `v0.8.1-public-mvp-v2`

## QC summary

PASS:
- exact pre-write collision check;
- expected Angkor source-version reuse only;
- exact tracked-table delta;
- 12/12 unpublished;
- 0 new P-levels;
- 9 resolved / 10 total geometry rows;
- 0 release membership delta;
- 0 public-channel movement.

Unresolved:
- inherited D-121 geometry provenance;
- successor case-identity reconciliation, especially legacy/current replacements;
- Dahomey and Taghaza geometry;
- source-amendment lane for the existing 11 current-method claims;
- #369 100/100 target remains incomplete.

## Rollback / staged cutover

This ingest is canonical research-state growth, not a public release mutation. Do not ad-hoc delete committed historical rows. If a substantive defect is found, preserve lineage and use governed correction/supersession.

A future public cutover must:
1. freeze an explicit successor selection;
2. satisfy D-121 and dependency closure;
3. build/verify an immutable materialization;
4. verify evidence panels and mapped roles;
5. capture pre-cutover channel state;
6. move the serving channel only after separate sponsor authorization;
7. retain a rollback target to the current `v0.8.1-public-mvp-v2` materialization.

## 100/100 implication

The 12 production rows are inputs to #369, not automatically 12 release-qualified cases. Case counting must follow #369's identity/reconciliation contract; geo counting must use explicit role/provenance and must not turn proxy points into historical extents.

