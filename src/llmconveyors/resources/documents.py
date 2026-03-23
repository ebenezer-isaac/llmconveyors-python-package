"""Documents resource — download."""

from __future__ import annotations

from typing import Any

from llmconveyors.resources._base import AsyncResource, SyncResource


class DocumentsResource(SyncResource):
    def download(self, path: str) -> Any:
        """Download a document by storage path. Returns binary or signed URL."""
        return self._client.get("/documents/download", params={"path": path})


class AsyncDocumentsResource(AsyncResource):
    async def download(self, path: str) -> Any:
        return await self._client.get("/documents/download", params={"path": path})
