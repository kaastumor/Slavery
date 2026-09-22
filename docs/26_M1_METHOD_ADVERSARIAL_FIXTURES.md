# M1 adversarial methodology fixtures

**Gate:** #100  
**Atomic task:** #101  
**Baseline attacked:** pre-M1 methodology/data model, schema draft-0.10

This is a falsification fixture, not a replacement ontology. It records where the current model survives and where a later task needs a discriminating redesign.

## Result

The current model **survives two important attacks**:

- claim-specific evidence directions can preserve supporting, challenging and qualifying material while still allowing a reviewed working synthesis (Mauryan case);
- claims can remain useful with unresolved geometry rather than inventing a polity polygon (Late Classic Maya case).

Six pressures require revision experiments:

| ID | Pressure | Disposition | Why this is not merely UI wording |
| --- | --- | --- | --- |
| M1-A01 | P0–P4 combines evidentiary configuration with historical structure | **revise** | It affects ordering, filtering and map encodings, not only labels. |
| M1-A02 | coverage state combines research stage with epistemic outcome | **revise** | “review completed” and “disputed” can both be true. |
| M1-A03 | dating window can become continuous selected-year validity | **revise** | It changes the truth condition of time queries. |
| M1-A04 | evidence locus and inference extent are not first-class separate concepts | **revise** | It determines which geometry may legitimately receive a claim/fill. |
| M1-A05 | bounded capture/enslavement event is stored through territorial-practice semantics | **revise** | Event occurrence and continuing social practice are different predicates. |
| M1-A06 | one practice-type code cannot carry simultaneous status/function/transmission/property facets | **revise** | Notes preserve prose but not queryable analytical dimensions. |

## Real-domain witnesses

### Silla Village Register

`data/research/ancient_expansion_02/04_silla_village_register_slavery.json` already states that 695–819 CE encodes competing document dates and **must not be read as a 125-year continuous observation**. This makes the temporal attack concrete. The same case correctly refuses to substitute a whole-Silla polygon for four uncertain village communities, but the rationale remains editorial/free-text rather than a separately queryable evidence-locus/inference-extent relation.

### Baekje 369

`data/research/ancient_expansion_02/03_baekje_369_war_captive_enslavement.json` is deliberately a one-year P1 claim. That restraint is good. The model pressure remains because a capture/distribution event reaches the same territorial-practice subtype used for enduring institutions; a query cannot distinguish “an enslavement event occurred here” from “this describes territorial practice” without reading notes.

### Hittite central Anatolia

`data/research/ancient_expansion_01/03_hittite_slavery.json` synthesizes status, legal pricing/property rules, herding function and status flexibility into one headline `slavery_enslavement` code. The headline is useful but insufficient for the atlas's comparative ambitions if these dimensions need to be queried independently.

### Mauryan Empire

`data/research/ancient_expansion_02/02_mauryan_slavery_disputed.json` is a successful counterexample to over-refactoring. The claim keeps supports/challenges/qualifies evidence directions and reaches a bounded reviewed synthesis. The adversary therefore marks this design **survives**; disagreement does not require a new parallel claim architecture by default.

### Late Classic Maya

`data/research/cases/global_04_late_classic_maya_captive_dependency.json` deliberately records recurrent captive-taking rather than blanket slavery and leaves geometry unresolved across multiple polities/sites. The geometry-restraint mechanism **survives**. The fact that `captive_taking_incorporation` still lives in the territorial-practice vocabulary is separate pressure captured by M1-A05/A06.

## What #101 does not decide

- It does not replace P0–P4.
- It does not declare a final faceted ontology.
- It does not change SQL.
- It does not reinterpret or republish any historical case.
- It does not change v0.6.1 or the public preview.

#102 and #103 now have specific failures to discriminate against. They should retain current semantics wherever a simpler model genuinely survives.
