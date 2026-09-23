# M2 complete Cliopatria selected-year resolver

**Gate:** #116  
**Task:** #121  
**Status:** implementation candidate validated in disposable PostGIS  
**Canonical release:** v0.6.1 unchanged  
**Public preview:** unchanged  
**Full-corpus validation run:** GitHub Actions 35877196416

## Question

Can the exact pinned 13,765-feature Cliopatria corpus produce a deterministic selected-year global baseline without flattening source hierarchy, leaking RELATION rows into the default polity layer, inventing atlas identities, or bypassing D-055 specialist precedence?

## Resolver boundary

The resolver remains under `experiments/m2/`. It is not a production migration and does not create a publish view.

The default selected-year baseline:

- translates atlas astronomical years to the pinned Cliopatria source calendar only at query time;
- selects active `POLITY` rows;
- recursively suppresses active POLITY components into a single active POLITY parent where that parent relation is unambiguous;
- does **not** suppress a polity merely because it belongs to a `RELATION`;
- keeps RELATION rows in a separate optional relation layer;
- returns exact source-row identity and pinned source/version/asset provenance;
- marks the output `raw_unapproved_global_baseline`;
- does not infer `atlas.spatial_entity` identity from a name.

Missing, conflicting, ambiguous, cyclic or multiple POLITY-parent references remain explicit unresolved states rather than choosing a parent heuristically.

## Calendar contract

D-059 is implemented as:

- atlas year -13 (14 BCE) -> Cliopatria source year -14;
- atlas year 0 (1 BCE) -> Cliopatria source year -1;
- atlas year 1 (1 CE) -> Cliopatria source year 1;
- all positive CE years remain unchanged.

Cliopatria source year zero is preserved in raw data but is never queried as an atlas selected year.

The real-corpus BCE/CE boundary check resolved the same named polities on distinct source rows either side of the seam. Examples include Roman Empire, Parthian Empire, Judea, Yuezhi, Indo-Greeks and Indo-Scythians.

## Complete-corpus observations

The exact pinned corpus was loaded and reconciled first, then queried through the resolver.

| Atlas selected year | Cliopatria source year | Baseline POLITY results | RELATION rows in optional layer | Composite results | Suppressed component rows | Unresolved hierarchy |
| --- | ---: | ---: | ---: | ---: | ---: | ---: |
| 14 BCE (-13) | -14 | 44 | 1 | 0 | 0 | 0 |
| 1 BCE (0) | -1 | 44 | 1 | 0 | 0 | 0 |
| 1 CE (1) | 1 | 45 | 1 | 0 | 0 | 0 |
| 369 CE | 369 | 51 | 1 | 0 | 0 | 0 |
| 1000 CE | 1000 | 107 | 1 | 6 | 25 | 0 |
| 2024 CE | 2024 | 190 | 0 | 3 | 5 | 0 |

These are observations for the exact pinned asset and current resolver prototype, not claims that the counts are historically exhaustive or editorially approved.

For 369 CE, the source contains one active Baekje POLITY row (raw ordinal 1478, source interval 347–391) and it resolves as a top polity. The default baseline contains no RELATION row, no duplicate selected key and no state other than `raw_unapproved_global_baseline`.

At 2024, representative returned rows included Afghanistan, Antigua and Barbuda, Arab Republic of Egypt, Argentine Republic, Barbados, Belize, Bolivia, Bosnia and Herzegovina, Burkina Faso, Canada, Central African Republic and Commonwealth of Australia. Their presence demonstrates source coverage only; it is not publication approval.

## D-055 precedence

Specialist precedence is intentionally **not** inferred from:

- `accuracy_status='specialist'`;
- source family;
- vertex count;
- existence of a reviewed geometry;
- newer date;
- apparent visual detail.

The prototype requires an explicit case-specific record tying an accepted geometry to an atlas spatial entity and bounded interval.

Synthetic adversarial acceptance proves that:

- an explicitly accepted reviewed specialist geometry outranks the raw Cliopatria baseline only inside its accepted interval;
- the same candidate does not override outside that interval;
- a quarantined specialist candidate does not override;
- an unreviewed specialist geometry cannot be registered as an accepted override;
- multiple accepted overrides remain an ambiguity rather than being ranked automatically.

No production geometry record or current public serving path is changed by this prototype.

## Synthetic hierarchy adversary

The cheap CI fixture covers cases that are hard to guarantee at arbitrary real selected years:

- direct POLITY -> POLITY component suppression;
- nested POLITY composites;
- RELATION membership without suppression;
- multiple active POLITY parents;
- missing parent reference;
- BCE/CE source-year translation;
- accepted specialist precedence;
- quarantined specialist fallback.

The synthetic fixture is dataset-scoped, so it also passes when the complete real corpus is loaded in the same disposable database.

## Reproduction

Cheap regression gate:

```bash
./scripts/db-test-cliopatria-resolver.sh
```

Complete pinned-corpus validation:

```bash
./scripts/db-test-cliopatria-resolver-full.sh
```

The full harness first executes the #119 exact ingestion/reconciliation and exact retry/no-op, then applies the resolver and emits the selected-year diagnostic.

## Integrated-gate correction (#136)

The first #122 integrated attack found that the resolver result could choose an accepted specialist geometry while still exposing generically named provenance columns that described the Cliopatria baseline. The underlying lineage was still reachable through `chosen_geometry_id`, but the result shape made accidental source misattribution too easy.

The corrected prototype makes the two lineages explicit:

- `baseline_source_version_id`
- `baseline_source_asset_id`
- `baseline_upstream_commit`
- `baseline_asset_sha256`
- `chosen_geometry_source_version_id`
- `chosen_geometry_source_native_id`

The specialist acceptance fixture now uses a source/version distinct from the synthetic Cliopatria baseline and requires both lineages to be returned correctly. A quarantined candidate must expose no chosen-specialist provenance.

The complete pinned-corpus harness also changed from an observational diagnostic to a fail-closed acceptance. The six selected-year count/composite observations in the table above, the Baekje 369 example, duplicate-key exclusion, RELATION exclusion from the default baseline, and raw/unapproved state are now assertions when `db-test-cliopatria-resolver-full.sh` is run against the exact pinned asset.

This correction remains disposable M2 infrastructure. It does not approve any specialist source, publish any raw baseline geometry, or change production.

## Gate meaning

Passing #121 means the project has a reproducible **raw selected-year global baseline resolver** with explicit source-calendar, hierarchy and D-055 precedence behavior.

It does **not** mean:

- every Cliopatria polygon is historically accepted;
- every source row has been matched to an atlas spatial identity;
- RELATION rows are public map features;
- specialist replacements have been automatically chosen;
- raw source availability authorizes map publication;
- the canonical release or public preview has changed.

Those remain integrated-gate, review, and release decisions.
