# R1.2 — Frozen Target Frame

**Programme:** R1 / #159  
**Frozen before new R1 slavery/coercion research:** 2026-09-23  
**Core Contract:** `programmes/r1/03_CORE_CONTRACT_V1.md`  
**Pinned Cliopatria commit:** `ad28a691b7c07c1fca89d0e0636d324667d2a258`  
**Pinned Cliopatria SHA-256:** `d01ae3a20d358cc5d54f69d9d725d390767d9c8759ac89ad6f90c58d106f3370`

## Calendar

R1 corrects the shorthand used in some earlier experiments:

- source-native `-500` = **500 BCE**;
- Atlas astronomical internal year = **-499**;
- source-native `-1` = **1 BCE** = Atlas internal **0**.

Source-native year values remain preserved separately.

## Frozen release-frame shape

- new polity C0: **41**
- new non-polity C0: **24**
- new C0 total: **65**
- new polity C1: **16**
- new non-polity C1: **8**
- new C1 total: **24**
- legacy C1 re-review: **12**
- planned C1 total: **36**

All are below R1 MAX ceilings.

## New polity C1 cohort

| Target | Display anchor | Sampling sector | Source row |
| --- | --- | --- | ---: |
| Middle Kingdom of Egypt | 2000 BCE | C | 30 |
| Sumerian City-States | 2000 BCE | D | 28 |
| Indus Valley Civilization | 2000 BCE | E | 27 |
| Kingdom of Kush | 500 BCE | C | 217 |
| Magadha - Haryanka dynasty | 500 BCE | E | 296 |
| Cai | 500 BCE | F | 173 |
| Teotihuacan | 500 CE | A | 1226 |
| Lazica | 500 CE | D | 1630 |
| Tamna | 500 CE | F | 1371 |
| Later Mayan City-States | 1300 CE | A | 5791 |
| Mali Empire | 1300 CE | C | 5645 |
| Grand Duchy of Lithuania | 1300 CE | D | 5987 |
| Khmer Empire | 1300 CE | F | 5654 |
| French Louisiana | 1800 CE | A | 10547 |
| Ethiopian Empire | 1800 CE | C | 10076 |
| Duchy of Bavaria | 1800 CE | D | 10468 |

## New non-polity C1 cohort

| Target | Anchor | Frame class |
| --- | ---: | --- |
| Gao | 1500 | node_site |
| Angkor | 1200 | node_site |
| Shaolin Monastery | 1000 | institution_estate |
| Nalanda Mahavihara | 700 | institution_estate |
| Incense Route network | -100 | mobile_network |
| Mongol Yam/postal network | 1300 | mobile_network |
| Inuit Arctic communities | 1800 | region_community |
| Yaghan communities, Tierra del Fuego | 1800 | region_community |

## Legacy Core-v1 promotion cohort

| Target | Anchor | Origin | Legacy outcome |
| --- | ---: | --- | --- |
| Carthage | -500 | legacy_promotion_polity | bounded_supported |
| United States of America | 1800 | legacy_promotion_polity | bounded_supported |
| Pandya Empire | 1300 | legacy_promotion_polity | bounded_supported |
| Portuguese Colonies | 1800 | legacy_promotion_polity | materially_disputed |
| Chámpa | 500 | legacy_promotion_polity | researched_inconclusive |
| Chimu Empire | 1300 | legacy_promotion_polity | researched_inconclusive |
| Cuzco | 1300 | legacy_promotion_polity | researched_inconclusive |
| Hadhramaut | -500 | legacy_promotion_polity | researched_inconclusive |
| Viking trade network | 900 | legacy_promotion_nonpolity | bounded_supported |
| Andaman Islands communities | 1800 | legacy_promotion_nonpolity | bounded_supported |
| Cahokia | 1200 | legacy_promotion_nonpolity | materially_disputed |
| al-Azhar Mosque/university | 1100 | legacy_promotion_nonpolity | researched_inconclusive |

No legacy row is grandfathered into publication. Every row requires Core Contract v1 re-review.

## Preserved sampling gaps

The new-unused-polity frame contains genuine gaps. In particular, sector B has no eligible unused Cliopatria polity candidate at any frozen R1 polity anchor after excluding prior sampled source rows.

R1 does **not** substitute another target to hide that gap.

The complete planned C1 release nevertheless retains all six neutral polity sampling sectors because the deterministic legacy re-review cohort contains sector-B South American targets (Chimú and Cuzco). The separately frozen new non-polity cohort also contains Yaghan/Tierra del Fuego.

This distinction is explicit:

> no new sector-B polity row available != South America absent from R1.

## Required balance gates

- all_five_source_anchor_bands_represented: **PASS**
- all_six_release_polity_sampling_sectors_represented: **PASS**
- at_least_three_frame_classes: **PASS**
- no_release_polity_sector_exceeds_25pct_of_planned_c1: **PASS**

New-polity sampling gaps are preserved as data, not repaired by historical-subject evidence.

## Freeze rule

From this point:
- no target substitution after slavery/coercion evidence is inspected;
- a target may fail identity/time validation and remain a failed target;
- C1 may end inconclusive/disputed;
- research difficulty does not permit replacement with a better-documented case.

**R1 subject research is authorized only against this frozen frame.**
