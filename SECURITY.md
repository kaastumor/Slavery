# Security and sensitive-data handling

This repository is private and currently contains historical research data and development tooling, not production secrets.

- Never commit `.env`, database passwords, cloud credentials, API tokens, or private keys.
- Use `.env.example` only for non-secret defaults and variable names.
- Production/staging secrets must come from the selected deployment platform's secret store.
- Do not publish restricted/copyrighted source assets merely because a citation exists; follow `docs/03_SOURCE_POLICY.md`.
- If a secret is committed accidentally, rotate/revoke it first, then remove it from Git history as a separate cleanup step.
- Public application services must read reviewed/published data only; unrestricted draft research tables are not a public API surface.
