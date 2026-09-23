# Historical Slavery Atlas

Public repository preserving the Historical Slavery Atlas's global, time-aware historical-evidence methodology, research/release artifacts, adversarial fixtures and experimental atlas/query work for slavery and related coerced-labour/dependency systems.

The repository is the canonical source of truth for project implementation, methodology and operating state. The immutable historical data baseline remains the external v0.6.1 workbook until a deliberately validated successor release is created.

## Start here

Read in this order:

1. `docs/23_PROJECT_CHARTER.md` — purpose, contribution, baseline, success/failure and horizons
2. `BACKLOG.md` — canonical execution queue and current stopping point
3. `docs/24_WAY_OF_WORKING.md` — evidence/adversarial/discovery method
4. `docs/25_PROJECT_HEALTH.md` — assumptions, risks, value evidence and health decisions
5. `docs/00_START_HERE.md` — historical methodology entry point
6. `docs/08_DECISIONS_LOG.md` — durable methodology/architecture decisions

For scheduled autonomous work, `docs/automation/hourly-worker.md` is the canonical runbook.

## Current state

- canonical historical data release: `v0.6.1` (external immutable workbook; unchanged);
- frozen legacy public preview: `mvp-preview-ancient-v2` (non-canonical demonstration);
- architecture experiments COV-001→004: completed;
- R1 historical subject research: **complete and frozen at 19 reviewed C1 rows**;
- R1.6 release QC: **PASS WITH EXPLICIT LIMITATIONS**;
- R1 candidate registry: 77 frozen targets = 19 reviewed C1 + 15 planned/unresearched C1 + 2 held + 41 C0-only;
- source dependency layer: 45 source relations / 37 independence groups;
- D-080: the project has crystallized to an **MVP v0.1** rather than returning to broad platform work;
- active MVP parent: **#174**;
- MVP definition: **immutable R1 candidate package + neutral world map + explicit geometry/research states + compact evidence register**;
- delivery queue: #175→#182, WIP=1, short-lived PRs, green CI;
- post-MVP discovery: #184→#187 only after #182 records `TECHNICAL_MVP_CANDIDATE`;
- no new subject-research tranche, production migration, backend/service expansion, or new universal P0–P4 scale is authorized.

See `programmes/r1/20_RELEASE_QC.md`, `docs/mvp/v0.1-plan.md`, and `docs/mvp/delivery-discovery-cadence.md`.

## Repository boundary

This repository is **public**. It stores code, migrations, tests, public-safe research fixtures, governance/methodology, release manifests/checksums and web code.

Do not commit secrets, the canonical workbook binary, restricted/copyrighted source assets, private source material or sensitive living-person material/derivatives. See `SECURITY.md`.

The exact canonical v0.6.1 workbook is identified by:

`Historical_Slavery_Atlas_v0.6.1_Controlled_Atlantic_Ingestion.xlsx`

SHA-256:

`0a38e4eb6f63c3bb4ce9543be379605d24dd9ff1c1cea1e0a49c0c3db7ba17d4`

## Development

`main` is the integration branch. Substantive work uses short-lived branches and pull requests. Applied SQL migrations are append-only.

Local verification:

```bash
./scripts/verify-dev.sh
python tools/sanitize_repo.py
```

Windows equivalents are available under `scripts/`.

The project deliberately prefers existing/simple capabilities over new infrastructure. A new dependency or service must solve a demonstrated problem that the current baseline cannot.
