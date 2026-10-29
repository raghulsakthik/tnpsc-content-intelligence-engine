"""Deterministic Phase 6 classifier.

The classifier produces a reviewable decision. It does not publish content,
call an LLM, write to a database, or infer unsupported curriculum nodes.
"""

from __future__ import annotations

import re
from typing import Iterable

from .models import ClassificationDecision, ClassificationScores, ClassificationStatus
from .rules import (
    CURRENT_AFFAIRS_RULES,
    GOVERNMENT_RULES,
    LANGUAGE_RULES,
    MOCK_RULES,
    PYQ_RULES,
    SUBJECT_RULES,
    UNIT_RULES,
)

EXAM = "TNPSC_GROUP_2_2A"


def _normalize(text: str) -> str:
    return re.sub(r"\s+", " ", text.casefold()).strip()


def _hits(text: str, rules: Iterable[str]) -> tuple[str, ...]:
    return tuple(rule for rule in rules if rule.casefold() in text)


def _best_group(text: str, groups: dict[str, tuple[str, ...]]) -> tuple[str | None, tuple[str, ...], float]:
    scored: list[tuple[int, str, tuple[str, ...]]] = []
    for key, rules in groups.items():
        hits = _hits(text, rules)
        if hits:
            scored.append((len(hits), key, hits))
    if not scored:
        return None, (), 0.0
    scored.sort(key=lambda item: (-item[0], item[1]))
    best = scored[0]
    score = min(1.0, best[0] / 3.0)
    return best[1], best[2], score


def _language(text: str) -> str | None:
    ta = len(_hits(text, LANGUAGE_RULES["ta"]))
    en = len(_hits(text, LANGUAGE_RULES["en"]))
    if ta and en:
        return "mixed"
    if ta:
        return "ta"
    if en:
        return "en"
    return None


def classify_text(
    text: str,
    *,
    document_id: str | None = None,
    exam: str = EXAM,
) -> ClassificationDecision:
    """Classify one document/chunk using explicit deterministic rules.

    PYQ signals are a hard exclusion. Ties or missing curriculum mappings are
    sent to review rather than guessed.
    """
    normalized = _normalize(text)
    pyq_hits = _hits(normalized, PYQ_RULES)
    mock_hits = _hits(normalized, MOCK_RULES)
    current_hits = _hits(normalized, CURRENT_AFFAIRS_RULES)
    government_hits = _hits(normalized, GOVERNMENT_RULES)

    subject, subject_hits, subject_score = _best_group(normalized, SUBJECT_RULES)
    unit, unit_hits, unit_score = _best_group(normalized, UNIT_RULES)
    language = _language(normalized)

    is_pyq = bool(pyq_hits)
    is_mock = bool(mock_hits)
    is_current = bool(current_hits)
    is_government = bool(government_hits)

    content_type: str | None = None
    if is_mock:
        content_type = "mock_test"
    elif is_current:
        content_type = "current_affairs"
    elif subject:
        content_type = "study_material"

    reasons: list[str] = []
    status = ClassificationStatus.CLASSIFIED
    if is_pyq:
        status = ClassificationStatus.EXCLUDED_PYQ
        reasons.append("pyq-signal-detected")
    else:
        if subject is None:
            reasons.append("subject-not-determined")
        if unit is None and subject == "general-studies":
            reasons.append("general-studies-unit-not-determined")
        if subject is None or (subject == "general-studies" and unit is None):
            status = ClassificationStatus.REVIEW_REQUIRED

    evidence = tuple(sorted(set(pyq_hits + mock_hits + current_hits + government_hits + subject_hits + unit_hits)))
    scores = ClassificationScores(
        subject=subject_score,
        unit=unit_score,
        content_type=1.0 if content_type else 0.0,
        pyq=1.0 if is_pyq else 0.0,
        government_material=1.0 if is_government else 0.0,
    )

    return ClassificationDecision(
        document_id=document_id,
        exam=exam,
        subject=subject,
        unit=unit,
        topic=None,
        subtopic=None,
        language=language,
        content_type=content_type,
        is_pyq=is_pyq,
        is_mock=is_mock,
        is_current_affair=is_current,
        is_government_material=is_government,
        evidence_terms=evidence,
        scores=scores,
        status=status,
        review_reasons=tuple(reasons),
    )
