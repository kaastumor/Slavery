# Release artifact experiment

Provider-neutral proof for exact release-artifact identity and database-membership digests.

This experiment does **not** upload artifacts, change the database, or declare a release canonical.

## What it proves

A release manifest can independently record:

- exact artifact filename;
- SHA-256;
- byte length;
- media type and role;
- external storage locator when known;
- database object membership count;
- deterministic digest of sorted stable object IDs.

This is deliberately simpler than DVC. If a later DVC trial is adopted, it must preserve these atlas-level semantics rather than replace them.
