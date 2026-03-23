"""Client logging models."""

from __future__ import annotations

from llmconveyors.models.common import APIModel


class SendLogRequest(APIModel):
    """Request body for POST /log."""

    model_config = APIModel.model_config.copy()
    model_config["extra"] = "allow"
