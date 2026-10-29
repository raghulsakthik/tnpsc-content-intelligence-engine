# Phase 10 — MCQ Engine

## Objective

Create a deterministic, source-backed MCQ domain that can receive proposed questions from lesson/evidence pipelines without allowing unsupported or previous-year questions into publication.

## Pipeline

```text
Lesson / Evidence
      ↓
MCQ Draft
      ↓
Structural Validation
      ↓
Quality Review (Phase 11)
      ↓
Admin Review
      ↓
Approved MCQ Version
```

## Domain

Each MCQ contains:

- lesson ID
- curriculum node ID
- question
- options
- exactly one intended correct option
- explanation
- difficulty (`easy`, `medium`, `hard`)
- source evidence IDs
- PYQ flag
- review status
- explicit version

## Hard rules

1. PYQ MCQs are never publishable.
2. Source evidence is mandatory for publication.
3. MCQs need at least two options.
4. Empty or duplicate options fail validation.
5. Zero correct options fail validation.
6. Multiple correct options fail validation.
7. Explanation is mandatory.
8. Missing lesson/curriculum ownership fails validation.
9. Validation does not approve content.

## What this phase validates

The current validator is deliberately deterministic. It checks structural integrity and explicit answer metadata. It can reliably detect malformed MCQs, but it does **not** claim to determine semantic ambiguity, factual correctness, distractor quality, or whether an answer is supported by the evidence.

Those checks belong to the Phase 11 quality system, where evidence-grounded validation, semantic review, duplicate detection across the corpus, and human review can be layered safely.

## Duplicate handling

A normalized question/options fingerprint is generated for downstream duplicate detection. The fingerprint is a review signal, not an instruction to delete or merge content.

## Publication boundary

`build_mcq()` always creates a draft, except a PYQ is explicitly marked `excluded_pyq`. The builder cannot approve or publish an MCQ. Publication remains a separate workflow with validation, quality gates, and admin approval.

## Tests

The unit suite covers:

- deterministic IDs
- valid MCQ acceptance
- no correct answer
- multiple correct answers
- duplicate option text
- PYQ hard exclusion
- missing source evidence
