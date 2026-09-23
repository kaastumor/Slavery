# M2 Cliopatria calendar and relation semantics

**Gate:** #116  
**Task:** #118  
**Pinned corpus:** Cliopatria v0.2.0 re-release at commit `ad28a691b7c07c1fca89d0e0636d324667d2a258`  
**Status:** source semantics resolved where supported; source year zero intentionally remains source-native rather than being given an invented historical label

## Question

What exact calendar mapping and POLITY/RELATION/component semantics are required to use the complete pinned Cliopatria corpus safely in selected-year atlas queries?

## Upstream facts

Pinned upstream README and visualization code establish:

- `FromYear` and `ToYear` are inclusive;
- negative integers are BCE and positive integers are CE;
- upstream selected-year filtering is `FromYear <= year <= ToYear`;
- `MemberOf` identifies composites a row contributes to;
- `Components` identifies rows contributing to a composite;
- upstream “Polities” display keeps rows with empty `MemberOf`;
- upstream “Components” display keeps rows with empty `Components`;
- composite geometry duplicates the geometry of its members.

The v0.2.0 release commit adds `RELATION` for a subset of Seshat-based supra-polity relationships including personal unions, vassalages, alliances and allegiances. These are relationship composites, not ordinary polity identities.

The 2025 Scientific Data descriptor likewise explains that composite names are parenthesized, that `MemberOf` / `Components` encode the composition graph, and that composite geometries duplicate member geometry.

## Exact pinned-corpus observations

The deterministic diagnostic against the exact pinned blob found:

- 13,765 total rows;
- 13,380 `POLITY` rows and 385 `RELATION` rows;
- all 385 `RELATION` names are parenthesized;
- all 385 `RELATION` rows have `Components`;
- no `RELATION` row has `MemberOf`;
- 2,656 rows have `MemberOf`;
- 1,722 rows have `Components`;
- 80 rows have both, proving nested composites exist;
- `MemberOf` can contain two memberships (86 rows);
- `Components` reaches 20 members in the pinned corpus;
- same-name chronological rows have 11,705 integer-contiguous transitions and 427 gaps larger than one integer;
- no same-name interval overlaps were observed in the pinned corpus.

The compact evidence record is `validation/cliopatria_v0.2.0_semantics.json`.

### Source year zero

Six rows end at source-native year `0`:

- Yuezhi: -50..0, next row starts 1
- Parthian Empire: -36..0, next starts 1
- Indo-Greeks: -31..0, next starts 1
- Indo-Scythians: -27..0, next starts 1
- Judea: -19..0, next starts 1
- Roman Empire: -14..0, next starts 1

The pinned original map sequence near the era boundary contains `B105-14.PNG` followed by `C001-1.PNG`; no explicit year-zero map image is present.

Upstream prose does not assign a BCE/CE historical label to source integer `0`.

## Atlas calendar decision

The atlas uses astronomical historical integers:

- 1 BCE = 0
- 2 BCE = -1
- 1 CE = 1

Cliopatria explicitly labels source negative integer `-N` as N BCE and source positive integer `N` as N CE.

Therefore selected-year lookup translates an atlas year to the Cliopatria source timeline as:

```
if atlas_year <= 0:
    cliopatria_source_year = atlas_year - 1
else:
    cliopatria_source_year = atlas_year
```

Examples:

| Atlas internal | Historical label | Cliopatria source query |
| ---: | --- | ---: |
| -13 | 14 BCE | -14 |
| -1 | 2 BCE | -2 |
| 0 | 1 BCE | -1 |
| 1 | 1 CE | 1 |
| 5 | 5 CE | 5 |

This mapping is derived from the upstream BCE/CE labels. It deliberately never queries source integer `0`.

**Source 0 is preserved exactly in raw data but has no independent atlas historical-year equivalent.** The observed corpus pattern supports treating it as a source-native bridge slot for the integer ranges; this is an atlas normalization policy, not a claim that upstream explicitly defined the meaning of year zero.

Do not rewrite source-native years during raw ingestion.

## Interval rules

- source row applicability remains inclusive;
- selected-year lookup happens by translating the atlas selected year to the source query year, then applying the upstream inclusive predicate;
- source row gaps remain gaps;
- do not interpolate a missing same-name period merely because rows exist before and after it;
- do not use the nearest Cliopatria row automatically to fill a corpus gap.

A separate specialist/approximate/proxy geometry may still be chosen through the normal reviewed geometry resolver.

## Composite and RELATION rules

Preserve the exact raw `MemberOf` and `Components` strings. Parsed semicolon-delimited lists may be stored additionally.

Do not treat the hierarchy as one level: nested POLITY composites exist.

### Reproducing upstream views

For diagnostic/source-faithful views:

- upstream top-level mode = active rows with empty `MemberOf`;
- upstream leaf/components mode = active rows with empty `Components`.

These modes can be reproduced for validation but are not automatically the atlas public polity baseline.

### Atlas default polity baseline

The atlas asks for political entities, while Cliopatria `RELATION` can represent allegiance, vassalage, alliance or personal-union composites. Rendering such a relationship composite as if it were one polity can overstate political unity.

Therefore the default atlas baseline should:

1. select rows active in the translated source year;
2. treat `Type=POLITY` as polity-geometry candidates;
3. resolve active source `MemberOf` links;
4. suppress a constituent POLITY only when the relevant active parent composite is itself `Type=POLITY`;
5. **not** suppress constituent polities merely because they participate in a `Type=RELATION` composite;
6. resolve nested POLITY composites recursively to the highest active POLITY composite;
7. keep `RELATION` rows separately as relationship/composite evidence or an optional relation layer;
8. if parent type/identity cannot be resolved unambiguously, preserve the constituent polity candidate and flag hierarchy resolution unresolved rather than guessing.

This avoids drawing both a polity composite and all of its duplicated components while also avoiding the opposite failure: replacing separate polities with an alliance/allegiance/vassalage composite.

Accepted specialist geometry still outranks the Cliopatria baseline under D-055.

## Identity warning

A source `Name` is not a durable atlas identity.

The exact corpus contains repeated names separated by large gaps, and identifiers may be missing or change. Raw ingestion must therefore retain each source row independently plus its native identifiers/values. Entity resolution into atlas `SPATIAL_ENTITY` remains a separate reviewed step.

Likewise, a RELATION row may contain semicolon-delimited Seshat IDs for multiple components. It must not be loaded into one polity-ID field.

## Adversarial alternatives

| Alternative | Disposition | Result |
| --- | --- | --- |
| Treat source year 0 as atlas astronomical 0 | **reject** | This would conflict with upstream negative=N BCE labeling and create an off-by-one BCE mapping. |
| Shift every source year by +1 | **reject** | Positive CE years are already explicitly CE labels and must not shift. |
| Rewrite raw source years during ingestion | **reject** | Destroys source-native lineage and makes the special zero irrecoverable. |
| Ignore source zero and map selected historical years around it | **survives** | Atlas-year → source-year translation is one-to-one for real BCE/CE years and never invents a year-zero historical label. |
| Use upstream top-level display unmodified as atlas polity map | **reject** | RELATION composites can replace member polities and visually imply political unity. |
| Drop all composites | **reject** | POLITY composites are legitimate source representations and nested composites exist. |
| Treat RELATION as POLITY | **reject** | Upstream explicitly introduced RELATION as a separate relationship type. |
| Flatten MemberOf/Components to one parent | **reject** | 86 rows have two memberships and 80 rows are nested composites. |
| Interpolate all same-name gaps | **reject** | Upstream descriptor explicitly notes substantial gaps can represent temporary incorporation; the pinned corpus has 427 such gaps. |

## Decision

**Survives with bounded normalization.**

The complete source corpus can support a selected-year resolver without silent year shifts or composite duplication, provided the raw source timeline/hierarchy is preserved and the atlas applies the explicit translation and type-aware hierarchy rules above.

No geometry is approved or published by this decision. No historical release changes.
