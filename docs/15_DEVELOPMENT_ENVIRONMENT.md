# Development Environment

**Status:** reproducible development environment prepared; core PostgreSQL/PostGIS CI has executed successfully. Exact canonical-release import/reconciliation remains artifact-gated.

## Purpose

The local environment is a disposable, reproducible development and validation environment. It is not the production atlas and it is not itself a canonical data release.

The environment contains:

- PostgreSQL 17 + PostGIS 3.5 in Docker;
- Python 3.12 migration/import tooling in Docker;
- release metadata/checksums under `data/releases/`;
- checksum-enforced SQL migration tracking;
- schema, importer, reconciliation and non-Atlantic tests;
- local backup/restore scripts;
- GitHub Actions CI;
- optional VS Code Dev Container support.

The canonical v0.6.1 workbook binary is an external immutable release artifact. It is not stored as an ordinary Git blob. When supplied locally for release validation, its exact SHA-256 must match the committed release metadata.

## Environment boundaries

### Local development

Purpose: schema work, importer development, tests, local map/API prototyping.

Data may be reset at any time. A successful local import does not make the database canonical.

### CI

Purpose: reproduce migrations and foundation tests from a clean database on every proposed code/schema change.

Foundation CI does not substitute synthetic data for the canonical workbook. Exact v0.6.1 import/reconciliation runs only when the checksum-matching artifact is explicitly supplied.

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

## Windows bootstrap

With Docker Desktop running:

```powershell
.\scripts\bootstrap-dev.ps1
```

The bootstrap always validates the database foundation. If the exact canonical v0.6.1 workbook is present at the expected local release path, it additionally verifies the checksum and runs the release-specific dry-run/import/reconciliation path.

Re-run all currently available checks with:

```powershell
.\scripts\verify-dev.ps1
```

## Git / GitHub

The private repository `kaastumor/Slavery` is the persistent engineering home. `main` is the integration branch; substantive changes use short-lived branches and pull requests with CI before merge.

Repository-local generated output, `.env`, database dumps and local backups remain ignored. Git stores release manifests/checksums, not ordinary copies of canonical research binaries.

GitHub integration is available to ChatGPT for repository-aware maintenance, issue/PR work and CI inspection.
