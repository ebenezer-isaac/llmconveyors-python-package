"""Referral models."""

from __future__ import annotations

from llmconveyors.models.common import APIModel


class ReferralStats(APIModel):
    """Response from GET /referral/stats."""

    model_config = APIModel.model_config.copy()
    model_config["extra"] = "allow"


class ReferralCode(APIModel):
    """Response from GET /referral/code."""

    model_config = APIModel.model_config.copy()
    model_config["extra"] = "allow"


class SetVanityCodeRequest(APIModel):
    """Request body for POST /referral/vanity-code."""

    code: str
