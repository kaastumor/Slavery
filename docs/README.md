# Historical Slavery Atlas — Documentation Index

This directory contains the project’s durable methodology, architecture, decisions, operating rules and historical gate records.

It is **not** a second project-status system. Current execution order lives in repository-root `BACKLOG.md`; current implementation truth lives on GitHub `main`; assumptions/risks/value evidence live in `25_PROJECT_HEALTH.md`.

## Start here

1. `23_PROJECT_CHARTER.md` — problem, contribution, north star, baseline, success/failure and horizons
2. `24_WAY_OF_WORKING.md` — evidence/adversarial/discovery method
3. `25_PROJECT_HEALTH.md` — live assumptions, risks, value evidence and health decisions
4. `00_START_HERE.md` — historical-methodology entry point
5. `08_DECISIONS_LOG.md` — durable canonical decisions
6. `01_PROJECT_STATUS.md` — subordinate current-state snapshot; verify against live GitHub state

Before data/schema work, follow the reading order in `00_START_HERE.md`.

## Canonical ownership

- execution queue: repository-root `BACKLOG.md`;
- durable task evidence: GitHub issues / pull requests;
- methodology and ontology: `02_METHOD_AND_ONTOLOGY.md` plus accepted Decisions Log entries;
- source policy: `03_SOURCE_POLICY.md`;
- data model: `04_DATA_MODEL.md`;
- geography/map rules: `05_GEOGRAPHY_AND_MAP.md`;
- decisions: `08_DECISIONS_LOG.md`;
- system architecture: `11_SYSTEM_ARCHITECTURE.md`;
- assumptions / material risks / value evidence / health dispositions: `25_PROJECT_HEALTH.md`;
- autonomous worker rules: `automation/hourly-worker.md`.

Historical gate/audit records (for example M1/M2 adversarial records) are evidence of how a decision was reached. They do not become competing current-state owners.

## Canonical historical data baseline

The immutable historical release remains v0.6.1 until a deliberately validated successor release is created. Git stores checksums/manifests and reconstruction logic; the canonical workbook binary remains external.

Architecture drafts, experiments, database working state, public previews and published/canonical historical releases are distinct states. A newer file is not canonical merely because it is newer.

## Historical documents

Several numbered documents record earlier implementation phases. Read them as historical evidence unless a current canonical document explicitly points to them for active rules.

Do not update historical phase documents merely to make their old status prose appear current. Prefer correcting the small set of canonical/current owner documents above.
