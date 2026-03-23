"""Sessions resource."""

from __future__ import annotations

from typing import Any

from llmconveyors.models.sessions import (
    Session,
    SessionHydration,
)
from llmconveyors.resources._base import AsyncResource, SyncResource


class SessionsResource(SyncResource):
    """Synchronous sessions resource."""

    def init(self) -> Any:
        return self._client.get("/sessions/init")

    def create(self, request: dict[str, Any] | None = None) -> Session:
        data = self._client.post("/sessions", json=request or {})
        return Session.model_validate(data)

    def list(self) -> list[Session]:
        """List all sessions. Returns a FLAT ARRAY (not paginated)."""
        data = self._client.get("/sessions")
        if isinstance(data, list):
            return [Session.model_validate(s) for s in data]
        return []

    def get(self, session_id: str) -> Session:
        data = self._client.get(f"/sessions/{session_id}")
        return Session.model_validate(data)

    def hydrate(self, session_id: str) -> SessionHydration:
        """Get full session data. Field is generationLogs, NOT logs."""
        data = self._client.get(f"/sessions/{session_id}/hydrate")
        return SessionHydration.model_validate(data)

    def download(self, session_id: str, key: str) -> bytes:
        """Download artifact by storage key. Returns binary."""
        return self._client.get(f"/sessions/{session_id}/download", params={"key": key})

    def delete(self, session_id: str) -> None:
        """Delete session. Returns 204."""
        self._client.delete(f"/sessions/{session_id}")

    def log(self, session_id: str, request: dict[str, Any]) -> None:
        self._client.post(f"/sessions/{session_id}/log", json=request)

    def init_generation_log(
        self, session_id: str, generation_id: str, request: dict[str, Any] | None = None
    ) -> None:
        self._client.post(
            f"/sessions/{session_id}/generation-logs/{generation_id}/init",
            json=request or {},
        )


class AsyncSessionsResource(AsyncResource):
    """Asynchronous sessions resource."""

    async def init(self) -> Any:
        return await self._client.get("/sessions/init")

    async def create(self, request: dict[str, Any] | None = None) -> Session:
        data = await self._client.post("/sessions", json=request or {})
        return Session.model_validate(data)

    async def list(self) -> list[Session]:
        data = await self._client.get("/sessions")
        if isinstance(data, list):
            return [Session.model_validate(s) for s in data]
        return []

    async def get(self, session_id: str) -> Session:
        data = await self._client.get(f"/sessions/{session_id}")
        return Session.model_validate(data)

    async def hydrate(self, session_id: str) -> SessionHydration:
        data = await self._client.get(f"/sessions/{session_id}/hydrate")
        return SessionHydration.model_validate(data)

    async def download(self, session_id: str, key: str) -> bytes:
        return await self._client.get(f"/sessions/{session_id}/download", params={"key": key})

    async def delete(self, session_id: str) -> None:
        await self._client.delete(f"/sessions/{session_id}")

    async def log(self, session_id: str, request: dict[str, Any]) -> None:
        await self._client.post(f"/sessions/{session_id}/log", json=request)

    async def init_generation_log(
        self, session_id: str, generation_id: str, request: dict[str, Any] | None = None
    ) -> None:
        await self._client.post(
            f"/sessions/{session_id}/generation-logs/{generation_id}/init",
            json=request or {},
        )
