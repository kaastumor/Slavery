# Geometry Source Survey

Updated: 2026-09-20

## Working conclusion

Cliopatria remains the best **open global long-duration baseline** currently identified for the atlas: it covers worldwide polities from 3400 BCE to the present in one consistent GeoJSON model and publishes its construction method and source bibliography.

It should not be treated as the best geometry for every place and period. The atlas already has the correct resolver model: use a stronger specialist historical GIS where one exists, and use Cliopatria as the global fallback.

## Sources worth preferring or evaluating

### CShapes 2.0
- Scope: independent states and dependent territories, 1886–2019 globally; European coverage extends to 1816.
- Strength: peer-reviewed research dataset built specifically for historical international borders.
- Atlas role: strong candidate to supersede Cliopatria for modern state/colonial boundaries in its covered period.
- Limitation: no ancient/medieval coverage.

### China Historical Geographic Information System (CHGIS)
- Scope: Chinese administrative geography from 221 BCE to 1911 CE, with detailed time-aware administrative units and source notes.
- Strength: specialist Harvard/Fudan historical GIS with much deeper regional granularity and scholarship than a world atlas can provide.
- Atlas role: evaluate as a preferred China source where its geometry, temporal model, and license permit public redistribution.
- Limitation: regional; licensing differs between releases and must be checked before publication.

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

- Compare CShapes 2.0 against Cliopatria for 1886–2019.
- Check CHGIS v6 license and polygon export suitability before ingesting China.
- Sample OpenHistoricalMap administrative boundary completeness for several benchmark dates/regions.
- Audit CONFOEDERATIO/Naissance licensing, provenance, source citations, temporal resolution and geometry quality before considering it as a second global baseline.
