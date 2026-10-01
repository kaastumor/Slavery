# #374 connected SQL transport - pending execution gate

The sponsor questioned the newly requested private local DATABASE_URL and
authorized preparation using the existing connection. Connected Supabase read
access succeeded on 2026-10-01 at 22:08:59 UTC; serving remained
`v0.8.1-public-mvp-v2`. Earlier receipts confirm committed rows and connected
readback, but do not preserve a reproducible write transport.

`tools/export_geometry_closure_tranche_02_sql.py` exports SQL without connecting
or executing. INSERTs come directly from the reviewed Python `apply_once`
helpers, preserving source metadata, Myanmar independence group, geometry roles
and locus notes. Default exported SQL raises before INSERTs. Executable export
requires the original literal `ISSUE-374-EXPLICIT`, environment gate
`ATLAS_GEOMETRY_WRITE_AUTHORIZED=1`, and expected checked-out revision guard.
Export does not grant authorization. The operator must verify merged adapter,
plan and review identities, exact green CI head, explicit sponsor authority for
the four-case write, and fresh live preconditions before submitting SQL.
No live-write authorization was received during transport preparation.

One atomic DO block uses bounded table locks/timeouts and verifies exact
claim/spatial identities, reviewed/unpublished/NULL-P states, candidate
identity/URL/link/release absence, India HRW reuse, and Brazil HOLD. Exact deltas
are +4 entities, +6 sources/versions, +4 points/links and +2 context relations.
Complete snapshots of claims, territorial facets, ingestion ledger, release
membership and serving channels must remain unchanged. The returned receipt
contains actual generated IDs and before/after counts.

A second submission after commit fails closed. An ambiguous connector response
requires independent row/ID/transaction readback before any retry; a timeout
does not prove rollback. The existing Python helper replay must recognize the
SQL-created rows as exact no-ops in the disposable test.

The existing foundation CI runs
`tools/test_geometry_closure_tranche_02_sql.py --disposable-test-db` in local
Compose PostGIS only with CI=true. It tests absent authorization, wrong claim
and source identities, a failure after all INSERTs with complete rollback,
Python no-op replay, generated-ID readback, duplicate submission rejection and
restoration of original counts. It has no production path. Unit checks cover
inert default export, unsupported helper queries and safe SQL literals.
No workflow or dependency is added. Local Docker is unavailable: real PostGIS
evidence must come from exact-head CI, not an asserted local pass.

After a separately authorized commit, independently read back all four points,
source/evidence metadata (including Myanmar dependency), Brazil HOLD and
unchanged claim/release/serving state; freeze the existing production receipt.
Immutable v0.8.1, D-121, released 48/16 counters, #370, #379 and public cutover
remain separate gates. This transport is pending until review/CI acceptance.
