"""Privacy resource — consent management."""

from __future__ import annotations

from typing import Any

from llmconveyors.resources._base import AsyncResource, SyncResource


class PrivacyResource(SyncResource):
    def list_consents(self) -> Any:
        return self._client.get("/privacy/consents")

    def grant_consent(self, purpose: str) -> Any:
        return self._client.post(f"/privacy/consents/{purpose}", json={})

    def revoke_consent(self, purpose: str) -> None:
        self._client.delete(f"/privacy/consents/{purpose}")


class AsyncPrivacyResource(AsyncResource):
    async def list_consents(self) -> Any:
        return await self._client.get("/privacy/consents")

    async def grant_consent(self, purpose: str) -> Any:
        return await self._client.post(f"/privacy/consents/{purpose}", json={})

    async def revoke_consent(self, purpose: str) -> None:
        await self._client.delete(f"/privacy/consents/{purpose}")
