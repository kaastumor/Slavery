# 100/100 released geo recovery tranche 4 — Sogdiana / Afrosiab

**Issue:** #383  
**Parent:** #369  
**Reviewed against main:** `eee51caa6569e3b433af60bc9a7a33f5e04622ed`  
**Fresh live preflight:** 2026-09-30 13:47:18 UTC

## Result

**ACCEPT_FOR_DISPOSABLE_REHEARSAL**

The released Sogdiana claim remains unchanged:

- claim: `63dda32b-6c3e-4b3e-9c5a-36596e6cdc1b`
- target: `a6718e1f-5683-48f4-90fb-cc35ad263ba5` — Early eighth-century Sogdiana
- interval: 709–710 CE
- existing practice level: P2 (legacy released state; not recalculated here)
- v0.8.1 object hash: `e1c7a4977a11a9e1ba50f1287776adf7b0d4def3bf449d318d19b9d11dca6b55`

The existing reviewed target-geometry row `ef33b27a-2b8f-4fc0-a523-885137706193` is `unresolved` with NULL geometry and must remain untouched.

## Historical place inference

Reuse existing source version `cc49573e-8621-43d2-b054-a496c66cdcc8`:

- Ilya Yakubovich, *Encyclopaedia Iranica*, Sogdian marriage contract.
- The documents were found at **Mount Mugh**.
- They are dated by the tenth regnal year of Tarkhun, ca. **709–710 CE**.
- Yakubovich states that the agreement was **likely concluded in Samarkand**.

This supports one **probable Samarkand legal-context evidence locus**. It does not make Mount Mugh the contract site and does not make Samarkand or Sogdiana a territorial-practice polygon.

## Chronology tension retained

Oxford Invisible East, citing Livshits 2015, catalogues Nov. 3/4 as **27 April 711**.

That later catalogue date is a review qualification, not a silent correction to the immutable released 709–710 claim. This tranche creates no new historical claim-source relation from the catalogue.

## Geometry source

UNESCO World Heritage Centre, *Samarkand – Crossroad of Cultures*:

- component: **603rev-001 — Afrosiab Archaeological Area**
- published coordinate: N 39°40′0″ / E 66°58′60″
- normalized point: **[66.9833333, 39.6666667]**
- component area: 229 ha
- source: https://whc.unesco.org/en/list/603/maps/

UNESCO identifies Afrosiab as the ancient city of Samarkand. The component coordinate is used as a representative archaeological-site locator only.

## Review resolution: specialist geometry, probabilistic role

The staging checkpoint had described the point as `approximate_historical`. This review resolves the geometry row to **`specialist`** because:

1. the mapped object is an authoritative UNESCO component for Afrosiab itself;
2. the Atlas already uses `specialist` for comparable authoritative site/component points, including UNESCO-located Songo Mnara and Tōdai-ji;
3. uncertainty belongs to the **claim-to-locus relation**: the contract was *likely* concluded in Samarkand, but the exact building/room is unknown.

Proposed locus entity type is **`site`**, not `city`, because the geometry is specifically the Afrosiab Archaeological Area component. Its display label may still explain that Afrosiab is ancient Samarkand.

Semantic role:

`claim_evidence_locus_probable_contract_setting`

Required role text:

> probable Samarkand legal-context locus; contract location inferred by specialist editor

This must never be rendered or described as a Sogdiana practice extent.

## Fresh live preflight

Observed production state:

- candidate Afrosiab/Samarkand locus entity collisions: 0
- exact UNESCO 603/603rev maps source-version collisions: 0
- existing claim-evidence-locus links for the released claim: 0
- existing target geometry rows: 1, reviewed + unresolved + NULL geometry
- v0.8.1 membership present and published
- public serving: `v0.8.1-public-mvp-v2`

## Expected disposable delta

- +1 spatial entity
- +1 UNESCO geometry source
- +1 UNESCO source version
- +1 specialist point geometry
- +1 claim-evidence-locus link
- +0 historical claims
- +0 historical claim-source relations
- +0 release membership / release geometry
- +0 publication or P-level changes
- +0 historical-practice polygons
- existing unresolved Sogdiana target geometry preserved

## Next gate

Implement a fail-closed **disposable-only** rehearsal that:

1. reconstructs the exact released claim/source/release identity;
2. asserts the unresolved target geometry still exists unchanged;
3. inserts only the Afrosiab locus, UNESCO geometry source/version, specialist point and one locus link;
4. requires unchanged replay to be an exact no-op;
5. proves v0.8.1 membership and `v0.8.1-public-mvp-v2` serving remain unchanged;
6. rolls back and restores all tracked counts.

A live database write remains a separate explicit sponsor gate.
