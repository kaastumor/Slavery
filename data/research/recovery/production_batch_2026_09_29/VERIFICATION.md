# Population batch — executable packet and import verification

Issue #360; map refinement remains deferred. This is verification of the existing
11 tracked packages, not permission to insert them again into production.

## Input identity

`preflight.json` preserves the observed production claim IDs, recorded packet
revisions and ingestion digests. `tools/add_research_case.py` hashes **canonical
parsed JSON** (`ensure_ascii=False`, sorted keys, compact separators, UTF-8). A
SHA-256 of the indented file bytes is a different value. Comparing those values as
though they used the same serialization produces a false integrity failure.

`tools/verify_population_packets.py` now reads each exact `commit:path` through
Git and reports both digests, byte length and Git blob identity. It also checks
the current checkout against the recorded content; a mismatch is not silently
normalized or applied. Unit tests compare its result to the actual importer.

Run from a complete repository checkout:

```sh
python tools/verify_population_packets.py --output /tmp/population-packet-verification.json
python -m unittest tests.test_population_packets -v
```

## Disposable database rehearsal

The existing `scripts/db-test-research-idempotency.sh` now additionally runs
`tools/test_population_replay.py` against the existing local Compose test DB.
It tests all 11 packets together, verifies persisted claim and evidence-link
fields, repeats the batch as 11 no-ops, refuses changed content under an existing
case key, and rolls the transaction back. It verifies restoration of tracked
table counts. Generated test UUIDs are never substituted for existing live IDs.

The driver requires an explicit disposable-test flag, `CI=true`, host `db`, user
`atlas`, database `slavery_atlas`, and no DSN overrides. There is no commit path.
No new workflow, paid resource, production access or publication is introduced.

## Interpretation limit

A green mechanical rehearsal is not historical acceptance or deployment readiness.
The 23 prospective new subjects are not included in these 11 replay fixtures.
Claim-specific source review, live field-level reconciliation, extended post-M1
annotations, geometry role/time fit, D-121 closure where applicable, immutable
successor selection and public-channel acceptance remain distinct gates.

Four synthetic regression checks and Python compilation were run locally before
submission. The real 11-packet/replay results must be read from the resulting
exact-commit CI run; this file does not predeclare their outcome.
