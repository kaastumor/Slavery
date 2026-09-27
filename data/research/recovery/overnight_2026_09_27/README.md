# Overnight evidence reconciliation — 2026-09-27

This directory reconciles the completed **Atlas Hourly Expansion** scheduler packets
into current post-M1 research packages.

The scheduler did not write canonical state. These files are the interactive
reconciliation of its bounded research packets.

## Accepted successor packages

Ten legacy `research_prototype_reviewed` country-indexed claims are replayed:

- Paraguay;
- Bolivia;
- India;
- Mauritania;
- Myanmar;
- Nepal;
- Pakistan;
- Peru / Peruvian Amazon logging evidence;
- Uzbekistan cotton harvest;
- Brazil rural forced-labour/debt-bondage evidence.

Every successor package:

- is reviewed but initially unpublished;
- has `practice_level=null`;
- names the legacy claim ID it supersedes for future release selection;
- narrows time/sector/place scope to what the cited evidence supports;
- preserves source versions, dependence and limitations;
- rejects the old modern-country polygon as historical/practice inference extent.

The legacy rows and proxy geometries remain immutable lineage. They are not deleted.

## Geometry boundary

Most legacy country entities already have a reviewed `modern_proxy` polygon from the
early MVP. Those polygons may remain useful as explicitly labelled navigation/context
geometry. They are **not** evidence that the documented labour practice filled the
whole country.

Accordingly, these successor claims remain geometry-unresolved until bounded evidence
loci or other defensible practice geometry is independently established. This is
consistent with D-115 and D-119: claim completeness and geometry completeness are
separate.

## Not silently processed

Two known legacy prototypes were not completed by the overnight expansion worker:

- Mycenaean mainland Linear B dependency claim
  `df374145-bfd5-414b-ba9f-2d85819b7626`;
- Nazi Germany forced-labour claim
  `ab1f826b-aecf-4f2b-a88a-bccf1eea4f9a`.

They remain explicit next-work items rather than being inferred from adjacent packets.

No public release changes merely because these files exist.
