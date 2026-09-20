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


## Full-state release bundles

D-054 separates a **candidate manifest** from the preservation-grade bundle that may be promoted.

A candidate manifest names the reviewed claims and release metadata. Before production publication, run `tools/release_bundle.py build` against the database state that is being reviewed. The resulting `*.bundle.json` freezes:

- exact release membership;
- full serialized state for claims, claim-source links, spatial entities, source geometries, resolved render geometries, source versions and parent sources;
- per-object SHA-256 values;
- active cartographic fabric identity/checksum;
- one aggregate database-state SHA-256;
- the candidate-file SHA-256 and source Git revision.

The bundle is the artifact that moves forward. `verify` must pass against the target database before `apply`. `apply` consumes only frozen membership, populates the D-054 typed membership tables with `captured_at_release` digests, registers the bundle in `audit.release_artifact`, and publishes the release. It does **not** move the D-053 serving channel.

The current bundle schema is intentionally scoped to the territorial-practice public preview. Broader release object types must extend the bundle contract explicitly rather than being silently omitted.
