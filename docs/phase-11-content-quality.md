# Phase 11 — Content Quality & Validation

## Goal

Prevent unsupported, structurally invalid, contaminated, or unreviewed content from being published to the TNPSC learning platform.

## Pipeline

```text
Lesson / MCQ
    ↓
Structural checks
    ↓
Provenance checks
    ↓
Contamination checks
    ↓
Deterministic quality report
    ↓
Semantic review when required
    ↓
Human approval
    ↓
Publication
```

## Quality dimensions

- completeness
- source provenance
- option uniqueness
- exactly one declared MCQ answer
- explanation presence
- PYQ contamination
- semantic/factual review requirement

## Publication rule

A quality report is publishable only when every check passes. A semantic-review check intentionally produces `REVIEW` for content that still needs evidence-aware semantic validation. Therefore merely having structurally valid AI-generated content is not enough to publish it.

## Hard failures

- missing required content
- missing source evidence
- duplicate MCQ options
- zero or multiple declared correct answers
- PYQ contamination

## Review boundary

This phase does **not** claim that regex/string rules can prove factual correctness, detect every ambiguity, or judge distractor quality. Those are review problems. Future AI-assisted validators may propose findings, but their output must remain reviewable and must never bypass publication controls.

## Provenance

Quality checks retain evidence IDs where available so reviewers can navigate back to the supporting material. Source documents remain immutable and derived content remains versioned.
