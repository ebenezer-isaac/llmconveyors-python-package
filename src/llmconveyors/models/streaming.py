"""SSE streaming event models."""

from __future__ import annotations

from typing import Any

from pydantic import Field

from llmconveyors.models.common import APIModel, LogLevel

# ---------------------------------------------------------------------------
# SSE event models
# ---------------------------------------------------------------------------


class ProgressEvent(APIModel):
    """Step progress notification (0-100%)."""

    job_id: str
    session_id: str
    step: str
    percent: int = Field(ge=0, le=100)
    message: str | None = None


class ChunkEvent(APIModel):
    """Streaming content chunk from LLM generation."""

    job_id: str
    session_id: str
    chunk: str
    index: int


class CompleteEvent(APIModel):
    """Generation finished — includes artifacts and status.

    When awaitingInput is True, this is a PHASE BOUNDARY (not terminal).
    The client should display interaction UI and call interact().
    """

    job_id: str
    session_id: str
    success: bool
    artifacts: list[dict[str, Any]] = Field(default_factory=list)

    # Optional fields
    generation_id: str | None = None
    error: str | None = None
    warnings: list[str] | None = None
    awaiting_input: bool | None = None
    interaction_type: str | None = None
    completed_phase: int | None = None
    interaction_data: dict[str, Any] | None = None
    persistence_warning: bool | None = None
    merged_artifact_state: dict[str, Any] | None = None


class SSEErrorEvent(APIModel):
    """Generation error with machine-readable code."""

    job_id: str
    session_id: str
    code: str
    message: str


class LogEvent(APIModel):
    """Structured log message for debugging UI."""

    message_id: str
    generation_id: str
    session_id: str
    content: str
    level: LogLevel
    timestamp: str


class HeartbeatEvent(APIModel):
    """Keep-alive during long operations. Clients should ignore."""

    job_id: str
    session_id: str
    timestamp: str


# Discriminated union of all SSE event types
StreamEvent = (
    ProgressEvent
    | ChunkEvent
    | CompleteEvent
    | SSEErrorEvent
    | LogEvent
    | HeartbeatEvent
)
