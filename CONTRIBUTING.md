# Contributing / development rules

1. Read `docs/00_START_HERE.md` and the required governance files before schema or data changes.
2. Do not edit an SQL migration once it has been applied in a shared/reviewed database. Add the next numbered migration.
3. Do not overwrite canonical historical release files under `data/releases/`.
4. Preserve source-native values and IDs; normalization creates additional structures rather than replacing the only raw copy.
5. Run `scripts/verify-dev.ps1` (Windows) or `scripts/verify-dev.sh` before merging changes.
6. Methodology, ontology or schema decisions must be recorded in `docs/08_DECISIONS_LOG.md` before they become canonical.
