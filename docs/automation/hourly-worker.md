# Hourly autonomous worker runbook

> **Current active horizon:** MVP v0.1 / #174.  
> **Current fixed serial queue:** #175 -> #176 -> #177 -> #178 -> #179 -> #180 -> #181 -> #182.  
> **Discovery gate:** #184 -> #185 -> #186 -> #187 only after #182 records **TECHNICAL_MVP_CANDIDATE**.  
> **WIP limit:** exactly one issue per run.


This file is the canonical execution contract for the scheduled Historical Slavery Atlas worker.

## Source of truth

Repository: `kaastumor/Slavery`

At the start of every run inspect current GitHub state. Do not rely on chat memory or an older handoff.

Read:
1. `docs/23_PROJECT_CHARTER.md`
2. repository-root `BACKLOG.md`
3. `docs/24_WAY_OF_WORKING.md`
4. `docs/25_PROJECT_HEALTH.md`
5. `docs/mvp/v0.1-plan.md`
6. `docs/mvp/delivery-discovery-cadence.md`
7. this runbook
8. the active parent gate issue
9. open PRs and open `AUTO READY —` issues
10. current `main` CI status
11. only the canonical methodology/architecture documents needed for the chosen task.

Repository decisions newer than an AUTO issue override that issue.

## Serial selection order

1. **Resume first:** if an unfinished `auto/*` PR exists from an earlier worker run, resume/repair/finish it. Do not claim another task.
2. During MVP delivery, use the fixed priority order **#175 -> #176 -> #177 -> #178 -> #179 -> #180 -> #181 -> #182**.
3. An issue is eligible only when its title begins `AUTO READY —` and every explicit dependency in its body is closed as completed.
4. Do not enter discovery #184–#187 unless #182 has explicitly recorded `TECHNICAL_MVP_CANDIDATE`.
5. After that gate, discovery priority is **#184 -> #185 -> #186 -> #187**.
6. Choose exactly one eligible issue.
7. If none is eligible, do not manufacture work. End the run without changing the project.

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


## MVP-specific boundaries

While #174 is active:

- preserve R1 subject-research stop at 19 C1 rows;
- use the existing Vite + TypeScript + MapLibre application;
- prefer a generated static/read-only candidate bundle over live backend coupling;
- do not add a backend, database migration, auth, framework replacement, graph/vector/search service or new historical ontology;
- do not derive new P0–P4/intensity values;
- neutral world land remains visible;
- unresearched / held / inconclusive / unresolved geometry never means absence;
- temporal rendering must obey the R1.6 temporal annotation artifact;
- review labels must not imply independent review;
- v0.6.1 remains canonical until R1.8 explicitly decides otherwise.

Issue #182 is a **technical** gate only. It may record TECHNICAL_MVP_CANDIDATE or HOLD_REWORK. It must not fake sponsor usability acceptance or canonical publication.

## Discovery-specific boundaries

For #184–#187:

- do not implement a production feature;
- state the user/research task and strongest boring baseline first;
- define a kill rule before prototyping;
- use external precedent to remove scope as readily as add it;
- prefer paper/mock/manual experiments over code;
- end with exactly one disposition: ADOPT_FOR_EXPERIMENT / REVISE / REJECT / PARK;
- an ADOPT_FOR_EXPERIMENT result still requires a later separately authorized delivery issue.
