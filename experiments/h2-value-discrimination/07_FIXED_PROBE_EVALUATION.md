# H2 Fixed-Probe Evaluation

**Issue:** #146  
**Protocol owner:** `02_PROTOCOL_REVISED.md`  
**Evidence:** `03_EVIDENCE_PACKETS.md`  
**Arms:** A=`04_ARM_A_BASELINE.md`, B=`05_ARM_B_CORPUS.md`, C=`06_ARM_C_THIN_VIEW.html`

States:
- **direct** — explicitly visible;
- **traceable** — recoverable through an explicit note/source link without reconstructive guesswork;
- **ambiguous/omitted** — missing or requires interpretive reconstruction;
- **misleading** — artifact encourages a materially incorrect inference.

The evaluation asks whether the *artifact* preserves/reveals the relevant boundary. It does not score historical sophistication or aesthetics.

## Q1 — Mexica / Nahua `tlacotli` (negative control)

| Probe | A — boring baseline | B — corpus/method | C — thin view | Observation |
| --- | --- | --- | --- | --- |
| 1 strongest defensible proposition | direct | direct | direct | all three state severe dependent/unfree labor with qualification |
| 2 strongest proposition that must remain unasserted | direct | direct | direct | all warn against one universal chattel bundle/prevalence |
| 3 evidence date/range vs positive applicability | traceable | **direct** | ambiguous/omitted | B explicitly separates colonial source date from retrospective/pre-Hispanic referent; C drops that detail |
| 4 evidence locus vs inference extent | traceable | **direct** | ambiguous/omitted | B explicitly bounds category-level inference; C mostly presents facets without locus/extent |
| 5 law/practice/participation separation | direct/not central | direct/not central | direct/not central | not the discriminating issue here |
| 6 decisive source recoverability | traceable | **direct** | ambiguous/omitted | B names sources per bounded claim and evidence direction; C only lists source names at case level |
| 7 contrary/qualifying evidence visibility | direct | direct | traceable | A and B visibly preserve Salazar/von Mentz tension; C compresses it |
| 8 cross-case comparison without equivalence | traceable | **direct** | direct | B/C expose a common failure-mode query; A can do it but only in synthesis |
| 9 visual/query prevents temporal/spatial inference error | ambiguous/not useful | ambiguous/not useful | ambiguous/not useful | negative control behaves as intended: no useful map interaction |

**A → B:** material advantage. At least probes 3, 4 and 6 improve from traceable to direct, with no new misleading result.  
**B → C:** no advantage; C loses important provenance and scope detail.  

## Q2 — East India Company territories around 1843

| Probe | A | B | C | Observation |
| --- | --- | --- | --- | --- |
| 1 strongest defensible proposition | direct | direct | direct | legal breakpoint is explicit everywhere |
| 2 strongest proposition that must remain unasserted | direct | direct | direct | all reject a universal practice-stop inference |
| 3 evidence date/range vs positive applicability | direct | direct | direct | A already keeps legal date separate from practice chronology |
| 4 evidence locus vs inference extent | direct | direct | direct | A already distinguishes Company territories/Bengal/modern India |
| 5 law vs practice vs participation | direct | direct | direct | A's two-lane recommendation already makes this explicit |
| 6 decisive source recoverability | traceable | **direct** | ambiguous/omitted | B is stronger claim-by-claim; C compresses sources to a case list |
| 7 contrary/qualifying evidence visibility | direct | direct | traceable | C summarizes the qualification but loses source-level direction |
| 8 cross-case comparison without equivalence | traceable | **direct** | direct | B/C provide a common structural comparison |
| 9 visual/query prevents concrete inference error | ambiguous/omitted | ambiguous/omitted | **direct** | year selector demonstrates that the legal lane changes while practice does not auto-switch |

**A → B:** **not material under the preregistered rule**. Probes 6 and 8 improve in form, but probe 8 is primarily organization rather than a demonstrated correctness gain; the competent baseline already states the same distinction. Only source recoverability is an unambiguous practical improvement.  
**B → C:** **not material**. Probe 9 improves, but source recoverability and qualification detail regress. C is useful pedagogically, not a net practical advantage under the rule.

## Q3 — Genoese Black Sea network

| Probe | A | B | C | Observation |
| --- | --- | --- | --- | --- |
| 1 strongest defensible proposition | direct | direct | direct | participation and local practice both explicit |
| 2 strongest proposition that must remain unasserted | direct | direct | direct | no route-volume → territorial-prevalence inference |
| 3 evidence date/range vs positive applicability | direct | direct | direct | all preserve 1475 as the Caffa control boundary |
| 4 evidence locus vs inference extent | direct | direct | direct | A already has proposition/evidence/scope table |
| 5 law/practice/participation separation | direct | direct | direct | A already distinguishes network from local-practice evidence |
| 6 decisive source recoverability | traceable | **direct** | ambiguous/omitted | B claim-source mapping is stronger; C has only case-level source names |
| 7 contrary/qualifying evidence visibility | direct | direct | traceable | C retains main warning but compresses evidentiary nuance |
| 8 cross-case comparison without equivalence | traceable | **direct** | direct | B/C make structural comparison explicit |
| 9 visual/query prevents concrete inference error | ambiguous/omitted | ambiguous/omitted | **direct** | 1395/1475/1480 interaction makes the control-boundary error immediately visible and keeps route separate from local practice |

**A → B:** **not material under the preregistered rule**. Claim-specific provenance improves, but the ordinary proposition/scope table already prevents the central network/territory error.  
**B → C:** **not material**. The visual makes the 1475/node distinction more salient, but provenance/qualification becomes less recoverable.

---

## Cross-case threshold result

### B over A

Material cases:
- Q1: **yes**
- Q2: no
- Q3: no

Required for project-level advantage: at least two independent cases.

**Result: threshold not met.**

The strongest boring baseline reaches practical parity with the Atlas corpus/method on the two cases where the central failure mode can already be represented cleanly in an ordinary timeline/table. B provides a real provenance/scope advantage in Q1, but that advantage is not repeatable across two cases under this test.

### C over B

Material cases:
- Q1: no
- Q2: no
- Q3: no

**Result: threshold not met.**

C improves temporal/spatial *salience* in Q2 and Q3, but each time it also compresses claim-level provenance/qualification. Under the preregistered rule, a visual gain that trades away evidentiary recovery is not a material net advantage.

## Observable overhead

| Arm | Persistent artifacts / structures | Bespoke code | Main maintenance burden |
| --- | --- | --- | --- |
| A | 1 synthesis file + ordinary source notes | none | historian must maintain careful prose/table discipline |
| B | 10 bounded claim objects represented in one file; repeated claim-source directions and explicit scope fields | none in this pilot | more concepts/links to maintain; advantage mainly auditability and later machine-queryability |
| C | 1 self-contained ~10 KB HTML file derived from B | small bespoke HTML/JS | presentation must stay synchronized with B; source drill-down was already lost in the minimal view |

B's overhead is modest for three cases but grows with claim count. C adds another derived artifact while not meeting the value threshold.

## Preliminary disposition

**The pre-registered project-value threshold is not met.**

This result should trigger the protocol's stop condition unless a result adversary identifies a methodological defect strong enough to invalidate the comparison.

Do not reinterpret a one-case B advantage or the Q2/Q3 visual salience as a project-level win after seeing the result.
