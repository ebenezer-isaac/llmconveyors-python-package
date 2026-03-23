"""Referral resource."""

from __future__ import annotations

from typing import Any

from llmconveyors.resources._base import AsyncResource, SyncResource


class ReferralResource(SyncResource):
    def get_stats(self) -> Any:
        return self._client.get("/referral/stats")

    def get_code(self) -> Any:
        return self._client.get("/referral/code")

    def set_vanity_code(self, request: dict[str, Any]) -> Any:
        return self._client.post("/referral/vanity-code", json=request)


class AsyncReferralResource(AsyncResource):
    async def get_stats(self) -> Any:
        return await self._client.get("/referral/stats")

    async def get_code(self) -> Any:
        return await self._client.get("/referral/code")

    async def set_vanity_code(self, request: dict[str, Any]) -> Any:
        return await self._client.post("/referral/vanity-code", json=request)
