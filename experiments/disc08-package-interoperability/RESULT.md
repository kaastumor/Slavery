# DISC-08 result — portable-package interoperability benchmark

**Issue:** #250  
**Disposition:** **NARROW REUSE**  
**Historical subject research:** none  
**Canonical release:** v0.6.1 unchanged

Frictionless Data Package v1 adds a material generic capability at the tabular boundary:
standard resource enumeration plus Table Schema declarations for the two portable CSVs.

It does **not** replace the Atlas custom package manifest. Standards-only Frictionless
cannot carry the project's structured release-effect guards, artifact roles and
review-gate semantics as generic meanings. Full reconstruction of the current
repository-spanning package also requires commit-pinned remote URLs because v1 forbids
parent local paths.

RO-Crate 1.3 was conditionally compared because that failure concerned research-object
/provenance structure. It models Dataset/File/provenance relationships better, but the
decisive release-safety semantics still require Atlas/domain meaning and the added
JSON-LD layer is not justified by a demonstrated workflow.

Durable direction:
- keep the custom Atlas manifest authoritative;
- permit an optional **generated Frictionless adapter** for actual CSV
  export/interoperability/validation needs;
- do not make Frictionless or RO-Crate a mandatory release layer;
- do not add RDF/JSON-LD infrastructure.

Reopen stronger adoption only on a demonstrated consumer/depository/interchange need or
repeated generic-validation benefit.

EXP-08 remains paused; Qi — 500 BCE remains frozen/unstarted.
