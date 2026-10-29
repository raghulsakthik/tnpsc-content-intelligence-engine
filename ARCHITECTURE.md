# Architecture

## Core principle

The system is not `PDF → LLM → database`. It is an evidence-preserving pipeline:

`SOURCE → IMMUTABLE DOCUMENT → EXTRACTION → STRUCTURAL IR → CLEANING → CLASSIFICATION → CURRICULUM MAPPING → EVIDENCE → GENERATION → VALIDATION → HUMAN REVIEW → VERSIONED PUBLICATION`

## Engine responsibilities

### Engine 1 — Material Retrieval

Owns:
- web/portal discovery
- authorized browser access
- downloading
- file integrity and SHA-256
- deduplication at resource level
- quarantine/recovery
- source metadata

### Engine 2 — Content Intelligence

Owns:
- document representation
- extraction normalization
- cleaning
- exam/subject/unit/topic classification
- curriculum mapping
- evidence extraction
- semantic duplicate/conflict detection
- lesson generation
- topic-bound MCQ generation
- quality validation
- admin review workflow
- course assembly
- versioned publishing

### Platform

Owns learner-facing delivery, authentication/RBAC integration, progress/mastery, tests, analytics and consumption of published canonical content.

## Pipeline stages

1. Ingest a completed Engine 1 resource through a contract.
2. Create an immutable document record.
3. Extract text, pages, tables and OCR results where required.
4. Build a structural intermediate representation.
5. Remove extraction noise without deleting evidence.
6. Classify exam, subject and content type.
7. Map content to a versioned curriculum.
8. Extract evidence and page/block references.
9. Find exact/text/semantic duplicate candidates and conflicts.
10. Build canonical lesson proposals.
11. Generate topic-specific MCQs.
12. Validate generated content against evidence and structural rules.
13. Place proposals in the admin review queue.
14. Approve/edit/reject.
15. Publish a versioned course graph.
16. Expose canonical published entities to web and Android clients through the same API contract.

## Provenance model

Every derived object must be traceable through:

`published object → content version → source reference → document version → immutable resource → SHA-256`

Page and block evidence should be retained whenever extraction permits it.

## AI boundary

AI may propose classification, summaries, lesson structure, MCQs, difficulty, duplicate candidates and conflict candidates. AI may not autonomously publish, delete evidence, bypass PYQ exclusion, alter approved content, overwrite curriculum definitions, or execute arbitrary database operations.

## Current affairs

Current affairs are time-sensitive content. Their validity interval and publication/update date must be explicit. Expired material is not deleted; it is versioned and can be excluded from active course views according to curriculum policy.

## Integration strategy

The two engines remain independently testable. Engine 1 emits a stable source-resource contract. Engine 2 consumes only that contract. The existing TNPSC platform is integrated after the content API and publication model stabilize.
