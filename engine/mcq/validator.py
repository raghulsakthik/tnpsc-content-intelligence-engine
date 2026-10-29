"""Deterministic structural validation for MCQs.

Semantic ambiguity and factual correctness require the Phase 11 quality layer;
this module deliberately does not pretend to solve those problems with rules.
"""

from __future__ import annotations

import hashlib
import re

from .models import MCQ, MCQValidationResult


def _normalize(text: str) -> str:
    return re.sub(r"\s+", " ", text).strip().casefold()


def fingerprint(mcq: MCQ) -> str:
    payload = "|".join(
        [_normalize(mcq.question)] + [_normalize(option.text) for option in mcq.options]
    )
    return hashlib.sha256(payload.encode("utf-8")).hexdigest()


def validate_mcq(mcq: MCQ) -> MCQValidationResult:
    errors: list[str] = []
    warnings: list[str] = []

    if mcq.is_pyq or mcq.status.value == "excluded_pyq":
        errors.append("pyq-mcq-is-not-eligible-for-publication")
    if not _normalize(mcq.question):
        errors.append("question-empty")
    if len(mcq.options) < 2:
        errors.append("minimum-two-options-required")
    if len(mcq.options) > 6:
        warnings.append("unusually-many-options")
    if not _normalize(mcq.explanation):
        errors.append("explanation-required")
    if not mcq.source_evidence_ids:
        errors.append("source-evidence-required")

    option_ids = [option.option_id for option in mcq.options]
    if len(set(option_ids)) != len(option_ids):
        errors.append("duplicate-option-id")

    option_texts = [_normalize(option.text) for option in mcq.options]
    if any(not text for text in option_texts):
        errors.append("empty-option")
    if len(set(option_texts)) != len(option_texts):
        errors.append("duplicate-option-text")

    correct_count = len(mcq.correct_options())
    if correct_count == 0:
        errors.append("no-correct-answer")
    elif correct_count > 1:
        errors.append("multiple-correct-answers")

    if correct_count == 1:
        answer = _normalize(mcq.correct_options()[0].text)
        if not answer:
            errors.append("correct-answer-empty")

    if not mcq.lesson_id:
        errors.append("lesson-id-required")
    if not mcq.curriculum_node_id:
        errors.append("curriculum-node-id-required")

    return MCQValidationResult(
        valid=not errors,
        errors=tuple(errors),
        warnings=tuple(warnings),
        fingerprint=fingerprint(mcq),
    )
