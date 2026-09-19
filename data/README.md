# Data layout

`data/releases/` contains immutable project data releases used to validate migrations.

Current canonical input:

- `releases/v0.6.1/Historical_Slavery_Atlas_v0.6.1_Controlled_Atlantic_Ingestion.xlsx`

Rules:

- never overwrite a historical release in place;
- add a new version directory for a new release;
- the database is not canonical merely because it imports a release successfully;
- release checksums and QC results must be retained with each canonical switch.
