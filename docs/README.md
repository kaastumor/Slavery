# Historical Slavery Atlas — Project Setup Pack

This folder is the governance, methodology and architecture layer for the Historical Slavery Atlas.

## Canonical data baseline

As of 2026-09-19, the latest canonical data workbook is:

- `Historical_Slavery_Atlas_v0.6.1_Controlled_Atlantic_Ingestion.xlsx`

Its global baseline is:

- `Historical_Slavery_Atlas_Global_Coverage_Audit_v0.5.0.xlsx`

Earlier v0.4.x and v0.5.1 files are historical intermediates, not the current source of truth unless a later file explicitly references them.

## Architecture state

The project is now preparing a migration from workbook-led storage to a PostgreSQL/PostGIS research database suitable for a fully interactive web map.

- `11_SYSTEM_ARCHITECTURE.md` defines the approved migration target.
- `schema_draft.yaml` draft-0.10 expresses the current structural model.
- These files do not replace or rewrite v0.6.1 until migration, reconciliation and QC succeed.

## How to use this pack

Start with `00_START_HERE.md`. Before data/schema work, read the methodology, source policy, data model, geography rules, decisions log and system architecture referenced there.

The canonical dataset must never be treated as self-explanatory. These files control how records may be interpreted, normalized, linked, published and visualized.

## Current execution plan

`12_DATABASE_FOUNDATION_PLAN.md` defines the acceptance tests and migration sequence that must pass before the database can replace the v0.6.1 workbook as canonical.

## Database implementation package

The repository database foundation now has migrations `0001`–`0012`, schema/non-Atlantic/release-reconstruction acceptance tests, and the automated v0.6.1 importer. Core migrations and acceptance tests execute successfully against live PostgreSQL/PostGIS in GitHub Actions. The workbook remains canonical because exact-artifact import/reconciliation and semantic migration of the global evidence sheets are still pending.


The v0.3 importer validates and raw-preserves all 18 workbook tabs / 288 non-empty rows. The global evidence sheets still require reviewed semantic migration, which remains a blocking condition before the database can replace v0.6.1 as canonical.

## Development environment v0.4

A repository-shaped Docker development environment wraps the database foundation. It includes containerized Python tooling, checksum-tracked migrations, v0.6.1 release metadata/checksum, one-command Windows bootstrap, backup/restore, GitHub Actions CI and staging/production boundary documentation. The canonical workbook binary remains external and artifact-gated.
