# Data Model

Phase 0 defines the logical model. Physical migrations are introduced in Phase 2/3 after the contracts are tested.

## Source/document layer

- `source_resources` — immutable Engine 1 resource references
- `document_versions` — parsed representation of one immutable source version
- `document_pages` — page-level metadata
- `document_blocks` — structural text/table/image/OCR blocks
- `content_chunks` — normalized retrieval/generation chunks

## Curriculum layer

- `curriculum_versions`
- `subjects`
- `units`
- `topics`
- `subtopics`
- `curriculum_aliases`

## Evidence layer

- `evidence_items`
- `content_evidence`
- `content_conflicts`
- `duplicate_candidates`

## Generated content

- `lessons`
- `lesson_versions`
- `lesson_sources`
- `mcq_sets`
- `mcqs`
- `mcq_options`
- `mcq_sources`
- `topic_tests`
- `courses`
- `course_versions`
- `course_nodes`

## Review/publication

- `content_reviews`
- `publish_queue`
- `publication_events`
- `audit_logs`

## AI reproducibility

- `ai_models`
- `ai_prompts`
- `ai_runs`
- `ai_outputs`

## Design constraints

- Preserve foreign-key provenance to immutable source resources.
- Never mutate a published content version in place.
- Use transactions around state transitions.
- Add unique/idempotency keys for processing runs.
- Keep review/audit history append-oriented.
- Prefer canonical references over copying content into course records.
