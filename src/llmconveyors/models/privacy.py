"""Privacy and consent models."""

from __future__ import annotations

from llmconveyors.models.common import APIModel


class Consent(APIModel):
    """A consent record."""

    model_config = APIModel.model_config.copy()
    model_config["extra"] = "allow"
