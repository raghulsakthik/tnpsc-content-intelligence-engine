"""Conservative MCQ construction from source-backed evidence."""

from __future__ import annotations

import hashlib
import re
from collections.abc import Iterable

from .models import Difficulty, MCQ, MCQOption, MCQStatus


def _clean(text: str) -> str:
    return re.sub(r"\s+", " ", text).strip()


def mcq_id(lesson_id: str, question: str, version: int = 1) -> str:
    key = f"{lesson_id}|{_clean(question).lower()}|{version}"
    return hashlib.sha256(key.encode("utf-8")).hexdigest()[:24]


def build_mcq(
    *,
    lesson_id: str,
    curriculum_node_id: str,
    question: str,
    options: Iterable[MCQOption],
    explanation: str,
    difficulty: Difficulty,
    source_evidence_ids: Iterable[str] = (),
    is_pyq: bool = False,
    version: int = 1,
) -> MCQ:
    """Build a draft MCQ; validation and approval are separate operations."""
    sources = tuple(dict.fromkeys(source_id for source_id in source_evidence_ids if source_id))
    status = MCQStatus.EXCLUDED_PYQ if is_pyq else MCQStatus.DRAFT
    return MCQ(
        mcq_id=mcq_id(lesson_id, question, version),
        lesson_id=lesson_id,
        curriculum_node_id=curriculum_node_id,
        question=_clean(question),
        options=tuple(
            MCQOption(option_id=_clean(option.option_id), text=_clean(option.text), is_correct=option.is_correct)
            for option in options
        ),
        explanation=_clean(explanation),
        difficulty=difficulty,
        source_evidence_ids=sources,
        is_pyq=is_pyq,
        status=status,
        version=version,
    )
