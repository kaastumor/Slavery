# Geometry Source Survey

Updated: 2026-09-20

## Working conclusion

Cliopatria remains the best **open global long-duration baseline** currently identified for the atlas: it covers worldwide polities from 3400 BCE to the present in one consistent GeoJSON model and publishes its construction method and source bibliography.

It should not be treated as the best geometry for every place and period. The atlas already has the correct resolver model: use a stronger specialist historical GIS where one exists, and use Cliopatria as the global fallback.

## Sources worth preferring or evaluating

### CShapes 2.0

**Evaluation status: completed. Strong preferred-source candidate for global state/dependency boundaries from 1886–2019, subject to bounded geometry comparison and CC BY-NC-SA compliance.**

- **Exact release:** CShapes 2.0, published with the 2022 Journal of Conflict Resolution dataset paper. The ETH Zürich International Conflict Research site identifies 2.0 as the current raw CShapes release.
- **Temporal scope:** global independent states and dependent territories from 1886 through 2019. The peer-reviewed dataset records territorial changes at their effective dates rather than only annual snapshots, making its temporal resolution materially stronger than coarse historical-atlas slices.
- **Coverage:** near-complete recent international-system coverage because dependencies/colonies are represented as well as independent states. It does not provide subnational administrative boundaries.
- **Export/tooling:** ETH distributes CSV, tab-delimited, GeoJSON, Shapefile, SQL and R formats. This is directly compatible with the atlas offline GIS/build pipeline and allows preservation of source-native identifiers/attributes alongside normalized geometry.
- **License:** the official ETH dataset page licenses CShapes under CC BY-NC-SA 4.0. Redistribution and adaptation are therefore possible for non-commercial use with attribution and ShareAlike obligations. This is materially more usable for a public atlas than CHGIS V6, but the NonCommercial/ShareAlike conditions must be carried into any release/licensing review before public ingestion.
- **Atlas fit:** CShapes is a strong candidate to supersede Cliopatria for state/dependency geometry within 1886–2019, especially colonial/dependent-territory boundaries. It should not replace Cliopatria outside its period or for non-state/subnational historical entities.
- **Do not auto-promote:** source reputation and licensing are not sufficient to replace existing geometry automatically. Run bounded comparisons against Cliopatria/current approved geometry for representative colonial, post-colonial, island/fragmented and border-change cases, including topology/coastline interaction with the Natural Earth render fabric.
- **Temporal identity rule:** preserve CShapes start/end dates and source-native identifiers exactly. Do not coerce its state/dependency model into atlas polity semantics where the concepts differ; document any crosswalk.
- **2019 cutoff:** CShapes 2.0 does not provide the atlas's post-2019 modern boundary layer. Later dates still require another reviewed modern source/fallback.
- **Separate Europe extension:** CShape-Europe is a distinct newer dataset and may extend useful European historical coverage; it is not evidence that the global CShapes 2.0 product itself covers the pre-1886 world.

Primary sources reviewed:
- https://icr.ethz.ch/data/cshapes/
- https://doi.org/10.1177/00220027211013563
- https://www.loc.gov/item/2023592015/

**Current atlas decision:** mark CShapes 2.0 as a preferred-source candidate for 1886–2019 state/dependency geometry. Before any public ingestion, complete a bounded geometry benchmark and confirm that the atlas distribution model satisfies CC BY-NC-SA 4.0 attribution, NonCommercial and ShareAlike conditions.

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

### OpenHistoricalMap
- Scope: global collaborative historical mapping with temporal administrative boundaries and other historical features.
- Strength: standard OSM-style vector model, active community, potentially much more detailed local coverage.
- Atlas role: useful supplementary geometry/source discovery and a possible specialist fallback after provenance review.
- Limitation: coverage and scholarly review are uneven; it is not a single curated global historical-boundary authority.

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
- Scope claimed by the project: global de facto polity extents from 3300 BCE to 2014 CE, currently beta.
- Potential: unusually close functional alternative to Cliopatria and worth direct evaluation.
- Atlas role: candidate benchmark/source after license, provenance, version stability and scholarly validation are assessed.
- Limitation: comparatively new beta dataset; do not replace Cliopatria merely because it is newer.

## Source strategy

1. Specialist historical GIS with stronger regional scholarship and compatible licensing.
2. Cliopatria as the open global temporal backbone.
3. Other reviewed historical geometry sources where they improve a bounded case.
4. Approximate historical geometry, explicitly marked.
5. Modern proxy only when defensible and explicitly marked.
6. Unresolved when no defensible geometry exists.

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

- CShapes 2.0 source evaluation complete; next use is a bounded CShapes-vs-Cliopatria geometry benchmark before any replacement/promotion.
- CHGIS V6 evaluation complete: technically suitable for internal comparison, but direct public redistribution is blocked by the dataset-specific license pending explicit permission.
- Sample OpenHistoricalMap administrative boundary completeness for several benchmark dates/regions.
- Audit CONFOEDERATIO/Naissance licensing, provenance, source citations, temporal resolution and geometry quality before considering it as a second global baseline.
