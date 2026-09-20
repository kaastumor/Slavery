# Pipeline Architecture

**Status:** approved implementation direction under D-046  
**Purpose:** keep research quality, cartographic processing, publication and runtime operations separated while preserving reproducibility.

## 1. Validation against standard practice

The architecture deliberately follows widely used scientific-data and CI/CD patterns rather than inventing an atlas-specific workflow model.

- USGS scientific-data guidance recommends scripted, modular workflows, standardized methods, explicit data-quality management, version control and process/provenance documentation throughout processing.
- FAIR requires detailed provenance and domain-relevant community standards for reusable research data and explicitly applies the principles to workflows and algorithms, not only final datasets.
- W3C PROV supplies the standard conceptual model for recording entities, activities and agents involved in producing derived data.
- GitHub Actions supports reusable workflows so repeated deterministic logic can be centralized rather than copied across many workflow files.
- GitHub deployment environments provide a standard boundary for staging/production secrets and deployment protection.
- Mainstream CI/CD guidance recommends **build once, deploy/promote many** so the artifact tested before release is the artifact promoted to production.
- QGIS processing algorithms are designed for scripted and batch execution, which fits the atlas requirement that render geometry be generated offline rather than inside public requests.

This means the atlas should use **separate logical pipeline lanes**, but should not create a separate top-level workflow for every small processing step.

## 2. Pipeline lanes

### A. Research curation

Unit of work: one bounded research case / claim package.

```
source discovery
  -> exact source/version registration
  -> bounded evidence extraction
  -> claim construction
  -> case/schema validation
  -> draft ingestion
  -> research/editorial review
  -> release eligible
```

Automated gates should verify structure, source-version presence, evidence direction, temporal consistency, claim/geometry constraints and publication state.

Automation must not turn a draft research case into a published claim merely because the file validates.

Historical interpretation remains a research-review responsibility. The project may automate evidence collection and consistency checks, but P-level and broad historical designation remain based on the interpreted evidence package.

### B. Cartography build

Unit of work: one source geometry plus an explicit render recipe.

```
immutable source geometry
  -> render candidate
  -> geometry validity/topology QC
  -> quantitative change QC
  -> representative visual QC
  -> approved render artifact
```

Candidate generation happens outside production.

Required provenance for a render artifact should include:

- source geometry ID and source version
- physical fabric version/checksum
- code commit
- tool/container version
- transformation recipe and parameters
- quantitative QC
- visual-review status
- artifact checksum

A generated candidate is not production geometry until it has been approved and promoted.

### C. Release / promotion

Unit of work: an immutable release bundle.

```
reviewed claims
    +
approved render geometry
    +
release metadata
  -> release gate
  -> immutable release artifact
  -> staging verification
  -> production promotion
  -> post-deploy health
  -> archived release record
```

The release stage does **not** reinterpret claims and does **not** regenerate geometry. It composes already-approved inputs.

Production must consume reviewed/published views or immutable release materializations, never unrestricted draft tables.

### D. Operations

Unit of work: service health and incidents.

```
external health probe
  -> healthy / degraded
  -> incident
  -> confirm failure
  -> guarded self-heal
  -> verify recovery
  -> escalate if needed
```

The existing MVP availability monitor and guarded Supabase restart belong here and remain independent of research and geometry builds.

## 3. State model

### Research

`proposed -> validated -> ingested_draft -> reviewed -> release_eligible -> published`

### Geometry

`source -> candidate -> qc_passed -> visually_accepted -> approved_render -> published`  
Failure path: `candidate -> quarantined/fallback`

### Release

`assembled -> gated -> staged -> promoted -> verified -> archived`

### Operations

`healthy -> degraded -> recovering -> healthy | escalated`

These states should be explicit in data/artifact metadata where practical. A workflow run being green is not itself a research-review or publication state.

Research ingestion should also become idempotent: each staged research case needs a stable case key/content identity so retrying the same approved input cannot silently create a duplicate claim. Until that identity is implemented in the database, automated research ingestion must remain an explicit controlled action rather than a retrying background writer.

## 4. Build once, promote unchanged

The tested artifact must be the promoted artifact.

Examples:

- a QGIS render candidate generated in CI should be checksummed and promoted unchanged rather than recomputed against production;
- a published release bundle should be generated once and moved through staging/production without rebuilding its contents;
- tool/container versions and inputs should be pinned enough to reproduce a build independently later.

Rebuilding the same conceptual release independently in different environments risks drift in software versions, geometry algorithms, source snapshots or configuration.

## 5. Workflow organization

Target top-level workflows:

- `ci.yml` — foundation/schema/unit/integration tests
- `research-case-ci.yml` — research-case structural/methodological validation
- `geometry-build.yml` — candidate generation and automated cartographic QC
- `release.yml` — release gate, staging and production promotion
- `mvp-health.yml` — external availability monitoring
- `mvp-self-heal.yml` — guarded operational recovery

Reusable sub-workflows or scripts should hold shared deterministic logic. Experiment-specific matrices belong as parameters to the geometry build rather than becoming permanent standalone architecture.

During migration, the current geometry experiment workflows may coexist with this target layout until their results are folded into the consolidated geometry build.

## 6. Environment boundary

### Local
Disposable development and exploratory research/geometry work.

### CI
Read-only validation against production. May start disposable local PostGIS/QGIS containers and produce artifacts.

### Staging
Production-like integration of release candidates. Expensive build work should already have completed; staging verifies the exact artifact that would be promoted.

### Production
Published serving only. Production receives approved artifacts/releases and bounded schema migrations. No exploratory spatial processing or ad-hoc research ingestion.

GitHub deployment environments should be used for `staging` and `production` so credentials and deployment rules are not shared with normal CI.

## 7. Quality gates

### Research gate
- valid case schema
- exact source-version identifiers
- at least one claim-specific evidence link
- evidence direction valid
- dates/spatial precision consistent
- unknown remains unknown
- P-level rules respected
- publication status remains unpublished before review

### Geometry gate
- valid geometry
- source geometry unchanged
- physical fabric version pinned
- quantitative change metrics recorded
- no unacceptable area/displacement/topology changes
- representative visual review where apparent extent changes
- artifact checksum/provenance recorded

### Release gate
- every claim reviewed
- every claim has evidence
- every territorial claim has approved or explicitly unresolved geometry
- only approved render artifacts included
- changelog/QC/unresolved issues present
- release manifest immutable
- staging API/map sanity passes
- production pre-health and post-health pass

## 8. What should remain manual/judgment-based

Do not automate away the places where expert judgment is the actual evidence standard:

- broad historical interpretation from mixed evidence
- resolving specialist historiographical disagreement
- assigning P-level where the evidence package requires contextual interpretation
- accepting a cartographic transformation that materially changes apparent extent
- declaring a new canonical data release

Everything around those decisions should be automated where practical so reviewers see consistent evidence and QC rather than doing mechanical checks by hand.

## 9. Near-term implementation

1. Add a dedicated research-case CI gate.
2. Consolidate the current geometry experiment workflows after issue #27 representative testing completes.
3. Make geometry builds output immutable candidate artifacts plus provenance/QC manifests.
4. Add a release workflow that promotes existing artifacts rather than recomputing them.
5. Add stable research-case identity/idempotency before making draft ingestion fully automatic.
6. Create/configure GitHub `staging` and `production` environments with scoped secrets and deployment protection.
7. Materialize published releases as static/recoverable snapshots so public availability is not tied entirely to live database health.

## References

- USGS data processing and workflow guidance: https://www.usgs.gov/data-management/process
- USGS process/analyze guidance: https://www.usgs.gov/data-management/process-and-analyze-closely-related-activities
- FAIR Guiding Principles: https://www.nature.com/articles/sdata201618
- W3C PROV primer: https://www.w3.org/TR/prov-primer/
- GitHub reusable workflows: https://docs.github.com/en/actions/how-tos/reuse-automations/reuse-workflows
- GitHub deployment environments: https://docs.github.com/en/actions/concepts/workflows-and-actions/deployment-environments
- QGIS batch processing: https://docs.qgis.org/testing/en/docs/user_manual/processing/batch.html

## Release-channel promotion and rollback

D-053 adds an explicit serving pointer after a release has been published. `public_mvp_preview` selects one immutable published release manifest. Promotion and rollback are compare-and-set pointer moves between existing published releases, followed by external health verification. Publication order is no longer a serving decision.

This improves rollback and promotion intent but does not replace the remaining build-once release-artifact work: release membership/digests still need the #4 reconstructibility model, and true staging/protected deployment environments remain #43 work.
