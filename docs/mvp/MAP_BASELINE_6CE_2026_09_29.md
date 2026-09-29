# 6 CE map reset and structural investigation

Follow-up: the untouched reset is now at `web/raw-baseline.html`. The coastal
comparison is at `web/coastal-preview.html`; the local root again serves the
evidence application. See [the coastal fitting preview](COASTAL_FIT_PREVIEW_2026_09_29.md)
for the candidate and its subsequent adversarial audit. The investigation below
records the preceding reset phase.

## Scope and status

Requested outcome: remove the accumulated custom fixes from the working map,
inspect the original polygons and basemap, and compare with Cliopatria/Seshat
before choosing another correction.

This branch replaces `web/index.html` with a raw-source inspection page. Its
active path does not load the Atlas application, API, transformed release assets,
Natural Earth land clipping, coastal buffers/recovery, Chaikin smoothing, QGIS
preprocessing, or AWMC substitutions. Leaflet draws the source GeoJSON directly.
The page defaults to the exact stored Seshat API geometry used for Rome at 6 CE.
Radio controls select the GitHub export for comparison; neighbouring source
polities and Esri imagery can be toggled separately.

This is a local inspection reset, **not a production candidate**. The existing
application, migration history, reproduction tools and immutable published
releases remain in the repository. No new geometry correction, merge, public
channel switch, deployment or production database change was made.

## What was checked

- User screenshot: 6 CE, Roman Mediterranean coverage.
- Stored source: geometry `edb239a8-4d54-44e4-970a-affb7c9af22e`, native Seshat
  record `16269`, interval 6–8 CE, from the v0.8.1 authority bundle.
- Original GitHub archive: Cliopatria commit
  `ad28a691b7c07c1fca89d0e0636d324667d2a258`, archive SHA-256
  `d01ae3a20d358cc5d54f69d9d725d390767d9c8759ac89ad6f90c58d106f3370`.
- Natural Earth 1:10m land used by the published map, SHA-256
  `1ac90796408bc6ad6911d69448485d3c4dbf2190370080368a09976e1c9f7416`.
- Published `v0.8.1-public-mvp-v2` Roman asset and its generating code.
- [Seshat's live viewer](https://seshat-db.com/core/world_map/), with its visible
  year control set to **6 CE**, at regional and detailed Adriatic zoom levels.
  Its URL retained `year=117`; the visible year slider/readout was the inspected
  state. This URL is therefore not a reproducible year bookmark.
- Seshat's actual `plotPolities` renderer and basemap configuration, plus the
  [Cliopatria notebook renderer](https://github.com/Seshat-Global-History-Databank/cliopatria/blob/main/notebooks/map_functions.py).

## Structural findings

### Two independent coastlines are being combined

The Atlas draws a detailed Natural Earth land fill and coastline, then historical
evidence geometry. The historical source has a much coarser, independently drawn
coastline. These boundaries do not coincide. Intersecting them can split a
continuous source region into islands and slivers; where the historical outline
lies inland, clipping cannot fill the uncovered land.

The v2 builder starts with source intersected with land, then attempts recovery
from the source's **offshore overhang**, using a 25 km buffer and an added-area
gate of 2%. That mechanism is directional: it can recover land near an offshore
overhang, but does not guarantee correction along an inward-offset source coast.
The near-zero source-land-loss test does not detect land already excluded by the
original source/land intersection. Passing it did not establish visual alignment.

The Mediterranean's many bays, narrow peninsulas and small islands expose the
mismatch strongly. A coast where the source extends offshore can look much
cleaner after clipping. This explains why uniform-looking results should not be
expected across regions; no blanket claim that every North Sea coast is correct
has been established.

### Seshat does not secretly align these coastlines

The live Seshat viewer uses Leaflet `L.geoJSON(JSON.parse(shape.geom_json))` over
Esri World Imagery. Its normal polygon border weight is 0 and fill opacity is
0.7. Detailed visual inspection at 6 CE shows coarse offsets, offshore extensions
and some uncovered coast there too. It does not perform the Atlas's Natural
Earth intersection or coastal recovery in this drawing path.

The notebook instead uses CARTO Voyager raster tiles with direct GeoJSON drawing.
That tile endpoint currently displayed an API-key-required image during this
inspection, so it was not accepted as a successful visual reference.

Seshat also draws neighbouring political entities. Atlas draws only regions
with active evidence. Some large blank regions therefore reflect different
coverage semantics, separate from the small coastline defects.

### The two upstream source variants are not identical

The stored source is labelled `Cliopatria v0.2.0-duplicate via Seshat API`.
Its shape is not geometrically equal to the pinned GitHub Roman feature. Both
have 32 components, but the stored API geometry has 13 interior rings whereas
the GitHub feature has none. Their exact historical/version relationship has
not been established; the GitHub export must not silently replace the stored
authority as if it were byte-equivalent.

### Screenshot follow-up: Gulf of Corinth

The user's second close-up selects the stored Seshat API geometry; the third
selects the GitHub geometry. The angular cutouts around the Gulf of Corinth are
present in the stored source and absent from the GitHub feature.

Follow-up retrieval of [Seshat API record 16269](https://seshat-db.com/api/core/cliopatria-shapefiles/16269/)
on 2026-09-29 established that **both `geom` and `simplified_geom` exactly match
the stored geometry**, coordinate for coordinate (`equals_exact(..., 0)`). Both
contain 32 components, 13 interior rings and 1,325 vertices. Thus these cutouts
are already present in the upstream API response; the local import, Leaflet,
and the later Atlas clipping are not their point of introduction.

Six of the API interior rings lie in the Gulf of Corinth region (approximately
22.20–23.06 E, 37.96–38.42 N). The largest has about 1,400 square kilometres of
area; five smaller rings are about 49 square kilometres each (EPSG:6933
equal-area calculation). These are geometric cutouts, not evidence of historical
exclusions. Their provenance/intent has not been established.

The source variants also differ in their outer boundaries: removing interior
rings for analysis does not make their shapes equal. Stored-source outer rings
have 1,252 vertices versus GitHub's 1,256. This rules out treating the entire
difference as merely missing hole handling in the viewer.

Metadata differs too: the API record has `member_of: "(Roman Empire)"`, whereas
the pinned GitHub feature has empty `MemberOf`. Searching the complete pinned
archive finds only one Roman Empire feature covering 6 CE, at zero-based ordinal
1118 (6–8 CE). No alternative Roman component in that archive explains the API
record. The exact upstream version/processing relationship remains unresolved.

The GitHub view visibly fills across the gulf's water as well as eliminating
the angular gaps. It is a useful clean source comparison, but its smoother
appearance alone does not establish coastline alignment or justify promotion.
This follow-up changed documentation only; no geometry correction was applied.

| Geometry inspected | Components | Interior rings | Vertices |
| --- | ---: | ---: | ---: |
| GitHub original | 32 | 0 | 1,256 |
| GitHub original intersected with land (analysis only) | 96 | 0 | 10,067 |
| Stored API original | 32 | 13 | 1,325 |
| Stored API original intersected with land (analysis only) | 94 | 1 | 10,008 |
| Published v2 | 67 | 8 | 21,401 |

All inspected geometries were valid. Component counts alone do not classify
each island as an error. They show that clipping changes structure materially;
they are not a historical coverage score. Analysis intersections are not used
by the baseline viewer.

## Verification and reproduction

`tools/build_raw_cliopatria_baseline.py` verifies the archive hash, selects the
46 top-level source features active at source-native year 6, and copies their
complete features without coordinate operations. It additionally decodes the
stored Roman EWKB to GeoJSON without rounding or spatial transformations.
`web/public/source-baseline/manifest.json` records provenance and output hashes.

```powershell
python tools/build_raw_cliopatria_baseline.py <pinned-archive.zip> --authority data/release_candidates/v0.8.1-rome-geometry-authority.bundle.json
cd web
npm ci
npm run dev
```

The extractor's stored-source export requires Shapely. The inspection page also
needs access to the Leaflet CDN and Esri tiles.

Actual checks on 2026-09-29:

- All 46 emitted GitHub features exactly equal the corresponding archive
  features, including their coordinates and properties: passed.
- Emitted stored-source geometry `equals_exact(authority, 0)`: passed.
- Raw baseline loaded in browser; stored API/GitHub selection and imagery
  verified, with Mediterranean geometry visually inspected: passed.
- `npm ci`, then `npm run build` via the bundled pnpm launcher for npm 11.6.2:
  passed (existing large-chunk warning).
- `python tools/sanitize_repo.py`: passed.
- `python -m unittest discover -s tests -v`: **not passed**; 355 tests,
  14 failures, 14 errors, 2 skipped. Two failures specifically enforce the
  canonical root entrypoint, which this inspection reset deliberately replaces.
  Other failures/errors report frozen artifact/hash or CRLF byte differences
  and missing `psycopg`. They were not repaired as part of this investigation.
- No development database validation or release promotion checks were run;
  this work does not alter schema or publish a release.

Self-review conclusion: the clean baseline is suitable for inspection. It is
not suitable for merging as the public evidence application. The next design
decision is how to combine source historical boundaries with a basemap, with
explicit source-version choice and coastal visual acceptance scenes. No new
buffer, smoothing threshold, manual fill, or historical boundary change has
been chosen.
