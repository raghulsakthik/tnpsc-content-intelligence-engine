# Engine → TNPSC Platform Publication Package

The Content Intelligence Engine publishes approved lessons and MCQs through a deterministic package consumed by the existing TNPSC platform Admin Content Engine.

## Flow

`Retrieval Engine → immutable source → extraction/cleaning → curriculum mapping → evidence → lesson/MCQ → validation/review → approved package → Admin Content Engine → Review Queue → platform`

The engine does not write directly to the learner-facing platform database.

## Platform topic mapping

The platform owns its real topic IDs. Before generating a publication package, an authorized admin can export the platform mapping from:

`GET /api/admin/content-engine/topic-map`

The export contains the real `topic_id`, topic name, chapter, and subject identifiers. The engine consumes that export and an explicit mapping of `curriculum_node_id → topic_id`.

Rules:

- Never invent a platform topic ID.
- Never silently map a missing curriculum node.
- Never collapse two engine curriculum nodes into one platform topic unless the mapping contract explicitly permits that relationship; the current validator fails closed on collisions.
- If the platform syllabus changes, export a fresh map before producing a new publication.

## Contract

The package shape is:

```json
{
  "publicationId": "group2a-2026-001",
  "manifestHash": "<sha256>",
  "items": [
    {
      "kind": "lesson",
      "content_id": "<engine lesson id>",
      "topic_id": "<existing platform topic id>",
      "payload": {
        "title": "...",
        "concept": "...",
        "definition": "...",
        "explanation": "...",
        "examples": [],
        "revisionNotes": [],
        "sourceIds": ["<evidence id>"],
        "version": 1,
        "isPyq": false
      }
    }
  ]
}
```

MCQs use `question`, `options`, `answerIndex`, `explanation`, `difficulty`, `sourceIds`, `version`, and `isPyq:false`.

## Safety rules

- Only `APPROVED` engine content with provenance can cross the boundary.
- PYQs are rejected by the engine and independently rejected by the platform.
- A curriculum node must have an explicit platform `topic_id` mapping; the exporter never guesses or creates one.
- MCQs must have exactly one correct answer and unique options.
- Items are sorted deterministically before hashing.
- The manifest uses recursive object-key sorting and SHA-256, matching the platform implementation.
- Import only stages content. Existing Admin Review approval is still required for learner publication.
- Publication IDs and content IDs are immutable lineage identifiers; a changed package must receive a new publication/version rather than overwriting an old package.

## Group 2 / Group 2A

Shared content should be represented once in the engine and mapped to the appropriate existing platform topic. Exam applicability belongs to curriculum/topic mapping, not duplicated lesson text. If Group 2 and Group 2A have different topic requirements, they must use distinct explicit mappings.

## Local/self-hosted operation

This contract does not require cloud storage. Retrieval and generated artifacts can remain on the existing local/self-hosted pipeline. Source immutability, SHA identity, evidence provenance, and publication versioning remain mandatory.
