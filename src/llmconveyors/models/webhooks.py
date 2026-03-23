"""Webhook event models."""

from __future__ import annotations

from typing import Any

from pydantic import Field

from llmconveyors.models.common import AgentType, APIModel

# ---------------------------------------------------------------------------
# Webhook event data payloads
# ---------------------------------------------------------------------------


class CompletedData(APIModel):
    """Data payload for generation.completed webhook."""

    status: str = "completed"
    artifacts: list[dict[str, Any]] = Field(default_factory=list)


class FailedData(APIModel):
    """Data payload for generation.failed webhook."""

    status: str = "failed"
    error: str = ""


class AwaitingInputData(APIModel):
    """Data payload for generation.awaiting_input webhook."""

    status: str = "awaiting_input"
    interaction_data: dict[str, Any] = Field(default_factory=dict)


# ---------------------------------------------------------------------------
# Webhook events
# ---------------------------------------------------------------------------


class GenerationCompletedEvent(APIModel):
    """Webhook event: generation.completed."""

    event: str = "generation.completed"
    generation_id: str
    session_id: str
    agent_type: AgentType
    timestamp: str
    data: CompletedData


class GenerationFailedEvent(APIModel):
    """Webhook event: generation.failed."""

    event: str = "generation.failed"
    generation_id: str
    session_id: str
    agent_type: AgentType
    timestamp: str
    data: FailedData


class GenerationAwaitingInputEvent(APIModel):
    """Webhook event: generation.awaiting_input."""

    event: str = "generation.awaiting_input"
    generation_id: str
    session_id: str
    agent_type: AgentType
    timestamp: str
    data: AwaitingInputData


WebhookEvent = (
    GenerationCompletedEvent | GenerationFailedEvent | GenerationAwaitingInputEvent
)

ALLOWED_WEBHOOK_EVENTS = frozenset(
    {
        "generation.completed",
        "generation.failed",
        "generation.awaiting_input",
    }
)
