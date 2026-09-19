# Local Database Development

**Purpose:** provide a reproducible local environment for database/schema/import work before any canonical switch.

## What local means

This database is disposable development infrastructure. It is not the production atlas and is never canonical merely because tests pass.

## Prerequisite on Windows

Docker Desktop, running with Docker Compose support. Local Python/PostgreSQL installations are not required because migration/import tooling runs in Docker.

Git is recommended for repository use but is not required to execute the environment.

## First run

From the repository root:

```powershell
.\scripts\bootstrap-dev.ps1
```

The script:

1. verifies Docker;
2. creates `.env` with a random local-only password if needed;
3. pulls PostgreSQL/PostGIS and builds the Python tooling image;
4. starts the database and waits for health;
5. applies pending checksum-tracked migrations;
6. runs schema and Python tests;
7. dry-runs and applies the canonical v0.6.1 workbook;
8. runs non-Atlantic and release-reconstruction rollback fixtures;
9. when the exact v0.6.1 artifact is present, runs v0.6.1 checksum/import/reconciliation checks;
9. creates a local database backup.

## Repeat validation

```powershell
.\scripts\verify-dev.ps1
```

## Migration status

```powershell
.\scripts\db-status.ps1
```

Applied migration filename/checksum state is recorded in `atlas_meta.schema_migration`. Do not edit an applied migration. Add the next numbered migration.

## Backup / restore

```powershell
.\scripts\backup-db.ps1
.\scripts\restore-db.ps1 backups\slavery_atlas_YYYYMMDD_HHMMSS.dump
```

Backups are local development artifacts and are git-ignored by default.

## Reset local database

```powershell
.\scripts\db-reset.ps1
```

This removes only the Docker development volume. It does not alter files under `data/releases/` or Project governance files.

## Canonical-switch warning

The importer intentionally leaves a blocking QC issue while the four global evidence sheets remain raw-preserved but not fully semantically normalized. Passing local/CI execution is therefore necessary but not sufficient for replacing v0.6.1 as canonical.
