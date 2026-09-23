# M2 integrated adversarial gate

**Parent:** #116  
**Gate:** #122  
**Final attack date:** 2026-09-23  
**Result:** **SURVIVES after two correction cycles**  
**Canonical historical release:** v0.6.1 unchanged  
**Public preview:** `mvp-preview-ancient-v2` unchanged  
**Production M2 apply:** not performed

## Purpose

M2 was not allowed to pass because its component tasks were individually green. This gate attacked the integrated result across semantics, relational integrity, complete raw geography, selected-year resolution, specialist precedence, release compatibility, complexity and user-visible truth.

The first and second attacks both found real weaknesses. Those findings were corrected before this final attack.

## Correction history

### First attack — REVISE

The first integrated attack found that valid child state could be made invalid by later parent mutation, and that chosen specialist geometry provenance could be confused with baseline Cliopatria provenance.

Corrections:

- **#135 / PR #137**
  - added deferred cross-table integrity over the post-M1 semantic package;
  - protected reverse mutation paths;
  - enforced post-M1 opt-in for target-only child structures;
  - preserved legacy compatibility.

- **#136 / PR #139**
  - separated baseline Cliopatria lineage from chosen specialist-geometry lineage;
  - tested accepted specialist precedence with a genuinely different source/version;
  - verified quarantined candidates expose no chosen specialist provenance.

### Second attack — REVISE

The second attack compared #135's open-terminus implementation against the surviving M1 temporal invariant:

`open_terminus_does_not_imply_indefinite_continuity`

#135 had made `terminus_after` and `terminus_before` half-infinite positive asserted intervals. That silently converted a date constraint into indefinite historical truth.

Correction:

- **#140 / PR #141 / D-061**
  - restored open termini as non-positive query-window constraints;
  - termini carry zero positive asserted intervals by themselves;
  - selected-year truth remains false from the terminus alone;
  - methodology and data-model documentation now state this explicitly.

## Final integrated attack

### 1. Canonical semantic definitions — SURVIVES

D-058 remains the target semantic model rather than a live-release rewrite.

The integrated prototype now preserves the required separations:

- attestation pattern vs interpretive basis;
- occurrence vs institutionalization vs prevalence vs structural significance;
- research stage vs classification outcome;
- event/process vs enduring practice/status;
- temporal query envelope vs positive applicability;
- evidence locus vs reviewed inference extent;
- post-M1 dimensions vs legacy P0–P4.

D-061 closes the only discovered M1→M2 semantic regression. No remaining M2 test is allowed to redefine methodology by implementation convenience.

### 2. Relational constraints and migration compatibility — SURVIVES / production apply PARKED

The disposable PostGIS prototype now enforces post-M1 integrity in both mutation directions through deferred cross-table validation.

Adversarial coverage includes:

- legacy → post-M1 retyping without complete dimensions;
- post-M1 → legacy downgrade with target child state;
- parent query-window narrowing that would strand asserted intervals;
- unknown or terminus modes receiving positive asserted intervals;
- positive applicability without intervals;
- interval-role/mode mismatch;
- deletion of an evidence locus required by `same_as_locus`;
- target-only child semantics attached to legacy claims;
- terminus modes with residual positive intervals.

Legacy P-level rows remain representable and unchanged.

**Park:** M2 is still under `experiments/m2/`. Turning this prototype into canonical production migrations is deliberately deferred until the Project Health Check decides the project should continue on this architecture.

### 3. Complete raw Cliopatria ingestion — SURVIVES

The exact pinned corpus remains reproducible:

- 13,765 source rows;
- 13,380 POLITY;
- 385 RELATION;
- 1,633 distinct names;
- exact asset SHA-256 and Git blob identity checked before writes;
- full raw payload retained;
- source-native years and hierarchy retained;
- exact retry becomes a no-op;
- no atlas polity/spatial identity is inferred during ingestion;
- no publish view is created.

Observed full-corpus ingestion: GitHub Actions **35871937554**.

### 4. Calendar boundary and POLITY/RELATION/composite behavior — SURVIVES

D-059 remains coherent under the complete corpus.

Atlas selected-year translation:

- 14 BCE (atlas -13) → source -14;
- 1 BCE (atlas 0) → source -1;
- 1 CE → source 1;
- source-native year zero remains preserved raw but is never directly queried as an atlas historical year.

The resolver:

- keeps RELATION outside the default polity baseline;
- suppresses components only under an active POLITY parent;
- handles nested POLITY composites recursively;
- retains RELATION membership without suppressing constituent polities;
- flags missing/multiple/ambiguous hierarchy instead of guessing;
- does not interpolate source gaps.

### 5. Selected-year global resolver — SURVIVES

The exact pinned corpus is frozen by a fail-closed acceptance gate.

Accepted observations:

| Atlas year | Source year | Baseline POLITY | RELATION layer | POLITY composites | Suppressed components | Unresolved |
| --- | ---: | ---: | ---: | ---: | ---: | ---: |
| 14 BCE (-13) | -14 | 44 | 1 | 0 | 0 | 0 |
| 1 BCE (0) | -1 | 44 | 1 | 0 | 0 | 0 |
| 1 CE | 1 | 45 | 1 | 0 | 0 | 0 |
| 369 CE | 369 | 51 | 1 | 0 | 0 | 0 |
| 1000 CE | 1000 | 107 | 1 | 6 | 25 | 0 |
| 2024 CE | 2024 | 190 | 0 | 3 | 5 | 0 |

The full gate also freezes:

- Baekje at 369 CE;
- no duplicate selected keys;
- no RELATION leakage into the default baseline;
- raw/unapproved baseline state.

The corrected provenance version passed the complete pinned corpus in GitHub Actions **35880057626**.

### 6. Specialist override precedence — SURVIVES

D-055 precedence is explicit, case-specific and bounded.

The resolver does not infer specialist precedence from:

- source family;
- geometry detail;
- vertex count;
- `accuracy_status='specialist'`;
- simple existence of a reviewed geometry.

Acceptance proves:

- accepted reviewed override wins only inside its approved interval;
- quarantined override does not win;
- unreviewed override cannot be accepted;
- ambiguous multiple accepted overrides are not silently ranked;
- baseline Cliopatria provenance and chosen specialist provenance are distinct fields.

### 7. Historical release and public-preview compatibility — SURVIVES

Current post-merge foundation CI **35882399396** passed release-channel, reconstructible-membership, full-state release-bundle, migration, security and M2 prototype gates.

Production verification at final attack:

- public channel remains `public_mvp_preview -> mvp-preview-ancient-v2`;
- `mvp-preview-ancient-v2` remains non-canonical;
- `0.6.1-db-migration-candidate` remains `draft`, `canonical=false`, schema head 0029;
- no M2 experiment has been applied to production;
- live availability monitor **35882399413** passed.

Canonical historical release v0.6.1 is therefore still reconstructible and untouched.

### 8. Simpler baseline / architecture complexity — SURVIVES

M2 did not add a new service, datastore, frontend state engine or background worker.

It reused:

- PostgreSQL/PostGIS;
- existing SOURCE → SOURCE_VERSION → SOURCE_ASSET → INGEST_RUN → RAW_RECORD lineage;
- existing CLAIM architecture;
- disposable SQL prototypes;
- existing CI and Docker Compose infrastructure.

The added complexity corresponds directly to adversarially demonstrated distinctions: temporal applicability, cross-table integrity, source hierarchy, identity separation and provenance. No equally simple single-field/P0–P4 or raw-source-map baseline survives the historical-truth requirements already established in M1/M2.

**Park:** productionizing all experimental tables/functions before the Project Health Check would create commitment without additional evidence.

### 9. Map / user-truth implications — SURVIVES with publication boundary

The prototype cannot currently become public map truth by accident through the reviewed path:

- raw Cliopatria rows do not carry atlas spatial identity;
- entity matching is explicit/reviewed;
- raw baseline is labelled `raw_unapproved_global_baseline`;
- RELATION has a separate optional layer;
- unresolved hierarchy is explicit;
- specialist precedence requires an explicit accepted record;
- existing publish views do not reference M2 raw/resolver structures;
- production/public pointers remain unchanged.

**Park:** broad source-row → atlas-identity resolution and actual publication of the global baseline remain future reviewed work. Their absence is a publication boundary, not evidence absence.

## Final disposition

| Attack surface | Disposition |
| --- | --- |
| Canonical semantics | **SURVIVES** |
| Relational integrity / legacy compatibility | **SURVIVES** |
| Complete raw Cliopatria ingestion | **SURVIVES** |
| Calendar / POLITY / RELATION / composite rules | **SURVIVES** |
| Selected-year resolver | **SURVIVES** |
| Specialist precedence + provenance | **SURVIVES** |
| v0.6.1 / release / preview compatibility | **SURVIVES** |
| Architecture vs simpler baseline | **SURVIVES** |
| Map/user-truth boundary | **SURVIVES** |
| Production migration | **PARK** pending #123 |
| Bulk atlas identity resolution / publication | **PARK** pending later reviewed runway |

There are no remaining **REVISE** or **REJECT** findings inside M2.

## Gate result

**#122 passes after two revise/correct/re-attack cycles.**

This result does **not** authorize bulk research, production migration, public geography promotion or a new canonical release.

The next project action is **#123 — M2 Project Health Check and reconciliation**, which must explicitly choose **continue / redirect / stop** before any new gate or broad execution runway is created.
