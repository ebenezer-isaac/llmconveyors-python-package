"""Streaming resource — SSE generation stream and health check."""

from __future__ import annotations

from collections.abc import Generator
from typing import Any

from llmconveyors._constants import SSE_READ_TIMEOUT
from llmconveyors.models.streaming import StreamEvent
from llmconveyors.resources._base import AsyncResource, SyncResource
from llmconveyors.streaming import parse_sse_lines


class StreamingResource(SyncResource):
    """Synchronous streaming resource."""

    def generation(
        self,
        generation_id: str,
        *,
        include_heartbeats: bool = False,
        include_logs: bool = True,
        last_event_id: str | None = None,
    ) -> Generator[StreamEvent, None, None]:
        """Connect to SSE stream for a generation job."""
        headers: dict[str, str] = {}
        if last_event_id:
            headers["Last-Event-ID"] = last_event_id

        with self._client.stream(
            f"/stream/generation/{generation_id}",
            headers=headers or None,
            timeout=SSE_READ_TIMEOUT,
        ) as response:
            response.read()  # type: ignore[union-attr]
            yield from parse_sse_lines(
                response.iter_lines(),  # type: ignore[union-attr]
                include_heartbeats=include_heartbeats,
                include_logs=include_logs,
            )

    def health(self) -> Any:
        """Get SSE server health. Note: returns SSE format, not JSON."""
        return self._client.get("/stream/health")


class AsyncStreamingResource(AsyncResource):
    """Asynchronous streaming resource."""

    async def generation(  # type: ignore[return]
        self,
        generation_id: str,
        *,
        include_heartbeats: bool = False,
        include_logs: bool = True,
        last_event_id: str | None = None,
    ) -> Any:
        """Connect to SSE stream for a generation job. Returns async generator."""
        headers: dict[str, str] = {}
        if last_event_id:
            headers["Last-Event-ID"] = last_event_id

        async with self._client.stream(
            f"/stream/generation/{generation_id}",
            headers=headers or None,
            timeout=SSE_READ_TIMEOUT,
        ) as response:
            async for raw_line in response.aiter_lines():
                line_bytes = raw_line.encode("utf-8") if isinstance(raw_line, str) else raw_line
                for event in parse_sse_lines(
                    iter([line_bytes]),
                    include_heartbeats=include_heartbeats,
                    include_logs=include_logs,
                ):
                    yield event

    async def health(self) -> Any:
        return await self._client.get("/stream/health")
