# EXP-03 — Heterogeneous Evidence Stress Test

**Issue:** #211  
**Preregistered:** 2026-09-24  
**State:** ACTIVE  
**Canonical historical release:** v0.6.1 unchanged  
**Parent decision:** D-088

## Question

Does the portable reviewed evidence core from EXP-02 remain sufficient when applied to fresh, structurally heterogeneous historical research?

The stress conditions are:
- polity and non-polity targets;
- location versus inference-extent mismatch;
- law/practice divergence;
- network/territorial overlap;
- historically specific status terminology;
- sharply different source traditions and archive densities;
- mixed geometry states.

## Frozen sample

Selected before subject-evidence search:

| Case | Anchor | Structural pressure |
| --- | ---: | --- |
| Classical Athens | c. 400 BCE | city/polity overlap; unusually dense source tradition; archive-density positive control |
| Mamluk Cairo | c. 1300 CE | city + polity context; military slavery; import/network versus territorial institution |
| Tenochtitlan | c. 1500 CE | city/polity overlap; category translation; conquest/colonial-source mediation |
| Joseon Korea | c. 1700 CE | hereditary/status dependency; law/social practice; category ambiguity |
| Zanzibar Town / port | c. 1850 CE | port/city; territorial slavery plus external slave-trade network; locus/extent pressure |
| British India | 1843–1850 CE | legal abolition/prohibition versus continuing practice; jurisdiction-scale stress |

The sample is frozen for structural diversity, not expected positivity.

## Research contract

For each case:
1. establish terminology and historiographic framing from specialist scholarship;
2. recover bounded primary/source-native material where practical;
3. search for limiting/counterevidence;
4. preserve exact source/version/locator and dependency family;
5. write a bounded proposition and required abstention;
6. keep evidence locus separate from inference extent;
7. keep law separate from practice;
8. keep external/network participation separate from territorial practice;
9. preserve language/access limitations;
10. never turn missing target-specific evidence into absence;
11. never infer prevalence from source/document density.

## Required packet fields

- target identity/type;
- anchor / temporal scope and precision;
- research state;
- bounded proposition;
- required abstention;
- evidence locus;
- inference extent;
- practice/status terminology;
- law/practice note;
- network/territorial note;
- source relations with exact version/locator;
- source family/dependency;
- supports/challenges/qualifies/context role;
- access/language limitation;
- coverage confidence;
- geometry state and geometry/inference warning;
- contrary/limiting evidence;
- unresolved questions.

## Portability audit

For every field used, classify it:
- EXP-02 core already preserves it;
- derivable safely at package/view level;
- must be reintroduced to portable core;
- research-only detail not needed in portable release.

## Falsifiers

CORE SURVIVES fails if a case cannot be represented without:
- strengthening the reviewed claim;
- collapsing law into practice;
- collapsing network participation into territorial practice;
- losing material source-role/dependency information;
- manufacturing extent from a point/location;
- manufacturing temporal precision;
- losing a material historiographic dispute/category distinction.

## Outcomes

Exactly one:
- **CORE SURVIVES**
- **CORE REQUIRES EXTENSION**
- **CORE FAILS FOR THIS CLASS**

## Complexity boundary

No frontend work, new service, schema migration, canonical release, bulk geometry programme or external recruitment is authorized.

If an extension is required, specify the smallest semantic addition first.
