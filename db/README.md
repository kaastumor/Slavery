# Historical Slavery Atlas — database foundation v0.4

This directory contains the executable migration and acceptance-test layer. The database remains a migration candidate; canonical data is still v0.6.1.

## Migration discipline

Run migrations through `tools/migrate.py` (normally `scripts/db-migrate.ps1` / `.sh`). The runner stores filename + SHA-256 in `atlas_meta.schema_migration`.

Rules:

- migrations are applied in filename order;
- an already-applied migration is skipped only when its checksum is unchanged;
- a checksum mismatch is a hard failure;
- never edit an applied migration in a shared/reviewed database; add the next numbered migration instead.

Current schema migrations: `0001` through `0011`.

## Acceptance order

1. migration ledger/status
2. `tests/001_schema_smoke.sql`
3. canonical workbook dry-run
4. transactional v0.6.1 import
5. `tests/002_v061_reconciliation.sql`
6. `tests/003_non_atlantic_acceptance.sql`

The non-Atlantic fixtures roll back and do not become atlas data.
