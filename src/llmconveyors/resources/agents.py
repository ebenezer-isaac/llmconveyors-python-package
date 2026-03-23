"""Agents resource — generate, status, interact, manifest, generate_cv, run, poll."""

from __future__ import annotations

import logging
import time
from collections.abc import Callable
from typing import TYPE_CHECKING, Any

from llmconveyors._constants import DEFAULT_POLL_INTERVAL, DEFAULT_POLL_TIMEOUT, SSE_READ_TIMEOUT
from llmconveyors.errors import TimeoutError
from llmconveyors.models.agents import (
    GenerateCVResponse,
    GenerateResponse,
    InteractResponse,
    JobStatusResponse,
    ManifestResponse,
    RunResult,
)
from llmconveyors.models.common import AgentType
from llmconveyors.models.streaming import (
    ChunkEvent,
    CompleteEvent,
    LogEvent,
    ProgressEvent,
)
from llmconveyors.resources._base import AsyncResource, SyncResource
from llmconveyors.streaming import parse_sse_lines

if TYPE_CHECKING:
    from llmconveyors.resources.streaming import AsyncStreamingResource, StreamingResource

logger = logging.getLogger("llmconveyors")

_TERMINAL_STATUSES = frozenset({"completed", "failed", "awaiting_input"})


class AgentsResource(SyncResource):
    """Synchronous agents resource."""

    _stream_resource: StreamingResource | None = None

    def _set_stream_resource(self, stream: StreamingResource) -> None:
        self._stream_resource = stream

    def generate(
        self, agent_type: AgentType, request: dict[str, Any]
    ) -> GenerateResponse:
        """Start a new generation job."""
        data = self._client.post(f"/agents/{agent_type}/generate", json=request)
        return GenerateResponse.model_validate(data)

    def generate_cv(self, request: dict[str, Any]) -> GenerateCVResponse:
        """Synchronous CV generation (200 OK, not 202)."""
        data = self._client.post("/agents/job-hunter/generate-cv", json=request)
        return GenerateCVResponse.model_validate(data)

    def get_status(
        self,
        agent_type: AgentType,
        job_id: str,
        *,
        include: str | None = None,
    ) -> JobStatusResponse:
        """Get generation job status and results."""
        params: dict[str, Any] = {}
        if include:
            params["include"] = include
        data = self._client.get(
            f"/agents/{agent_type}/status/{job_id}", params=params or None
        )
        return JobStatusResponse.model_validate(data)

    def interact(
        self, agent_type: AgentType, request: dict[str, Any]
    ) -> InteractResponse:
        """Submit phased interaction. Returns NEW jobId + streamUrl for Phase B."""
        data = self._client.post(f"/agents/{agent_type}/interact", json=request)
        return InteractResponse.model_validate(data)

    def get_manifest(self, agent_type: AgentType) -> ManifestResponse:
        """Get agent capabilities, billing, and input fields."""
        data = self._client.get(f"/agents/{agent_type}/manifest")
        return ManifestResponse.model_validate(data)

    def poll(
        self,
        agent_type: AgentType,
        job_id: str,
        *,
        interval: float = DEFAULT_POLL_INTERVAL,
        timeout: float = DEFAULT_POLL_TIMEOUT,
        include: str | None = None,
    ) -> JobStatusResponse:
        """Poll for job completion. Blocks until terminal state."""
        start = time.monotonic()
        while True:
            status = self.get_status(agent_type, job_id, include=include)
            if status.status in _TERMINAL_STATUSES:
                return status
            elapsed = time.monotonic() - start
            if elapsed + interval > timeout:
                raise TimeoutError(
                    f"Poll timeout after {elapsed:.0f}s (status: {status.status})"
                )
            time.sleep(interval)

    def run(
        self,
        agent_type: AgentType,
        request: dict[str, Any],
        *,
        on_progress: Callable[[ProgressEvent], None] | None = None,
        on_chunk: Callable[[ChunkEvent], None] | None = None,
        on_log: Callable[[LogEvent], None] | None = None,
        interaction_handler: Callable[[str, dict[str, Any]], dict[str, Any]] | None = None,
    ) -> RunResult:
        """High-level: generate + stream + interact (if phased).

        Returns RunResult with artifacts on completion.
        """
        gen = self.generate(agent_type, request)
        return self._stream_to_completion(
            agent_type,
            gen.generation_id,
            gen.session_id,
            on_progress=on_progress,
            on_chunk=on_chunk,
            on_log=on_log,
            interaction_handler=interaction_handler,
        )

    def _stream_to_completion(
        self,
        agent_type: AgentType,
        generation_id: str,
        session_id: str,
        *,
        on_progress: Callable[[ProgressEvent], None] | None = None,
        on_chunk: Callable[[ChunkEvent], None] | None = None,
        on_log: Callable[[LogEvent], None] | None = None,
        interaction_handler: Callable[[str, dict[str, Any]], dict[str, Any]] | None = None,
    ) -> RunResult:
        """Stream events and handle phased interactions."""
        with self._client.stream(
            f"/stream/generation/{generation_id}",
            timeout=SSE_READ_TIMEOUT,
        ) as response:
            response.read()  # type: ignore[union-attr]
            for event in parse_sse_lines(
                response.iter_lines(),  # type: ignore[union-attr]
                include_logs=on_log is not None,
            ):
                if isinstance(event, ProgressEvent) and on_progress:
                    on_progress(event)
                elif isinstance(event, ChunkEvent) and on_chunk:
                    on_chunk(event)
                elif isinstance(event, LogEvent) and on_log:
                    on_log(event)
                elif isinstance(event, CompleteEvent):
                    if event.awaiting_input and interaction_handler:
                        interaction_data = interaction_handler(
                            event.interaction_type or "",
                            event.interaction_data or {},
                        )
                        self.interact(
                            agent_type,
                            {
                                "generationId": generation_id,
                                "sessionId": session_id,
                                "interactionType": event.interaction_type or "",
                                "interactionData": interaction_data,
                            },
                        )
                        # Recurse for Phase B with new stream
                        return self._stream_to_completion(
                            agent_type,
                            generation_id,
                            session_id,
                            on_progress=on_progress,
                            on_chunk=on_chunk,
                            on_log=on_log,
                            interaction_handler=interaction_handler,
                        )
                    return RunResult(
                        success=event.success,
                        artifacts=event.artifacts,
                        warnings=event.warnings or [],
                        session_id=session_id,
                        generation_id=generation_id,
                    )

        return RunResult(success=False, session_id=session_id, generation_id=generation_id)


class AsyncAgentsResource(AsyncResource):
    """Asynchronous agents resource."""

    _stream_resource: AsyncStreamingResource | None = None

    def _set_stream_resource(self, stream: AsyncStreamingResource) -> None:
        self._stream_resource = stream

    async def generate(
        self, agent_type: AgentType, request: dict[str, Any]
    ) -> GenerateResponse:
        data = await self._client.post(f"/agents/{agent_type}/generate", json=request)
        return GenerateResponse.model_validate(data)

    async def generate_cv(self, request: dict[str, Any]) -> GenerateCVResponse:
        data = await self._client.post("/agents/job-hunter/generate-cv", json=request)
        return GenerateCVResponse.model_validate(data)

    async def get_status(
        self,
        agent_type: AgentType,
        job_id: str,
        *,
        include: str | None = None,
    ) -> JobStatusResponse:
        params: dict[str, Any] = {}
        if include:
            params["include"] = include
        data = await self._client.get(
            f"/agents/{agent_type}/status/{job_id}", params=params or None
        )
        return JobStatusResponse.model_validate(data)

    async def interact(
        self, agent_type: AgentType, request: dict[str, Any]
    ) -> InteractResponse:
        data = await self._client.post(f"/agents/{agent_type}/interact", json=request)
        return InteractResponse.model_validate(data)

    async def get_manifest(self, agent_type: AgentType) -> ManifestResponse:
        data = await self._client.get(f"/agents/{agent_type}/manifest")
        return ManifestResponse.model_validate(data)

    async def poll(
        self,
        agent_type: AgentType,
        job_id: str,
        *,
        interval: float = DEFAULT_POLL_INTERVAL,
        timeout: float = DEFAULT_POLL_TIMEOUT,
        include: str | None = None,
    ) -> JobStatusResponse:
        import asyncio

        start = time.monotonic()
        while True:
            status = await self.get_status(agent_type, job_id, include=include)
            if status.status in _TERMINAL_STATUSES:
                return status
            elapsed = time.monotonic() - start
            if elapsed + interval > timeout:
                raise TimeoutError(
                    f"Poll timeout after {elapsed:.0f}s (status: {status.status})"
                )
            await asyncio.sleep(interval)

    async def run(
        self,
        agent_type: AgentType,
        request: dict[str, Any],
        *,
        on_progress: Callable[[ProgressEvent], None] | None = None,
        on_chunk: Callable[[ChunkEvent], None] | None = None,
        on_log: Callable[[LogEvent], None] | None = None,
        interaction_handler: Callable[[str, dict[str, Any]], Any] | None = None,
    ) -> RunResult:
        gen = await self.generate(agent_type, request)
        return await self._stream_to_completion(
            agent_type,
            gen.generation_id,
            gen.session_id,
            on_progress=on_progress,
            on_chunk=on_chunk,
            on_log=on_log,
            interaction_handler=interaction_handler,
        )

    async def _stream_to_completion(
        self,
        agent_type: AgentType,
        generation_id: str,
        session_id: str,
        *,
        on_progress: Callable[[ProgressEvent], None] | None = None,
        on_chunk: Callable[[ChunkEvent], None] | None = None,
        on_log: Callable[[LogEvent], None] | None = None,
        interaction_handler: Callable[[str, dict[str, Any]], Any] | None = None,
    ) -> RunResult:
        async with self._client.stream(
            f"/stream/generation/{generation_id}",
            timeout=SSE_READ_TIMEOUT,
        ) as response:
            async for raw_line in response.aiter_lines():
                line_bytes = raw_line.encode("utf-8") if isinstance(raw_line, str) else raw_line
                for event in parse_sse_lines(iter([line_bytes]), include_logs=on_log is not None):
                    if isinstance(event, ProgressEvent) and on_progress:
                        on_progress(event)
                    elif isinstance(event, ChunkEvent) and on_chunk:
                        on_chunk(event)
                    elif isinstance(event, LogEvent) and on_log:
                        on_log(event)
                    elif isinstance(event, CompleteEvent):
                        if event.awaiting_input and interaction_handler:
                            result = interaction_handler(
                                event.interaction_type or "",
                                event.interaction_data or {},
                            )
                            if hasattr(result, "__await__"):
                                result = await result
                            await self.interact(
                                agent_type,
                                {
                                    "generationId": generation_id,
                                    "sessionId": session_id,
                                    "interactionType": event.interaction_type or "",
                                    "interactionData": result,
                                },
                            )
                            return await self._stream_to_completion(
                                agent_type,
                                generation_id,
                                session_id,
                                on_progress=on_progress,
                                on_chunk=on_chunk,
                                on_log=on_log,
                                interaction_handler=interaction_handler,
                            )
                        return RunResult(
                            success=event.success,
                            artifacts=event.artifacts,
                            warnings=event.warnings or [],
                            session_id=session_id,
                            generation_id=generation_id,
                        )

        return RunResult(success=False, session_id=session_id, generation_id=generation_id)
