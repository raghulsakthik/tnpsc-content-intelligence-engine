"""Contracts connecting material retrieval with content intelligence."""

from .models import IngestionEnvelope, IngestionStatus
from .pipeline import IntegrationPipeline

__all__ = ["IngestionEnvelope", "IngestionStatus", "IntegrationPipeline"]
