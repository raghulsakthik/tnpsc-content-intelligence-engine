# Phase 17 — Platform Integration

## Purpose

Expose approved content from the content-intelligence engine to the TNPSC
learning platform without allowing the platform layer to bypass provenance,
approval, curriculum, or course-version boundaries.

## Boundary

```text
Approved lesson / MCQ / test
          ↓
Approved content identity + evidence
          ↓
Versioned course manifest
          ↓
Platform publication envelope
          ↓
TNPSC platform ingestion
          ↓
Learner-facing course
```

The platform adapter is not a second content authority. It does not generate,
approve, edit, delete, or silently rewrite content.

## Publication invariants

1. Every published content reference belongs to the selected course version.
2. Content must be explicitly approved before it is emitted.
3. Every emitted content item must retain at least one source/evidence ID.
4. The course manifest hash is required for publication identity.
5. Publication IDs are deterministic for the same course/version/manifest.
6. Published versions are immutable; a changed course/content version produces
   a new publication identity.
7. Unapproved content is omitted rather than silently promoted.
8. The existing platform can consume these references through an adapter/API
   without changing its current UI structure.

## Integration contract

The platform should eventually map:

```text
curriculum subject → course unit → topic → lesson
                              ├→ MCQ set
                              └→ topic test
```

The content engine remains responsible for source provenance, quality gates,
admin approval, and versioning. The platform remains responsible for learner
accounts, progress, delivery, attempts, analytics, and access control.

## No false integration claim

This phase defines and tests the platform boundary. It does not claim that the
separate production TNPSC backend/frontend has already been connected. That
connection requires its actual repository/API/schema to be inspected and
mapped before any production adapter is enabled.
