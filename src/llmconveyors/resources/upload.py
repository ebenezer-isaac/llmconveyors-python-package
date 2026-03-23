"""Upload resource — resume and job description uploads."""

from __future__ import annotations

from pathlib import Path
from typing import IO, Any

from llmconveyors.models.upload import JobDescriptionResponse, ResumeUploadResponse
from llmconveyors.resources._base import AsyncResource, SyncResource


def _prepare_file(file: str | bytes | IO[bytes]) -> tuple[str, Any]:
    """Prepare a file for multipart upload."""
    if isinstance(file, str):
        p = Path(file)
        return (p.name, p.read_bytes())
    if isinstance(file, bytes):
        return ("file", file)
    return ("file", file)


class UploadResource(SyncResource):
    """Synchronous upload resource."""

    def resume(self, file: str | bytes | IO[bytes]) -> ResumeUploadResponse:
        name, content = _prepare_file(file)
        data = self._client.post("/upload/resume", files={"file": (name, content)})
        return ResumeUploadResponse.model_validate(data)

    def job_file(self, file: str | bytes | IO[bytes]) -> JobDescriptionResponse:
        name, content = _prepare_file(file)
        data = self._client.post("/upload/job", files={"file": (name, content)})
        return JobDescriptionResponse.model_validate(data)

    def job_text(self, request: dict[str, Any]) -> JobDescriptionResponse:
        data = self._client.post("/upload/job-text", json=request)
        return JobDescriptionResponse.model_validate(data)


class AsyncUploadResource(AsyncResource):
    """Asynchronous upload resource."""

    async def resume(self, file: str | bytes | IO[bytes]) -> ResumeUploadResponse:
        name, content = _prepare_file(file)
        data = await self._client.post("/upload/resume", files={"file": (name, content)})
        return ResumeUploadResponse.model_validate(data)

    async def job_file(self, file: str | bytes | IO[bytes]) -> JobDescriptionResponse:
        name, content = _prepare_file(file)
        data = await self._client.post("/upload/job", files={"file": (name, content)})
        return JobDescriptionResponse.model_validate(data)

    async def job_text(self, request: dict[str, Any]) -> JobDescriptionResponse:
        data = await self._client.post("/upload/job-text", json=request)
        return JobDescriptionResponse.model_validate(data)
