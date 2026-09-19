# Zotero source-crosswalk proof

This experiment evaluates Zotero as a researcher-facing bibliography/source-library layer.

It deliberately does **not** write to PostgreSQL.

## Principle

A Zotero item may initialize a candidate `SOURCE`, but it must not automatically become a reviewed `SOURCE_VERSION` or `CLAIM_SOURCE`.

Reasons:

- Zotero bibliographic metadata may identify a work without identifying the exact edition/PDF/web snapshot actually reviewed;
- attachments are separate digital objects;
- Zotero's local object version is a synchronization/edit version, not a historical publication version;
- a bibliography item is not evidence for a claim merely because it exists in the library.

The proof therefore emits:

- source candidate;
- source-version candidate with an explicit resolution state;
- external Zotero identifiers;
- no canonical UUIDs;
- no claim links.

Exact version resolution remains a human/research workflow step.
