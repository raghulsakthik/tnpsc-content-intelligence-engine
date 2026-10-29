# Phase 13 — Course Builder & Versioned Course Structure

## Purpose

Turn approved lessons, MCQ sets, and tests into a deterministic, versioned learning course without allowing the course layer to bypass content approval.

## Structure

```text
Exam
└── Course (versioned)
    ├── Unit
    │   └── Topic
    │       ├── Lesson
    │       ├── MCQ Set
    │       └── Topic Test
    └── Dependencies / prerequisites
```

## Guarantees

- Every course is tied to an explicit exam and curriculum version.
- Course and node identifiers are deterministic.
- Nodes are ordered and parent-linked.
- Lesson, MCQ-set, and test nodes require content references.
- A manifest hashes the course structure and referenced content identities.
- Foreign-course nodes and missing parents are rejected.
- A course with no lessons cannot pass structural validation.
- Test absence is a warning rather than an automatic structural failure.
- Course construction never approves or publishes lesson/MCQ content.

## Versioning

A changed course structure creates a new course version. Existing published manifests remain immutable. Content changes must also follow their own content-version and review rules.

## Publication boundary

```text
Approved content
      ↓
Course composition
      ↓
Structural validation
      ↓
Course review
      ↓
Course publication
```

The course builder is intentionally not an authorization layer. Final publication must be controlled by the platform's review/RBAC layer introduced in later integration phases.
