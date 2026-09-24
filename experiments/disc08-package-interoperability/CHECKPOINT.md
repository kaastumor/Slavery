# DISC-08 checkpoint

**Issue:** #250  
**State:** benchmark + adversary complete; result ready for merge  
**Disposition:** **NARROW REUSE**  
**Historical subject research:** none  
**EXP-08:** paused; Qi — 500 BCE frozen/unstarted

## Frictionless result

Artifacts:
- `frictionless/datapackage.json`
- `02_BENCHMARK.md`

Observed:
- standard resource enumeration: useful generic gain;
- Table Schema for 21-column target table + 16-column source table: useful narrow gain;
- SHA-256 resource identity: representable;
- complete repository-spanning boundary: representable only through commit-pinned
  remote URLs without moving files;
- Atlas release-effect / review-gate / artifact-role semantics: not generic
  Frictionless semantics.

## RO-Crate conditional result

Artifact:
- `ro-crate/ro-crate-metadata.json`

RO-Crate 1.3 was authorized because Frictionless's remaining weakness was
research-object/provenance structure.

It better represents Dataset/File/lineage relationships but still does not replace the
Atlas-specific safety/release semantics without a custom/domain layer.

Disposition: **LEARN FROM / not default package layer**.

## Durable decision

- Atlas `manifest.json` remains authoritative;
- optional generated Frictionless adapter is allowed for concrete
  interoperability/validation needs;
- no mandatory Frictionless/RO-Crate layer;
- no JSON-LD/RDF infrastructure.

Artifacts:
- `02_BENCHMARK.md`
- `03_ADVERSARY.md`
- `RESULT.md`

## Next exact action

Merge if CI is green, close #250, then freeze one bounded **historical place/time
interchange benchmark** using WHG Linked Places Format + PeriodO.

Do not resume Qi or begin new historical subject research.
