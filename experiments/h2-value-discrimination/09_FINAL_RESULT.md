# H2 Final Result — Value-Discrimination Pilot

**Issue:** #146  
**Date:** 2026-09-23  
**Protocol:** `02_PROTOCOL_REVISED.md`  
**Setup adversary:** REVISE → cleared  
**Preliminary evaluation:** `07_FIXED_PROBE_EVALUATION.md`  
**Result adversary:** REVISE Arm C → provenance repair completed  
**Final disposition:** **STOP ACTIVE ATLAS EXPANSION; PRESERVE METHOD/CORPUS/AUDIT ARTIFACTS**

This is a project-horizon disposition, not a claim that every possible future use of structured historical data or maps lacks value.

## Re-evaluation after Arm C repair

The result adversary correctly identified that the first thin view had needlessly compressed provenance. Arm C was repaired to include claim-level evidence details and direct source links without adding a framework, package, service, database change or production deployment.

After repair:

### Q1 — Mexica category negative control

- **A → B:** still **material**.
  - B makes source-date vs historical applicability, evidence-locus vs inference-extent, and claim-specific source direction more explicit/recoverable than A.
- **B → C:** **not material**.
  - C now preserves provenance better, but the case remains category/terminology-heavy and gains no useful temporal/spatial interaction.
  - B remains the better artifact for the fine-grained category boundary.

### Q2 — India 1843 law/practice

- **A → B:** **not material**.
  - B improves claim-specific provenance organization, but A already directly separates the legal breakpoint, historical jurisdiction and non-identical practice chronology.
- **B → C:** **not material**.
  - C now matches B on practical source recovery well enough for this pilot and makes the legal/practice lane distinction more salient through selected-year interaction.
  - That is one clear probe improvement (visual/query prevention of the 1843 practice-stop error), not the two required by the preregistered rule.

### Q3 — Genoese Black Sea network

- **A → B:** **not material**.
  - B improves claim-specific source mapping, but A's ordinary proposition/evidence/scope table already blocks the central route-volume → territorial-prevalence inference.
- **B → C:** **not material**.
  - C now preserves direct evidence links and makes the 1475 Caffa control boundary plus route/local-practice separation immediately visible.
  - Again, this is one clear probe improvement, not two.

## Threshold outcome

### Corpus/method over strongest boring baseline

Material in:
- Q1: yes
- Q2: no
- Q3: no

Pre-registered requirement: at least two independent cases.

**Threshold: FAIL.**

### Thin view over corpus/method

Material in:
- Q1: no
- Q2: no
- Q3: no

Pre-registered requirement: at least two independent cases.

**Threshold: FAIL.**

## What the pilot actually learned

### 1. The methodology contains durable value

The negative-control Q1 shows that explicit claim/source direction, temporal source-vs-applicability separation and evidence-locus/inference-extent fields can make a difficult category problem more auditable.

The project's M1/M2 methodological work was therefore not empty process. Preserve it.

### 2. A competent ordinary artifact can carry most of that discipline

In Q2 and Q3, careful narrative + ordinary tables already preserve the decisive distinctions:
- legal change is not a practice stop;
- network participation is not territorial prevalence;
- historical jurisdiction/control boundaries can be written explicitly.

The Atlas corpus structure makes these boundaries more formal and machine-addressable, but in this pilot that did not produce two practical probe improvements over the strong baseline.

### 3. Thin interaction has bounded pedagogical value

The repaired thin view makes two errors easier to see:
- the 1843 legal lane can change without the practice lane auto-switching;
- Caffa can cease being Genoese in 1475 even when a study's analytical period continues to 1500.

That is real, but it is not enough to justify another application horizon.

### 4. The strongest current project contribution is smaller than an atlas platform

What survives best is:
- the domain methodology;
- adversarial fixtures and failure cases;
- claim/source/version/provenance conventions;
- selected exemplary evidence packets/corpus material;
- reproducible release/audit history;
- historical geography/query logic as preserved research tooling where already built.

What has **not** earned further investment is the active expansion of:
- a bespoke public atlas product;
- richer interactive UI;
- larger serving/operations infrastructure;
- bulk evidence collection in order to feed that product;
- production migration of experimental M2 structures.

## Decision against D-062 kill rule

D-062 / HC-003 said:

- if corpus/method adds value but thin atlas does not, shrink to methodology/corpus;
- if neither materially outperforms the strongest baseline, stop further Atlas expansion and preserve methodology/corpus/audit artifacts.

Under the preregistered project-level threshold, B does **not** materially outperform A in two cases, and C does not materially outperform B in any case.

Therefore the applicable disposition is:

# **STOP ACTIVE ATLAS EXPANSION**

Preserve the useful methodology/corpus/audit work as the project result.

This does **not** mean delete the repository, discard v0.6.1, or undo M1/M2. It means the project should not manufacture H3/H4 work to escape a negative value experiment.

## Reopen conditions

A future Atlas-development horizon may be considered only if new external evidence changes the baseline, for example:
- a real researcher/user presents a repeated task that ordinary notes/table/GIS cannot handle without losing provenance or uncertainty;
- a materially larger real corpus exposes a concrete failure of the simpler workflow that cannot be solved by a small script/table convention;
- an external consumer requires machine-addressable cross-case queries that the preserved corpus method demonstrably answers better;
- a new independent evaluation shows repeatable practical gain on the D-062 criteria.

Such a trigger authorizes evaluation, not automatic platform expansion.

## Canonical-data effect

None.

- v0.6.1 remains the canonical historical data release.
- The H2 cases remain experiment evidence only.
- No M2 production migration is authorized.
- No public release/preview is promoted.
