# Release Package Contract — Evaluation Draft

**Status:** evaluation-only. This is a proposed release contract, not yet a canonical methodology/schema decision.

## Why define a package contract

A release should remain understandable even if:

- GitHub is unavailable;
- the production cloud provider changes;
- DVC is no longer used;
- the live database has moved on;
- the public frontend has been replaced.

The release therefore needs a self-describing package whose identity does not depend on one service.

## Three separate concerns

### 1. Working artifact storage

Purpose: store source datasets, geometry packages, intermediate exports and other large files used during research/development.

Possible implementation:

- S3-compatible object storage;
- equivalent managed object storage;
- institutional storage.

DVC may later be layered over this for researcher convenience.

### 2. Canonical release identity

Purpose: say exactly what release X contains.

Authority:

- atlas release manifest;
- SHA-256 checksums;
- exact database release membership;
- schema/methodology/code versions;
- QC/unresolved-issues documentation.

This identity must be independent of the storage vendor.

### 3. Scholarly preservation/distribution

Purpose: make a published release independently citable and durable.

Candidate destinations:

- discipline-specific repository where suitable;
- institutional repository;
- Zenodo/general-purpose research repository;
- optional GitHub Release mirror for convenience.

A preservation deposit gets referenced *from* the atlas manifest; it does not redefine the atlas release.

---

## Proposed release directory

```text
release-X/
├── manifest.json
├── CHANGELOG.md
├── QC_SUMMARY.md
├── UNRESOLVED_ISSUES.md
├── README.md
├── data_dictionary/
│   └── ...
├── exports/
│   ├── claims.*
│   ├── sources.*
│   ├── actors.*
│   ├── spatial_entities.*
│   ├── geometries.*
│   └── research_coverage.*
└── checksums.sha256
```

Not every early release needs every export format. The contract is about identity and documentation, not forcing CSV/Parquet/RDF simultaneously.

## Proposed manifest fields

### Release identity

- release version;
- release status;
- created/published timestamp;
- canonical predecessor;
- methodology version;
- schema version;
- source-code Git commit/tag;
- database migration ledger digest.

### Artifacts

For each artifact:

- role;
- filename/object name;
- SHA-256;
- bytes;
- media type;
- format/version where relevant;
- storage/preservation locator(s);
- rights/redistribution state where relevant.

### Database membership

For each publishable object type:

- object type;
- count;
- deterministic digest of sorted stable IDs;
- optionally a membership file whose own SHA-256 is in the artifact list.

Candidate types include:

- claim;
- actor;
- spatial entity;
- geometry;
- voyage/network relationship as applicable;
- research-coverage assessment;
- source version.

### Documentation

- changelog;
- QC summary;
- unresolved issues;
- known disputes;
- known unresolved geometry;
- known missing source versions/assets.

### Preservation identifiers

After scholarly deposit:

- version DOI/handle/ARK/etc.;
- concept DOI where applicable;
- repository name;
- deposit record/version.

---

## Database membership file

A simple release can export one newline-delimited stable-ID list per object type:

```text
membership/
  claims.txt
  actors.txt
  spatial_entities.txt
  geometries.txt
  source_versions.txt
```

Rules:

1. one stable UUID per line;
2. sorted bytewise/lexically;
3. no duplicates;
4. UTF-8;
5. LF line endings;
6. final newline;
7. SHA-256 recorded in `manifest.json`.

This is intentionally boring. It can be validated without PostgreSQL, DVC, Python package managers or a particular cloud SDK.

## Why both membership and exports

They solve different problems:

- membership answers **which canonical objects belonged to the release**;
- exports answer **what data were distributed in a particular representation**.

An export format can change while canonical object membership remains stable.

## Database reconstruction requirement

Before a database release becomes canonical, we should be able to run:

```text
release manifest
       +
membership inventory
       +
immutable release export / database snapshot
       +
schema migrations + code version
       =
reconstructable released state
```

The first canonical database release should have an automated verification command that fails when:

- a member is missing;
- an unexpected object is present;
- counts differ;
- membership digests differ;
- artifact hashes differ;
- migration/schema versions differ.

## Public preservation candidate: Zenodo

Zenodo is worth evaluating for *published* releases because it:

- assigns DOIs on publication;
- supports version-specific and concept-level DOIs;
- treats new file versions as new records/versions;
- provides a general-purpose research-data preservation/distribution path;
- supports substantial dataset deposits.

This is not a working-storage recommendation. It is a possible preservation/deposit target after atlas review and release validation.

## Current proposed operating model

```text
research / imports
      |
      v
working object store
      |
      v
PostgreSQL/PostGIS reviewed release candidate
      |
      v
atlas release builder
      |
      +--> manifest + membership + exports
      |
      +--> immutable internal release storage
      |
      +--> scholarly preservation deposit (when public)
      |
      +--> optional GitHub Release convenience mirror
```

## Decisions still required

Before implementation becomes canonical:

1. choose typed DB membership tables vs another membership mechanism;
2. define stable release URI/identifier policy;
3. choose first internal object-store implementation;
4. decide when a release qualifies for external DOI deposit;
5. define which exports are mandatory for the first database release;
6. record the resulting choices in the Decisions Log.
