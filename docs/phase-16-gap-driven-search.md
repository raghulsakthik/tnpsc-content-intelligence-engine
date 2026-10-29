# Phase 16 — Gap-Driven Search

## Purpose

Turn curriculum coverage evidence into deterministic, reviewable acquisition requests for Engine 1.

This phase does **not** perform web searches, downloads, publishing, or automatic content creation.

## Flow

```text
Canonical Curriculum
      ↓
Approved Content Coverage
      ↓
Coverage Analysis
      ↓
Weak / Missing Topic
      ↓
Coverage Gap
      ↓
Priority
      ↓
Acquisition Request
      ↓
Engine 1 Discovery
```

## Coverage signals

A curriculum node is considered weak when one or more of these conditions apply:

- no approved lessons
- fewer than two approved lessons
- fewer than ten approved MCQs
- no topic test
- no source provenance
- quality score below the configured threshold

Coverage is based on approved content, not drafts or rejected content.

## Priority

Gaps are ranked as:

1. `critical` — no approved content or extremely low coverage
2. `high` — substantially incomplete coverage
3. `medium` — partially incomplete coverage
4. `low` — minor coverage deficiency

The ranking is deterministic so repeated analysis produces stable acquisition order.

## Engine 1 boundary

`AcquisitionRequest` is a signal, not a download command. Engine 1 remains responsible for:

- discovery
- source authorization
- SSRF protection
- download validation
- SHA-256 hashing
- PYQ exclusion
- disk safety
- retry/recovery

Engine 2 must never directly bypass those controls.

## Idempotency

Gap IDs and acquisition request IDs are deterministic. Re-running the same coverage snapshot should not create a new logical request merely because the analyzer was run again.

## Safety

The analyzer does not infer that a missing topic means any arbitrary document is suitable. Retrieved material still passes the complete Engine 1 and Engine 2 pipeline, including classification, provenance, quality validation, PYQ exclusion, and admin review.

## Future extension

Later phases can add query expansion using curriculum aliases, language-aware search terms, source-quality weighting, temporal current-affairs requirements, and feedback from successful acquisitions. Those additions must remain deterministic where possible and auditable when AI-assisted.
