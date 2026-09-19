# Historical Slavery Atlas — development environment

This repository is the reproducible development/database foundation for the Historical Slavery Atlas. It is **not yet the canonical data store**. The canonical data release remains `data/releases/v0.6.1/Historical_Slavery_Atlas_v0.6.1_Controlled_Atlantic_Ingestion.xlsx` until all migration, semantic-normalization, QC and release gates pass.

## What is included

- PostgreSQL 17 + PostGIS 3.5 development database in Docker;
- Dockerized Python 3.12 tooling, so local Python is not required;
- checksum-enforced SQL migration ledger;
- v0.6.1 importer and reconciliation tests;
- non-Atlantic rollback-only acceptance fixtures;
- immutable canonical workbook input under `data/releases/v0.6.1/`;
- local backup/restore scripts;
- GitHub Actions CI workflow;
- optional VS Code Dev Container configuration;
- governance/methodology documentation under `docs/`.


## Repository layout

```text
.
├── data/releases/       # immutable canonical/historical input releases
├── db/migrations/       # append-only PostgreSQL/PostGIS schema migrations
├── db/tests/            # schema, reconciliation and acceptance SQL tests
├── db/migration/        # explicit release-to-database mapping specifications
├── tools/               # migration/import utilities
├── tests/               # Python unit tests
├── scripts/             # Windows + Bash developer operations
├── docker/              # tooling container definitions
├── docs/                # methodology, ontology, architecture and project governance
├── validation/          # checked-in validation reports, never runtime state
├── deploy/              # deployment boundary; provider-specific IaC comes later
├── backups/             # local-only database backups (ignored except .gitkeep)
└── build/               # local generated output (ignored except .gitkeep)
```

The root is intentionally kept small. New code should go into an existing domain folder unless a genuinely new subsystem is introduced. Do not create framework-specific web/API directories until those implementation choices are actually made.

## Repository workflow

`main` is the integration branch. Substantive changes should be made on a short-lived branch and merged by pull request after CI passes. Database migrations are append-only once shared: never rewrite an already-applied migration. Canonical release files under `data/releases/` are immutable.

## Windows first run

Prerequisite: Docker Desktop running. Git is recommended once this is placed in a repository.

```powershell
.\scripts\bootstrap-dev.ps1
```

The bootstrap creates a local `.env` with a random development password, builds the tooling image, starts PostGIS, applies migrations, runs tests, imports v0.6.1 into the **local development database**, performs reconciliation/non-Atlantic acceptance tests and creates a local backup.

Re-run verification later with:

```powershell
.\scripts\verify-dev.ps1
```

## Important status

Passing local/CI tests does not make PostgreSQL canonical. The four global evidence sheets are raw-preserved but still require reviewed semantic migration. A blocking QC issue intentionally remains until that work is complete.

## Environment model

```text
GitHub repository
   |-- code / SQL migrations / tests / governance docs
   |-- immutable canonical input release(s)
   |-- GitHub Actions clean-room CI
   |
   +--> local development: Docker Compose (disposable)
   |
   +--> future staging: managed Postgres/PostGIS + private app services
   |
   +--> future production: reviewed release/publish layer only
```

The local Docker database is intentionally replaceable. It is a development target, not a historical release artifact or production database.
