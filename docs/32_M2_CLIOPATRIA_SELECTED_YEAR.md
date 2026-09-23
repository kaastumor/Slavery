# M2 complete Cliopatria selected-year resolver

**Gate:** #116  
**Task:** #121  
**Status:** experimental resolver validated against the exact complete pinned corpus; no production/public promotion  
**Canonical release:** v0.6.1 unchanged  
**Public preview:** `mvp-preview-ancient-v2` unchanged

## Result

The selected-year resolver now survives both adversarial synthetic fixtures and one complete 13,765-feature Cliopatria run.

The resolver implements D-059 directly:

- atlas years <= 0 translate to Cliopatria source year `atlas_year - 1`;
- positive CE years are unchanged;
- source integer zero is preserved in raw data but is never queried as an atlas historical year;
- only active `POLITY` rows enter the default baseline;
- active POLITY parents suppress their components recursively;
- participation in a `RELATION` composite does not suppress the constituent polity;
- RELATION rows are available only through a separate optional relation layer;
- missing, ambiguous or multiple POLITY parents remain explicit unresolved hierarchy rather than being guessed.

D-055 precedence is likewise explicit. A source row does not acquire atlas identity by name, and a specialist-looking geometry does not outrank Cliopatria by itself. Precedence requires an explicit reviewed atlas-entity match plus an accepted, bounded specialist-override decision. Quarantined, rejected, out-of-interval and unreviewed candidates do not override.

## Complete-corpus observations

GitHub Actions run `35877196416` loaded and reconciled the exact pinned asset, performed the exact no-op retry, applied the resolver, passed the synthetic adversary, and emitted these deterministic probes:

| Atlas year | Source query | Baseline POLITY candidates | RELATION layer | Composite roots | Suppressed components | Unresolved hierarchy |
| ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| -13 / 14 BCE | -14 | 44 | 1 | 0 | 0 | 0 |
| 0 / 1 BCE | -1 | 44 | 1 | 0 | 0 | 0 |
| 1 / 1 CE | 1 | 45 | 1 | 0 | 0 | 0 |
| 369 | 369 | 51 | 1 | 0 | 0 | 0 |
| 1000 | 1000 | 107 | 1 | 6 | 25 | 0 |
| 2024 | 2024 | 190 | 0 | 3 | 5 | 0 |

The six known source-zero bridge sequences—Yuezhi, Parthian Empire, Indo-Greeks, Indo-Scythians, Judea and Roman Empire—resolve through source year -1 for atlas year 0 and through source year 1 for atlas year 1. Source year zero is never requested.

Baekje at 369 resolves to pinned source row ordinal 1478, source-native interval 347–391, as a top-level POLITY. No RELATION row leaks into the 369 default baseline, no duplicate selected-year candidate key is returned, and every baseline row remains explicitly marked raw/unapproved.

The machine-readable evidence is `validation/cliopatria_v0.2.0_selected_year.json`. `experiments/m2/cliopatria_selected_year_full_acceptance.sql` freezes these observations as a fail-closed complete-corpus acceptance contract.

## Boundary

This proves the complete raw corpus can produce a deterministic source-faithful **global fallback candidate set**. It does not approve 13,765 source geometries as atlas geometry, resolve every raw source identity into an atlas entity, or move any publication pointer.

Case-specific specialist geometry still outranks the baseline only after the existing D-055 acceptance process. Raw availability is infrastructure, not historical or cartographic approval.
