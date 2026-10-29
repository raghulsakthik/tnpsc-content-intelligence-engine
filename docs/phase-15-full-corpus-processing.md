# Phase 15 — Full Corpus Processing

## Objective

Provide a safe orchestration layer for processing the complete TNPSC material corpus without losing progress or reprocessing immutable inputs unnecessarily.

## Design

```text
Engine 1 resource
      |
      v
Batch manifest (stable resource + SHA-256 identity)
      |
      v
Registration -> Extraction -> Cleaning -> Classification -> Evidence
      |              |            |             |             |
      +-------------- checkpointed item state ----------------+
                              |
                              v
                    Lesson / MCQ / Quality
```

## Guarantees

- Batch manifests are deterministic and sorted by stable item identity.
- Resource SHA-256 participates in the manifest identity.
- Completed items are idempotent and are not executed again.
- Failed items retain the stage checkpoint and error information.
- Resume starts from the failed checkpoint rather than silently restarting the corpus.
- Stage names must be unique.
- Orchestration does not mutate source documents.
- The processor does not publish content; publication remains behind quality and admin-review gates.

## Operational requirements

A production runner should persist `BatchItem` state after every stage boundary. A process restart must reload the latest checkpoint before continuing. Large batches should be partitioned into bounded manifests so one corrupt document cannot block unrelated material.

## Failure policy

Failures are item-scoped. Transient failures can be retried by the runner. Deterministic validation failures should remain failed until the underlying input or stage implementation changes. The system must preserve the original error and stage for auditability.

## Corpus safety

PYQ exclusion remains enforced upstream at the Engine 1 -> Engine 2 integration boundary. The corpus runner must never turn an excluded resource into publishable content.

## Current scope

This phase provides the deterministic orchestration primitives and tests. It does not claim that the live local Engine 1 corpus has been processed; live corpus execution requires an authorized runtime connection to that corpus.
