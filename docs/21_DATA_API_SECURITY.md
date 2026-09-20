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

Migration `0024_fix_make_year_range_search_path.sql` pins `atlas.make_year_range(integer, integer)` to `search_path = pg_catalog`. The authoritative Supabase security advisor was rerun after the live change and returned **zero security lints**.

A generic table-inspection warning had earlier flagged the absence of RLS on internal tables without accounting for the project's schema/grant boundary. That warning triggered this audit, but it should not be interpreted as proof of active Data API exposure.

## Scoped Management API limitation

The GitHub Actions secret `SUPABASE_MANAGEMENT_TOKEN` is intentionally narrow.

During this audit it returned HTTP 403 for:

- `GET /v1/projects/{ref}/postgrest`;
- `GET /v1/projects/{ref}/api-keys?reveal=true`.

Do not broaden the operations/self-heal token merely to make a security audit convenient. Exact platform configuration can be inspected through an appropriately authorized administrative session when needed; effective client access is separately constrained by the PostgreSQL grants above.

## Hardening completed

Migration `0023_private_data_api_boundary.sql` is live and makes D-051 enforceable:

1. `PUBLIC`, `anon` and `authenticated` are explicitly revoked from the internal schemas and their tables/sequences/functions;
2. matching restrictive default privileges prevent future objects from silently becoming client-accessible;
3. foundation CI now runs `004_private_data_api_boundary.sql` as a regression gate;
4. post-migration production checks show both client roles have zero schema usage, zero relation read/write privileges, zero sequence usage and zero function execution privileges across the internal boundary;
5. explicit `SET ROLE anon` / `SET ROLE authenticated` read and side-effect-free write probes against `atlas.geometry` fail with PostgreSQL `42501 permission denied for schema atlas`;
6. MVP Availability Monitor run `35530806716` passed after migrations 0023/0024, validating the public Edge Function and GitHub Pages serving path;
7. migration `0024_fix_make_year_range_search_path.sql` resolved the remaining advisor finding, and the authoritative Supabase security advisor now reports zero lints.

Do not enable RLS indiscriminately on every internal table without first defining policies. The intended control for these private schemas is non-exposure plus explicit grants; RLS is required for any table deliberately exposed to client roles.
