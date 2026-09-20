# Release Candidate Artifacts

This directory contains proposed **non-canonical immutable release artifacts** before database publication.

A candidate is not merely a request to discover membership later. It freezes the exact tested release membership: sorted unique `claim_ids`, `spatial_entity_ids`, `geometry_ids`, and `source_version_ids`, together with release metadata and `artifact_sha256`. The SHA-256 is computed from canonical JSON over every field except `artifact_sha256` itself.

CI validates artifact structure and integrity with `tools/publish_release.py` without modifying any database. Production promotion must consume these exact bytes (or an equivalently checksum-verified retained artifact); `publish_release.py` verifies that the frozen members still exist in acceptable reviewed state but does **not** expand membership from whatever happens to be reviewed at apply time.

Promotion rules:

- claims must already be reviewed;
- geometry membership is explicit and every listed geometry must still be reviewed;
- source-version and spatial-entity membership must exactly match the frozen claim membership;
- changelog, QC summary and unresolved-issues list are mandatory;
- `canonical` must remain false unless a separate canonical-release decision/process is explicitly introduced;
- production publication is a separate protected promotion action;
- promotion records the artifact checksum in the release manifest;
- any membership change creates a new artifact/checksum; never mutate a reviewed artifact in place.

This implements the build-once/promote-unchanged boundary from D-046 for preview release membership. Exact historical row reconstruction/digest semantics remain issue #4 and are deliberately not invented here.
