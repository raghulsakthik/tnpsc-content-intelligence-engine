# TNPSC Content Intelligence Engine

A standalone content-intelligence and course-building engine for the TNPSC learning platform.

## Purpose

This repository transforms validated study materials into structured, reviewable learning content:

`Material → Document → Clean Content → Exam/Subject/Unit/Topic → Evidence → Lessons → Topic MCQs → Quality Review → Admin Approval → Published Course`

The engine is intentionally separated from the existing material-retrieval engine. Integration happens only after both systems have stable contracts.

## Non-negotiable rules

- Previous-year questions (PYQ) and PYQ compilations are never processed into publishable content.
- Original source documents are immutable.
- Every generated lesson and MCQ must retain source/evidence provenance.
- AI proposes; validation and human review control publication.
- Published content is versioned and auditable.
- Semantic duplicates are candidates for review, not automatic destructive merges.
- No generated content may silently overwrite approved content.

## Repository structure

```text
engine/          Core content-intelligence pipeline
api/             Integration/API boundary
database/        Migrations and seeds
admin/           Admin-facing contracts and workflows
docs/            Architecture, decisions, operations and testing
tests/           Unit, integration, security and corpus tests
scripts/         Development/maintenance utilities
.github/         CI/CD workflows
```

## Phase 0 status

Phase 0 establishes the architecture, contracts, security boundaries, canonical curriculum model, testing strategy and project skeleton. It does not mass-process the existing corpus.

## Integration boundary

```text
                 ┌─────────────────────────────┐
                 │       TNPSC PLATFORM        │
                 └──────────────┬──────────────┘
                                │ API
                 ┌──────────────▼──────────────┐
                 │ Content Intelligence Engine │
                 └──────────────┬──────────────┘
                                │ source contract
                 ┌──────────────▼──────────────┐
                 │ Material Retrieval Engine   │
                 └─────────────────────────────┘
```

The retrieval engine owns acquisition, validation, hashing and raw-source lifecycle. This repository owns transformation, curriculum mapping, evidence, generated learning content, quality and publication.

## Development

Python 3.11+ is the target runtime. Keep pipeline stages deterministic where practical and make every external/AI dependency explicit.

See `ROADMAP.md`, `ARCHITECTURE.md`, `CONTENT_CONTRACT.md` and `SECURITY.md` before implementing new pipeline stages.
