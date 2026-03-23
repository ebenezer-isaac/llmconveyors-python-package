"""Share link models."""

from __future__ import annotations

from llmconveyors.models.common import APIModel


class ShareCreate(APIModel):
    """Request body for POST /shares."""

    model_config = APIModel.model_config.copy()
    model_config["extra"] = "allow"


class ShareCreateResponse(APIModel):
    """Response from POST /shares."""

    model_config = APIModel.model_config.copy()
    model_config["extra"] = "allow"


class ShareStats(APIModel):
    """A share entry from GET /shares/stats."""

    model_config = APIModel.model_config.copy()
    model_config["extra"] = "allow"


class PublicShare(APIModel):
    """Response from GET /shares/:slug/public."""

    model_config = APIModel.model_config.copy()
    model_config["extra"] = "allow"


class ShareVisitStats(APIModel):
    """Response from GET /shares/:slug/stats."""

    model_config = APIModel.model_config.copy()
    model_config["extra"] = "allow"
