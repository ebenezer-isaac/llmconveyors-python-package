"""Content resource — save and delete generation."""

from __future__ import annotations

from typing import Any

from llmconveyors.resources._base import AsyncResource, SyncResource


class ContentResource(SyncResource):
    def save(self, request: dict[str, Any]) -> Any:
        return self._client.post("/content/save", json=request)

    def delete_generation(self, generation_id: str, *, session_id: str) -> None:
        self._client.delete(
            f"/content/generations/{generation_id}", params={"sessionId": session_id}
        )


class AsyncContentResource(AsyncResource):
    async def save(self, request: dict[str, Any]) -> Any:
        return await self._client.post("/content/save", json=request)

    async def delete_generation(self, generation_id: str, *, session_id: str) -> None:
        await self._client.delete(
            f"/content/generations/{generation_id}", params={"sessionId": session_id}
        )
