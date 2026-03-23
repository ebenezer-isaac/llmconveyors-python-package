"""SSE stream parser and consumer.

CRITICAL: The server uses NestJS @Sse() which emits ONLY id: + data: lines.
There is NO SSE event: field. The event type is INSIDE the JSON payload:
    data: {"event":"progress","data":{"jobId":"...","step":"Research","percent":5}}

Standard SSE libraries (sseclient, sseclient-py) will SILENTLY DROP all events
because they route on the `event:` field which does not exist.
"""

from __future__ import annotations

import json
import logging
from collections.abc import Generator
from typing import Any

from llmconveyors.errors import (
    LLMConveyorsError,
    ServerRestartingError,
    SessionDeletedError,
    StreamError,
    StreamNotFoundError,
)
from llmconveyors.models.streaming import (
    ChunkEvent,
    CompleteEvent,
    HeartbeatEvent,
    LogEvent,
    ProgressEvent,
    SSEErrorEvent,
    StreamEvent,
)

logger = logging.getLogger("llmconveyors")

# SSE error codes that are terminal (no reconnect)
_TERMINAL_SSE_CODES = frozenset({"STREAM_NOT_FOUND", "SESSION_DELETED"})

# Map SSE error codes to exception classes
_SSE_ERROR_MAP: dict[str, type[LLMConveyorsError]] = {
    "SERVER_RESTARTING": ServerRestartingError,
    "STREAM_NOT_FOUND": StreamNotFoundError,
    "STREAM_ERROR": StreamError,
    "SESSION_DELETED": SessionDeletedError,
}

# Map event type strings to Pydantic model classes
_EVENT_MODEL_MAP: dict[str, type[Any]] = {
    "progress": ProgressEvent,
    "chunk": ChunkEvent,
    "complete": CompleteEvent,
    "error": SSEErrorEvent,
    "log": LogEvent,
    "heartbeat": HeartbeatEvent,
}


def _parse_sse_event(data_payload: dict[str, Any]) -> StreamEvent | None:
    """Parse a JSON SSE payload into a typed StreamEvent.

    The payload has shape: {"event": "progress", "data": {...}}
    """
    event_type = data_payload.get("event", "")
    event_data = data_payload.get("data", {})

    model_cls = _EVENT_MODEL_MAP.get(event_type)
    if model_cls is None:
        # Unknown event type — skip gracefully
        logger.debug("Skipping unknown SSE event type: %s", event_type)
        return None

    return model_cls.model_validate(event_data)


def parse_sse_lines(
    lines: Generator[bytes, None, None] | Any,
    *,
    include_heartbeats: bool = False,
    include_logs: bool = True,
) -> Generator[StreamEvent, None, None]:
    """Parse raw SSE byte lines into typed StreamEvent objects.

    Args:
        lines: Iterator of raw byte lines from an HTTP streaming response.
        include_heartbeats: Whether to yield heartbeat events.
        include_logs: Whether to yield log events.

    Yields:
        StreamEvent objects for each valid SSE data line.

    Raises:
        StreamError subclasses for terminal SSE error events.
    """
    _last_event_id_holder: list[str] = [""]  # Mutable holder for reconnection tracking
    first_chunk = True

    for raw_line in lines:
        if not raw_line:
            continue

        # Decode bytes to string
        if isinstance(raw_line, bytes):
            line = raw_line.decode("utf-8", errors="replace")
        else:
            line = raw_line

        # Strip BOM from first chunk
        if first_chunk:
            line = line.lstrip("\ufeff")
            first_chunk = False

        # Normalize line endings
        line = line.rstrip("\r\n")

        if not line:
            continue

        # Track event ID for reconnection
        if line.startswith("id:"):
            _last_event_id_holder[0] = line[3:].strip()
            continue

        # Skip comment lines
        if line.startswith(":"):
            continue

        # Parse data lines
        if not line.startswith("data:"):
            continue

        # Extract JSON after "data:" or "data: "
        raw_data = line[5:].lstrip(" ")
        if not raw_data:
            continue

        try:
            payload = json.loads(raw_data)
        except json.JSONDecodeError:
            logger.warning("Failed to parse SSE JSON: %s", raw_data[:200])
            continue

        event = _parse_sse_event(payload)
        if event is None:
            continue

        # Handle error events — raise as exceptions for terminal codes
        if isinstance(event, SSEErrorEvent):
            exc_cls = _SSE_ERROR_MAP.get(event.code, StreamError)
            raise exc_cls(event.message, code=event.code)

        # Filter heartbeats
        if isinstance(event, HeartbeatEvent) and not include_heartbeats:
            continue

        # Filter logs
        if isinstance(event, LogEvent) and not include_logs:
            continue

        yield event


def get_last_event_id(
    lines: Generator[bytes, None, None] | Any,
) -> str:
    """Extract the last event ID from SSE lines without consuming events.

    This is a utility for reconnection tracking.
    """
    last_id = ""
    for raw_line in lines:
        if isinstance(raw_line, bytes):
            line = raw_line.decode("utf-8", errors="replace").strip()
        else:
            line = str(raw_line).strip()
        if line.startswith("id:"):
            last_id = line[3:].strip()
    return last_id
