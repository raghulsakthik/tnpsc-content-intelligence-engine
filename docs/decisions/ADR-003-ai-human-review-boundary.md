# ADR-003: AI Is a Proposal System, Not the Publication Authority

## Status
Accepted

## Decision

AI may generate or classify proposals, but publication requires deterministic validation and the configured human/admin review gate.

## AI may propose

- subject/topic mapping
- summaries
- lesson structure
- examples
- MCQs and distractors
- difficulty
- duplicate candidates
- conflict candidates

## AI may not autonomously

- publish content
- delete evidence
- bypass PYQ exclusion
- overwrite approved content
- change curriculum definitions
- alter learner marks/mastery
- execute arbitrary database/tool operations

## Consequence

Every AI-generated artifact is a reviewable version with reproducibility metadata.
