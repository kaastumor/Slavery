# 100/100 released geo recovery tranche 3 — ISIL/Yazidi Sinjar locus

**Issue:** #379  
**Parent:** #369  
**Reviewed against main:** `9677a601003668404ca5630d0c0fdcc7546dce70`

## Result

**ACCEPT_FOR_DISPOSABLE_REHEARSAL**

The already released ISIL/Yazidi case cluster has two v0.8.1 territorial-practice facets:

- slavery/enslavement — `88e48d2e-5b06-5b37-80bb-82e07db36a3f`
- sexual slavery — `b862e0a9-a857-57e0-8aa3-e37daf0844cf`

Both already reuse UNITAD source version `dc410234-3f13-5e41-9ce9-4391a850cc23`.

No new historical evidence family is needed.

## Why Sinjar town is a valid locus

UNITAD section 7.1 supplies the required case-to-place link:

- para. 193 explicitly lists **Sinjar town** among locations where Yazidis were captured;
- para. 195 explicitly lists **Sinjar town** among initial holding sites for women, boys and girls;
- para. 196 describes the subsequent selection/distribution/sale system from holding sites.

Therefore Sinjar town is a defensible capture/initial-holding evidence locus inside the already accepted evidence package.

It does **not** establish:
- an ISIL territorial-practice polygon;
- regional prevalence;
- the location of every enslavement or sexual-slavery act;
- the location of every later sale/transfer.

## Geometry

GeoNames feature **448149** identifies the populated place Sinjar / Sinjār at:

- 36.320901 N
- 41.876562 E

Use as one reviewed `modern_proxy` point only.

Stable source:
`https://www.geonames.org/448149/sinjar.html`

## Claim links

The same Sinjar locus may link to both released claim facets, but with different bounded semantics:

1. slavery/enslavement — capture + initial-holding locus, UNITAD paras. 193 and 195;
2. sexual slavery — upstream initial-holding locus feeding the later distribution/sale system, UNITAD paras. 195–196.

The second link must not state that later sexual violence occurred in Sinjar town in every case.

## Kocho deferred

UNITAD strongly supports Kocho as another capture site. However, current modern coordinate references conflict materially. Kocho is deliberately excluded from this tranche until a separate coordinate/identity review resolves the discrepancy.

One defensible locus is sufficient to close the case-level geometry gap; adding more points is not a KPI objective.

## Expected disposable delta

- +1 spatial entity
- +1 GeoNames source + source version
- +1 reviewed point geometry
- +2 claim-evidence-locus links
- +0 historical claims
- +0 historical claim-source relations
- +0 release membership / release geometry
- +0 publication or P-level changes
- +0 practice polygons

## Next gate

Implement a fail-closed disposable rehearsal. It must:

1. reconstruct the two released claims and prerequisite source linkage;
2. insert the Sinjar locus and geometry;
3. add exactly two locus links;
4. replay unchanged as exact no-op;
5. verify v0.8.1 membership and public serving are unchanged;
6. roll back and restore counts.

A live database write remains a separate explicit gate.

