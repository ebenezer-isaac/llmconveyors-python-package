"""Auth resource — GDPR data export and account deletion."""

from __future__ import annotations

from typing import Any

from llmconveyors.resources._base import AsyncResource, SyncResource


class AuthResource(SyncResource):
    def export_data(self) -> Any:
        return self._client.get("/auth/export")

    def delete_account(self) -> None:
        self._client.delete("/auth/account")


class AsyncAuthResource(AsyncResource):
    async def export_data(self) -> Any:
        return await self._client.get("/auth/export")

    async def delete_account(self) -> None:
        await self._client.delete("/auth/account")
