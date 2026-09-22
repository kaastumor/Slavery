## Question / summary

What project question does this change answer, and what is the smallest useful proposal?

## Adversarial check

State the strongest credible attack and the resulting disposition: **survives / revise / reject / park / experiment**.

## Change type

- [ ] Documentation / governance only
- [ ] Research data / semantic migration
- [ ] Database schema / migration
- [ ] Importer / tooling
- [ ] Map / API / application
- [ ] CI / infrastructure

## Required checks

- [ ] I read the relevant governance files in `docs/`.
- [ ] Raw/source-native values and identifiers remain preserved.
- [ ] No actor nationality or political identity was inferred from flag, port, residence, business base, surname, or company jurisdiction.
- [ ] Research coverage was not used as a territorial-practice score.
- [ ] New methodology/ontology/schema decisions are recorded in `docs/08_DECISIONS_LOG.md` where required.
- [ ] Existing applied SQL migrations were not edited; a new numbered migration was added instead.
- [ ] `scripts/verify-dev.ps1` or `scripts/verify-dev.sh` passes, or the failure is documented below.
- [ ] `python tools/sanitize_repo.py` passes.
- [ ] No new dependency/infrastructure was added without a demonstrated simpler-baseline failure.

## Validation / evidence

Describe tests, reconciliation, source checks, or QC performed.

## Unresolved issues

List anything intentionally deferred or still uncertain.
