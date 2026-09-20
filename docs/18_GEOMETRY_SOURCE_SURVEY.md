# Geometry Source Survey

Updated: 2026-09-20

## Working conclusion

Cliopatria remains the best **open global long-duration baseline** currently identified for the atlas: it covers worldwide polities from 3400 BCE to the present in one consistent GeoJSON model and publishes its construction method and source bibliography.

It should not be treated as the best geometry for every place and period. The atlas already has the correct resolver model: use a stronger specialist historical GIS where one exists, and use Cliopatria as the global fallback.

## Sources worth preferring or evaluating

### CShapes 2.0

**Evaluation status: completed for the published 2.0 dataset. Strong modern-era comparator, but not currently suitable for direct public redistribution by this atlas.**

- **Exact release / authority:** CShapes 2.0, published by ETH Zurich's International Conflict Research group and described by Schvitz et al. (2022), *Journal of Conflict Resolution* 66(1), 144–161, DOI `10.1177/00220027211013563`.
- **Temporal scope:** global independent states and dependent territories from 1886 through 2019. The companion CShapes-Europe dataset extends European coverage to 1816. This is therefore a modern historical-boundary source, not an ancient/medieval replacement.
- **Political-unit model:** unlike the earlier independent-state-only dataset, CShapes 2.0 includes colonies and other dependencies and is designed to provide near-complete global coverage of political units in its period. Two coding variants are available, based on Gleditsch-Ward and Correlates of War state-system definitions.
- **Boundary provenance:** the project documents border-change coding using the Territorial Change Dataset (Tir et al.), *Encyclopedia of International Boundaries* (Biger), and *Encyclopedia of African Boundaries* (Brownlie). This makes CShapes a substantially better-purpose specialist source than a deep-time generalized polity layer for bounded modern international-border questions.
- **Temporal model / tooling:** boundary features carry validity intervals; official distribution is available as GeoJSON, Shapefile, CSV, SQL and an R package. The raw vector products are therefore technically compatible with the atlas's offline QGIS/PostGIS comparison pipeline without format conversion being a methodological obstacle.
- **License:** ETH's official CShapes page licenses the dataset under **CC BY-NC-SA 4.0**. The Library of Congress catalogue independently records the same dataset and license. The CRAN *software package* is GPL, but that package license must not be confused with the dataset license.
- **Atlas licensing consequence:** because the atlas is intended as an openly redistributable public data product and we should not silently impose a NonCommercial/ShareAlike restriction on downstream atlas geometry, CShapes 2.0 should **not currently be copied into the canonical/public geometry layer**. It may be used for internal scholarly comparison and source discovery under the license. Public ingestion requires an explicit project-level decision that the CC BY-NC-SA obligations are compatible with the atlas's distribution model, or separate permission/clarification from the rights holders.
- **Atlas role now:** preferred **internal comparator** for modern international/state/dependency boundaries within 1886–2019 (and CShapes-Europe for 1816+ Europe), particularly when assessing whether a Cliopatria geometry is materially deficient. It does not automatically supersede Cliopatria merely because it is more specialized.
- **Promotion rule:** if licensing is resolved, replacement still requires a bounded source-vs-source comparison for the exact place/date, temporal fit, political-unit semantics, provenance retention, and normal geometry QC. Do not mix a CShapes boundary silently into a Cliopatria geometry record.
- **No semantic inference:** CShapes inclusion or dependent-territory coding says nothing by itself about slavery, territorial-practice prevalence, sovereignty in the atlas ontology, actor nationality, or evidentiary absence.

Primary documentation reviewed:
- ETH ICR CShapes dataset page: https://icr.ethz.ch/data/cshapes/
- Schvitz et al. dataset article / project page: https://icr.ethz.ch/publications/cshapes-2/
- Library of Congress CShapes 2.0 catalogue/data mirror: https://www.loc.gov/item/2023592015/

### China Historical Geographic Information System (CHGIS)

**Evaluation status: completed for Version 6. Do not directly redistribute V6 geometry in the public atlas without permission.**

- **Exact release:** CHGIS Version 6, published December 2016 by the Fairbank Center for Chinese Studies (Harvard University) and the Center for Historical Geographical Studies (Fudan University). The CHGIS site still identifies V6 as the latest released dataset.
- **Temporal scope/model:** 221 BCE–1911 CE. Time-series records have begin/end years with one-year temporal granularity and are designed to be filtered into year-specific time slices.
- **Spatial scope:** strong coverage of the core provinces of dynastic China, but CHGIS explicitly excludes Inner Mongolia, Qinghai, Xinjiang and Tibet from the main Time Series coverage. Those areas appear only in some time-slice material.
- **Polygon coverage:** the database model distinguishes point locations from jurisdictional polygons. Prefecture, province, dynasty/regime and other higher administrative units can have changing polygon objects. County-level time-series records are predominantly point locations because CHGIS states that accurate historical jurisdiction boundaries are often unavailable; county polygons exist for selected time slices such as 1911 rather than as a complete deep-time polygon series.
- **Export/tooling:** the official documentation expects desktop GIS use and explicitly supports QGIS/ArcGIS workflows. V6 distributes downloadable Time Series and Time Slice packages; published scholarship describes V6 as providing point and polygon files. This is technically compatible with offline comparison and bounded GIS evaluation in the atlas pipeline.
- **Provenance strength:** historical-instance records link to change types, temporal extents, administrative hierarchy and source-note identifiers. This makes CHGIS substantially stronger than a generic world polity layer for many China-specific identity/administrative questions.
- **License:** the V6 publication page states that it is free for academic research but prohibits commercial use, resale and redistribution. The general CHGIS introduction is more permissive in tone about scholarly use/publications, but the dataset-specific V6 license is the controlling conservative interpretation for atlas ingestion.
- **Atlas decision:** use CHGIS V6 as an **internal specialist comparator, source-discovery aid and potential geometry-validation source**, including for bounded tests such as Western Han. Do **not** ingest/publish its polygon coordinates as a public geometry source under the current license. A public CHGIS-derived geometry path requires explicit redistribution permission or a clarified license from the rights holders.
- **No inference from availability:** CHGIS polygon granularity varies by administrative level and period; absence of a polygon is not evidence that a historical jurisdiction had no territorial extent.
- **Version/lineage rule:** any internal comparison must preserve CHGIS Version 6 (2016) as the source version and retain CHGIS-native identifiers/temporal values rather than silently converting them into atlas-native claims.

Primary documentation reviewed:
- https://chgis.fas.harvard.edu/data/chgis/v6/
- https://chgis.fas.harvard.edu/pages/intro/
- https://chgis.fas.harvard.edu/pages/howto/
- https://chgis.fas.harvard.edu/pages/database/

Recent scholarly status check:
- Tao Sun, Peter K. Bol, Xiaohong Zhang, “Advancing historical geography through the Chinese Historical Geographic Information System (CHGIS),” Journal of Historical Geography (2026), DOI 10.1016/j.jhg.2026.06.018.

### Ancient World Mapping Center (AWMC) and bounded Greco-Roman boundary sources

**Evaluation status: completed for the current AWMC geodata repository and adjacent Roman GIS comparators. AWMC is a strong bounded specialist source for named snapshots, not a continuous ancient political-boundary backbone.**

- **Current AWMC source:** `AWMC/geodata`, default branch `master`. The current repository head reviewed for this evaluation is commit `7ecf8bccea2efe1e1e9df2daf6001942de73fb87` (2024-04-22). AWMC's 2026 GIS Data page still points users to this repository as its open GIS-data distribution.
- **Formats/version discipline:** AWMC states that the GeoJSON files are its most up-to-date working data; the shapefile ZIP archives are periodic snapshots. Atlas comparisons should therefore pin the exact Git commit and individual file/blob SHA rather than referring generically to “AWMC data.”
- **License:** the current GeoJSON repository is ODbL-1.0. It permits reuse, modification and redistribution, including commercial use, but attribution/share-alike and machine-readable derivative-database obligations apply. If AWMC geometry is promoted into a public atlas database, the release design must preserve those obligations rather than silently relicensing the derived database.
- **Provenance:** AWMC states that the repository is derived from the Barrington Atlas of the Greek and Roman World and AWMC modifications to OpenStreetMap. Preserve that source lineage; AWMC is not an independently source-free geometry family.
- **Current political layers:** the repository currently contains discrete political datasets for Alexander's empire, Persian extent, Hasmonean and Herodian realms, Roman extent at 60 BCE, Roman extent at 117 CE, Roman extent at 200 CE, Roman provinces at 200 CE, post-Diocletian Roman provinces, and a senatorial-province layer. These are separately named files, not one temporally continuous polygon series.
- **Temporal semantics:** most inspected political GeoJSON files encode the date/context in the file/directory name rather than as a standardized per-feature begin/end-year field. The generic AWMC attribute vocabulary includes `timeperiod`/PeriodO support, but the inspected Roman extent/province files retain legacy GIS attributes and cannot be treated as a normalized temporal database without an explicit source-specific crosswalk.
- **Geometry quality:** AWMC's Roman layers are substantially more detailed than the generic Cliopatria polity polygons and are already aligned to an ancient-world cartographic workflow, but historical inland borders remain interpreted reconstructions. Physical coastline still comes from the atlas's Natural Earth render fabric; never promote AWMC merely because its shoreline is more detailed.
- **Atlas role:** AWMC is a **preferred candidate source for bounded Greco-Roman comparison at dates for which AWMC publishes an explicit layer**, especially Roman 60 BCE / 117 CE / 200 CE and 200 CE province cases. Replacement of a Cliopatria geometry still requires exact date/entity semantic matching, bounded source-vs-source comparison, normal D-048 quantitative QC, D-050 visual/semantic acceptance, and explicit ODbL release handling.
- **No interpolation:** do not interpolate an arbitrary Roman boundary between AWMC snapshots or infer that a named snapshot remains valid until the next available file. Unsupported intermediate years continue to use another defensible source/fallback or remain unresolved.
- **Third-party mirrors:** older AWMC-derived mirrors expose additional dates such as 14 CE and 69 CE, but the current AWMC repository does not presently contain those layers. Do not silently ingest a mirror as though it were current AWMC; recover/pin the original AWMC source and provenance first.

Adjacent Roman datasets reviewed:

- **Mapping Past Societies / DARMC (Harvard):** useful supplementary dated comparator. Its map-source documentation identifies Roman province layers around 117 CE, 303–324 CE and 500 CE, based on the Barrington Atlas. Downloadable MAPS data are released under CC BY-NC-SA 4.0. Use for bounded comparison/source discovery; public ingestion requires explicit handling of NonCommercial/ShareAlike obligations and exact layer/version provenance.
- **Digital Atlas of the Roman Empire (DARE):** a public GeoJSON/API resource and useful place/province comparator. The inspected GitHub `provinces.geojson` is distributed in an Apache-2.0 repository but contains province names and database timestamps, not a historical validity date. Do not treat that file as a dated province boundary source until the intended historical slice and upstream data rights are independently documented.
- **Pleiades:** remains the preferred scholarly gazetteer/identity source for ancient places and some local geometries, but is not a continuous Roman or Greco-Roman polity-boundary series.

Primary material reviewed:
- https://awmc.unc.edu/gis-data/
- https://github.com/AWMC/geodata
- https://darmc.harvard.edu/map-sources
- https://darmc.harvard.edu/data-availability
- https://www.imperium.ahlfeldt.se/

**Current atlas decision:** AWMC may outrank Cliopatria for an exact bounded Greco-Roman snapshot when semantic/date fit, provenance, license handling and geometry QC all pass. It does not become the ancient-world default and it does not authorize temporal interpolation between snapshots.
### OpenHistoricalMap

**Evaluation status: completed. Retain as supplementary/source-discovery material and a case-by-case geometry candidate; do not assign automatic authority or global precedence.**

- **Project/model:** OpenHistoricalMap (OHM) is a global, community-edited historical map built on the OpenStreetMap data model. Administrative areas use boundary relations and can carry `start_date`, `end_date`, `admin_level`, `border_type`, source and other provenance tags.
- **Temporal capability:** the production map/time-slider filters features using basic `start_date=*` and `end_date=*`. OHM also documents richer EDTF-style date tags, but current slider support does not uniformly honor `start_date:edtf` / `end_date:edtf`. The atlas must therefore preserve OHM's raw temporal strings/uncertainty rather than treating the visible OHM time filter as an authoritative normalization.
- **Coverage reality:** OHM's own administrative-boundary project describes the first goal as mapping current top-level boundaries globally, with historical backfilling as an additional goal, and lists country coverage as uneven/partial. Coverage is contributor- and project-dependent rather than a completed scholarly global series.
- **License:** OHM data is CC0/public-domain by default unless an element carries its own `license=*` restriction. A small subset has feature-specific open licenses; some inherited physical features have older OSM licensing lineage. Any atlas import must inspect and retain feature-level `license`, `attribution` and `source` tags rather than assuming every selected geometry is unconditionally CC0.
- **Data access:** OHM supports normal OSM-style raw API/export, Overpass querying, bulk data paths and vector-tile delivery. This is technically compatible with targeted extraction and QGIS/PostGIS comparison, but API convenience does not establish historical authority.
- **Boundary semantics:** OHM documents an “on the ground” approach to disputed boundaries, generally preferring internationally recognized/physical-control realities and allowing approximate lines where borders are unclear. That may differ from the atlas's historical-jurisdiction question in a given case, so semantic matching is mandatory.
- **Versioning requirement:** if an OHM feature is used for research or promoted geometry, retain the element/relation ID, element version, retrieval timestamp, raw tags, member geometry lineage and source/license tags. A mutable live relation without a pinned version is not sufficient release provenance.
- **Promotion gate:** an OHM boundary may outrank Cliopatria only for a bounded case when the exact feature has adequate cited provenance, defensible temporal fit, complete/valid relation geometry, compatible licensing, and a source-vs-source comparison demonstrating improvement. Community popularity or map detail alone is not evidence of correctness.
- **No absence inference:** absence of a boundary, date, source tag or country coverage in OHM is a research-coverage state only. It must never be translated into territorial-practice absence, political nonexistence, or an unresolved geometry being “ocean.”
- **No automatic source-family precedence:** unlike a versioned specialist scholarly GIS, OHM is heterogeneous at feature level. Precedence therefore belongs to an accepted **feature/version**, not to OHM globally.

Primary documentation reviewed:
- https://wiki.openstreetmap.org/wiki/OpenHistoricalMap/Boundaries
- https://wiki.openstreetmap.org/wiki/OpenHistoricalMap/Projects/Administrative_Boundaries
- https://wiki.openstreetmap.org/wiki/OpenHistoricalMap/License
- https://wiki.openstreetmap.org/wiki/OpenHistoricalMap/Tags/Key/license
- https://wiki.openstreetmap.org/wiki/OpenHistoricalMap/Tags/Key/start_date
- https://wiki.openstreetmap.org/wiki/OpenHistoricalMap/QGIS
- https://www.openhistoricalmap.org/export

**Current atlas decision:** use OHM to discover sources, reconcile identities, inspect local historical boundaries and propose bounded geometry candidates. Never use OHM coverage density as an authority signal; every promoted OHM geometry must be independently reviewed and pinned at feature/version level.

### Pleiades
- Scope: ancient places, locations, names and connections, strongest in the Greek and Roman world.
- Strength: mature scholarly gazetteer with open data and editorial provenance.
- Atlas role: excellent for place identity, point locations and some local polygons.
- Limitation: not a replacement for a global polity-boundary time series.

### GeaCron / Running Reality
- Strength: broad world historical map coverage.
- Limitation: Cliopatria's published comparison notes that the underlying data are not as openly available for scholarly computational use and that construction references are not equivalently exposed.
- Atlas role: visual/reference comparison only unless data accessibility and provenance materially improve.

### CONFOEDERATIO Atlas / Naissance HGIS

**Evaluation status: completed for the currently public beta material. Retain as an experimental global comparator; do not give the source family automatic or specialist precedence yet.**

- **Project/source:** Confoederatio's Atlas is a global historical-border dataset edited/viewed through Naissance HGIS. The public project describes de facto polity extents at sub-yearly resolution and separately uses CShapes 2.0 for de jure modern borders.
- **Current maturity:** the public Atlas is explicitly labelled **Beta (Ongoing)** / work-in-progress. The Dataview currently identifies itself as `Version 0.5b` with domain 3300 BCE–2014 CE, while the current Naissance README describes Atlas as 3000 BCE–2026 CE and the repository bundles `saves/atlas_0.51b.naissance` (50 MB), updated in commit `78a55e2b24b3e04ce8c205e3a849a71801e2ba85` on 2026-06-10. These are meaningful version/domain inconsistencies for reproducible research.
- **Temporal machinery:** Naissance stores history as geometry keyframes and can use static or interpolated transitions depending on the use case. Public Atlas material is described as sub-yearly; daily keyframes are available on request, while public files may be simplified/compressed. The atlas must therefore never assume that an interpolated visual boundary represents an independently evidenced historical boundary at every intermediate date.
- **License:** Confoederatio currently states that accessible CRD work, including datasets, is MIT-licensed. That is permissive for the project's own de facto material. However, Atlas also states that de jure extents use CShapes 2.0; those upstream CShapes geometries retain their own CC BY-NC-SA 4.0 obligations and cannot be treated as relicensed by a general MIT statement.
- **Source base:** Confoederatio publishes/maintains a large historical-map and atlas archive (`Preservés`) and lists many reference works used in its broader research environment. During this evaluation, however, no public machine-readable or clearly documented **per-polity/per-keyframe citation mapping** for Atlas 0.5b/0.51b was identified. A general archive catalogue is not equivalent to claim-specific geometry provenance.
- **Reproducibility consequence:** any future Atlas comparison must pin the exact downloadable dataset/save version, file checksum, Naissance version and extraction method. Referring simply to “Confoederatio Atlas” is insufficient while public 0.5b/0.51b scope descriptions differ and the public dataset is under active refinement.
- **Atlas role now:** useful **second-global-baseline benchmark** for stress-testing Cliopatria and locating suspicious extents/gaps across regions that lack specialist GIS. It may motivate further source research, but the geometry itself should not be promoted merely because it appears more detailed or temporally dense.
- **Promotion threshold:** a Confoederatio geometry may only become a candidate source for a bounded case if its exact geometry/keyframe can be traced to adequate source citations, its temporal semantics are explicit, its source-native version/ID is preserved, applicable upstream licensing is resolved, and a bounded comparison demonstrates a defensible improvement.
- **No interpolation / no archive-density inference:** Naissance's ability to interpolate keyframes is a visualization/tooling capability, not historical evidence. Likewise the size of the Preservés archive cannot mechanically establish boundary accuracy, political control, territorial-practice prevalence or evidentiary confidence.
- **Tooling:** Naissance HGIS itself is an interesting experimental editor for spatiotemporal GIS/keyframe inspection. There is no current reason to replace the atlas's QGIS/GEOS/GDAL + MapLibre production architecture with it; evaluate the editor separately only if a concrete workflow benefit emerges.

Primary material reviewed:
- https://confoederatio.org/
- https://confoederatio.org/pages/dataview
- https://github.com/ConfoederatioVF/Naissance
- `ConfoederatioVF/Naissance` bundled save `saves/atlas_0.51b.naissance`, Git blob `4c33f013d11fd4364cdeeacc274942ba6c5456d4`

**Current atlas decision:** keep Confoederatio Atlas as an experimental comparator/source-discovery aid. Do not use it as a default replacement for Cliopatria or a specialist regional source until exact-version provenance and feature/keyframe source traceability are strong enough for the atlas's claim-specific evidence standard.

## Source strategy

D-055 separates candidate discovery from accepted precedence.

Resolver order:

1. accepted specialist geometry for the exact bounded entity/time case;
2. Cliopatria as the open global temporal baseline;
3. other defensible historical geometry marked approximate;
4. modern proxy, explicitly marked;
5. unresolved, with neutral world land retained.

### Current candidate guidance

| Region / period / source | Current role | Public-source precedence today |
| --- | --- | --- |
| **Cliopatria, global 3400 BCE–2024 CE** | Open global baseline/fallback | Yes, unless an explicitly accepted specialist case supersedes it |
| **AWMC, explicit Greco-Roman snapshot dates** | Strong bounded specialist candidate | Possible after exact date/entity match, ODbL handling and bounded acceptance |
| **CHGIS V6, China 221 BCE–1911 CE** | Strong internal specialist comparator | No direct public polygon redistribution under current V6 terms without permission |
| **CShapes 2.0, global 1886–2019; CShapes-Europe 1816+** | Strong modern internal comparator | Not yet; requires an explicit atlas distribution-license decision/permission for CC BY-NC-SA geometry |
| **OpenHistoricalMap** | Source discovery / local feature-level candidate | Never by family; only an individually pinned relation/version after provenance review |
| **Confoederatio Atlas / Naissance** | Experimental second-global-baseline comparator | No; beta/version/provenance limitations currently block source-family precedence |
| **Baekje 347–391 CE specialist search** | No period-appropriate promotion-ready specialist vector found | Keep current source/fallback; failed render remains quarantined |

This table is research guidance, not executable routing logic. Source status can change as versions, licenses, scholarship and provenance improve.

### Replacement gate

A source replacement requires all of:

- same historical target / defensible semantic equivalence;
- temporal fit without unsupported interpolation;
- exact version/native ID and claim-specific lineage;
- compatible publication rights;
- valid geometry/topology;
- a bounded comparison demonstrating a defensible improvement;
- explicit historical/semantic acceptance and normal render QC.

One geometry record carries one historical source lineage. A composite historical reconstruction, if ever needed, must be registered as a new derived source/version with all contributors and methodology preserved. Natural Earth remains a render-only physical coastline/land fabric and does not count as changing the historical source family.

The physical coastline is a separate concern: Natural Earth remains the canonical cartographic land/coastline fabric. A historical political source does not become the physical coastline authority.

## Case investigation — Baekje (347–391 CE)

**Status:** investigated; no promotion-ready specialist vector replacement identified.

The quarantined Baekje candidate is not a reason to relax the generic Cliopatria render-QC gates. A targeted source search found:

- The National Institute of Korean History (NIKH) Historical Geographic Information Database is an authoritative Korean historical-GIS project and publishes downloadable polygon GIS data, but its currently documented nationwide polygon coverage is modern: principally 1910–1945 and 1955–1975. It therefore cannot be reused as a 4th-century Baekje boundary source.
  - https://hgis.history.go.kr/
  - https://hgis.history.go.kr/pro_g1/intro/intro01.do
  - https://hgis.history.go.kr/pro_g1/dataset.do
- Specialist Korean historical-geography scholarship does reconstruct ancient interstate borders. A useful example is *한국 고대 사국의 국경선* (Kim Tae-sik et al.), which explicitly synthesizes scholarly border reconstructions and map drafts, but its principal scope is the **late 5th century**, later than the atlas's current Baekje geometry slice (347–391 CE), and it was not identified as an open machine-readable vector dataset with redistribution terms suitable for direct ingestion.
- Other located Baekje historical-geography scholarship is valuable for interpretation and source discovery but likewise does not currently provide a versioned, license-clear 347–391 CE polygon dataset suitable for replacing the Cliopatria source geometry.

**Decision for the current atlas state:**

1. Keep the Baekje QGIS candidate e5a720f8-9e22-45fe-a5b0-c6464686525d quarantined/fallback.
2. Do not create a hand-drawn or inferred replacement polygon from a printed map.
3. Do not substitute modern Korean administrative GIS for an ancient political extent.
4. Preserve the current source geometry/provenance while withholding the failed transformed render from promotion.
5. Reopen the source search only when a period-appropriate specialist dataset or citable reconstruction can be ingested with explicit provenance, temporal fit and redistribution rights.
6. Treat the current evidence claim's bounded-event semantics separately from polity geometry: even a better Baekje polity polygon would not by itself establish territory-wide prevalence.

This is a resolved source-search outcome, not a claim that the surviving Cliopatria Baekje polygon is historically superior. Unknown/unsupported geometry remains preferable to false precision.

## Near-term evaluation backlog

- CShapes 2.0 evaluation complete: strong modern specialist comparator for 1886–2019 (CShapes-Europe 1816+), but dataset licensing is CC BY-NC-SA 4.0; do not directly ingest into the public canonical geometry layer without an explicit license/distribution decision or permission.
- CHGIS V6 evaluation complete: technically suitable for internal comparison, but direct public redistribution is blocked by the dataset-specific license pending explicit permission.
- AWMC / bounded Greco-Roman evaluation complete: use current AWMC ODbL GeoJSON snapshots as preferred candidates only for exact supported dates/entities; MAPS/DARMC and DARE remain supplementary comparators with their own temporal/license limits.
- OpenHistoricalMap evaluation complete: global/community temporal infrastructure is valuable, but coverage/provenance are feature-level and uneven. Use as supplementary/source discovery and accept individual pinned relations only after source/date/license/geometry review; no global OHM precedence.
- CONFOEDERATIO/Naissance evaluation complete: Atlas is a useful experimental second-global-baseline comparator, but its beta/WIP status, public version/domain inconsistencies, compressed/keyframed temporal model and currently unverified feature-level source traceability block source-family precedence or direct promotion.
