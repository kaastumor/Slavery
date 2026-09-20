# Release Candidate Manifests

This directory contains proposed **non-canonical** release manifests before database publication.

A manifest here is only a release candidate. CI performs syntax/structure checks with `tools/publish_release.py` without modifying any database.

Promotion rules:

- claims must already be reviewed;
- geometry must be approved or explicitly unresolved;
- changelog, QC summary and unresolved-issues list are mandatory;
- `canonical` must remain false unless a separate canonical-release decision/process is explicitly introduced;
- production publication is a separate protected promotion action;
- a promoted release artifact must be immutable and retained with checksums/provenance.
