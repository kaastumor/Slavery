# Data API Security Boundary

**Status:** production-verified 2026-09-20  
**Related:** issue #62, D-051

## Intended boundary

The browser does not query canonical research tables through Supabase PostgREST.

The current public path is:

```text
browser
  -> atlas-data Edge Function
      -> audit.release_manifest
      -> publish views
      -> approved cartography materializations
```

The internal schemas `atlas`, `audit`, `cartography` and `publish` are not client Data API contracts. Draft/research tables must not become directly reachable merely because they exist in the same Supabase project.

If a direct Data API surface is added later, use a deliberately exposed API schema (or another explicit reviewed interface) with least-privilege grants and RLS/policies appropriate to that public contract.

## Production verification

Read-only checks against production project `dilnayfllygkplsdymel` found:

- `anon` has no schema `USAGE` on `atlas`, `audit`, `cartography` or `publish`;
- `authenticated` has no schema `USAGE` on those schemas;
- both roles have `USAGE` on `public` and `graphql_public`;
- across 54 checked tables/views in `atlas`, `audit`, `cartography` and `publish`:
  - anonymous SELECT privileges: 0
  - anonymous INSERT privileges: 0
  - anonymous UPDATE privileges: 0
  - anonymous DELETE privileges: 0
  - authenticated SELECT privileges: 0
  - authenticated INSERT privileges: 0
  - authenticated UPDATE privileges: 0
  - authenticated DELETE privileges: 0
- no custom default ACL was found granting those client roles privileges in the internal schemas.

This means an RLS-disabled internal table is not currently equivalent to an anonymously reachable table: the client roles cannot enter the schema or access the object.

## Supabase advisor result

The authoritative Supabase security advisor was rerun after the privilege audit. It did **not** report RLS-disabled-table exposure as a current security lint. Its current finding was:

- `function_search_path_mutable` on `atlas.make_year_range`.

That function warning should be fixed separately as ordinary security hardening.

A generic table-inspection warning had earlier flagged the absence of RLS on internal tables without accounting for the project's schema/grant boundary. That warning triggered this audit, but it should not be interpreted as proof of active Data API exposure.

## Scoped Management API limitation

The GitHub Actions secret `SUPABASE_MANAGEMENT_TOKEN` is intentionally narrow.

During this audit it returned HTTP 403 for:

- `GET /v1/projects/{ref}/postgrest`;
- `GET /v1/projects/{ref}/api-keys?reveal=true`.

Do not broaden the operations/self-heal token merely to make a security audit convenient. Exact platform configuration can be inspected through an appropriately authorized administrative session when needed; effective client access is separately constrained by the PostgreSQL grants above.

## Hardening still required

Current production state is safe by grants, but it should be made resistant to future accidental exposure:

1. explicitly revoke `PUBLIC`, `anon` and `authenticated` access to the internal schemas/objects where those roles exist;
2. set default privileges so future tables/functions/sequences in those schemas do not become client-accessible;
3. add regression tests for the private-schema invariant;
4. verify the public Edge Function/browser still works after the hardening migration;
5. rerun security advisors and resolve the mutable function `search_path` warning.

Do not enable RLS indiscriminately on every internal table without first defining policies. The intended control for these private schemas is non-exposure plus explicit grants; RLS becomes mandatory for any table deliberately exposed to client roles.
