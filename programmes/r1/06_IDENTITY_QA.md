# R1.3 — C0 Register and Identity/Time QA

**Issue:** #161  
**Subject-matter slavery/coercion research performed in this stage:** **NO**

## Result

Planned C1 targets reviewed: **36**

- validated: **18**
- validated_with_frame_limitation: **16**
- ambiguous_requires_C2_or_hold: **1**
- invalid_or_mismatched_hold: **1**

Subject-research queue: **34**

Held without replacement:
- **French Louisiana, 1800** — treaty/title versus effective possession/administration is not safely resolvable at annual precision.
- **Duchy of Bavaria, 1800** — source-native label is wrong for the anchor; Bavaria was an Electorate from 1623–1806.

No substitute target is introduced.

## New polity C1 QA

| Target | Anchor | QA | Effective frame | Limitation |
| --- | --- | --- | --- | --- |
| Middle Kingdom of Egypt | 2000 BCE | validated | historical_period_polity | None material to target identity at this anchor. |
| Sumerian City-States | 2000 BCE | validated_with_frame_limitation | polity_aggregate | Aggregate of multiple Sumerian city-state polities around a transition period; never treat as one sovereign territorial polity. |
| Indus Valley Civilization | 2000 BCE | validated_with_frame_limitation | civilization_region | Civilization/archaeological-cultural frame, not one demonstrated sovereign polity; territorial inference must remain bounded. |
| Kingdom of Kush | 500 BCE | validated | polity | Anchor falls in the Kushite/Napatan kingdom; later Meroitic phase must not be back-projected. |
| Magadha - Haryanka dynasty | 500 BCE | validated_with_frame_limitation | dynastic_polity | Early Magadhan dynastic chronology is tradition-dependent and contested; treat 500 BCE as approximate anchor, not exact regnal dating. |
| Cai | 500 BCE | validated | polity | None material to target identity at anchor. |
| Teotihuacan | 500 CE | validated_with_frame_limitation | urban_polity_site | Major urban/political centre; exact territorial jurisdiction is uncertain and must not be inferred from city/site geometry. |
| Lazica | 500 CE | validated | polity | Byzantine/Iranian suzerainty and changing dependency must be kept separate from target identity. |
| Tamna | 500 CE | validated | island_polity | Island kingdom frame; later tributary/title relations do not erase local polity identity. |
| Later Mayan City-States | 1300 CE | validated_with_frame_limitation | polity_aggregate | Multi-polity Postclassic Maya aggregate; no single territorial jurisdiction or uniform practice may be inferred. |
| Mali Empire | 1300 CE | validated | polity | Imperial extent changes over time; selected-year geometry must remain year-specific. |
| Grand Duchy of Lithuania | 1300 CE | validated | polity | Territorial extent is historically changing; identity itself is valid. |
| Khmer Empire | 1300 CE | validated | polity | Angkor is a capital/site locus; empire-wide geometry must not be inferred from the site boundary. |
| French Louisiana | 1800 CE | ambiguous_requires_C2_or_hold | jurisdiction_title_transition | Treaty of San Ildefonso in 1800 created a French title/cession claim, but Spanish administration and actual delivery to France continued until 1803. Annual anchor cannot safely collapse title, possession and governance. |
| Ethiopian Empire | 1800 CE | validated_with_frame_limitation | imperial_title_fragmented_sovereignty | At 1800 the Solomonic imperial institution persists during Zemene Mesafint, but effective sovereignty is fragmented among regional lords; do not infer uniform imperial territorial practice. |
| Duchy of Bavaria | 1800 CE | invalid_or_mismatched_hold | invalid_label_at_anchor | Bavaria was an Electorate from 1623 to 1806. The source-native label 'Duchy of Bavaria' is not valid for 1800. Do not silently replace it with Electorate of Bavaria. |

## New non-polity C1 QA

| Target | Anchor | QA | Effective frame | Limitation |
| --- | --- | --- | --- | --- |
| Gao | 1500 CE | validated | node_site | City/site locus; not identical to the entire Songhai Empire. |
| Angkor | 1200 CE | validated | node_site | Capital/site complex; no empire-wide inference from the archaeological park boundary. |
| Shaolin Monastery | 1000 CE | validated | institution_estate | Institution/site locus; broader holdings or dependencies require separate evidence. |
| Nalanda Mahavihara | 700 CE | validated | institution_estate | Scholastic/monastic institution; site geometry is not territorial jurisdiction. |
| Incense Route network | 100 BCE | validated_with_frame_limitation | mobile_network | Multi-route, changing trade network; any display geometry is schematic and never territorial. |
| Mongol Yam/postal network | 1300 CE | validated_with_frame_limitation | mobile_network | Imperial/postal network varied by khanate and period; route/station extent must be source-specific. |
| Inuit Arctic communities | 1800 CE | validated_with_frame_limitation | region_community | Very broad multi-community/circumpolar frame with different colonial-contact histories; no single society, jurisdiction, or uniform institution may be inferred. |
| Yaghan communities, Tierra del Fuego | 1800 CE | validated_with_frame_limitation | region_community | Community/ethnonym and archipelago frame; no single territorial polity or fixed boundary. |

## Legacy promotion QA

| Target | Anchor | QA | Effective frame | Limitation |
| --- | --- | --- | --- | --- |
| Carthage | 500 BCE | validated | polity | Frozen Cliopatria row spans the anchor; no identity defect identified in prior QC. |
| United States of America | 1800 CE | validated | polity | Frozen Cliopatria row/anchor is valid; no frame defect identified. |
| Pandya Empire | 1300 CE | validated | polity | Frozen source-native polity interval contains the anchor. |
| Portuguese Colonies | 1800 CE | validated_with_frame_limitation | jurisdiction_aggregate | Aggregate of multiple Portuguese colonial jurisdictions; no single territorial-practice claim may attach to the aggregate. |
| Chámpa | 500 CE | validated | polity | Frozen source-native interval contains the anchor; identity retained. |
| Chimu Empire | 1300 CE | validated | polity | Frozen source-native interval contains the anchor; identity retained. |
| Cuzco | 1300 CE | validated_with_frame_limitation | node_or_incipient_polity | Cuzco around 1300 must not be treated as the later mature Inca imperial polity. |
| Hadhramaut | 500 BCE | validated | polity | Frozen source-native interval contains the anchor; identity retained. |
| Viking trade network | 900 CE | validated_with_frame_limitation | mobile_network | Network is not one society or territorial jurisdiction. |
| Andaman Islands communities | 1800 CE | validated_with_frame_limitation | region_community | Multiple distinct island peoples; no single indigenous polity. |
| Cahokia | 1200 CE | validated_with_frame_limitation | node_site | Archaeological urban/site frame; no automatic territorial polity extent. |
| al-Azhar Mosque/university | 1100 CE | validated_with_frame_limitation | institution_estate | Institutional point/locus inside Cairo; city/imperial context is not institutional practice. |

Legacy historical outcomes are **not** promoted by this QA. All legacy rows still require Core Contract v1 subject re-review.

## Core methodological consequences

1. Raw source-native classification is preserved even when the effective R1 frame differs.
   - Indus remains source-native Cliopatria `POLITY`, but R1 treats the target as a civilization/region frame.
   - Later Mayan City-States remains the source-native aggregate but cannot become one jurisdiction.

2. Annual anchors can be too coarse for jurisdictional transitions.
   - French Louisiana is held rather than pretending title and administration are equivalent.

3. Source-native target names can be historically wrong at the selected year.
   - Duchy of Bavaria is held rather than silently rewritten to Electorate of Bavaria.

4. Fragmented sovereignty is not target invalidity.
   - Ethiopian Empire remains researchable at 1800, but Zemene Mesafint fragmentation is a mandatory frame limitation.

5. Non-polity targets remain non-polity.
   - routes, institutions, sites and communities retain frame-specific inference limits.

## R1 subject-research gate

Only targets in `subject_research_queue.json` may enter R1.4.

Held targets remain in the frozen frame as QA failures/ambiguities and may be revisited only through an explicit later review decision.

**No post-evidence replacement is allowed.**
