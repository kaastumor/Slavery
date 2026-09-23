# Historical Slavery Atlas — Backlog

**Updated:** 2026-09-24  
**Role:** canonical execution queue only; assumptions/risks/value evidence live in `docs/25_PROJECT_HEALTH.md`  
**Canonical historical data release:** `v0.6.1` (unchanged)  
**Current public preview:** `mvp-preview-ancient-v2` (non-canonical legacy demonstration)

This file answers **what is justified to work on next**.

---

# ACTIVE R1 / RELEASE QC — subject research stopped at 19 C1 rows

**Parent programme:** #159
**Completed closing tranche:** #170
**Decisions:** D-078, D-079
**Current stage:** **R1.6 — release-level QC and candidate-release assembly**

The midpoint-authorized final three-row subject tranche is complete.

## Frozen subject-research result

Across all R1 C1 tranches:
- **19** researched C1 rows;
- **5** classified / bounded-supported;
- **14** inconclusive for the exact frozen target/year/frame question;
- **0** final disputed;
- **4** completed C2 packets;
- **19/19** internally adversarially replayed;
- **0** target substitutions.

These counts are not prevalence and are not completion percentages against the 36-row ceiling.

The remaining frozen queue rows stay unresearched/planned research-state information. They do not imply historical absence.

## Final closure tranche

- Tamna 500 CE — inconclusive; peninsula-wide Korean slavery is context, not Tamna evidence.
- Pandya Empire 1300 CE — inconclusive after C2; strong contemporary Tamil slavery evidence did not safely reproduce target-polity synchronization.
- Chimu Empire 1300 CE — bounded-supported for state labor service/corvée only; not chattel slavery or universal household coercion.

Legacy state was not sticky:
- Pandya legacy positive did not survive Core-v1 rereview;
- Chimú legacy inconclusive became a narrower positive corvée/labor-service claim.

## Balance state

Researched polity sectors after the closing tranche:
- A: 2
- B: 1
- C: 3
- D: 2
- E: 1
- F: 3

12 researched polity rows; maximum sector share = **25%**.

The midpoint balance gap is therefore closed without expanding toward the 36-row ceiling.

## Subject-research stop

**Do not start another C1 subject-research tranche.**

R1.6 should now:
- verify the 19-row candidate package against Core Contract v1;
- audit exact source/version recoverability and dependency groups;
- audit language/access and coverage-state declarations;
- verify all C2 packets are resolved and replayed;
- verify selected-year / target / dimension guards globally;
- verify frozen target-frame and balance invariants;
- run geometry/Atlas-release checks without letting geometry create historical truth;
- assemble candidate release manifest/changelog/QC/unresolved issues;
- keep candidate research release separate from independently reviewed/public/canonical release.

No new subject research is justified merely to fill remaining queue rows.

## Still unchanged

- v0.6.1 remains canonical;
- no production migration;
- no schema/ontology/intensity-scale change;
- no bespoke Atlas/platform feature is earned;
- no target substitution.

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
