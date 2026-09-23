# M2 complete Cliopatria raw/staging ingestion

**Gate:** #116  
**Task:** #119  
**Status:** implementation candidate; disposable PostGIS integration only  
**Canonical release:** v0.6.1 unchanged  
**Public preview:** unchanged

## Question

Can the complete pinned Cliopatria corpus be ingested reproducibly into relational raw/staging PostGIS without turning source rows into approved atlas geography?

## Boundary

This task implements the source-infrastructure layer required by D-059. It does **not**:

- create or resolve `atlas.spatial_entity` identities;
- turn `POLITY` rows into reviewed atlas polity records;
- coerce `RELATION` rows into polities;
- flatten `MemberOf` / `Components`;
- normalize source-native BCE/CE integers into atlas years during ingestion;
- interpolate gaps;
- create publish views;
- promote geometry.

The prototype DDL therefore lives under `experiments/m2/`, not `db/migrations/`. Production receives no schema or data change from #119.

## Exact source

The ingestion reuses the existing M1/D-059 pin:

- repository: `Seshat-Global-History-Databank/cliopatria`
- release: `v0.2.0-duplicate`
- commit: `ad28a691b7c07c1fca89d0e0636d324667d2a258`
- asset: `cliopatria.geojson.zip`
- Git blob SHA-1: `cefab0f4b622e2e7fb3daf68d4f461f83991204c`
- SHA-256: `d01ae3a20d358cc5d54f69d9d725d390767d9c8759ac89ad6f90c58d106f3370`
- source CRS: EPSG:4326
- upstream license: CC BY 4.0

The importer hard-fails before database writes if asset size, Git blob identity, SHA-256, or the previously accepted deterministic full-corpus profile differs.

## Relational shape

The existing atlas provenance model remains authoritative:

`SOURCE -> SOURCE_VERSION -> SOURCE_ASSET -> INGEST_RUN -> RAW_RECORD`

Each source feature is preserved in `raw.raw_record.raw_payload` with a canonical per-feature checksum.

A thin `staging.cliopatria_feature` projection exposes only fields needed for subsequent resolver work:

- exact row ordinal within the pinned immutable asset;
- optional upstream feature id where supplied;
- raw `Name`, `Type`, `FromYear`, `ToYear`, `MemberOf`, `Components`, `SeshatID`, `Wikidata`, `Wikipedia`;
- a PostGIS EPSG:4326 geometry;
- a generated **source-native** integer range for indexing.

The row ordinal is explicitly an atlas import locator within one exact asset, **not** a claim that Cliopatria defines that ordinal as a durable semantic identifier. Any upstream feature `id` remains separate and may be NULL.

There is deliberately no `spatial_entity_id`, `polity_id`, or `geometry_id` on the staging row.

## Idempotency

The exact pinned dataset receives a stable `dataset_key` tied to its commit/checksum. The initial load is one database transaction. A failed load rolls back; an exact completed retry verifies metadata and both raw/staging row counts and becomes a no-op. A conflicting existing dataset state fails closed.

## Reconciliation contract

`experiments/m2/cliopatria_reconciliation.sql` checks the database against the already accepted whole-corpus observations, including:

- 13,765 raw rows and 13,765 staging rows;
- 1,633 distinct names;
- 13,380 POLITY / 385 RELATION rows;
- 6,531 Polygon / 7,234 MultiPolygon geometries;
- source-native year extent -3400..2024;
- 1,106 rows with a negative source year;
- 39 rows crossing numeric zero;
- six rows with a zero endpoint;
- 2,656 rows with MemberOf;
- 1,722 rows with Components;
- 80 nested-composite rows;
- 86 rows with multiple MemberOf memberships;
- zero raw/staging mismatches for the projected source fields;
- no atlas identity columns;
- no publish-view exposure.

## Reproduction

With the ordinary disposable PostGIS stack already running and repository migrations applied:

```bash
./scripts/db-test-cliopatria-ingest.sh
```

The script downloads/caches only the exact pinned asset, runs the full ingestion and reconciliation, then repeats the exact input and requires the second run to report `noop`.

## Gate meaning

Passing #119 proves that the entire source corpus can live in the project as reproducible **raw geography infrastructure**. It does not prove that any individual source polygon is historically correct for an atlas case, that source hierarchy has been resolved correctly for a selected year, or that the source should be published. Those remain #121 / D-055 / cartographic review concerns.
