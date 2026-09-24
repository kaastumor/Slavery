# Autonomous evidence worker runbook

> **Current active horizon:** #213 / EXP-04 blind frontier tranche
> **WIP limit:** exactly one active issue/experiment at a time.  
> **Operating decision:** D-088 / HC-024.

This file is the canonical execution contract for scheduled/autonomous Historical Slavery Atlas work.

## Source of truth

Repository: `kaastumor/Slavery`

At every run inspect current `main`, root `BACKLOG.md`, open PRs/issues and CI before relying on chat memory or an older handoff.

Read:
1. `docs/23_PROJECT_CHARTER.md`
2. root `BACKLOG.md`
3. `docs/24_WAY_OF_WORKING.md`
4. `docs/25_PROJECT_HEALTH.md`
5. this runbook
6. the active issue/protocol
7. only the methodology/source/data/geography documents needed for the chosen task.

## Core scheduling rule

**Do not optimize for returning to idle.**

Elapsed time is not treated as the scarce resource. Optimize for:
1. evidence quality;
2. focus;
3. bounded project complexity;
4. expected information gain.

When the current bounded horizon completes:
- reconcile its evidence;
- identify the most decision-relevant unresolved uncertainty;
- compare plausible next experiments;
- create/preregister exactly one bounded successor;
- continue.

A no-work run is justified only when:
- useful work is blocked by missing evidence/permissions/capability;
- continuing would violate project constraints;
- or no bounded experiment can materially change belief.

An empty issue queue by itself is **not** a reason to idle.

## Selection order

1. Resume an unfinished project PR/branch for the active WIP item.
2. Otherwise continue the current active issue.
3. If that issue is complete, perform the evidence reconciliation and select the next highest-information bounded experiment.
4. Prefer real historical/source research over meta-work when both resolve the uncertainty.
5. Do not select parked operational debt unless it blocks the active evidence horizon.

## Required experiment contract

Every new horizon records before execution:
- question;
- why it matters;
- strongest credible alternative/baseline;
- frozen sample or selection rule when applicable;
- evidence contract;
- falsifier;
- complexity boundary;
- canonical-effect boundary.

Stopping/rejecting/simplifying/parking are valid results, not scheduling defaults.

## Work loop

**Question → smallest discriminating proposal → adversarial attack → research/experiment → evidence → decision → regression/fixture where warranted → sanitation → project-state reconciliation → next-question selection**

Green CI is necessary for repository integrity. It is not historical/editorial approval.

## Historical constraints

Never:
- infer absence from unknown/inconclusive/missing evidence;
- infer actor nationality/political identity from flag, port, residence, surname, business base or company jurisdiction;
- infer territorial practice from external/network participation;
- treat law as practice;
- use source/document/voyage counts as prevalence;
- manufacture temporal or spatial precision;
- let geometry prove a slavery/coercion claim;
- expose draft research as canonical/public by default.

Use specialist scholarship for interpretation/prevalence/structure and primary/source-native evidence for bounded facts where appropriate. Preserve contrary evidence and source dependency.

## Complexity boundary

The worker may create small scripts, fixtures, research packets and experiment artifacts when they directly answer the active question.

Do not create a new service, framework, datastore, generic platform, major schema migration or production/public release merely because work is available.

## External/sensitive boundary

External participant recruitment/review remains deferred unless explicitly reopened by sponsor.

Living-person/sensitive modern data remains separately policy-gated.

## Branch/PR discipline

Use a short-lived branch from current `main`. One active WIP issue normally produces one coherent PR.

Before merge:
- run relevant focused tests;
- run sanitation;
- require normal CI green;
- preserve provenance/reproducibility metadata;
- record unresolved items honestly.

After merge:
- close/reconcile the issue;
- immediately apply the continuation rule rather than defaulting to idle.

## End-of-run report

Report:
- active issue;
- evidence gained;
- material changes;
- tests/CI;
- disposition;
- blockers;
- selected next experiment when the current one closed.

Progress is evidence gained or a justified reduction in uncertainty—not commits, issues, record count or elapsed time.

## Actions cost discipline — 2026-09-24

Run focused tests and sanitation locally; batch one coherent checkpoint per PR.
Known documentation/research text changes receive lightweight PR checks; database,
code, workflow and unknown paths retain full PostGIS validation. Manual foundation
dispatch runs all checks. Do not duplicate successful PR validation after merge,
trigger unrelated workflows, or rerun unchanged passing jobs. Weekly/manual preview
monitoring remains. A partial research checkpoint does not close the active issue.
