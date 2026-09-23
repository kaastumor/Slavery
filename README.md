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

- canonical historical data release: `v0.6.1` (external immutable workbook);
- public non-canonical preview: `mvp-preview-ancient-v2` (frozen legacy demonstration);
- M1 and M2 methodology/integration gates: completed;
- HC-003: **CONTINUE + SIMPLIFY**;
- H2 / #146 value-discrimination pilot: completed;
- HC-004 / D-063: **STOP ACTIVE ATLAS EXPANSION; PRESERVE METHOD/CORPUS/AUDIT ARTIFACTS**;
- COV-001 / #148 coverage-value experiment: **completed — NARROW SURVIVE**;
- COV-002 / #151 scale/reuse experiment: **completed — STOP FURTHER AUTOMATIC SCALING**;
- execution state: **IDLE / PRESERVATION**; active Atlas expansion remains stopped;
- compact coverage-register pattern is preserved for concrete task-driven use; systematic scale economics did not pass;
- no H3/H4 bulk research, production-migration, frontend/platform or infrastructure horizon is authorized.

The H2 pilot found a material corpus-method advantage in one of three cases, below the pre-registered two-case threshold; the repaired thin visual/query arm did not materially beat the corpus/method in any case.

See `experiments/h2-value-discrimination/09_FINAL_RESULT.md` / D-063 for the Atlas stop decision, `experiments/coverage-value/11_FINAL_RESULT.md` / D-065 for the narrow corpus-value result, and `experiments/coverage-scale/13_FINAL_RESULT.md` / D-067 for the scale stop decision.

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
