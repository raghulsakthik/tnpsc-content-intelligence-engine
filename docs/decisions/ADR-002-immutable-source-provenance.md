# ADR-002: Immutable Source Provenance

## Status
Accepted

## Decision

Original source bytes are immutable and identified by SHA-256. Derived documents, evidence, lessons and MCQs retain references to the source version.

## Rationale

A learning platform needs to answer where a claim came from and reproduce how generated content was created. Mutable source records make auditing and regeneration unreliable.

## Consequences

- Source replacement creates a new version.
- Derived content is versioned.
- Evidence references should include page/block coordinates where available.
- Deletion is replaced by quarantine/archive where possible.
