# Security and sensitive-data handling

This repository is **public**. Treat every tracked file, GitHub issue, pull request, Actions log and retained CI artifact as potentially world-readable.

## Data classes

### Public-safe
May be tracked when licensing/provenance permits:
- source code, migrations, tests and synthetic fixtures;
- governance/methodology documentation;
- reviewed historical research records intended for public development;
- public source metadata and redistribution-safe derived artifacts.

### External canonical / restricted source material
Keep outside ordinary Git unless an explicit release policy says otherwise:
- the canonical v0.6.1 workbook binary;
- copyrighted/restricted PDFs, archive images or dataset snapshots without redistribution permission;
- local database backups and dumps.

Git may store checksums, manifests, stable locators and non-restricted metadata for these materials.

### Sensitive personal / unpublished material
Do not put living-person sensitive data, confidential correspondence, private research material or equivalent derived content into Git, CI fixtures, CI logs/artifacts or external model/provider calls without an explicit reviewed policy and lawful basis.

Derived artifacts inherit sensitivity. Extracted passages, embeddings, semantic annotations, model interpretations, screenshots, logs and metadata can reveal protected source content even when the original file is absent.

### Secrets
Never commit:
- `.env` files;
- database passwords;
- cloud credentials;
- API/access tokens;
- private keys;
- production/staging connection strings containing credentials.

Use platform secret stores. `.env.example` may contain variable names and clearly non-secret placeholders only.

## Operational rules

- CI uses synthetic or explicitly public-safe fixtures.
- Production/staging secrets are injected by the deployment platform.
- Public application services consume reviewed/published data only; draft research tables are not a public client API.
- The canonical workbook and other important non-Git artifacts require checksummed, recoverable storage; local-first must not become single-copy storage.
- If a secret is committed, rotate/revoke it first, then remove it from Git history as a separate incident cleanup.
- If modern or living-person research becomes operational, define a specific privacy/threat model before ingestion or publication.

Run `python tools/sanitize_repo.py` before merge. The sanitation check catches a small set of repository-level failure modes; it is not a substitute for source licensing, editorial review or privacy judgment.
