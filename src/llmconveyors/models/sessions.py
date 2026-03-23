"""Session management models."""

from __future__ import annotations

from typing import Any

from pydantic import Field

from llmconveyors.models.common import APIModel, SessionLogRole

# ---------------------------------------------------------------------------
# Session
# ---------------------------------------------------------------------------


class Session(APIModel):
    """A generation session.

    Note: agentType is inside metadata, not a top-level field.
    Session status values differ from job status (e.g., 'active', 'completed').
    """

    id: str
    user_id: str | None = None
    status: str | None = None  # Session statuses: active, completed, etc.
    created_at: str | None = None
    updated_at: str | None = None
    metadata: dict[str, Any] | None = None
    chat_history: list[dict[str, Any]] | None = None


class SessionCreate(APIModel):
    """Request body for POST /sessions.

    All fields are optional — an empty body creates a valid session.
    """

    id: str | None = None
    metadata: dict[str, Any] | None = None


# ---------------------------------------------------------------------------
# Session hydration
# ---------------------------------------------------------------------------


class SessionHydration(APIModel):
    """Response from GET /sessions/:id/hydrate.

    CRITICAL: The field is `generationLogs`, NOT `logs`.
    """

    session: Session
    artifacts: list[dict[str, Any]] = Field(default_factory=list)
    generation_logs: list[dict[str, Any]] = Field(default_factory=list)
    active_generation: dict[str, Any] | None = None
    cv_versions: list[dict[str, Any]] = Field(default_factory=list)
    cover_letter_versions: list[dict[str, Any]] = Field(default_factory=list)
    cold_email_versions: list[dict[str, Any]] = Field(default_factory=list)
    ats_versions: list[dict[str, Any]] = Field(default_factory=list)


# ---------------------------------------------------------------------------
# Session init
# ---------------------------------------------------------------------------


class SessionInitResponse(APIModel):
    """Response from GET /sessions/init."""

    # Flexible — server returns profile, sessions, strategies, etc.
    # Keep as dict since exact shape varies
    model_config = APIModel.model_config.copy()
    model_config["extra"] = "allow"


# ---------------------------------------------------------------------------
# Session log
# ---------------------------------------------------------------------------


class AppendLogRequest(APIModel):
    """Request body for POST /sessions/:id/log."""

    role: SessionLogRole
    content: str | None = Field(None, max_length=100_000)
    payload: dict[str, Any] | None = None
