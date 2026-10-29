# Phase 06 — Curriculum & Content Classification

## Goal

Convert cleaned document text into a deterministic, reviewable classification decision before topic/lesson generation.

## Pipeline position

`Document IR → Extraction → Cleaning → Classification → Topic Mapping → Evidence → Lessons`

## Baseline behavior

The Phase 6 classifier uses explicit English/Tamil rules for:

- exam: `TNPSC_GROUP_2_2A`
- subjects: General Studies, Aptitude & Mental Ability, General Tamil, General English, Thirukkural, Current Affairs
- General Studies units defined by the canonical curriculum
- content type: study material, mock test, current affairs
- government-material signal
- language hint: English, Tamil, or mixed
- PYQ detection

This is intentionally deterministic. It does not use an LLM, fuzzy matching, embeddings, or automatic database publication.

## PYQ safety rule

Any strong PYQ signal immediately produces `excluded_pyq`. A PYQ classification is never publishable, even if another rule identifies a valid subject. PYQ detection is a safety gate, not merely a label.

Question-paper material is not deleted by this phase. It is excluded from downstream content generation/publishing and remains traceable for audit.

## Review behavior

The classifier returns `review_required` when it cannot safely determine the subject or, for General Studies, the unit. It does not invent a topic or subtopic. Topic/subtopic mapping is a later curriculum-aware phase.

## Evidence

Every matched rule is returned as an evidence term. Scores are separated by dimension rather than collapsed into a single opaque confidence number.

## Next phase

Phase 7 will build page/chunk-level evidence extraction and provenance links so that curriculum mappings and generated content can point back to exact source material.
