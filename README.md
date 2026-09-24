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

- canonical historical data release: `v0.6.1` (external immutable workbook; unchanged);
- frozen legacy public preview: `mvp-preview-ancient-v2` (non-canonical demonstration);
- architecture experiments COV-001→004: completed;
- R1 historical subject research: **complete and frozen at 19 reviewed C1 rows**;
- R1.6 release QC: **PASS WITH EXPLICIT LIMITATIONS**;
- R1 candidate registry: 77 frozen targets = 19 reviewed C1 + 15 planned/unresearched C1 + 2 held + 41 C0-only;
- source dependency layer: 45 source relations / 37 independence groups;
- R1 closure: **HOLD_NO_RELEASE**; no automatic publication;
- EXP-02: portable evidence packet survived; EXP-03 added terminology/mapping and source-role/claim-fitness requirements (D-089);
- EXP-04 and EXP-06 historical tranches are complete; EXP-07 identity/anchor qualification closed with 7 ready + 1 hold;
- active horizon: **#232 / EXP-08 cross-frame historical evidence tranche**, four frozen targets;
- EXP-08 has 3/4 frozen cases completed: Great Zimbabwe researched-inconclusive for slavery/status; Māori 1700 bounded-supported for pre-contact war-captive unfreedom; Nobatia 500 bounded-supported for royal retainer sacrifice with slave status unresolved;
- **Qi — 500 BCE remains frozen/unstarted**; EXP-08 is paused after Nobatia by sponsor priority;
- next: a bounded **project-discovery research run** on adjacent methods, comparable projects and evidence-corpus opportunities;
- no production migration, new public release or platform expansion authorized.

See `BACKLOG.md`, `experiments/exp08-cross-frame-evidence/CHECKPOINT.md`, and `docs/08_DECISIONS_LOG.md`.

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
