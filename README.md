# Historical Slavery Atlas — development environment

This private repository is the reproducible engineering foundation for the Historical Slavery Atlas. It is **not yet the canonical data store**. The canonical data release remains the external, immutable v0.6.1 workbook identified by the release manifest in `data/releases/v0.6.1/` until database migration, semantic normalization, QC and release gates pass.

## Repository boundary

Git stores code, SQL migrations, tests, governance documentation, release manifests and checksums. Canonical research binaries are treated as immutable release artifacts and are **not stored as ordinary Git blobs**. This keeps the code repository clean, avoids rewriting large historical binaries, and gives us a path to a proper release/object-storage layer later.

The exact canonical v0.6.1 artifact is:

`Historical_Slavery_Atlas_v0.6.1_Controlled_Atlantic_Ingestion.xlsx`

SHA-256:

`0a38e4eb6f63c3bb4ce9543be379605d24dd9ff1c1cea1e0a49c0c3db7ba17d4`

## What is included

- PostgreSQL 17 + PostGIS 3.5 development database in Docker;
- Dockerized Python 3.12 tooling;
- checksum-enforced SQL migration ledger;
- v0.6.1 importer and reconciliation tests for artifact-gated release validation;
- non-Atlantic rollback-only acceptance fixtures;
- release manifests/checksums under `data/releases/`;
- local backup/restore scripts;
- GitHub Actions clean-room foundation CI;
- optional VS Code Dev Container configuration;
- governance/methodology documentation under `docs/`.

## Repository layout

```text
.
├── data/releases/       # immutable release metadata/checksums; binaries external
├── db/migrations/       # append-only PostgreSQL/PostGIS migrations
├── db/tests/            # schema, reconciliation and acceptance SQL tests
├── db/migration/        # release-to-database mapping specifications
├── tools/               # migration/import utilities
├── tests/               # Python unit tests
├── scripts/             # Windows + Bash developer operations
├── docker/              # tooling container definitions
├── docs/                # methodology, ontology, architecture and governance
├── validation/          # checked-in validation reports, never runtime state
├── deploy/              # future staging/production boundary
├── backups/             # local-only database backups
└── build/               # generated local output
```

The root is intentionally small. Do not create framework-specific web/API directories until those implementation choices are justified.

## Development workflow

`main` is the integration branch. Substantive changes use short-lived branches and pull requests after CI passes. Applied SQL migrations are append-only.

### Core bootstrap

With Docker Desktop running:

```powershell
.\scripts\bootstrap-dev.ps1
```

This always validates the database foundation. If the exact v0.6.1 workbook is present at the path configured in `.env`, bootstrap additionally performs checksum verification, dry-run import, transactional import and v0.6.1 reconciliation. If the release artifact is absent, those release-specific gates are skipped explicitly rather than replaced by fake data.

## Important status

Foundation CI validates the executable database/schema/tooling layer without pretending it has access to the canonical binary. The canonical switch remains blocked until the external v0.6.1 artifact has passed the release-validation path and the four global evidence sheets have been semantically migrated.
