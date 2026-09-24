# DISC-08 adversarial review

## Attack: a standard descriptor is obviously better than a custom manifest

Rejected.

A standard is valuable only where a generic consumer can act on the semantics. The
Frictionless resource/table vocabulary earns that bar for the CSV edge. Atlas release
effects and historical-safety states do not.

## Attack: Frictionless allows arbitrary extra metadata, so it can preserve everything

Technically true, methodologically insufficient.

Data Package v1 explicitly permits additional metadata properties. But an
`atlas_release_effect` extension would remain Atlas-defined. Generic Data Package
consumers would not gain the semantics. Counting that as standards interoperability
would violate the frozen discriminator.

## Attack: remote URLs solve all path problems cleanly

They solve enumeration, not locality.

The commit-pinned URLs preserve exact resources without moving them, but turn an
otherwise repository-local package into a web-dependent detached description. The
custom Atlas manifest can refer to the same repository tree directly.

This is acceptable for an interoperability adapter, not evidence that it should own the
package.

## Attack: Table Schema duplicates existing Python assertions

Partially true, but this is where the standard still earns narrow value.

The Atlas builder already checks candidate counts, target uniqueness and exact artifact
bytes. Table Schema adds a **generic declaration** of expected columns and keys that
another tool can understand without Atlas code.

That is new interoperability, even if it is not new historical information.

## Attack: RO-Crate solves the semantic problem

Only partly.

RO-Crate is a better research-object/provenance model than Frictionless. It can express
a Dataset, its Files, lineage and actions. But the project's most safety-critical
release assertions are domain semantics, not generic provenance.

A domain RO-Crate profile could encode them, but that would be a new Atlas semantic
profile with additional governance. DISC-08 found no demonstrated need for that cost.

## Attack: not running an installed third-party Frictionless validator invalidates the result

It limits one evidence class.

The environment did not have the library and could not install it because outbound
package resolution was unavailable. The experiment therefore does **not** claim a tool-
compatibility pass.

The result rests on the pinned normative v1 structure and a representation comparison.
Because the final disposition is only NARROW REUSE rather than mandatory adoption, the
missing runtime validation does not inflate the conclusion.

A real integration use case should run the chosen consumer's validator before adoption.

## Final adversarial disposition

**NARROW REUSE survives attack.**

The simplest durable architecture is still:
- Atlas manifest owns safety/release semantics;
- optional generated Frictionless schema/descriptor adapts the two portable tables when
  needed;
- RO-Crate remains a reference for future research-object exchange, not a default layer.
