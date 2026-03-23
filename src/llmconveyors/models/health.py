"""Health check models."""

from __future__ import annotations

from llmconveyors.models.common import APIModel


class HealthResponse(APIModel):
    """Response from GET /health."""

    model_config = APIModel.model_config.copy()
    model_config["extra"] = "allow"
