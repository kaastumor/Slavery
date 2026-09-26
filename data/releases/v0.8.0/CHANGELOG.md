# v0.8.0 changelog

Compared with canonical predecessor `v0.7.0`:

- Extends canonical v0.7.0 by exact predecessor union rather than reviewed-row discovery.
- Adds 35 complete reviewed territorial-practice claim states, bringing canonical membership to 75 total claims and 50 spatial entities.
- Adds 46 exact reviewed and resolved historical geometry records while preserving unresolved geometry as explicit non-mapped state.
- Includes reviewed disputed and date-disputed interpretations explicitly rather than silently normalizing disagreement away.
- Preserves post-M1 practice_level as NULL; legacy P-levels remain historical compatibility metadata only on predecessor/direct-recovery rows.
- Expands exact source-version closure from 211 to 294 while preserving claim-specific provenance and source-family dependence.
- Retains the 12 unreconciled legacy research_prototype_reviewed rows outside this release until replayed under the current method.
- Does not move the public UI/API release channel; serving cutover is a separate step.

No predecessor bytes are modified.
