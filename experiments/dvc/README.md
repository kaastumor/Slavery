# DVC bounded evaluation

**Status: completed experiment; PARKED / not adopted.**

This experiment tested DVC as an optional research-artifact convenience layer. It used no canonical atlas data, did not write PostgreSQL and did not select a cloud provider.

## Executed result

GitHub Actions run `tooling-dvc-evaluation` passed on 2026-09-19 using DVC 3.66.0.

A deterministic 4 MiB synthetic file survived:

`add → push → local file deletion → local cache deletion → pull`

with the exact same SHA-256.

This proves basic technical viability only.

## Project-value result

The experiment did **not** demonstrate a current atlas problem that DVC solves materially better than the existing checksum manifest + immutable artifact/release approach.

Current tooling triggers explicitly say that repository/Actions size, retention and reproducibility have not crossed the adoption threshold.

Disposition: **PARK**.

DVC is therefore not a required dependency, not part of the canonical release mechanism and not a persistent CI responsibility.

The dedicated evaluation workflow was retired after the experiment. If the large-artifact trigger in `docs/22_TOOLING_EVALUATION_TRIGGERS.md` fires later, reopen the comparison as a new bounded experiment against the then-current simple baseline rather than silently reviving this workflow.

## What the experiment did not test

- S3/Azure/GCS authentication;
- cloud version-aware remotes;
- multi-user conflict handling;
- long-term preservation;
- DOI/repository deposit;
- database release membership.

Those omissions are acceptable because adoption is not currently justified.
