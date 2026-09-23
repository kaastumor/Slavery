# Historical Slavery Atlas

Public development repository for the Historical Slavery Atlas: a global, time-aware evidence corpus and comparison method for slavery and related coerced-labour/dependency systems, with a thin atlas/query surface where that adds demonstrated value.

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

- canonical historical data release: `v0.6.1` (external immutable workbook);
- public non-canonical preview: `mvp-preview-ancient-v2` (frozen legacy demonstration);
- working normalized research store: PostgreSQL/PostGIS;
- M1 and M2 implementation/adversarial gates: completed;
- HC-003 wide-angle review: **CONTINUE + SIMPLIFY**;
- working identity: **auditable evidence corpus + comparison method + thin atlas/query surface**;
- execution state: **IDLE** — no new horizon is authorized;
- M2 production migration, broad evidence expansion and richer application/platform work remain parked pending a future value-discrimination decision.

See `docs/34_WIDE_ANGLE_PROJECT_REVIEW.md` and D-062.

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
