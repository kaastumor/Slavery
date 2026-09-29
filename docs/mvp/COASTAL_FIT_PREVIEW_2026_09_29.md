# Coastal fitting solution: local 6 CE comparison

## Outcome

The local map now compares a coastal-fit candidate with published v2 and both
original source variants. The previous raw baseline remains available through
its link. Fixed Greece, Mediterranean and North Sea views make comparisons
repeatable. This is a presentation experiment for the 6–8 CE Roman slice, not a
new canonical release or a replacement of the evidence application.

## Existing approach adopted

[History Atlas](https://github.com/laurencefwhite/history-atlas#coastlines), another
Cliopatria consumer, documents extending polygons within a coastal strip and
clipping to the displayed land. Its documented setting is 13 km. Its source-file
URLs and repository contents API returned 404 during this task; the method was
implemented independently from the description. No third-party code was copied.

The first 13 km candidate improved Greece but left visible coastal gaps and
introduced small uncovered areas on the Dutch coast relative to v2. The local
candidate uses 25 km after that comparison. This value is a presentation
tolerance tested for this slice, not an established worldwide accuracy bound.

## Inputs and operations

- Use the pinned GitHub Roman feature (6–8 CE), avoiding the 13 angular interior
  rings present in the Seshat API variant. This is an explicit source change in
  the preview; no canonical source record has been replaced.
- Use the same Natural Earth 1:10m geometry for the fitting and displayed land.
- In EPSG:8857, compute the land within 25 km of its boundary.
- Add land only where it is both in that strip and within 25 km of the source.
- Keep every piece of original source-covered land; exclude sea.
- Export additions separately and union them with the original WGS84
  source/land intersection. This avoids changing inland edges through projection
  round trips. Standard geometry validity repair handles projection artifacts.

Unlike the previous offshore-overhang recovery, this reaches land where the
source coastline sits inland. It does not apply general smoothing. Source and
release files remain unchanged. Distances are projected metres; this is not a
claim of geodesic 25 km accuracy everywhere.

## Evidence and checks

The generated `web/public/source-baseline/coastal-fit-report.json` records the
input land hash, output hashes and measured checks. The proposal adds about
101,675 km² (2.832%) relative to the GitHub source intersected with land. Added
area is a presentation adjustment, not newly supported historical territory.

Final output is valid, with zero measured area outside land. Source-land loss
and changes beyond the exported coastal strip are at numerical overlay noise
levels (1.51e-15 and 5.29e-11 square degrees respectively). Metric checks restrict
additions to both the coastal strip and the source-distance limit.

Browser self-review:

- Greece: Gulf of Corinth cutouts absent; gulf remains water; the broad beige
  strips on the Peloponnese and western Greece visible in v2 are removed.
- North Sea: the extra gaps observed with 13 km are removed at 25 km; Britain
  remains uncoloured at 6 CE.
- Source variants and published v2 can be selected without changing the view.
- Some Aegean islands and larger source omissions remain uncoloured. The method
  does not establish that every island belonged to Rome, and no such assertion
  is made from appearance alone.

Verification:

- Two focused geometry tests passed: inland-frontier preservation, inward
  coastline recovery, ocean exclusion, retained source land, distant-island
  exclusion and preservation of an inland hole.
- Final-output geometric checks passed after correcting a projection round-trip
  issue discovered by the additional checks.
- Full suite: 357 tests, 14 failures, 14 errors, 2 skipped. This retains the
  diagnostic-root incompatibility and environment/artifact failures recorded in
  the baseline report; it is not a green release gate.
- Web TypeScript/Vite build passed; raw baseline is included as an entrypoint.
- Repository sanitation and diff whitespace checks passed.

## Integration boundary

This is a concrete solution candidate for the reported slice, with a known
tradeoff: nearby coastal borders and islands can gain presentation coverage.
The earlier 2% recovery policy would reject this candidate; it must not be
silently re-labelled as that policy. A public release requires source/interval
matching for every affected slice, overlap review against neighbouring polities,
integration into the evidence application, required release checks, and scoped
publication authorization. No merge, deployment or public-channel update was
performed in this task.

Rebuild:

```powershell
python tools/build_coastal_strip_preview.py <pinned-ne_10m_land.geojson>
python -m unittest discover -s tests -p test_coastal_strip_preview.py -v
cd web
npm run build
```

The builder requires Shapely and pyproj and reads the already extracted pinned
baseline. It writes only local preview assets.
