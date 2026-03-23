"""Health resource."""

from __future__ import annotations

from typing import Any

from llmconveyors.resources._base import AsyncResource, SyncResource


class HealthResource(SyncResource):
    def check(self) -> Any:
        return self._client.get("/health")

    def ready(self) -> Any:
        return self._client.get("/health/ready")

    def live(self) -> Any:
        return self._client.get("/health/live")


class AsyncHealthResource(AsyncResource):
    async def check(self) -> Any:
        return await self._client.get("/health")

    async def ready(self) -> Any:
        return await self._client.get("/health/ready")

    async def live(self) -> Any:
        return await self._client.get("/health/live")
