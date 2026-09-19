# Engineering changelog

This changelog tracks repository and development-environment changes. Historical **data releases** keep their own release notes under `data/releases/<version>/` and remain governed by the atlas QC/versioning policy.

## v0.4 — 2026-09-19

- Established the private GitHub repository as the persistent engineering home.
- Added Dockerized PostgreSQL/PostGIS and Python tooling.
- Added checksum-enforced SQL migration tracking through migration `0011`.
- Added the v0.6.1 importer, reconciliation tests, non-Atlantic rollback fixtures, and exact canonical-workbook checksum enforcement.
- Added CI, local backup/restore, Windows/bash bootstrap and verification scripts, and optional Dev Container support.
- Added pull-request and issue templates plus CODEOWNERS review boundaries.
- Preserved all 18 v0.6.1 workbook tabs / 288 non-empty rows in the migration path; global evidence sheets remain semantically unresolved and blocking for canonical database cut-over.
