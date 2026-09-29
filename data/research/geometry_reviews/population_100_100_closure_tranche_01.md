# 100/100 geometry closure tranche 1 — internal review

Issue: #370  
Parent milestone: #369  
Production batch: #360 / merged #367

## Result

All three missing map-representation cases survive the **internal geometry-role review** for a bounded disposable rehearsal.

This is not production authorization.

| Case | Review disposition | Proposed mapped role | Historical practice extent? |
| --- | --- | --- | --- |
| Goryeo 956 | ACCEPT_FOR_DISPOSABLE_REHEARSAL | Goryeo jurisdiction navigation via Manwoldae/Kaesong royal-capital point | No |
| Dahomey 1727 | ACCEPT_FOR_DISPOSABLE_REHEARSAL | Jakin transaction evidence locus via modern Godomè proxy | No |
| Taghaza 1352 | ACCEPT_FOR_DISPOSABLE_REHEARSAL | Taghaza site navigation via modern gazetteer proxy | No |

## Goryeo

UNESCO describes Kaesong as the ruling base/capital of the Koryo dynasty and publishes component 1278rev-001, Manwoldae & Kaesong Chomsongdae, at N37°59′9.28″ E126°32′32.795″. Korean heritage documentation dates the Goryeo royal palace at Manwoldae from 919, so the site is temporally valid as royal-capital context for 956.

The source passage for the nobi status review does **not** state a physical event location. The point therefore belongs on the Goryeo jurisdiction entity as a `modern_proxy` navigation/context geometry, not as `claim_evidence_locus`.

## Dahomey

Robin Law identifies Allada's western port as **Jakin [Godomey]**. The Atlas of Mutual Heritage independently records the historical titles Jaquin, Jakri, Godomey and Jakin. GeoNames feature 2394092 gives modern Godomè/Godomey at 6.389484 N, 2.34581 E.

The 1727 claim itself explicitly places part of the accepted sale process at Jakin. Unlike the royal camp, Jakin is therefore a defensible evidence/transaction locus.

Model it as:
- new site spatial entity `Jakin (Godomey)`;
- one `modern_proxy` point from GeoNames;
- one `claim_evidence_locus` link to claim `1567b140-eeba-4b32-b37d-f31dcb35e1dd`;
- one contextual claim-source relation to Law 1989 for historical place identity.

Keep the existing unresolved Dahomey target geometry untouched.

## Taghaza

NGA-derived geographic-name data gives Teghaza at 23.6101 N, 4.9939 W; GeoNames exposes the same coordinate with Teghaza/Tghaza/Tghâza aliases. This is sufficient for a modern navigation proxy, not for an exact medieval archaeological point.

The prior candidate's coordinate-conflict warning remains binding. Do not average the competing coordinates. The accepted point stays `modern_proxy`, with the conflict stated in its resolution notes.

## Expected disposable delta

If implemented exactly as reviewed:

- +1 spatial entity (Jakin/Godomey)
- +3 geometry rows
- +1 claim-evidence-locus relation
- +1 contextual claim-source relation
- expected +4 source/source-version records, subject to live exact-URL reuse
- +0 claims
- +0 release membership
- +0 publication changes
- +0 P-level changes
- +0 historical-practice polygons

## Next gate

Implement a fail-closed bounded amendment/rehearsal path on a disposable PostGIS database. The rehearsal must reconstruct the merged #367 production state first, apply these three amendments, replay unchanged as exact no-ops, verify the semantic roles and exact deltas, then roll back.

A live geometry amendment remains a **separate explicit production-write gate**.

