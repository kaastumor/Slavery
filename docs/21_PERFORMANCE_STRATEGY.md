# Published Atlas Performance Strategy

**Status:** implementation policy for the current thin MapLibre client  
**Scope:** published/read-only atlas delivery; not research ingestion or canonical evidence storage  
**Historical release:** unchanged (`v0.6.1`)

## Goal

Keep interaction responsive as published releases grow without prematurely replacing the current API-first GeoJSON architecture. Performance work must preserve release identity, provenance, geometry accuracy metadata, static outage fallback, and the rule that the browser consumes reviewed/published materializations only.

## Principles

1. **Measure before changing transport.** Record payload bytes, feature counts, geometry coordinate/vertex counts, request latency, parse/render time, and representative browser interaction performance per published release.
2. **Scale stable map layers independently from evidence detail.** Large immutable geometry layers are candidates for tiled delivery; claim/evidence detail remains keyed, inspectable data rather than being duplicated into every tile.
3. **Release-bound artifacts only.** Any PMTiles/vector-tile artifact must be generated from an exact reviewed release/materialization, carry a digest plus release/provenance metadata, and be immutable once published. Switching transport must not change historical semantics.
4. **No silent simplification.** Generalized/tiled geometry is a render derivative. Source historical geometry remains immutable, accuracy/proxy status remains available, and simplification must be reproducible and QC'd at representative zooms.
5. **Fallback remains viable.** A transport optimization must not make an already-published atlas disappear during a transient database/API outage. Static release snapshots remain a supported recovery path.
6. **Partition by need, not fashion.** PMTiles/vector tiles are justified when measured payload/render cost warrants them; small layers stay simple.

## Baseline instrumentation

For each public-preview/canonical publication candidate, capture at least:

- compressed and uncompressed response/snapshot size;
- counts of places, claims, evidence links, drawable geometry records and features;
- total and high-percentile geometry coordinate/vertex counts;
- cold and warm API response latency where safely observable;
- browser load-to-map-ready time on desktop and a mobile viewport;
- year-change interaction time and map frame responsiveness on representative dense years.

Measurements should run against immutable fixtures, release snapshots, CI artifacts, or a disposable environment. Do not load-test live Supabase.

## Escalation ladder

### Stage A — current architecture

Keep API-first published GeoJSON plus deployment-bound static fallback while measured costs are comfortably small. Reduce avoidable client recomputation and cache immutable release data by release/channel identity.

### Stage B — split payloads

If evidence/detail growth dominates transfer, separate lightweight map/index payloads from on-demand claim/source detail while retaining stable IDs and exact release membership. Do not make map visibility depend on downloading all evidence prose.

### Stage C — immutable vector tiles / PMTiles

Move a large, stable geometry layer to release-bound vector tiles or PMTiles when at least one of these is repeatedly observed in representative CI/browser measurements:

- a single map geometry payload exceeds roughly 5 MiB compressed;
- map geometry exceeds roughly 50,000 rendered features or 500,000 vertices/coordinates for a representative view/release;
- map-ready or year-change interaction exceeds 2 seconds on the project's mobile browser profile primarily because of geometry transfer/parse/render work.

These are investigation triggers, not historical-QC waivers. A bounded benchmark must show that tiling materially improves the failing metric before adoption.

## Tile contract

A tiled publication artifact must include:

- release identifier and source Git commit;
- exact upstream published-materialization/bundle digest;
- tile artifact SHA-256;
- generator/tool version and deterministic command/config;
- layer schema and stable feature IDs linking back to published place/geometry records;
- zoom-dependent simplification/generalization policy;
- land-fabric/render-transform identity where relevant;
- automated geometry validity/coverage checks plus representative visual review.

Tiles are derived publication artifacts, never canonical research geometry. Claim/source text and interpretive P-level remain governed by the canonical database/release bundle.

## Performance acceptance

Optimization is accepted only when it improves a measured bottleneck without changing release membership, claim semantics, geometry provenance/accuracy disclosure, or outage recoverability. Compare old/new paths using the same immutable release fixture and retain the benchmark result with the change.

## Explicit non-goals

- no live-production stress testing;
- no second canonical datastore;
- no automatic geometry simplification merely because a feature is old or approximate;
- no vector-tile rewrite while current measured scale does not justify it;
- no coupling of evidence confidence/P-level to rendering or performance decisions.
