# Historical Slavery Atlas — Backlog

**Updated:** 2026-09-27  
**Role:** canonical execution queue only; assumptions/risks/value evidence live in `docs/25_PROJECT_HEALTH.md`  
**Canonical research authority:** PostgreSQL/PostGIS, explicit governed membership under D-109  
**Canonical historical data release:** `v0.8.1`  
**Current public serving adapter:** `v0.8.1-public-mvp-v1` → canonical source `v0.8.1`  
**Public Atlas:** `https://kaastumor.github.io/Slavery/`  
**Preserved R1 technical candidate:** `r1-candidate.html` (non-canonical historical project artifact)

This file answers **what is justified to work on next**.

---

# CURRENT MODE — EXECUTION / CONSOLIDATION — ATLAS EXPANSION 01 (#332)

**Gate 0→5 canonicalization programme:** **COMPLETE**  
**Canonical historical data release:** `v0.7.0`  
**Live schema head:** `0034`  
**Public serving adapter:** `v0.8.1-public-mvp-v1`  
**Independent historical review:** 0  
**Open delivery WIP:** **#332 — balanced claim intake + defensible mapped loci**

## Sponsor-authorized D-096 reopening trigger

On 2026-09-26 the sponsor explicitly authorized historical intake to begin filling the
Atlas in both claims and mapped coverage. This activates D-096 mode
**execution / consolidation**. It does not authorize automatic publication, P-level
inference, indiscriminate geometry, or source-density-driven case selection.

The active WIP has two inseparable safeguards:

1. **Claim lane:** admit reviewed evidence packages only at their defensible temporal,
   spatial and categorical scope. Start with already-reviewed weak-region research
   before returning to source-dense Atlantic/Mediterranean defaults.
2. **Geometry lane:** resolve geometry independently. Prefer exact/authoritative site
   loci and genuinely defensible historical polygons; unresolved stays unresolved.
   Geometry must never strengthen the historical claim.

Current checkpoint: canonical **v0.8.1** and public serving materialization
**v0.8.1-public-mvp-v1** are live. The release contains 75 canonical claims / 50
spatial entities / 46 reviewed resolved historical geometries; the public territorial
adapter displays 53 territorial-practice claims across 48 places.

D-116 now requires every public polygon to come from the reviewed render layer rather
than raw research geometry. The v0.8.1 corpus alignment audit covers all 46 release
geometries; all 39 polygons use the canonical Natural Earth land fabric and pass the
outside-land tolerance. D-117 replaces only the Roman 14–22 CE slice with the reviewed
AWMC-derived specialist geometry.

Active expansion continues through #332 and the two hourly lanes:
- evidence/entry completion;
- geometry resolution and corpus-wide cartographic QC.

Prior releases remain immutable. New complete entries and defensible geometries move
through explicit successor release membership and serving cutover rather than mutating
v0.8.1.

## Previous D-096 post-cutover boundary

The post-cutover whole-project review found **no justified automatic successor** before
the sponsor-authorized intake trigger.

Why:

- the canonicalization/release/cutover programme is complete and production verification
  is green;
- no unresolved historical-method question currently blocks routine use of the accepted
  evidence contract;
- no coherent unreleased candidate currently requires a release gate;
- no observed public-serving defect, security lint or payload drift requires repair;
- bespoke Atlas expansion remains unsupported by the earlier value evidence;
- new historical intake is not authorized merely because capacity exists;
- #43's remaining protected-environment / paid-staging work did not cause a demonstrated
  Gate-5 failure and has no active production-promotion task to serve.

This is **not** a claim that the project is finished forever. D-096 explicitly permits a
no-active-work boundary when all useful modes are complete, unjustified or trigger-bound.

The standing weekly public-health monitor remains ordinary maintenance. Static fallback
and exact release identity reduce outage risk; no user-critical SLA has been demonstrated
that would justify higher-frequency monitoring.

## Reopening triggers

Choose one new WIP only when a concrete trigger occurs:

1. **maintenance** — public API/site failure, release-byte mismatch, security regression,
   migration/recovery defect, or a demonstrated released-data correction;
2. **execution / consolidation** — sponsor-authorized historical intake, changed evidence,
   or a recorded HOLD/accepted-row reopen condition;
3. **review/release** — a coherent reviewed candidate plus a concrete publication need;
4. **discovery** — a material unresolved method/value/representation question tied to a
   real task rather than adjacency or unused capacity;
5. **#43 infrastructure** — a future approved production mutation/release specifically
   requires protected environments, durable least-privilege write credentials, or a
   real staging target that the current bounded manual process cannot safely provide;
6. **independent review** — only when an actual external-review horizon is explicitly
   authorized.

Until one trigger is present, do not manufacture a research tranche, UI redesign,
infrastructure project or discovery experiment.

# Discovery execution

Use `docs/discovery/DISCOVERY_EXECUTION.md` and `docs/discovery/RUN_PROMPT.md`.
D-091/D-092 govern execution discipline; neither changes EXP-08's frozen sample,
historical acceptance criteria or release boundary.

## Actions budget

Batch one coherent checkpoint per PR. Run Python tests/sanitation locally first.
Normal PR checks run sanitation and Python regressions; PostGIS runs for changes
outside known documentation/research text paths, or on manual dispatch. No duplicate
foundation run on merge. Public Atlas health remains weekly/manual, not every push.
Do not skip required relevant checks or rerun unchanged successful jobs.

## Continuation rule

D-096 governs continuation.

At a boundary choose the next justified **mode**:
1. discovery;
2. execution;
3. consolidation;
4. review/release;
5. maintenance;
6. no justified work.

WIP = one active priority, not one mandatory experiment.

Choose by:
1. evidence quality;
2. decision importance / project goal;
3. focus;
4. review/reconciliation capacity;
5. whole-project complexity;
6. only then execution convenience.

Elapsed time alone is not a stop rule, and unused capacity is not a reason to invent
another experiment.

Accepted methods may be used within their declared operational scope without re-proving
their value. Reopen them only on a concrete trigger recorded in D-096.

---

# PARKED / trigger-bound operational debt

These remain trigger-bound and are not the default horizon.

## #43 — protected staging / release-promotion administration

**Parked after the Gate-5 review.** Gate 5 completed with an immutable staged
materialization, production CAS/rollback proof, manifest immutability and successful
post-deploy verification. No release incident demonstrated that paid Supabase staging
or protected GitHub deployment administration is currently necessary.

Reopen #43 only for a future approved production mutation/release when the current
bounded manual promotion path is insufficient or a durable least-privilege automated
write boundary is concretely required. Do not create paid staging or credential
infrastructure merely to make the issue disappear.

## #26 — migration-history reconciliation

**Closed / historical.** Gate 0 passed `MIGRATION_HISTORY_RECONCILED`. Do not reopen the
old mismatch as active work unless a new concrete migration-history inconsistency is
observed.

## Managed backup/PITR

Current Supabase Free-plan recovery evidence is logical/preservation-grade rather than
physical managed backup/PITR. Revisit if plan/capabilities change or operational
durability becomes a release requirement; do not require a paid temporary branch merely
for process ceremony.

## Repository administration

- `main` currently reports unprotected;
- historical remote topic branches remain;
- current integration lacks some repository-admin capability.

Handle when it materially blocks evidence/release work; do not turn administration into
the project horizon.

---

# Explicitly NOT the current horizon

The completed Gate-0→Gate-5 programme does **not** authorize:

- automatic new historical subject research;
- richer frontend/application expansion;
- automatic P-level inference;
- inferred historical-practice geometry;
- PMTiles/vector-tile infrastructure expansion;
- new search, graph, vector-store/RAG or generic platform infrastructure;
- contributor/peer-review platform work;
- external recruitment/review without an explicit horizon;
- paid staging/protected-environment administration without a concrete release need;
- higher-frequency availability automation without evidence of a user-critical SLA;
- another experiment merely because there is no active WIP.

The current state is **sponsor-authorized Atlas expansion with one coordinated evidence/geometry WIP (#332)**.

