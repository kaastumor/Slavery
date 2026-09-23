# COV-001 — Setup Adversary

**Issue:** #148  
**Input:** `00_PROTOCOL_PREREGISTERED.md` + `01_BASELINE_LANDSCAPE.md` + deterministic sampler  
**Historical slavery research started:** no  
**Disposition:** **REVISE**

The coverage-value question survives, but the first setup would bias the result.

## Attacks and dispositions

| Attack | Disposition | Finding / repair |
| --- | --- | --- |
| A Cliopatria polity sample is not a neutral sample of all known human societies | **revise** | Cliopatria is useful as an independent historical-geography frame, but polity-only sampling excludes stateless/small-scale societies and inherits its coverage. Keep the 24 polity-year strata as the primary frame and add four predeclared non-polity challenge contexts. Limit conclusions accordingly. |
| The mini-index could quietly become “Atlas v2” | **revise** | The experiment artifact must be a plain CSV/JSON + human-readable Markdown profile. No database migration, API, map UI or new service. If the value requires the old platform, it has not been demonstrated by this experiment. |
| Coverage queries are index-shaped, so the index can win tautologically | **revise** | Keep the six fixed user-facing queries, but evaluate against a strong **plain ordinary matrix** baseline as well as external narrative resources. Extra fields do not count unless they change correctness/recoverability. |
| Research-from-scratch versus preassembled index trivially favors preassembly | **revise** | Lookup reduction is recorded but cannot establish value alone. A material gain requires information-state improvements: explicit coverage state, provenance, abstention, layer separation or correct aggregation. |
| Same-model/order contamination can make the comparison circular | **revise** | Baseline-query and index-query evaluations should be done in fresh isolated runs/chats where practical. The baseline evaluator receives sample IDs + baseline resources but not the frozen mini-index; the index evaluator receives the frozen mini-index. If isolation is not available, report the limitation and do not claim human-performance evidence. |
| Global handbooks are regional/essay-based; “direct coverage” needs a rule | **revise** | Define direct = sampled target/society and relevant period are substantively treated; adjacent = region/period context is useful but target is not treated directly; none = no usable target-level context. |
| English/digital accessibility may become a fake global-knowledge gap | **revise** | Every cell records language/access limitations. `insufficient_access` is distinct from researched-inconclusive. A missing English/open source never becomes historical absence or proof of historiographical absence. |
| Deterministic hash can select obscure targets and turn the test into an access lottery | **survives with constraint** | That is partly the point of a coverage index. Preserve obscure/inconclusive results, but record whether the problem is scholarship absence, access, language, source survival or sampling-frame ambiguity. |
| Four anchor years are too sparse to represent all history | **survives with scope limit** | This is a value pilot, not a coverage release. A positive result says only that systematic coverage indexing shows value on this sample. |
| Bounding-box midpoint is crude and can mis-bin large/transcontinental polities | **survives with constraint** | It is used only to distribute the sample. Preserve the source row and exact geometry; sector assignment must never become a historical-geography claim. |
| A positive result could still be driven by our own ontology | **revise** | The mini-index uses only the minimum fields required by the fixed queries and project invariants. Do not reproduce the full post-M1 schema. |
| A global index may hide conceptual disagreement under one “slavery” field | **revise** | Every row must preserve terminology/classification qualification and strongest proposition that must not be asserted. No binary slavery-present field. |
| A positive result could be overinterpreted as permission for bulk research | **survives with hard boundary** | Even a positive pilot authorizes at most one further bounded corpus-scale test. It cannot reactivate H3, production migration, frontend or infrastructure work. |

## Added non-polity / frame-bias challenge contexts

These are selected **before research** because they deliberately stress the polity sampling frame, not because of known slavery evidence.

They are broad region-period research contexts, not historical-polity claims:

1. **NP-01 — Central Australian interior, c. 1800 CE**
2. **NP-02 — New Guinea Highlands, c. 1800 CE**
3. **NP-03 — North American Great Plains, c. 1300 CE**
4. **NP-04 — Upper Amazon / western Amazonia, c. 1300 CE**

Purpose:
- test whether the coverage method can represent societies/contexts not naturally captured as one Cliopatria polity;
- expose archaeology/ethnohistory/oral-history/source-access limitations;
- prevent “global” from silently meaning “places with state polygons.”

These four do not count toward the deterministic 18/24 Cliopatria viability threshold. They are separate challenge cases.

## Negative-control interpretation

The negative controls are mandatory:
- deep specialist explanation should remain better in specialist narrative;
- bounded voyage quantification should remain better in SlaveVoyages.

If the mini-index seems generally superior, that is evidence of an unfair baseline or overclaim.

## Gate result

**REVISE → proceed only under the revised protocol.**

No slavery/coercion research may begin until:
- the revised protocol is committed;
- the deterministic sample is generated/frozen;
- the four non-polity challenge contexts remain unchanged.
