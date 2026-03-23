"""Logging resource — forward client logs."""

from __future__ import annotations

from typing import Any

from llmconveyors.resources._base import AsyncResource, SyncResource


class LoggingResource(SyncResource):
    def send(self, request: dict[str, Any]) -> Any:
        return self._client.post("/log", json=request)


class AsyncLoggingResource(AsyncResource):
    async def send(self, request: dict[str, Any]) -> Any:
        return await self._client.post("/log", json=request)
