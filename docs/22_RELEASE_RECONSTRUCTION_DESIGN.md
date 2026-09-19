# Release Reconstruction Design

**Status:** architecture proposal accompanying D-030 and migration 0012. Not canonical until merged after review/QC.

## Problem

A release is not reconstructible merely because its input files are checksummed.

The current foundation can answer:

- which release manifest exists;
- which source versions were associated with it.

It cannot yet answer, with foreign-key integrity:

- which claims belonged to release X;
- which actors/places/geometries were exposed in release X;
- which voyage/network relationship rows were included;
- whether release membership changed after publication.

## Chosen prototype

Use explicit typed membership tables plus immutable release artifacts.

Typed membership is intentionally verbose because the alternative generic table would lose ordinary FK enforcement.

Membership covers:

- claims;
- actors;
- spatial entities;
- geometries;
- spatial relations;
- voyages;
- voyage owners;
- voyage finance rows;
- voyage stops;
- source versions;
- research-coverage assessments.

Release artifacts cover the preservation/export side:

- role;
- filename;
- SHA-256;
- bytes;
- media type;
- storage locator;
- preservation identifier.

## Freeze point

A release starts as `draft`.

While draft:

- membership may be added/removed;
- artifacts may be registered;
- manifest/changelog/QC/unresolved issues may be edited.

Transition:

```text
draft -> validated -> published -> archived
```

After `validated`:

- membership and artifact rows are immutable;
- release content is immutable;
- only lifecycle status may advance.

This means validation is the freeze point, not publication.

## Why validation freezes the release

Publication may occur later than technical/historical validation. If content could change between validation and publication, the validation result would no longer describe the published release.

## Why this still needs an immutable bundle

Foreign-key membership tells us **which canonical IDs** belonged to the release.

It does not guarantee old row values remain unchanged forever.

Therefore a canonical database release must also emit an immutable, checksummed release bundle/export containing the released state. That artifact is the preservation-grade reconstruction source; membership tables provide queryability and integrity.

## What migration 0012 does not do

It does not:

- choose an object-storage provider;
- introduce DVC as a requirement;
- publish any current draft data;
- change P0-P4 semantics;
- alter evidence/source interpretation;
- make the database canonical;
- define the first canonical database release.

## Later work

After this mechanism is accepted:

1. create release-builder tooling that populates memberships from reviewed/published candidates;
2. emit membership files and exports;
3. verify counts and digests against the release package;
4. add release-scoped API queries;
5. tighten public serving so current publication and historical-release views are explicit;
6. run exact v0.6.1 migration/reconciliation before any canonical database cut-over.
