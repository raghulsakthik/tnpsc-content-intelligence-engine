# Roadmap

## Phase 00 — Foundation
- Freeze architecture boundaries
- Define contracts and canonical entities
- Define security rules
- Define curriculum versioning
- Establish CI and test skeleton
- No corpus-wide processing

## Phase 01 — Corpus Inventory
- Consume Engine 1 resource metadata
- Inventory available non-PYQ material
- Record document/resource provenance
- Identify extraction/OCR requirements
- Produce corpus coverage report

## Phase 02 — Canonical Curriculum
- Model TNPSC exam → subject → unit → topic → subtopic
- Version curriculum definitions
- Add mapping aliases and language variants
- Establish coverage requirements

## Phase 03 — Document Intelligence / IR
- Immutable document versions
- Page/block/chunk representation
- File fingerprints
- Structural metadata
- Document-level processing states

## Phase 04 — Extraction
- PDF text extraction
- OCR path for scanned documents
- Table-aware extraction
- Tamil/English normalization
- Extraction quality scoring

## Phase 05 — Cleaning
- Header/footer detection
- Repeated-section removal
- Broken line and whitespace repair
- Noise classification
- Preserve source coordinates/evidence

## Phase 06 — Classification
- Exam classification
- Subject/content-type classification
- PYQ hard exclusion
- Mock/current-affair/government-material labels
- Confidence vectors

## Phase 07 — Evidence
- Evidence blocks and page references
- Claim/evidence links
- Source corroboration
- Conflict candidates

## Phase 08 — Deduplication & Conflicts
- Exact duplicates
- Text duplicates
- Semantic duplicate candidates
- Conflicting claims
- Human resolution workflow

## Phase 09 — Lesson Builder
- Topic-bound lesson proposals
- Objectives/prerequisites
- Explanations/examples/revision notes
- Source attribution
- Canonical lesson versions

## Phase 10 — MCQ Engine
- Topic-specific MCQs
- Four-option structure
- Answer/explanation/evidence
- Easy/medium/hard
- Duplicate and ambiguity checks
- Tamil/English support

## Phase 11 — Quality Engine
- Evidence coverage
- Answer correctness
- Difficulty consistency
- Language quality
- Safety/security checks
- Publish gates

## Phase 12 — Admin Content Inbox
- Search/filter/review
- Source preview
- Label editing
- Lesson editing
- MCQ review
- Approve/reject/publish
- Audit history

## Phase 13 — Course Builder
- Subject → unit → topic → lesson graph
- Topic practice and tests
- Unit/subject tests
- Versioned course releases

## Phase 14 — Engine Integration
- Stable Engine 1 ingestion adapter
- Idempotency
- Retry/replay
- Backpressure and storage limits
- End-to-end processing

## Phase 15 — Full Corpus Processing
- Process all eligible material
- Generate coverage report
- Review low-confidence content
- Resolve duplicate/conflict queues

## Phase 16 — Gap-Driven Acquisition
- Detect missing curriculum coverage
- Generate acquisition requirements
- Feed requirements to Engine 1
- Re-process newly acquired evidence

## Phase 17 — Platform Integration
- Content API
- Admin integration
- Web learner integration
- Android integration
- Shared canonical entities

## Phase 18 — Security & Production
- SSRF/DNS/redirect controls
- Archive bomb/path traversal controls
- Prompt injection isolation
- RBAC/audit hardening
- Observability
- Backup/recovery
- Performance/load testing

Each phase should end with tests, documentation, a reviewable commit and a clear Definition of Done.
