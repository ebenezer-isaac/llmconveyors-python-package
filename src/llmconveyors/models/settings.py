"""Settings, API key, and usage models."""

from __future__ import annotations

from pydantic import Field

from llmconveyors.models.common import APIModel, Tier

# ---------------------------------------------------------------------------
# Profile
# ---------------------------------------------------------------------------


class Profile(APIModel):
    """Response from GET /settings/profile."""

    credits: float
    tier: Tier
    byo_key_enabled: bool


# ---------------------------------------------------------------------------
# Preferences
# ---------------------------------------------------------------------------


class Preferences(APIModel):
    """Response from GET/POST /settings/preferences.

    Shape varies — allow extra fields.
    """

    model_config = APIModel.model_config.copy()
    model_config["extra"] = "allow"


# ---------------------------------------------------------------------------
# API keys
# ---------------------------------------------------------------------------


class APIKeyCreate(APIModel):
    """Request body for POST /settings/platform-api-keys."""

    label: str
    scopes: list[str]
    expiry: str | None = None
    credit_limit: int | None = None


class APIKeyInfo(APIModel):
    """An API key entry from list or create response."""

    hash: str = ""
    label: str = ""
    scopes: list[str] = Field(default_factory=list)
    created_at: str | None = None
    expires_at: str | None = None
    last_used_at: str | None = None
    key: str | None = None  # Only present on create response

    model_config = APIModel.model_config.copy()
    model_config["extra"] = "allow"


class APIKeyRotate(APIModel):
    """Request body for POST /settings/platform-api-keys/:hash/rotate."""

    grace_period_hours: int = 0


class APIKeyUsage(APIModel):
    """Response from GET /settings/platform-api-keys/:hash/usage."""

    model_config = APIModel.model_config.copy()
    model_config["extra"] = "allow"


# ---------------------------------------------------------------------------
# BYO key
# ---------------------------------------------------------------------------


class BYOKeyStatus(APIModel):
    """Response from GET /settings/api-key."""

    model_config = APIModel.model_config.copy()
    model_config["extra"] = "allow"


class BYOKeySet(APIModel):
    """Request body for POST /settings/api-key."""

    key: str = Field(min_length=30, max_length=256)


# ---------------------------------------------------------------------------
# Usage
# ---------------------------------------------------------------------------


class UsageLog(APIModel):
    """A single usage log entry."""

    model_config = APIModel.model_config.copy()
    model_config["extra"] = "allow"


class UsageSummary(APIModel):
    """Response from GET /settings/usage-summary."""

    total_credits_used: float
    total_generations: int
    average_credits_per_generation: float


# ---------------------------------------------------------------------------
# Webhook secret
# ---------------------------------------------------------------------------


class WebhookSecretResponse(APIModel):
    """Response from GET/POST /settings/webhook-secret."""

    model_config = APIModel.model_config.copy()
    model_config["extra"] = "allow"
