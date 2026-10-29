# ADR-005: Versioned Publishing

## Status
Accepted

## Decision

Published lessons, MCQs and course graphs are immutable versions. Updates create new versions and publication events.

## Rationale

Learners may have consumed an earlier version. In-place mutation makes historical analytics and review/audit trails unreliable.

## Consequences

- Draft and published states are distinct.
- Unpublish/archive actions retain history.
- Course nodes reference canonical content versions.
