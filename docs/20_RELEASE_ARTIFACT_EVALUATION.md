# Release Artifact and Reconstruction Evaluation

**Status:** evaluation-only. This document does not change the canonical schema or release architecture.

## Why this layer matters

A historical release must answer two separate questions:

1. **Which exact external bytes belong to the release?**
2. **Which exact reviewed database records belong to the release?**

Checksumming a workbook solves only the first problem. A database release manifest that lists source versions solves only part of the second.

The current schema has `audit.release_manifest` and `audit.release_source_version`, but does not yet identify the exact claims, actors, spatial entities, geometries, voyages, or coverage assessments that formed a published release. That means release reconstruction is not yet complete.

## Artifact-storage candidates

### A. Plain immutable object storage + atlas manifest

Model:

```text
Git
  release metadata / schema / code / manifest
             |
             v
object storage
  immutable release artifacts
             |
             v
SHA-256 verification + release inventory
```

Advantages:

- storage-provider-neutral at the atlas level;
- simple preservation model;
- exact bytes identified independently from filenames;
- external scholars can understand a manifest without specialist tooling;
- compatible with S3-compatible storage, institutional repositories, Zenodo-style deposits, or other immutable archives;
- can use object versioning/retention where the provider supports it.

Costs:

- we must implement the small amount of manifest/upload/download plumbing ourselves;
- switching among many frequently changing research datasets is less convenient than DVC.

### B. DVC

DVC stores small metadata in Git and data in a configured remote. In version-aware mode it can record cloud object version IDs as well as checksums/metadata.

Advantages:

- convenient `push` / `pull` workflow;
- good for multiple analysts working with large changing datasets;
- supports several remote-storage backends;
- can associate Git states with corresponding data versions.

Costs for this project:

- another required tool for retrieving research artifacts;
- DVC metadata becomes an additional release representation that must stay consistent with atlas release manifests;
- optimized for data/project version-control workflows rather than scholarly preservation semantics;
- remote credentials/configuration remain an operational concern;
- does not solve database release membership by itself.

**Current outcome:** do not make DVC foundational. Run a later bounded trial if dataset volume/collaboration makes manual artifact retrieval burdensome.

### C. Git LFS

Git LFS stores pointer files in Git and large content outside normal Git objects.

Advantages:

- familiar Git workflow;
- GitHub manages access with the repository;
- straightforward for assets that naturally belong to a code repository.

Costs:

- ties canonical artifact retrieval closely to Git/GitHub tooling;
- collaborators need Git LFS for full content;
- each changed large file version consumes storage again;
- GitHub bandwidth/storage accounting becomes part of research-data distribution;
- not sufficient for database release membership or preservation metadata.

**Current outcome:** useful for occasional development assets, not the canonical research-release layer.

### D. GitHub Release assets

GitHub Releases can distribute attached binary assets and are convenient for human downloads.

Advantages:

- convenient project-facing distribution;
- version/tag association;
- no need to put binary data into ordinary Git history.

Costs:

- provider-coupled;
- per-asset size constraints;
- not a substitute for an independent release manifest or preservation repository;
- does not solve canonical DB record membership.

**Current outcome:** potentially useful as a convenience mirror for moderate-size public releases, not the sole canonical archive.

## Object-store immutability

The atlas should not require one cloud provider. However, an eventual object store should ideally support:

- object versioning;
- full-object checksum verification;
- retention/immutability controls;
- read-only/public distribution for published artifacts;
- lifecycle/archive classes where appropriate.

For example, S3 Object Lock uses a WORM model on versioned buckets and can prevent overwrite/deletion for defined retention periods. This demonstrates the capability class we want without committing to AWS.

## Release manifest baseline

The atlas manifest should be understandable without DVC or GitHub.

Minimum artifact entry:

```yaml
role: canonical_input
filename: Historical_Slavery_Atlas_v0.6.1_Controlled_Atlantic_Ingestion.xlsx
sha256: 0a38...
media_type: application/vnd.openxmlformats-officedocument.spreadsheetml.sheet
size_bytes: 57140
storage:
  status: external
  locator: null
```

A published database release additionally needs a stable membership inventory.

## Database release reconstruction gap

Current tables:

- `audit.release_manifest`
- `audit.release_source_version`

are insufficient to reconstruct the exact released graph.

A future canonical schema decision should choose between:

### Option 1 — typed release-membership tables

Examples:

- `audit.release_claim`
- `audit.release_actor`
- `audit.release_spatial_entity`
- `audit.release_geometry`
- `audit.release_voyage`
- `audit.release_coverage_assessment`

Pros: relational foreign-key integrity.

Cons: more tables and maintenance as publishable object types grow.

### Option 2 — generic release object inventory

Example:

```text
release_version
object_type
object_id
row_digest
```

Pros: compact/extensible.

Cons: polymorphic IDs cannot have normal foreign-key enforcement.

### Option 3 — immutable release materialization/export only

Generate an immutable database export/bundle and checksum it.

Pros: strongest byte-level reconstruction.

Cons: less convenient for querying “which release contained this claim?” without importing/reading the bundle.

### Proposed hybrid to evaluate

Use:

1. **typed membership for the important canonical/publishable entities**, plus
2. **an immutable release bundle with checksums and row-count/digest metadata**.

The membership tables support database queries and integrity. The immutable bundle is the preservation/reconstruction artifact.

No migration should be added until this is recorded as a durable decision.

## Publish-view implication

Release membership should eventually be part of the public boundary. “reviewed/published now” and “belongs to historical release X” are different questions.

A public release endpoint should be able to answer:

- current published state;
- exact state for release X.

This avoids a later edit silently changing the meaning of an earlier release.

## Experimental baseline

`experiments/release_artifacts/` contains a small provider-neutral manifest implementation.

It intentionally:

- computes SHA-256 itself;
- verifies exact filename/size/hash;
- supports database membership counts/digests without requiring a live DB;
- does not upload anything;
- does not imply that an artifact is canonical merely because its checksum validates.

This becomes the baseline a DVC trial must beat in usability without weakening preservation/audit semantics.


## DVC bounded trial result — 2026-09-19

A real isolated GitHub Actions trial was executed with DVC 3.66.0 and a 4 MiB deterministic synthetic artifact.

Sequence:

1. initialize temporary Git + DVC repository;
2. configure temporary filesystem DVC remote;
3. compute original SHA-256;
4. `dvc add`;
5. `dvc push`;
6. delete workspace artifact;
7. delete local DVC cache;
8. `dvc pull`;
9. recompute SHA-256.

Result:

- roundtrip: **passed**;
- restored bytes: 4,194,304;
- atlas-side SHA-256 before/after: `d4093f28a49d61c459a09647038e6d9c9e0686811f382a447a38969032583773`;
- DVC pointer recorded MD5 `d65067deec71e3472f2647b1089f90af` and size 4,194,304;
- remote object count: 1.

Interpretation:

- DVC demonstrably restores byte-identical artifacts and gives a convenient add/push/pull workflow;
- its metadata/checksum mechanism is useful operationally, but the atlas should continue to verify SHA-256 independently for canonical release identity;
- DVC still does not define database release membership, QC, unresolved issues, methodology version, or scholarly preservation identifiers.

**Revised outcome:** DVC is a viable optional working-data layer. It should not replace the provider-neutral atlas release manifest. Adoption can wait until source/geometry volume or multi-researcher workflow makes the convenience worthwhile.

## Current recommendation

For the next architecture phase:

- **baseline:** immutable external object store + atlas-controlled release manifest;
- **optional later:** DVC for research-dataset convenience if justified;
- **optional distribution mirror:** GitHub Release assets;
- **not canonical layer:** Git LFS.

The provider remains undecided.
