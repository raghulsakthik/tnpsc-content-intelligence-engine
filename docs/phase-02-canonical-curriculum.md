# Phase 02 — Canonical Curriculum

## Goal

Create a versioned taxonomy that every classifier, lesson and MCQ can reference. Content labels are not free-form strings and must not redefine the syllabus independently for each document.

## Implemented

- `CurriculumVersion` with source reference, effective date and lifecycle status.
- Stable `CurriculumNode` identifiers.
- Explicit node types: exam, subject, unit, topic and subtopic.
- English/Tamil labels and separate aliases.
- Parent-child relationships.
- Initial Group II/IIA subject domains.
- General Studies unit seed.
- Deterministic exact/alias mapping primitives.
- Tests protecting stable identifiers and non-fuzzy behavior.

## Mapping policy

1. Exact canonical terminology wins.
2. Known aliases are explicit data, not hidden fuzzy logic.
3. English and Tamil labels may resolve to the same node.
4. Multiple plausible mappings become review candidates.
5. Historical content retains its original curriculum version.
6. A future syllabus revision creates a new curriculum version instead of silently mutating the old one.

## Next work

Phase 03 will introduce the immutable document/intermediate-representation layer. Topic and subtopic seeds will be expanded using the selected official syllabus version before full-corpus classification begins.

## Definition of Done

- [x] Versioned curriculum model
- [x] Stable node IDs
- [x] Initial subjects
- [x] Initial General Studies units
- [x] Mapping primitives
- [x] Unit tests
- [ ] Full topic/subtopic seed
- [ ] Database persistence/migrations
- [ ] Coverage requirements per topic
