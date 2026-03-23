"""Auth models (GDPR export/delete)."""

from __future__ import annotations

from llmconveyors.models.common import APIModel


class ExportDataResponse(APIModel):
    """Response from GET /auth/export."""

    model_config = APIModel.model_config.copy()
    model_config["extra"] = "allow"
