# Phase 19 — Live TNPSC Platform Integration Boundary

Phase 19 connects the content intelligence engine's approved output to the
existing `raghulsakthik/yash-tnpsc` platform without bypassing its review and
publication rules.

## Existing platform discovered

The platform is a Next.js application with PostgreSQL. Its current content
surface already has admin APIs for content classification, processing,
review, lessons, questions, resources, curriculum and tests. Migration
`V21__content_engine.sql` adds question metadata, richer lesson fields and a
review-batch table.

The existing platform question schema uses:

- `topic_id`
- `language`
- `prompt`
- `options`
- `answer_index`
- `explanation`
- `difficulty`
- `source`
- `source_year`
- `status`

The existing lesson table is keyed by `topic_id`, which means it currently
supports one primary lesson per topic. The intelligence engine intentionally
supports multiple versioned lessons. Therefore this phase does **not** silently
collapse multiple approved lessons into one platform row.

## New adapter

`engine/platform/tnpsc_import.py` creates a deterministic `PlatformImportPlan`.
It transforms approved engine `Lesson` and `MCQ` objects into a platform-shaped
payload without performing network or database writes.

The adapter enforces a final boundary check:

```text
APPROVED ENGINE CONTENT
        |
        +-- lesson -> exactly one primary lesson per platform topic
        |
        +-- MCQ -> exactly one correct option + provenance
        |
        +-- PYQ -> BLOCK
        |
        +-- unapproved -> NOT INCLUDED
        |
        +-- multiple lessons/topic -> REVIEW REQUIRED
        |
        v
DETERMINISTIC IMPORT PLAN
```

## Non-negotiable rules

1. Engine approval is required before import planning.
2. PYQs cannot cross the platform boundary as normal learning MCQs.
3. Every imported MCQ must have source evidence.
4. MCQs must have exactly one correct option.
5. Multiple approved lessons for one existing platform topic require an
   explicit content-model decision; they are never silently discarded.
6. The manifest hash is deterministic and can be stored with a publication
   event for idempotency.
7. The adapter cannot approve, publish, delete, or rewrite engine content.

## Current platform mapping

| Engine | Existing platform |
|---|---|
| curriculum node | `subject → chapter → topic` |
| approved lesson | primary `lesson` row for topic |
| approved MCQ | `question` row |
| evidence IDs | provenance/source metadata |
| difficulty enum | numeric platform difficulty mapping required at persistence boundary |
| engine version | content-version/publication metadata |
| course manifest | publication manifest |

## Remaining production wiring

The next implementation step is the authenticated platform persistence
adapter. It must run inside the TNPSC platform's existing permission model and
transaction boundary, then create/update draft rows and review batches. It must
not expose a public unauthenticated ingestion endpoint.

The current `yash-tnpsc` repository is therefore treated as the target platform,
not as a second content engine. Existing frontend behavior remains unchanged.
