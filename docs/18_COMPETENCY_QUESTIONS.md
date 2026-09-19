# Atlas Competency Questions

**Status:** proposed design questions for evaluating ontology, schema, APIs and research workflow. These are not historical answers and do not change canonical classifications.

The purpose of competency questions is to test whether the atlas model can answer historian/public-user questions without category collapse or invented certainty. The Enslaved Ontology project used historian-authored competency questions to scope ontology development; this atlas adopts that design technique while defining its own broader question set.

## A. Territorial practice

1. For a selected place and year, what forms of slavery, coerced labour or servile dependency are evidenced **within the territory**?
2. What is the P0–P4 assessment, if any, and what evidence package justifies it?
3. Which evidence is direct attestation, which is interpretive scholarship, and which only provides context?
4. Which supporting sources are genuinely independent?
5. What important contrary or qualifying evidence exists?
6. Can a territorial claim remain reviewed while its P-level is still unassigned?
7. Can the system distinguish P0 from both “not researched” and “researched inconclusive”?
8. Can it distinguish isolated attestation from evidence of systemic/institutional practice?

## B. Legal status versus practice

9. What laws, decrees, court decisions or other legal events affected slavery/coerced labour in a jurisdiction during the selected period?
10. What changed legally, and on what effective date or approximate interval?
11. Does the system keep prohibition/abolition separate from evidence that practice actually stopped?
12. Can competing national, subnational, colonial or customary legal regimes coexist?
13. Can a legal event exist without creating or modifying a territorial P-level automatically?

## C. External/network participation

14. Did a place, polity, organization or person participate in enslavement/trading networks without evidence of territorial prevalence?
15. Was the participation through voyage ownership, finance, insurance, markets, routes, captive export/import or another role?
16. Can the system represent participation without converting it into territorial practice?
17. What exact claim/source evidence supports each network edge?

## D. Actors and identity

18. Who is the historical actor referred to by a source-native name?
19. Which aliases/variants are documented, and by which source versions?
20. What historical roles did the actor hold, and during what periods?
21. Is a nationality/political identity independently evidenced?
22. Can nationality remain unknown even when vessel flag, port, residence, business base or company jurisdiction is known?
23. Can two sources disagree about an actor's identity or role without one being silently overwritten?

## E. Sources and provenance

24. What exact source version supports a claim?
25. What conceptual source does that version belong to?
26. What page, archive locator, voyage record, IIIF canvas or dataset row contains the relevant evidence?
27. Is the evidence primary, secondary or another class, and what role does that classification play for this specific claim?
28. Was the source used to support the claim, challenge it, qualify it or provide context?
29. What derivative steps—OCR, HTR, translation, extraction—occurred between the source asset and the candidate assertion?
30. Which tool/model/version produced a derivative?
31. Can the original source-native text/value always be recovered?

## F. Research coverage

32. Has a region-period cell actually been researched?
33. Which exact source versions were reviewed for that coverage assessment?
34. Was the result classified, disputed or researched-inconclusive?
35. Can research coverage be shown publicly without changing territorial-practice intensity?
36. Can the system avoid treating missing sources as evidence of absence?

## G. Time

37. Can the system represent exact years, ranges, approximate ranges, centuries and unknown bounds without false precision?
38. Does 1 BCE map internally to astronomical year 0 while the UI remains conventional BCE/CE?
39. Can a claim's temporal certainty differ from the lifetime/existence interval of an actor or polity?
40. Can source-native date wording be preserved alongside normalized query ranges?

## H. Place and historical geography

41. What spatial entity does a source-native place string refer to?
42. What alternative names and authority identifiers are associated with it?
43. What polity/jurisdiction, if any, was the place related to at the selected time?
44. Can place identity remain resolved while historical jurisdiction remains uncertain?
45. Which geometry is being displayed for a selected year?
46. Is the geometry exact, specialist, approximate historical, modern proxy or unresolved?
47. What source/version supports that geometry?
48. Can neutral land remain visible where no historical political geometry is resolved?

## I. Dispute and uncertainty

49. Can two competing classifications coexist with separate evidence packages?
50. Can a claim be reviewed as disputed rather than forced into a single conclusion?
51. Can spatial, temporal and identity uncertainty be represented independently?
52. Can later scholarship supersede a claim without destroying the previous reviewed state?
53. Can users see why a claim is unresolved?

## J. Data ingestion and lineage

54. Which source release/run produced a normalized record?
55. What source-native identifier/value was preserved?
56. Was a value documented or imputed?
57. Which transformation produced the canonical candidate?
58. Can every normalized row be traced back to raw ingestion material?
59. Can a partial migration be prevented from masquerading as a complete canonical release?

## K. Release and publication

60. Which exact claims, actors, spatial entities, geometries and source versions belong to release X?
61. Can release X be reconstructed after later research changes?
62. What changed from the prior release?
63. What QC checks passed?
64. What unresolved issues remained?
65. Which reviewed records are intentionally not public?
66. Can the public application be restricted to reviewed/published release material only?

## L. Public map experience

67. At a selected year, what territorial-practice layer is shown?
68. Can the user independently toggle legal status, external participation and research coverage?
69. Can the user tell whether displayed geometry is approximate or a modern proxy?
70. Can clicking a feature reveal the underlying claim, evidence package and sources?
71. Does “no data” look different from P0, RI, disputed, prohibited/abolished and genuinely classified practice?
72. Can a user follow a map assertion back to an exact source locator?

## M. Comparative/research queries

73. Which territories have comparable evidence for a specific practice type during a selected interval?
74. Can comparisons be filtered by research-coverage state to avoid misleading archive-density comparisons?
75. Which sources attest the same practice independently across multiple regions?
76. How did legal status and territorial practice diverge over time in a given jurisdiction?
77. Which external networks connected actors/places whose territorial practice classifications differ?
78. Where do unresolved geometry or source-version problems currently block stronger conclusions?

## Acceptance use

A proposed schema/ontology/tool should be evaluated against these questions.

A tool is **not** automatically a good fit merely because it can answer more questions. It must also preserve:

- source/version provenance;
- uncertainty;
- raw/source-native values;
- claim dimensions;
- historical time;
- review/publication boundaries;
- human judgment where reconciliation/interpretation is contested.

Future additions should be driven by real historian/public-user questions rather than by available software features.
