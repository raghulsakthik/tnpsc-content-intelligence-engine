# Phase 7 — Evidence Extraction & Provenance

## Goal

Make every downstream classification, lesson, MCQ, and review decision traceable to immutable source material.

## Pipeline position

`source → document → document version → page → block/chunk → evidence → derived content`

## Guarantees

- Evidence contains document and extraction-version identity.
- Source SHA-256 can be carried through every evidence record.
- Page numbers are preserved.
- Chunk identity is preserved where chunking exists.
- Evidence spans contain the exact extracted text and offsets.
- Evidence IDs are deterministic for repeatable processing.
- Empty source material does not create fake evidence.
- This layer never paraphrases, translates, summarizes, or invents source text.

## Why this matters

An AI-generated lesson or MCQ must eventually answer: “Where did this claim come from?” Evidence coordinates provide the foundation for page-level review, source attribution, conflict detection, and auditability.

## Important boundary

Evidence is not truth validation. A source can be authoritative, outdated, incorrect, or conflicting. Phase 7 records what the source says; later quality and conflict stages determine how that evidence may be used.

## Next phase

Phase 8 introduces duplicate detection and source-conflict candidates while keeping semantic similarity as a review signal rather than an automatic merge decision.
