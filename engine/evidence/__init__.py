"""Evidence extraction and provenance primitives."""

from .models import Evidence, EvidenceSpan, EvidenceType
from .extractor import extract_evidence

__all__ = ["Evidence", "EvidenceSpan", "EvidenceType", "extract_evidence"]
