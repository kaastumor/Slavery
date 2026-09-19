# DVC bounded evaluation

This experiment tests DVC as an **optional research-artifact convenience layer**.

It does not use canonical atlas data, write to PostgreSQL, or select a cloud provider.

## Test

The dedicated GitHub Actions workflow:

1. creates a synthetic deterministic binary artifact;
2. initializes an isolated temporary Git/DVC repository;
3. configures an isolated filesystem directory as a fake DVC remote;
4. records the original SHA-256;
5. runs `dvc add` and `dvc push`;
6. removes the workspace file and local DVC cache;
7. runs `dvc pull`;
8. verifies the restored bytes with SHA-256.

This validates DVC's basic data-version workflow without changing the atlas repo into a DVC project.

## What this does not test

- S3/Azure/GCS authentication;
- cloud version-aware remotes;
- multi-user conflict handling;
- long-term preservation;
- DOI/repository deposit;
- database release membership.

## Decision criterion

DVC should be adopted only if its researcher convenience materially outweighs:

- another installed tool/dependency;
- another metadata representation;
- remote configuration/credentials;
- the need to keep DVC metadata consistent with atlas release manifests.

Even if adopted, the atlas release manifest remains the preservation/canonical identity layer.
