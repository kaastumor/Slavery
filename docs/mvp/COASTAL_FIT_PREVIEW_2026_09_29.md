# Coastal fitting solution: local 6 CE comparison

## Outcome

The local `web/coastal-preview.html` compares a coastal-fit candidate with
published v2 and both original source variants. The raw baseline remains at
`web/raw-baseline.html`; `web/index.html` again opens the evidence application.
Fixed Greece, Mediterranean and North Sea views make comparisons repeatable.
This is a presentation experiment for the 6–8 CE Roman slice, not a new
canonical release or a replacement of the evidence application.

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

### Follow-up adversarial audit

`tools/audit_coastal_strip_preview.py` checks the same pinned 46-feature 6 CE
selection against the exported fitted polygon. In an equal-area projection, the
candidate adds about 101,659 km². About 4,934 km² of those additions overlap
five other top-level source polygons: Nabataeans (1,787 km²), Thracian Kingdom
(1,536 km²), Kingdom of Pontus (674 km²), Mauretania (659 km²), and Greek
City-States (278 km²). These are added overlaps, not necessarily new conflicts
in the source corpus. Separately, 151 land components with no original Roman
source coverage gain about 4,388 km² of fill. The count is a geometry signal,
not evidence that any specific island was or was not Roman.

This audit does not validate other dates, source-to-record identity, or reviewed
neighbor boundaries. The pinned GitHub polygon is still known to differ from
the stored Seshat API record. The candidate therefore has **not** passed the
release gate. The evidence application uses unchanged released geometry by
default; the fitted version remains a separately labeled preview.

### Constrained local candidate and adjacent-interval screen

With sponsor authorization for a **local presentation candidate only**,
`tools/constrain_coastal_strip_preview.py` now removes additions that overlap
other pinned top-level 6 CE source polygons or lie on a land component with no
original Roman source coverage. It never removes source-covered land. The
constrained candidate adds about 92,477 km² (2.576% of source-covered land),
after excluding about 9,183 km² of the earlier additions. The repeat audit
finds zero added neighbor overlap and zero newly colored unsupported land
components within this 6 CE source selection. Both candidates remain selectable
on `web/coastal-preview.html`; the constrained version is the default. Browser
spot checks covered Greece, the North Sea, the eastern Mediterranean and the
North African coast. The detailed eastern view still has uncoloured Aegean
islands; visual appearance alone does not resolve their historical status.

`tools/audit_coastal_strip_intervals.py` screened the adjacent pinned Roman
source intervals using the same local land crop. The raw 25 km method would add
2.796% at 1–5 CE, 2.832% at 6–8 CE, and 2.893% at 9–13 CE. Each raw slice also
adds thousands of square kilometres over other top-level source polygons and
onto land components without Roman source coverage. The corresponding stored
authority records (native IDs 16261, 16269 and 16272) are **not exactly equal**
to the GitHub features. The 14–22 CE release uses specialist AWMC geometry, so
the GitHub interval is not a candidate replacement for it. This is a source-level
screen, not visual acceptance or release source-to-record reconciliation.

The initial evidence-app integration exposed the candidate at
`web/index.html?coastal-preview=1` while leaving the default map unchanged.
That step established the 6–8 CE geometry-ID guard and verified the released
9–13 CE record still appeared at 9 CE. It preceded the temporary live decision
below.

The earlier 2% limit still is not met. The sponsor's local-candidate authorization
does not promote the GitHub variant or the 25 km rule to released/canonical
status. Broader dates, other regions, historical island/border review and the
normal release gate remain open.

### Temporary live presentation decision

The sponsor subsequently authorized shipping the **best temporary map fix live**
while reserving a fuller solution for later work. The web client now selects the
constrained 6–8 CE Roman fill by default only when the API reports v0.8.1 and
the pinned land hash. A visible notice identifies the 2.576% presentation
addition and links to `?coastal-fit=off&year=6` for the released geometry.
Dates outside 6–8 CE, missing assets, and mismatched release/land metadata use
the released geometry. No API, canonical source, or immutable release asset is
changed. This is a scoped temporary exception to the prior 2% presentation
limit, not a new general coastal-fitting policy or a historical review decision.

Rebuild:

```powershell
python tools/build_coastal_strip_preview.py <pinned-ne_10m_land.geojson>
python tools/audit_coastal_strip_preview.py
python tools/constrain_coastal_strip_preview.py
python tools/audit_coastal_strip_preview.py --candidate coastal-fit-constrained.geojson
python tools/audit_coastal_strip_intervals.py <pinned-cliopatria-archive.zip>
python -m unittest discover -s tests -p test_coastal_strip_preview.py -v
cd web
npm run build
```

The builder requires Shapely and pyproj and reads the already extracted pinned
baseline. It writes only local preview assets.
