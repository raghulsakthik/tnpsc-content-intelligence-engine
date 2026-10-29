# Phase 03 — Document Intelligence / Intermediate Representation

## Objective

Create a stable, provenance-preserving representation between the Material Retrieval Engine and all downstream content-intelligence stages.

## Design

```text
Engine 1 Resource
      |
      v
Immutable Document
      |
      v
Document Version
      |
      +--> Pages
      |      |
      |      +--> Blocks
      |
      +--> Chunks
```

## Invariants

1. The original Engine 1 resource is never mutated.
2. A document is identified by the source resource and SHA-256 identity.
3. Every derived page/block/chunk references its parent version.
4. Extraction changes create a new document version rather than overwriting old output.
5. Text fingerprints support idempotency and duplicate detection.
6. Bounding boxes and page numbers are retained when available so later evidence can point back to source locations.
7. Metadata is extensible but provenance identifiers are mandatory.

## Why this exists

A PDF file is not yet learning content. The IR creates a common representation for native-text PDFs, OCR output, table extraction and future parsers. Cleaning, classification, evidence extraction and generation can operate on this representation without coupling themselves to a particular PDF library.

## Phase 03 does not do

- OCR
- lesson generation
- MCQ generation
- semantic classification
- publication
- corpus-wide processing

Those are later phases.

## Definition of Done

- Document models exist and are immutable at the application layer.
- Provenance chain is testable.
- Stable text fingerprints exist.
- Extraction stages can create versioned representations.
- Tests cover the core invariants.
