"""Conservative quality checks for generated learning content.

This module intentionally does not claim semantic fact verification. It
checks provenance, structure, unsupported claims, and obvious contradictions
that can be detected deterministically. Semantic review remains a human/AI
review concern and is represented as REVIEW rather than PASS.
"""

from __future__ import annotations

import re
from collections.abc import Iterable

from .models import CheckSeverity, QualityCheck, QualityReport, QualityStatus


def _norm(text: str) -> str:
    return re.sub(r"\s+", " ", text).strip().casefold()


def _check_nonempty(name: str, value: str, message: str) -> QualityCheck:
    if _norm(value):
        return QualityCheck(name, QualityStatus.PASS, CheckSeverity.INFO, "present")
    return QualityCheck(name, QualityStatus.FAIL, CheckSeverity.ERROR, message)


def check_lesson(*, lesson_id: str, title: str, concept: str,
                 explanation: str, source_ids: Iterable[str]) -> QualityReport:
    sources = tuple(dict.fromkeys(x for x in source_ids if x))
    checks = (
        _check_nonempty("title", title, "lesson title is empty"),
        _check_nonempty("concept", concept, "lesson concept is empty"),
        _check_nonempty("explanation", explanation, "lesson explanation is empty"),
        QualityCheck(
            "source-provenance",
            QualityStatus.PASS if sources else QualityStatus.FAIL,
            CheckSeverity.INFO if sources else CheckSeverity.ERROR,
            "lesson has source evidence" if sources else "lesson has no source evidence",
            sources,
        ),
        QualityCheck(
            "semantic-review",
            QualityStatus.REVIEW,
            CheckSeverity.WARNING,
            "semantic factual accuracy requires evidence-aware review",
            sources,
        ),
    )
    return QualityReport(lesson_id, checks, {"source_count": len(sources)})


def check_mcq(*, mcq_id: str, question: str, options: Iterable[str],
              correct_option_ids: Iterable[str], explanation: str,
              source_ids: Iterable[str], is_pyq: bool = False) -> QualityReport:
    options_tuple = tuple(options)
    correct = tuple(dict.fromkeys(x for x in correct_option_ids if x))
    normalized_options = tuple(_norm(x) for x in options_tuple)
    checks: list[QualityCheck] = [
        _check_nonempty("question", question, "MCQ question is empty"),
        _check_nonempty("explanation", explanation, "MCQ explanation is empty"),
    ]
    checks.append(QualityCheck(
        "option-uniqueness",
        QualityStatus.PASS if len(normalized_options) == len(set(normalized_options)) else QualityStatus.FAIL,
        CheckSeverity.INFO if len(normalized_options) == len(set(normalized_options)) else CheckSeverity.ERROR,
        "options are unique" if len(normalized_options) == len(set(normalized_options)) else "duplicate options detected",
    ))
    checks.append(QualityCheck(
        "single-correct-answer",
        QualityStatus.PASS if len(correct) == 1 else QualityStatus.FAIL,
        CheckSeverity.INFO if len(correct) == 1 else CheckSeverity.ERROR,
        "exactly one correct option declared" if len(correct) == 1 else "MCQ must declare exactly one correct option",
    ))
    sources = tuple(dict.fromkeys(x for x in source_ids if x))
    checks.append(QualityCheck(
        "source-provenance",
        QualityStatus.PASS if sources else QualityStatus.FAIL,
        CheckSeverity.INFO if sources else CheckSeverity.ERROR,
        "MCQ has source evidence" if sources else "MCQ has no source evidence",
        sources,
    ))
    checks.append(QualityCheck(
        "pyq-contamination",
        QualityStatus.FAIL if is_pyq else QualityStatus.PASS,
        CheckSeverity.ERROR if is_pyq else CheckSeverity.INFO,
        "PYQ content is forbidden" if is_pyq else "not marked as PYQ",
    ))
    checks.append(QualityCheck(
        "semantic-review",
        QualityStatus.REVIEW,
        CheckSeverity.WARNING,
        "answer correctness, ambiguity, and distractor quality require semantic review",
        sources,
    ))
    return QualityReport(mcq_id, tuple(checks), {"option_count": len(options_tuple), "source_count": len(sources)})
