"""Deterministic curriculum/content classification."""

from .classifier import classify_text
from .models import ClassificationDecision, ClassificationStatus

__all__ = ["classify_text", "ClassificationDecision", "ClassificationStatus"]
