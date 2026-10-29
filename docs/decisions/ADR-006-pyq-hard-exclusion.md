# ADR-006: PYQ Hard Exclusion

## Status
Accepted

## Decision

Previous-year question papers and PYQ compilations are permanently excluded from generated publishable content in this engine.

## Rationale

The platform's content corpus must remain distinct from historical question-paper practice data. Mixing them creates provenance and curriculum-quality problems and can cause generated material to reproduce examination questions.

## Consequences

- Classification includes an explicit `is_pyq` decision.
- High-confidence PYQ resources stop before generation.
- Low-confidence cases are quarantined/reviewed.
- Existing question-paper storage is not deleted by this repository.
