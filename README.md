# Historical Slavery Atlas

Public development repository for the Historical Slavery Atlas: a global, time-aware evidence-synthesis system for slavery and related coerced-labour/dependency systems.

The repository is the canonical source of truth for project implementation, methodology and operating state. The immutable historical data baseline remains the external v0.6.1 workbook until a deliberately validated successor release is created.

## Start here

Read in this order:

1. `docs/23_PROJECT_CHARTER.md` — purpose, north star, success/failure and horizons
2. `BACKLOG.md` — current execution order
3. `docs/24_WAY_OF_WORKING.md` — evidence/adversarial loop
4. `docs/25_PROJECT_HEALTH.md` — assumptions, risks, value evidence and health decisions
5. `docs/00_START_HERE.md` — historical methodology entry point
6. `docs/08_DECISIONS_LOG.md` — durable decisions

For scheduled autonomous work, `docs/automation/hourly-worker.md` is the canonical runbook.

## Current state

- canonical historical data release: `v0.6.1` (external immutable workbook);
- public non-canonical preview: `mvp-preview-ancient-v2`;
- working normalized store: PostgreSQL/PostGIS;
- public client: MapLibre web application backed by the release-gated `atlas-data` API and deployment-bound static fallback;
- current substantive gate: M1 methodology hardening, issue #100.

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
