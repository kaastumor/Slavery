# Historical Slavery Atlas — Backlog

**Updated:** 2026-09-23  
**Role:** canonical execution queue only; assumptions/risks/value evidence live in `docs/25_PROJECT_HEALTH.md`  
**Canonical historical data release:** `v0.6.1` (unchanged)  
**Current public preview:** `mvp-preview-ancient-v2` (non-canonical legacy demonstration)

This file answers **what is justified to work on next**.

Detailed completed-work history belongs in GitHub issues/PRs, the Decisions Log and durable gate/audit records. It is intentionally not repeated here.

---

# IDLE — no new execution horizon is authorized

HC-003 / issue #123 completed the M2 wide-angle review with:

**CONTINUE + SIMPLIFY**

Working identity:

> **auditable historical slavery/coercion evidence corpus + comparison method + thin atlas/query surface**

Durable review:
- `docs/34_WIDE_ANGLE_PROJECT_REVIEW.md`

Direction decision:
- D-062 in `docs/08_DECISIONS_LOG.md`

Completed horizons:
- M1 methodology hardening — #100 / `docs/29_M1_INTEGRATED_ADVERSARIAL_GATE.md`
- M2 semantic/geography integration — #116 / `docs/33_M2_INTEGRATED_ADVERSARIAL_GATE.md`

The execution queue is deliberately idle. Do **not** manufacture an AUTO runway merely because the previous gate finished.

## Candidate next experiment — NOT AUTHORIZED

**Value-discrimination pilot**

Question:

> Does the corpus/method, and then the smallest thin atlas/query view, materially improve difficult cross-place/time historical reasoning over the strongest boring/external workflow?

Candidate design:
- three independent difficult historical questions from different regions/periods;
- at least one temporal/spatial ambiguity case;
- at least one conflicting/qualified-evidence case;
- compare:
  1. specialist literature + structured notes/table + QGIS/nodegoat/general model as appropriate;
  2. Atlas corpus/method without bespoke map interaction;
  3. smallest thin atlas/query/evidence view;
- record effort, provenance recovery, uncertainty/abstention preservation, cross-place/time comparison quality, overclaim and parity/no-value.

Starting this pilot requires an explicit new authorization/horizon. HC-003 itself does not start it.

## Kill rule

A richer Atlas product earns no further application/infrastructure horizon unless at least two independent tasks from different historical contexts demonstrate a repeatable practical advantage over the strongest baseline in inspectable cross-place/time reasoning, provenance recovery or uncertainty preservation without increased overclaim.

If the corpus/method provides the advantage but the thin atlas does not, shrink to the methodology/corpus identity and stop application expansion.

If neither materially outperforms the strongest baseline, stop further Atlas expansion and preserve the methodology/corpus/audit artifacts as the result.

---

# PARKED / trigger-bound operational debt

These are not eligible autonomous work.

## #43 — protected staging / release-promotion administration

Remaining protected environment / staging work matters only if production mutation or a new public release is again justified.

Current controls intentionally reduce mutation:
- production geometry promotion is manual/explicit;
- current preview has static fallback;
- no new production migration is authorized.

Do not create paid staging or new credentials merely to close this issue.

## #26 — live Supabase migration-history reconciliation

The documented live history mismatch remains real.

Do not rewrite migration history casually. Reconcile it only before a future production migration/change actually requires that boundary.

## Repository administration

Not represented as a new issue/queue:
- `main` currently reports unprotected;
- approximately 100 historical remote topic branches remain;
- current integration lacks the repository-admin capability needed for branch protection/bulk pruning.

Handle when an admin-capable maintenance opportunity exists. Do not let it create a development horizon.

## Frontend reproducibility

A real `web/package-lock.json` is still absent.

Generate and commit the genuine lockfile in a networked environment before the next substantive frontend change. Do not invent one offline and do not add package-management infrastructure merely for this.

---

# Explicitly NOT next

Do not next start:

- M2 production schema migration;
- bulk/global H2 evidence expansion;
- bulk Cliopatria source-row → atlas identity publication;
- another frontend redesign;
- PMTiles/vector-tile infrastructure;
- new search service;
- graph database;
- vector store/RAG infrastructure;
- generic ontology/platform work;
- generic digital-humanities research UI;
- custom gazetteer/reconciliation service;
- RDF/CIDOC/PROV infrastructure without a real consumer;
- contributor/peer-review platform;
- new monitoring/self-healing machinery;
- new autonomous execution runway.

If the repository has no explicitly authorized issue after HC-003, **idle is the correct state**.
