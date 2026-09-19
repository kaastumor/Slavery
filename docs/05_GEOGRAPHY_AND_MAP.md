# Geography and Map Rules

## Base layer

Always render a neutral world land outline. No-data areas remain land.

Missing historical political geometry must never be rendered as ocean, disappearance, or evidence of no slavery.

## Spatial identity

Map targets are not limited to polities. Use `SPATIAL_ENTITY` for polities, regions, provinces, cities, ports, sites and other defensible geographic units.

`POLITY` is a specialization of `SPATIAL_ENTITY`.

A place such as a port must not carry one timeless political owner. Historical containment/control is represented through time-bounded spatial relationships.

## Historical boundary backbone

Intended backbone: Cliopatria / Seshat Global History Databank historical political polygons, using valid date ranges and source identifiers where available.

## Geometry resolver hierarchy

For a selected year:

1. Exact Cliopatria polygon valid for that year
2. Better specialist historical geometry where available and defensible
3. Nearest defensible historical geometry, marked `approximate_historical`
4. Modern geographic proxy, marked `modern_proxy`
5. No political polygon; retain neutral world land only and mark geometry unresolved

Never silently substitute a modern boundary for a historical one.

## Required geometry metadata

Every mapped historical geometry should expose:

- `spatial_entity_id`
- target year / interval
- source version
- source-native spatial/polity identifier
- validity interval
- temporal precision where relevant
- resolution method
- accuracy status
- whether geometry is exact, specialist, approximate or proxy

## Temporal rule

A claim and a geometry must overlap in time to be joined.

Do not attach a historical claim to a later nation-state solely because the modern location falls within it.

Internally, temporal joins should use the project historical-year convention defined in `04_DATA_MODEL.md` and `11_SYSTEM_ARCHITECTURE.md`.

## Visual separation

Conceptual layers:

- neutral land base
- historical polity/other geometry
- territorial practice fill P0–P4
- legal status overlay
- research coverage / uncertainty overlay
- participation networks: voyages, ports, actors, companies, finance

Do not let voyage density recolor territorial practice.

## Web-map delivery

The map client should not dictate the research data model.

Preferred client: MapLibre GL JS.

Use the simplest suitable delivery format per layer:

- GeoJSON is acceptable for small/simple/static layers
- vector tiles are preferred for large, detailed or dense global layers
- detailed claims/sources should normally be loaded through an API rather than embedded fully in map tiles

Martin is the preferred initial/prototype PostGIS/vector-tile server, but it is not a permanent methodological dependency.

PMTiles may later be used for stable/read-heavy published layers or release snapshots; it is optional rather than required.

## Map-query principle

The selected year and selected layer/filter determine the visible state. Do not pre-create one duplicated full-world dataset for every year when the same result can be obtained from time-bounded records.

## Published coastline clipping

Historical polity polygons may contain coarse reconstructed coastlines that extend into the neutral ocean/land base layer.

For public map rendering only, polygonal reviewed geometry may be intersected with the atlas neutral land mask before delivery.

Rules:

- canonical/research geometry in `atlas.geometry` remains unchanged;
- reviewed source geometry in `publish.geometry` remains unchanged;
- coastline clipping is applied only in a dedicated map/render view such as `publish.map_geometry`;
- points and non-polygon geometries are not land-clipped;
- the neutral land mask must be versioned and provenance-tracked;
- API/render metadata must state when `land_clip` was applied;
- clipping does not improve or reinterpret inland historical boundaries;
- clipping must never be described as a more historically accurate source polygon;
- a better specialist historical coastline/geometry may later supersede the display treatment.

Purpose: prevent coarse historical source polygons from visually filling modern ocean while preserving the original historical reconstruction intact.

## Canonical cartographic land fabric

The atlas uses one physical land geometry for both the neutral basemap and the coastline constraint applied to historical polygon fills.

Current master fabric:

- Natural Earth `ne_10m_land`
- Natural Earth release: 5.1.1
- pinned upstream repository commit: `ca96624a56bd078437bca8184e78163e5039ad19`
- pinned GeoJSON blob: `2d76878175b8054acd9c5a52917ee9ea59a36fc5`
- immutable source URL: `https://raw.githubusercontent.com/nvkelso/natural-earth-vector/ca96624a56bd078437bca8184e78163e5039ad19/geojson/ne_10m_land.geojson`

The active fabric is registered in `cartography.land_fabric` with source identifiers and content checksums.

Rules:

- the browser basemap reads the active fabric URL returned by the release API;
- `publish.map_geometry` intersects historical polygon fills with the active fabric;
- therefore basemap coastlines and historical overlay coastlines derive from the same geometry source;
- no second hand-maintained or independently simplified land outline should be used for normal rendering;
- source historical geometry remains untouched in `atlas.geometry` and `publish.geometry`;
- the cartographic fabric constrains physical land/water edges only; it does not replace or modernize inland historical boundaries;
- higher-quality specialist historical geometry can supersede a Cliopatria polygon without changing this physical-land rule;
- a future fabric version must be registered as a new version with source and checksum provenance rather than silently replacing the current one.

Natural Earth 1:10m is used because this atlas supports country/region zoom levels. The old 1:110m land outline is retained only as a legacy migration fallback until an active canonical fabric has been loaded; it is not the normal web basemap.

