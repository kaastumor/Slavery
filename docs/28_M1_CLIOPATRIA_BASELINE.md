# M1 complete Cliopatria baseline profile

**Gate:** #100  
**Atomic task:** #104  
**Status:** experimental raw-geography preparation; not canonical methodology, approved geometry, or a release change

## Question
Can the complete Cliopatria corpus become a reproducible raw geography backbone without importing its assumptions into atlas historical claims?

## Pinned source
- repository: `Seshat-Global-History-Databank/cliopatria`
- upstream release: `v0.2.0-duplicate` (a re-release of v0.2.0)
- exact commit: `ad28a691b7c07c1fca89d0e0636d324667d2a258`
- file: `cliopatria.geojson.zip`
- upstream Git blob checksum: `cefab0f4b622e2e7fb3daf68d4f461f83991204c`
- blob size: 44,231,317 bytes

The profiler additionally emits SHA-256 of the downloaded bytes. It hard-fails unless the Git blob checksum matches, so a mutable network response cannot silently become the baseline.

## Smallest proposal
`tools/profile_cliopatria.py` downloads (or accepts a local copy of) that one immutable source blob, verifies its Git content identity, opens the single GeoJSON member, and emits a deterministic JSON profile. It does **not** write the database, normalize years, resolve atlas entities, or promote geometry.

The profile reports whole-corpus feature/name counts, every source-native `Type` value (including composite/unexpected values rather than coercing them), geometry types, property-presence counts, and temporal diagnostics. Every property remains in the upstream object; this preparation step summarizes rather than rewrites the corpus.

## BCE/year convention test
Upstream documents `FromYear`/`ToYear` as signed integers: negative for BCE, positive for CE, inclusive for row applicability. The profiler deliberately preserves those values and reports negative-year rows, rows spanning numeric zero, and invalid `FromYear > ToYear` rows. **No conversion to the atlas historical-year convention occurs in M1.** Any zero-boundary/calendar normalization must be a later explicit integration decision after the observed corpus is profiled.

## Adversary
| Attack / alternative | Disposition | Evidence / consequence |
| --- | --- | --- |
| Keep fetching `main` or “latest” on demand | **reject** | Reproducibility fails when upstream changes; exact commit + blob identity is smaller and sufficient. |
| Cherry-pick only atlas polities from upstream | **reject** | It hides global/type/time failure modes and cannot establish baseline coverage. |
| Import all rows directly into approved atlas geometry | **reject** | Raw geography availability is not historical-claim acceptance; D-055 specialist precedence and geometry QC remain binding. |
| Normalize BCE/CE while profiling | **reject** | That would erase the source-native convention before the zero-boundary behavior is inspected. |
| Preserve every raw feature/property and derive only a sidecar profile | **survives** | Gives inspectable corpus evidence without schema or publication coupling. |
| Treat `Type` as a closed POLITY/RELATION enum | **revise** | The profiler records all observed strings so composite/novel semantics remain visible rather than coerced. |
| Build a new ingestion service/cache | **park** | A single deterministic script is enough for M1; no demonstrated infrastructure failure. |
| Assume full-corpus import improves selected-year atlas coverage | **experiment** | #104 measures the corpus; usefulness versus on-demand resolution belongs in the integrated #105 adversary once the actual profile exists. |

## Reproduction

```bash
python tools/profile_cliopatria.py --output cliopatria-profile.json
```

The generated profile is analytical output, not a source asset to commit. The 44 MB upstream zip is also not vendored. CI/unit fixtures are synthetic and public-safe.

## Decision
**Experiment.** Pin and profile the complete corpus as a raw fallback candidate, while preserving source-native semantics and the existing specialist-override hierarchy. Do not promote or normalize it during M1. Canonical release v0.6.1 and the public preview remain unchanged.
