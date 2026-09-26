# Historical Slavery Atlas

Public repository preserving the Historical Slavery Atlas's global, time-aware historical-evidence methodology, research/release artifacts, adversarial fixtures and experimental atlas/query work for slavery and related coerced-labour/dependency systems.

The repository is the canonical source of truth for project implementation, methodology and operating state. PostgreSQL/PostGIS is the governed current research authority under D-109, while immutable release packages own citable historical release identity. The current canonical historical release is v0.7.0; v0.6.1 remains its immutable predecessor.

## Start here

Read in this order:

1. `docs/23_PROJECT_CHARTER.md` — purpose, contribution, baseline, success/failure and horizons
2. `BACKLOG.md` — canonical execution queue and current stopping point
3. `docs/24_WAY_OF_WORKING.md` — evidence/adversarial/discovery method
4. `docs/25_PROJECT_HEALTH.md` — assumptions, risks, value evidence and health decisions
5. `docs/00_START_HERE.md` — historical methodology entry point
6. `docs/08_DECISIONS_LOG.md` — durable methodology/architecture decisions

For discovery execution use `docs/discovery/DISCOVERY_EXECUTION.md`; the reusable
5.6-compatible continuation prompt is `docs/discovery/RUN_PROMPT.md`.
For scheduled autonomous work, `docs/automation/hourly-worker.md` is the canonical runbook.

## Current state

For the **current priority and mode**, read repository-root `BACKLOG.md`; this README
does not own the next action.

Durable state:
- canonical current research authority: explicit D-109 PostgreSQL/PostGIS membership
  closure;
- canonical historical data release: **`v0.7.0`** under D-110;
- immutable canonical predecessor: `v0.6.1` workbook and exact checksum lineage;
- v0.7.0 preserves 40 claims / 11 actors / 18 spatial entities / 0 reviewed historical
  evidence geometries / 8 voyages / 99 coverage assessments / 211 exact source
  versions / 26 research-target results;
- independent historical review remains **0**;
- the public UI/API has **not** moved with the release: `public_mvp_preview` still
  points to `mvp-preview-ancient-v2`;
- Gate 5 / #323 is the active priority: stage and verify an exact v0.7.0-derived serving
  materialization, prove rollback, and only then decide whether to move the public
  release channel;
- best-supported project form remains **portable reviewed evidence core + governed
  database research authority + immutable release packages + replaceable
  Atlas/map/table/API views**;
- D-096 continues to govern mode-level continuation and WIP=1.

## Repository boundary

This repository is **public**. It stores code, migrations, tests, public-safe research fixtures, governance/methodology, release manifests/checksums and web code.

Do not commit secrets, the canonical workbook binary, restricted/copyrighted source assets, private source material or sensitive living-person material/derivatives. See `SECURITY.md`.

The exact immutable v0.6.1 predecessor workbook is identified by:

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
