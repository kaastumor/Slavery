# Gate 4 adversarial release review — v0.7.0

**Gate:** #319 under parent #300  
**Date:** 2026-09-26  
**Disposition:** `PUBLISH_DB_BACKED_CANONICAL_RELEASE`  
**Canonical package commit:** `1cc7c227de9559a4659058d38327befdfdec6b5b`  
**Publisher commit:** `1818ccfdd735a44907e19ea8fd7d4cbf3423c6e7`

## Question

Can the project publish the first immutable DB-backed canonical historical release from
the D-109 research-authority closure without weakening membership, provenance,
uncertainty, review truth, cartography boundaries or release immutability?

## Adversarial result

**PASS.**

The release is not derived from every reviewed database row. It is a deterministic
package of the exact frozen D-109 authority closure, with exact typed membership and
object digests registered in PostgreSQL. The package is independently rebuildable from
its committed specification and frozen authority input.

## Acceptance attacks

| # | Attack | Result | Evidence |
|---|---|---|---|
| 1 | Legacy preview/prototype rows leak into the release | PASS | Membership is copied from the frozen D-109 closure rather than rediscovered from mutable rows. Live pre-publication comparison matched the frozen authority exactly. |
| 2 | Bare `review_status` defines membership | PASS | The release builder consumes exact D-109 membership IDs and authority bundle SHA-256. No membership query over `review_status` is used. |
| 3 | Gate-3 authority members are lost or added | PASS | Published membership is exactly 40 claims / 11 actors / 18 spatial entities / 0 geometries / 8 voyages / 99 coverage assessments / 211 source versions / 26 research-target results; membership SHA-256 remains `ebc9d32f09857744841a0cf92699c41739b624ac4bd94c43798eb1f61e3b0dd3`. |
| 4 | HOLD / under-review / researched-inconclusive becomes absence | PASS | Frozen target states retain 21 `researched_internal` and 5 `under_review`; six recorded outcomes remain explicitly inconclusive. No negative claim is created from those states. |
| 5 | Distinct historical dimensions collapse into one slavery flag | PASS | Frozen claim kinds remain separate: 18 territorial practice, 12 voyage owner, 6 actor attribute, 3 external participation and 1 legal event; research coverage remains a separate release family. |
| 6 | Source-version or source-native lineage is lost | PASS | 211 exact source-version objects are frozen with parent source/assets as applicable. v0.6.1 raw/source-native lineage remains governed by the immutable predecessor plus Gate-1 ingest/reconciliation tooling. |
| 7 | Cartography recovery silently relies on runtime EWKB | PASS | The exact D-108 portable cartography fingerprint is shipped as `cartography-recovery-fingerprint.json`; production raw EWKB remains a runtime fingerprint, not the cross-runtime identity. |
| 8 | v0.6.1 is overwritten or reinterpreted | PASS | The predecessor workbook remains separately identified by filename and SHA-256 `0a38e4eb6f63c3bb4ce9543be379605d24dd9ff1c1cea1e0a49c0c3db7ba17d4`. |
| 9 | Rebuild is nondeterministic | PASS | PR #321 tests a byte-for-byte rebuild of the committed package and rejects tampering. |
| 10 | Published membership/artifacts remain mutable | PASS | Post-publication no-op UPDATE probes against a release artifact and release claim were blocked by the existing published-release immutability guards. |
| 11 | Internal review is represented as independent review | PASS | Independent historical review remains exactly 0 in the spec, manifest and release documentation. |
| 12 | Gate 4 silently moves the public UI/API | PASS | `audit.release_channel.public_mvp_preview` remained `mvp-preview-ancient-v2`; all 40 authority claim `publication_status` values also remained unchanged. |

## Live-state verification

Immediately before publication, live Supabase was checked read-only:

- `v0.7.0` did not yet exist;
- schema head was `0033_release_research_target_result_membership.sql`;
- public serving pointer was `mvp-preview-ancient-v2`;
- Supabase security advisor returned zero lints;
- all eight D-109 object families reconstructed from live tables matched the frozen
  authority bundle exactly;
- the active production cartography snapshot also matched exactly.

The atomic publication then inserted the exact manifest, exact typed membership digests
and nine package-file artifact records, before transitioning the release
`validated -> published`.

Post-publication verification found:

- release status: `published`;
- canonical manifest flag: `true`;
- exact membership counts unchanged;
- artifact count: 9;
- reviewed historical evidence geometry membership: 0;
- all 40 authority claims still `publication_status='unpublished'`;
- public preview still `mvp-preview-ancient-v2`;
- security advisor: zero lints.

## Release identity

Canonical historical release: **v0.7.0**

Frozen identifiers:

- schema: `0033`;
- membership SHA-256:
  `ebc9d32f09857744841a0cf92699c41739b624ac4bd94c43798eb1f61e3b0dd3`;
- D-109 production DB-state SHA-256:
  `31b7a7b675445e5758ffd68d64ff0f0cde83df1b0ea65f29835246deb2ae26ff`;
- authority bundle SHA-256:
  `e26bc9243c71226e6107162d15c44a0fa13d063ed7708bb12627e4ee8f13c54b`;
- release manifest SHA-256:
  `f65964221cbe2045d75303a5940c75f4526e9110a2b2cf323a9d0979e2f5e57a`;
- `SHA256SUMS.txt` SHA-256:
  `16f6ecfcafbf145441066ff8db9a5dd2c258b857a692f2de7847e65f25879c0d`.

## Residual limits

This release does not erase the explicit unresolved issues carried in
`data/releases/v0.7.0/UNRESOLVED_ISSUES.md`.

In particular:

- independent historical review remains 0;
- reviewed historical evidence geometry membership remains 0;
- the Fredensborg arrival/disembarkation disagreement remains unresolved;
- the v0.6.1 source-registry gap remains preserved rather than silently normalized;
- Supabase managed backup/PITR is not claimed. Recovery evidence remains the
  preservation-grade logical recovery established in Gate 3.

These are release facts, not reasons to infer historical absence.

## Public boundary

Gate 4 changes canonical historical release identity only. It does not make every
release member a public map feature and does not authorize direct public reads from
unrestricted research tables.

Gate 5 / #323 owns the separate staging, serving-materialization, rollback and final
public-channel cutover decision.
