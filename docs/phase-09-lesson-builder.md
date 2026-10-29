# Phase 09 — Lesson Builder

## Purpose

Convert classified, curriculum-mapped evidence into structured lesson drafts while retaining provenance and keeping publication under human review.

## Contract

`Evidence -> Curriculum Node -> Lesson Draft -> Review -> Approved Version`

A lesson contains concept, optional definition, explanation, examples, revision notes, source evidence IDs, status, and version.

## Guarantees

- Deterministic lesson IDs for the same curriculum node, title, and version.
- Multiple evidence sources are supported.
- Source IDs are deduplicated without deleting evidence.
- Text normalization is conservative and deterministic.
- New versions receive explicit version numbers.
- Builder never approves or publishes a lesson.
- A lesson is not publishable without source evidence and explicit approval.

## Boundaries

This phase does not generate factual content from an LLM. It provides the canonical lesson-domain contract and deterministic builder. AI-assisted lesson drafting can be layered later, but every generated claim must remain evidence-backed and reviewable.

## Future integration

Phase 10 will generate topic-specific MCQs against approved/evidence-backed lesson material. Phase 12 will expose lesson review and approval in the admin workflow.
