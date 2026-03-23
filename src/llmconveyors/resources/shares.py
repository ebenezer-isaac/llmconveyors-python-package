"""Shares resource — 5 endpoints."""

from __future__ import annotations

from typing import Any

from llmconveyors.resources._base import AsyncResource, SyncResource


class SharesResource(SyncResource):
    def create(self, request: dict[str, Any]) -> Any:
        return self._client.post("/shares", json=request)

    def get_stats(self) -> Any:
        return self._client.get("/shares/stats")

    def get_public(self, slug: str) -> Any:
        return self._client.get(f"/shares/{slug}/public")

    def record_visit(self, slug: str) -> Any:
        return self._client.post(f"/shares/{slug}/visit", json={})

    def get_share_stats(self, slug: str) -> Any:
        return self._client.get(f"/shares/{slug}/stats")


class AsyncSharesResource(AsyncResource):
    async def create(self, request: dict[str, Any]) -> Any:
        return await self._client.post("/shares", json=request)

    async def get_stats(self) -> Any:
        return await self._client.get("/shares/stats")

    async def get_public(self, slug: str) -> Any:
        return await self._client.get(f"/shares/{slug}/public")

    async def record_visit(self, slug: str) -> Any:
        return await self._client.post(f"/shares/{slug}/visit", json={})

    async def get_share_stats(self, slug: str) -> Any:
        return await self._client.get(f"/shares/{slug}/stats")
