"""Curriculum-gap signals that can be fed back to material discovery."""

from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class CurriculumGap:
    curriculum_node_id: str
    reason: str
    priority: int = 0
    preferred_language: str | None = None


def rank_gaps(gaps: list[CurriculumGap]) -> tuple[CurriculumGap, ...]:
    """Deterministically rank gaps; discovery remains a separate engine concern."""
    return tuple(sorted(gaps, key=lambda g: (-g.priority, g.curriculum_node_id)))
