# Contributing / development rules

1. Read `docs/23_PROJECT_CHARTER.md`, repository-root `BACKLOG.md`, `docs/24_WAY_OF_WORKING.md`, and the relevant methodology files before substantive work.
2. Use the evidence loop: question → smallest proposal → adversary → experiment/implementation → evidence → decision → sanitation → reconciliation.
3. Do not edit an SQL migration once it has been applied in a shared/reviewed database. Add the next numbered migration.
4. Do not overwrite canonical historical release files under `data/releases/`.
5. Preserve source-native values and IDs; normalization creates additional structures rather than replacing the only raw copy.
6. Run `scripts/verify-dev.ps1` (Windows) or `scripts/verify-dev.sh`, plus `python tools/sanitize_repo.py`, before merging changes.
7. Methodology, ontology or schema decisions must be recorded in `docs/08_DECISIONS_LOG.md` before they become canonical.
8. Use GitHub issues for work needing durable acceptance/evidence. Do not create a second backlog or roadmap beside repository-root `BACKLOG.md`.
9. Treat this repository as public; follow `SECURITY.md` for source, derived-data and secret boundaries.
