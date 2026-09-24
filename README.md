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

For discovery execution use `docs/discovery/DISCOVERY_EXECUTION.md`; the reusable
5.6-compatible continuation prompt is `docs/discovery/RUN_PROMPT.md`.
For scheduled autonomous work, `docs/automation/hourly-worker.md` is the canonical runbook.

## Current state

For the **current priority and mode**, read repository-root `BACKLOG.md`; this README
does not own the next action.

Durable state:
- canonical historical data release: `v0.6.1` unchanged;
- best-supported project form: **portable reviewed evidence core + replaceable Atlas/map/table/API views**;
- R1 closed with `HOLD_NO_RELEASE`; later EXP artifacts remain non-canonical research evidence;
- EXP-08 is paused after 3/4 frozen cases; Qi — 500 BCE remains frozen/unstarted;
- DISC-06 rejected a permanent inference-ledger layer;
- DISC-07 added the joint chronology × broad-frame-family QA rule (D-094);
- DISC-08 permits only narrow/optional Frictionless reuse; the Atlas manifest remains authoritative (D-095);
- D-096 changes continuation from automatic successor experiments to mode-level selection and requires cross-batch consolidation/review-capacity control before sustained scaling;
- cross-batch consolidation now reconciles 41 unique R1/EXP-04/06/07/08 targets and selects **review/release** as the next mode rather than new intake;
- DISC-09 is parked, not rejected.


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
