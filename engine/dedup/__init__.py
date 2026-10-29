"""Deduplication and source-conflict detection."""

from .detector import DeduplicationDetector
from .models import ConflictCandidate, DuplicateCandidate, DuplicateKind

__all__ = ["ConflictCandidate", "DeduplicationDetector", "DuplicateCandidate", "DuplicateKind"]
