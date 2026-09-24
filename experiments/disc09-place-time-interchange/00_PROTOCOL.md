# DISC-09 — historical place/time interchange benchmark

**Issue:** #253  
**Primary gate:** method / spatial-temporal interchange discovery  
**Status:** preregistered before adapter construction  
**Base commit:** `4d05c2f5ccea3719823ae0bd8fb83443dfd2fcee`

## 1. Question

Can established historical place/time interchange standards add useful generic
reconciliation/linking capability without becoming the canonical owner of Atlas target
identity, historical jurisdiction, temporal applicability or geometry?

## 2. Frozen sample

Use only existing qualified/researched target frames.

### Great Zimbabwe — 1400
- target: `R1:N:great_zimbabwe_1400`
- frame: `node_site`
- anchor: 1400
- temporal precision: anchor supported
- spatial limit: site/capital locus; no automatic state polygon
- geometry role in EXP-08: navigation/reference only; no practice polygon

### Khanate of Kokand — 1800
- target: `R1:P:1800:E:r1`
- frame: `polity`
- anchor: 1800
- temporal precision: early-state anchor supported
- spatial limit: Fergana-centered early polity; later nineteenth-century maximum extent
  must not be projected backward

### Māori communities in Aotearoa — 1700
- target: `R1:N:maori_1700`
- frame: `region_community`
- anchor: 1700
- temporal precision: broad community frame supported
- spatial limit: multi-community archipelago/region; no single polity
- identity limit: “Māori” is a retrospective umbrella over distinct iwi/hapū, not one
  1700 jurisdiction

Frozen source blobs:
- EXP-07 qualification results:
  `8dbde6731aa5b59272b7288f6887045dbf1f3a15`
- EXP-08 target rows:
  `819106bf82231d710fb8d6693a9b252ba81a2795`

No target substitution after adapter construction.

## 3. External baselines

### Linked Places Format (LPF)

Normative format reference for this experiment:
- LinkedPasts `linked-places-format` repository;
- repository README identifies **LPF v1.3** (24 June 2024);
- https://github.com/LinkedPasts/linked-places-format

Current WHG documentation is also recorded because deployed/docs version labels differ:
- upload guide references LPF v1.2.2;
- Entity API documentation says returned place features are LPF v1.1;
- WHG v4 data-model docs describe LPF as its interchange format.

This version drift is part of the benchmark. Do not silently collapse the labels into
one claimed deployed version.

LPF capabilities under test:
- persistent record identity;
- preferred + variant names;
- `fclasses` / place-type information;
- temporally scoped `when`;
- zero/multiple geometry, null geometry and geometry certainty;
- relations/links;
- source/citation/provenance.

### PeriodO

Pinned documentation:
- https://perio.do/technical-overview/
- accessed 2026-09-25.

PeriodO models **source-defined historical period definitions**, requiring:
- a period name;
- temporal bounds;
- geographic association;
- a citable source.

It preserves source expressions and structured temporal approximations separately.

Do not force Atlas target anchors, entity lifespans or research windows into PeriodO
period concepts unless they satisfy that source-defined-period contract.

## 4. Strongest current baseline

The Atlas already separates:
- target identity from geometry;
- spatial identity from historical jurisdiction;
- exact selected anchor from broader temporal applicability/precision;
- site / polity / community / network frame;
- historical geometry from navigation/reference geometry;
- exact / approximate / proxy / unresolved geometry state;
- source-native labels from normalized identity;
- historical evidence claims from target/frame metadata.

## 5. Experimental adapters

Construct disposable artifacts only under this experiment directory.

### LPF arm
Build one LPF-style Feature per frozen target.

Rules:
- use Atlas target ID as the stable experiment-local URI/identifier;
- do not mint a WHG canonical ID;
- do not upload/reconcile to WHG;
- use `geometry: null` unless a separately reviewed historical/navigation geometry is
  already present in the frozen project evidence;
- preserve anchor/time limits in `when` without claiming that the anchor equals an
  entity lifespan;
- preserve source/frame limitations in descriptions/relations;
- do not turn modern `ccodes` into historical jurisdiction;
- classify `fclasses` only where the target cleanly fits the LPF place class; record
  fit failure rather than force it.

### PeriodO arm
For each target ask whether there is an already-frozen **source-defined period concept**
that should be referenced.

Possible outcomes:
- reference an existing/source-defined period;
- construct a disposable source-definition-shaped example;
- **not applicable** because the Atlas anchor/frame is not itself a period definition.

A “not applicable” outcome is valid and must not be repaired by inventing a period.

## 6. Benchmark tasks

For each target compare baseline vs adapters on:
1. identity preservation;
2. temporal preservation;
3. spatial/geometry preservation;
4. source-scoped provenance;
5. resistance to overclaim;
6. generic reconciliation/linking value;
7. additional maintenance/semantic complexity.

## 7. Frozen discriminator

**REUSE**
if LPF and/or PeriodO add material generic interchange/reconciliation value while
preserving Atlas identity/time/geometry safety without becoming the canonical model.

**NARROW REUSE**
if a standard is useful only for a bounded subset, e.g. identifiable places or genuine
source-defined periods.

**REJECT AS DEFAULT**
if the standards force target reification, temporal flattening, spatial overclaim or a
parallel semantic model.

No threshold changes after adapter construction.

## 8. Adversarial attacks

Attack for:
- place = polity = community;
- target anchor = entity lifespan = period;
- modern country code = historical jurisdiction;
- one geometry = canonical historical extent;
- retrospective umbrella label = single place;
- source-defined period = Atlas research interval;
- LPF specification/deployment version drift;
- custom extension fields masquerading as standards reuse.

## 9. Complexity boundary

No historical/slavery research. No geometry promotion. No registry/target mutation. No
WHG upload/reconciliation submission. No PeriodO contribution. No new geography
ontology. No database/API/frontend/service work. No canonical/public release.

EXP-08 remains paused; Qi — 500 BCE remains frozen/unstarted.

## 10. Freeze rule

Do not construct or score adapters until this protocol/sample is merged.
