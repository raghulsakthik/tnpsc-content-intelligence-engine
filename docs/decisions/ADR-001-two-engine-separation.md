# ADR-001: Keep Retrieval and Content Intelligence Separate

## Status
Accepted

## Decision

Maintain Engine 1 (material retrieval) and Engine 2 (content intelligence) as independently deployable/testable boundaries.

## Rationale

Retrieval failures, source validation and browser/network concerns have different failure modes from classification, generation and publication. Separation allows each engine to evolve without coupling raw acquisition to learner-facing content.

## Consequences

- A stable source-resource contract is required.
- Integration is explicit rather than sharing internal modules.
- End-to-end tests must cover the contract boundary.
- The existing retrieval engine is not modified during Phase 0.
