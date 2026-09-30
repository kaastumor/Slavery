# 100/100 geometry closure tranche 2 — internal review

**Issue:** #374  
**Parent:** #369  
**Reviewed against main:** `521ae2d9b5d3e31390d7025492bb18335752c6df`

## Result

- **4 ACCEPT_FOR_DISPOSABLE_REHEARSAL**
- **1 HOLD_PLACE_IDENTITY_BEFORE_GEOMETRY**
- **0 country-proxy polygons promoted**
- **0 historical-practice polygons proposed**

| Case | Disposition | Mapped role |
| --- | --- | --- |
| India 2003–2005 | ACCEPT | Ramanagaram HRW fieldwork evidence locus; modern city proxy |
| Myanmar 1998 | ACCEPT | Shadaw Township / Daw Taku testimony context; modern admin proxy |
| Pakistan 1990s | ACCEPT | Lahore-outskirts brick-kiln evidence context; modern city proxy |
| Brazil 2003–2005 | **HOLD** | Corrente/Correntes identity not frozen |
| Nazi Germany 1942–1944 | ACCEPT | Schöneweide GBI camp 75/76 historic-site evidence locus |

## Core methodological result

The old timeless country polygons are not repaired or repurposed. Each accepted representation is attached through an explicit evidence-locus/context identity. Brazil remains unmapped in this tranche because resolving source-native `Correntes` to official `Corrente (PI)` by assumption would violate the raw/source identity rule.

## Expected disposable delta for the four accepted cases

- +4 spatial entities
- +4 point geometries
- +4 claim-evidence-locus relations
- +2 new claim-source context relations (Myanmar witness 101; Pakistan HRW)
- expected +6 source/source-version rows before exact live URL reuse
- +0 claims
- +0 release membership
- +0 publication/P-level changes
- +0 historical-practice polygons

## Next gate

Adversarially review:
1. evidence locus versus navigation context;
2. modern city/admin point versus exact incident site;
3. source independence;
4. source-native place identity;
5. whether any accepted point would misleadingly imply practice extent.

Only the surviving subset may enter disposable PostGIS rehearsal. No production write is authorized.



## Adversarial dependence correction

A fresh adversarial review found one material source-independence defect before production gating:

- the Myanmar witness-101 transcript is part of the **same 1998 ILO Commission of Inquiry evidence family** as the existing Myanmar inquiry claim source;
- it must therefore reuse `independence_group = ilo-myanmar-commission-inquiry-1998`;
- it may support a bounded testimony/location context, but it is **not** a second independent attestation.

The previously successful disposable rehearsal is therefore superseded for production-gate purposes until the corrected review is rerun. India, Pakistan and Schöneweide survive the adversarial role check; Brazil remains HOLD.
