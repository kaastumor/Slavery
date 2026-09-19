# Development Environment

**Status:** reproducible development environment prepared; live PostgreSQL/PostGIS execution still required.

## Purpose

The local environment is a disposable, reproducible development and validation environment. It is not the production atlas and it is not itself a canonical data release.

The environment contains:

- PostgreSQL 17 + PostGIS 3.5 in Docker;
- Python 3.12 migration/import tooling in Docker;
- the immutable v0.6.1 canonical workbook under `data/releases/v0.6.1/`;
- checksum-enforced SQL migration tracking;
- schema, importer, reconciliation and non-Atlantic tests;
- local backup/restore scripts;
- GitHub Actions CI;
- optional VS Code Dev Container support.

## Environment boundaries

### Local development

Purpose: schema work, importer development, tests, local map/API prototyping.

Data may be reset at any time. A successful local import does not make the database canonical.

### CI

Purpose: reproduce migrations/import/tests from a clean database on every proposed code/schema change.

CI is a validation gate, not durable storage.

### Staging

Future purpose: integration testing of API/map publication, release candidates and deployment migrations against production-like infrastructure.

Staging should use its own database, credentials and release artifacts. It must not share the local Docker volume or production credentials.

### Production

Future purpose: serve reviewed/published atlas data.

Production requires managed/operational PostgreSQL + PostGIS, private networking/TLS, backup/recovery, separate write/read roles, deployment secrets, release artifact storage and public services restricted to `publish` data. Provider-specific infrastructure remains intentionally undecided.

## Migration ledger

`tools/migrate.py` creates `atlas_meta.schema_migration` and records:

- migration filename;
- SHA-256 checksum;
- applied timestamp.

The runner:

- applies pending migrations in filename order;
- skips an already-applied migration only when its checksum is unchanged;
- fails if an applied migration file has changed;
- treats an applied migration missing from the repository as an error state.

The `atlas_meta` schema contains deployment/schema-history metadata, not historical research data.

## One-command Windows setup

With Docker Desktop running:

```powershell
.\scripts\bootstrap-dev.ps1
```

This creates `.env` with a random local password, builds the tooling container, starts PostGIS, applies migrations, runs all current tests, imports v0.6.1 into the local development DB, runs reconciliation/non-Atlantic tests and creates a backup.

Re-run validation with:

```powershell
.\scripts\verify-dev.ps1
```

## Git / GitHub

The private repository `kaastumor/Slavery` is the persistent engineering home. `main` is the integration branch; substantive changes should use short-lived branches and pull requests with CI before merge.

The included GitHub Actions workflow runs the full foundation validation from a clean database. Repository-local generated output, `.env`, database dumps and local backups remain ignored. Canonical input releases under `data/releases/` are committed intentionally and checksum-locked.

GitHub integration is available to ChatGPT for repository-aware maintenance, issue/PR work and CI inspection.
