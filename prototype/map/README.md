# First map slice

A deliberately small UI proof for the Historical Slavery Atlas.

## What it proves

- a neutral world land layer is always visible;
- a selected year controls claim visibility;
- a territorial-practice area can be highlighted;
- clicking the area exposes evidence/source information;
- P-level can remain visibly unassigned;
- modern-proxy geometry is clearly distinguished from historical/exact geometry.

The current slice is **Brazil at year 2000**, using the canonical v0.6.1 Brazil evidence row and a Natural Earth modern country polygon.

This is not yet database-driven. That is intentional: it isolates the map interaction before we introduce an API. The next step is to replace `data/slice.json` and the proxy geometry with output exported from PostgreSQL/PostGIS.

## Run locally

From the repository root:

```bash
cd prototype/map
python -m http.server 8000
```

Then open `http://localhost:8000`.

## Dependencies

MapLibre GL JS 6.10.0 is loaded directly as an ES module from unpkg for this proof. No npm project or frontend framework is introduced yet.

## Data provenance

- Historical evidence: canonical v0.6.1 workbook, Brazil row in `v0.4.7 Evidence`.
- Neutral land: Natural Earth `ne_110m_land.geojson`, copied from the public Natural Earth vector repository.
- Brazil modern proxy: extracted from Natural Earth `ne_110m_admin_0_countries.geojson`.
- Natural Earth Admin 0 Countries current release page identifies the 1:110m dataset as version 5.1.1.
- Natural Earth country boundaries are contemporary/de facto cartography and are used here only as an explicit `modern_proxy`.

This prototype must not be treated as the historical geometry resolver.
