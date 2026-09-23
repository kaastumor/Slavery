# H2 Value-Discrimination Pilot — Revised Protocol After Setup Adversary

**Issue:** #146  
**Base:** `00_PROTOCOL_PREREGISTERED.md`  
**Adversarial result:** REVISE — see `01_SETUP_ADVERSARY.md`  
**State:** cleared for historical execution

## Experiment question

Given the same evidence package, does the Atlas representation provide a practical advantage over a competent ordinary research artifact, and does a minimal visual/query layer provide additional value over the Atlas corpus alone?

This evaluates **artifact affordances and error behavior**, not independent model intelligence or raw fact-discovery speed.

## Cases

### Q1 — negative control: Mexica category problem, c. 1400–1521

What can a responsible synthesis say about `tlacotin`/enslaved or dependent statuses in Mexica/Aztec central Mexico, and which aspects should remain category-qualified rather than flattened into a modern slavery label?

Expected pressure:
- specialist terminology and interpretation dominate;
- spatial visualization should add little;
- a narrative may beat a structured corpus on economy;
- Atlas only earns value if provenance/qualification becomes materially more recoverable without over-formalizing uncertainty.

### Q2 — British India, 1843: law vs practice

What can a selected-year historical view defensibly say around Act V of 1843 when legal enforceability/status changed but social/economic dependency and coerced labour did not necessarily vanish on that date?

Expected pressure:
- abolition/law must not create a false practice discontinuity;
- jurisdiction and subregional variation matter;
- legal, observed-practice and later interpretive evidence must stay distinct.

### Q3 — Genoese Black Sea slave-trade network, c. 1260–1500

What does Genoese participation in the Black Sea slave trade establish about Caffa/other trade nodes, network participation, and territorial practice in Genoa itself—and what does it not establish?

Expected pressure:
- network participation must not recolor territorial practice;
- evidence locus vs inference extent matters;
- historical place/jurisdiction and route context may give C its strongest chance to add value.

## Minimum evidence package per case

Before comparing arms, freeze:
- at least one specialist scholarly synthesis/interpretive source;
- at least one independent corroborating scholarly source **or** bounded primary/source-native item where feasible;
- an explicit search for contrary/limiting evidence or historiographical qualification;
- exact URLs/identifiers, source roles and locators where available.

If that minimum cannot be met from accessible evidence, mark the case insufficient rather than padding it with weak sources.

## Arm A — strongest boring baseline

A competent researcher may use:
- specialist literature and source-native material;
- ordinary notes, spreadsheet/table or citation manager;
- simple timeline;
- QGIS/static map or nodegoat-like organization when it genuinely helps;
- ordinary search and a strong general-purpose model.

Do not force A to be text-only or manually inconvenient.

Deliverable: concise synthesis + ordinary source table + any simple conventional visual genuinely warranted.

## Arm B — Atlas corpus/method

Translate **only the frozen evidence packet** into:
- bounded claims;
- source/version entries;
- evidence direction;
- evidence class;
- temporal scope and precision;
- spatial evidence locus and inference extent;
- law / practice / external participation separation;
- uncertainty/abstention;
- post-M1 independent dimensions where supported;
- no new P0–P4.

Deliverable: human-readable structured case file. It remains experimental and non-canonical.

## Arm C — smallest thin query/visual artifact

Consume only Arm B.

Default: one static self-contained HTML experiment view for all three cases, with no package/dependency/service addition. It may expose:
- case selector;
- time/layer distinction;
- evidence-locus / inference-extent display;
- claim/source drill-down;
- a minimal map only where location is analytically relevant.

Do not modify the production web app.

If a case gains nothing from mapping, show that honestly rather than manufacturing a map.

## Fixed probes

For every arm/case classify each probe as:

- **direct** — answer/boundary is explicitly visible;
- **traceable** — recoverable through an explicit source/note link without reconstructive guesswork;
- **ambiguous/omitted** — possible only by inference or missing;
- **misleading** — artifact encourages a materially incorrect inference.

Critical probes:
1. strongest defensible proposition;
2. strongest proposition that must remain unasserted;
3. evidence date/range vs positive applicability;
4. direct evidence locus vs permissible inference extent;
5. law vs observed practice vs external participation;
6. decisive source recoverability;
7. contrary/qualifying evidence visibility;
8. cross-case comparison without equivalence;
9. whether visual/query interaction prevents a concrete temporal/spatial inference error.

## Material-advantage rule

No aggregate score.

A B-over-A or C-over-B advantage is **material** only if:
- at least **two critical probe states improve** in a case;
- the improvement is not merely extra prose/fields;
- no new critical probe becomes misleading.

To support a project-level advantage, the same arm transition must be material in at least **two independent cases**.

Q1 is deliberately allowed—and expected—to return parity/no-value for C.

## Overhead

Do not report wall-clock performance.

Record observable overhead:
- files/artifacts required;
- bespoke code required;
- number of claim/note/source-link objects;
- manual cross-links;
- concepts a maintainer must understand.

## Interpretation bounds

Three cases cannot validate global usefulness.

Possible outcomes:
- A ≈ B ≈ C → stop Atlas expansion;
- B > A, C ≈ B → methodology/corpus identity;
- B > A and C > B on at least two cases → thin atlas hypothesis survives one bounded gate;
- mixed results → simplify toward the smallest artifact that owns the demonstrated gain.

No result authorizes a full platform or infrastructure horizon automatically.
