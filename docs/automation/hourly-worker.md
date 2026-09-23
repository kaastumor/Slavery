# Hourly autonomous worker runbook

This file is the canonical execution contract for the scheduled Historical Slavery Atlas worker.

## Source of truth

Repository: `kaastumor/Slavery`

At the start of every run inspect current GitHub state. Do not rely on chat memory or an older handoff.

Read:
1. `docs/23_PROJECT_CHARTER.md`
2. repository-root `BACKLOG.md`
3. `docs/24_WAY_OF_WORKING.md`
4. `docs/25_PROJECT_HEALTH.md`
5. this runbook
6. the active parent gate issue
7. open PRs and open `AUTO READY —` issues
8. current `main` CI status
9. only the canonical methodology/architecture documents needed for the chosen task.

Repository decisions newer than an AUTO issue override that issue.

## Serial selection order

1. **Resume first:** if an unfinished `auto/*` PR exists from an earlier worker run, resume/repair/finish it. Do not claim another task.
2. Otherwise identify the highest-priority open issue whose title begins `AUTO READY —`.
3. The issue is eligible only when every explicit dependency in its body is closed as completed.
4. Choose exactly one eligible issue.
5. If none is eligible, do not manufacture work. End the run without changing the project.

Blocked and parked work is not eligible.

## Branching

Use a short-lived branch named `auto/<issue-number>-<short-name>` from current `main`.

One issue normally produces one coherent PR.

## Required work loop

For the selected issue follow:

**Question → smallest proposal → adversary → experiment/implementation → evidence → decision → sanitation → reconciliation**

For each material adversarial finding use exactly one disposition:

**survives / revise / reject / park / experiment**

Attack the strongest credible version of the proposal. Test simpler alternatives. Green CI is necessary, not evidence that the idea itself is useful.

## Scope restrictions

The worker may:
- implement/test a bounded issue;
- research within that issue;
- add fixtures;
- repair CI caused by its work;
- update evidence and the issue;
- merge the completed atomic PR.

The worker may not silently:
- change the project north star;
- skip a gate;
- enter the next strategic horizon;
- promote an experimental method into canonical methodology;
- weaken privacy/provenance/QC;
- introduce major infrastructure;
- redefine success criteria;
- broaden scope because time remains.

When one of those becomes necessary, document the evidence/blocker and stop.

## Privacy and repository boundary

This repository is public.

Never commit:
- secrets, credentials, private keys or access tokens;
- the external canonical workbook binary;
- copyrighted/restricted source assets that are not redistribution-safe;
- private/unpublished personal source material;
- living-person sensitive data without an explicit reviewed policy;
- derived passages, embeddings, annotations, logs or model output that reveal restricted/private source content;
- machine-specific local paths.

CI fixtures must be synthetic or explicitly public-safe.

External model/provider use with restricted/private material requires an explicit approved policy; do not infer permission.

## Reproducibility

For meaningful analytical/research output, preserve the applicable source/data version, checksum, Git revision, tool/model/config version, parameters, methodology/schema version and output identity using existing manifests/audit structures.

## Tests and sanitation

Before opening/merging the PR:
- run the relevant focused tests;
- run the repository sanitation check;
- run the normal project verification required by the issue;
- add/update regression fixtures where behavior can regress.

Do not weaken a test/QC threshold merely to get green CI.

## PR and merge

Open a PR describing:
- question;
- smallest proposal;
- adversarial attack;
- evidence;
- disposition/decision;
- tests/sanitation;
- unresolved items.

Inspect CI and fix failures.

Squash-merge only when:
- issue acceptance criteria are satisfied;
- CI is green;
- no newer repository decision invalidates the issue.

Then close the AUTO issue and update the parent gate/backlog/decision record only when project state actually changed.

## Gate boundaries

Gate adversary and Project Health Check AUTO issues are dependency-gated.

The worker must not create or enter a new gate because the old issue list is empty. The health task must explicitly choose **continue / simplify / redirect / stop**. If continuing, it may establish only a short justified runway after the health evidence supports that choice.

## Blockers

If work requires:
- sponsor judgment;
- paid resource approval;
- unavailable private data;
- credentials/permissions;
- an unapproved project-level decision;

record the blocker on the issue and stop that run. Do not substitute unrelated future-gate work.

## End-of-run report

Report only:
- what issue was worked;
- what materially changed;
- evidence/tests;
- disposition/decision;
- blocker if any;
- next eligible AUTO issue, if one exists.

Progress is evidence gained or capability improved—not commits, issues or lines changed.
