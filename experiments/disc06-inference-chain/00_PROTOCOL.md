# DISC-06 — inference-chain stress test

**Issue:** #240  
**Primary gate:** method / representation  
**Status:** preregistered before prototype execution  
**Base commit:** `af42df969e0baccbb44ae4f162a8758581161d0b`

## 1. Question

Does the current portable evidence packet preserve enough explicit reasoning dependency
to reconstruct:
- why a reviewed conclusion follows from its premises; and
- what conclusions should be reconsidered if a premise/source interpretation changes?

Or does a minimal explicit inference ledger materially improve review safety?

## 2. Frozen sample

No new historical research is allowed. Use only existing reviewed artifacts.

| Case | Anchor | Known correction mechanism |
| --- | --- | --- |
| Teotihuacan | 500 CE | temporal leakage |
| Shaolin | 1000 CE | target/context join |
| Inuit frame | 1800 CE | dimension + temporal/spatial leakage |
| Cahokia | 1200 CE | status + temporal leakage |
| Lazica | 500 CE | temporal + dependency + network/territorial leakage |
| Nālandā Mahāvihāra | 700 CE | target/context + dependency |

The sample is selected because the corrections already happened and span distinct
failure mechanisms. It is **exposed regression material**, not fresh/blind historical
evaluation.

## 3. Baseline

Current portable packet:
- bounded proposition;
- required abstention;
- temporal applicability / precision;
- evidence locus / inference extent;
- law/practice and network/territorial notes;
- source version / locator / direction / claim fitness;
- independence group;
- adversarial correction prose.

## 4. Experimental representation

A minimal CRMinf/FPO-inspired ledger only:

- `inference_id`
- `target_id`
- `conclusion_key`
- `premise_refs`
- `reasoning_rule`
- `result`: supports / blocks / qualifies
- `review_state`

Allowed reasoning-rule vocabulary:
- `temporal_applicability`
- `target_specificity`
- `dimension_separation`
- `inference_extent`
- `status_mapping`
- `source_dependency`

Free-text justification may remain in the case packet; the experiment does not attempt
to formalize historical reasoning exhaustively.

## 5. Comparison tasks

For every case compare baseline versus ledger:

1. identify the exact premise(s) whose correction changed the conclusion;
2. identify conclusions affected if one premise/source family changes;
3. distinguish source evidence from Atlas/project inference;
4. determine whether the ledger adds material information unavailable from the baseline;
5. record duplication and review burden.

## 6. Frozen discriminator

**SURVIVES** only if the ledger adds material reconstructibility or revision-impact
information in at least **two distinct failure mechanisms**, without requiring
infrastructure or merely duplicating existing fields/prose.

**REJECT** if the current packet reconstructs the same reasoning dependencies without
material ambiguity.

**PARK / NARROW** if useful only for one rare mechanism.

No threshold changes after constructing the ledger.

## 7. Adversarial attacks

Assume the ledger is unnecessary and attack it for:
- post-hoc encoding of known corrections;
- false formal precision;
- duplication of source direction / claim fitness / abstention;
- review burden larger than the failure it prevents;
- graph-shaped solutionism;
- encoding only the final correction rather than the reasoning dependency that made it
  necessary.

## 8. Complexity boundary

No historical/slavery subject research. No schema/ontology migration. No RDF, knowledge
graph or graph database. No API/frontend feature. No canonical/public release. No
external participant work.

EXP-08 remains paused. Qi — 500 BCE remains frozen/unstarted.

## 9. Freeze rule

Do not construct or score the experimental ledger until this protocol/sample is merged.
