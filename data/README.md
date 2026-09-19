# Data and release artifacts

`data/releases/` stores immutable **release metadata**: version notes, expected filenames, checksums and later QC/release manifests.

Canonical research binaries are kept outside ordinary Git history. A release artifact is accepted only when its exact filename/version is known and its checksum matches the committed manifest.

Current canonical artifact:

- version: v0.6.1
- filename: `Historical_Slavery_Atlas_v0.6.1_Controlled_Atlantic_Ingestion.xlsx`
- SHA-256: see `releases/v0.6.1/SHA256SUMS.txt`

Rules:

- never overwrite a historical release in place;
- changed bytes require a new release/version;
- never silently substitute a related file for a missing canonical artifact;
- the database is not canonical merely because migrations or CI pass;
- every canonical switch needs changelog, QC summary and unresolved-issues list.
