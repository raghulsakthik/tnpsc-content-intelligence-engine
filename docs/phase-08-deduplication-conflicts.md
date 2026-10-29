# Phase 8 — Deduplication & Conflict Detection

## Goal

Identify duplicate candidates and source conflicts without deleting, merging, or overwriting evidence.

## Duplicate levels

1. **Exact resource** — matching SHA-256.
2. **Normalized text** — extracted text matches after deterministic whitespace/case normalization.
3. **Exact text** — byte-for-byte text equality when available.
4. **Possible semantic duplicate** — token cosine similarity crosses a configurable candidate threshold.

Semantic similarity is never an automatic merge decision.

## Safety rules

- Original documents remain immutable.
- Duplicate candidates remain reviewable records.
- No source is deleted by the detector.
- No curriculum node is rewritten by deduplication.
- No approved lesson is silently replaced.
- Every candidate records its evidence and similarity.

## Conflict model

`ConflictCandidate` supports future detection of:

- conflicting factual values;
- competing curriculum mappings;
- publication-date discrepancies;
- source metadata disagreements.

Conflicts require review and preserve both source references.

## Next integration

Phase 9 will consume these candidates while building canonical lessons. A lesson can have multiple supporting sources, but a suspected duplicate must not cause evidence loss. Conflict candidates should flow into the admin review queue before publication.
