"""Content management models."""

from __future__ import annotations

from llmconveyors.models.common import APIModel


class SaveContentRequest(APIModel):
    """Request body for POST /content/save."""

    model_config = APIModel.model_config.copy()
    model_config["extra"] = "allow"


class SaveContentResponse(APIModel):
    """Response from POST /content/save."""

    model_config = APIModel.model_config.copy()
    model_config["extra"] = "allow"


class DeleteGenerationParams(APIModel):
    """Query params for DELETE /content/generations/:id."""

    session_id: str
