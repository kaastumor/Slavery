# Engineering changelog

This changelog tracks repository and development-environment changes. Historical data releases retain their own immutable release metadata and QC/versioning records.

## v0.4 — 2026-09-19

- Established the private GitHub repository as the persistent engineering home.
- Added Dockerized PostgreSQL/PostGIS and Python tooling.
- Added checksum-enforced SQL migration tracking through migration `0011`.
- Added the v0.6.1 importer, reconciliation tests and non-Atlantic rollback fixtures.
- GitHub Actions successfully executed migrations `0001`–`0011` and the schema smoke test against live PostGIS.
- Separated canonical release binaries from ordinary Git history: Git stores immutable filename/version/checksum manifests; exact release artifacts are supplied to the release-validation path.
- Added CI, backup/restore, Windows/Bash bootstrap, Dev Container support, review templates and CODEOWNERS.
- Canonical database cut-over remains blocked by exact-artifact reconciliation and semantic migration of the four global evidence sheets.
