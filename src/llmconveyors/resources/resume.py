"""Resume resource — parse, validate, render, preview, themes, import/export, master CRUD."""

from __future__ import annotations

from pathlib import Path
from typing import IO, Any

from llmconveyors.models.resume import (
    MasterResume,
    MasterResumeList,
    ParseResumeResponse,
    PreviewResponse,
    RenderResponse,
    ValidateResumeResponse,
)
from llmconveyors.resources._base import AsyncResource, SyncResource


class ResumeResource(SyncResource):
    """Synchronous resume resource."""

    def parse(
        self, file: str | bytes | IO[bytes], *, mode: str | None = None
    ) -> ParseResumeResponse:
        if isinstance(file, str):
            p = Path(file)
            files = {"file": (p.name, p.read_bytes())}
        elif isinstance(file, bytes):
            files = {"file": ("resume", file)}
        else:
            files = {"file": ("resume", file)}
        data_dict: dict[str, Any] = {}
        if mode:
            data_dict["mode"] = mode
        data = self._client.post("/resume/parse", files=files, data=data_dict or None)
        return ParseResumeResponse.model_validate(data)

    def validate(self, resume: dict[str, Any]) -> ValidateResumeResponse:
        data = self._client.post("/resume/validate", json={"resume": resume})
        return ValidateResumeResponse.model_validate(data)

    def render(self, request: dict[str, Any]) -> RenderResponse:
        data = self._client.post("/resume/render", json=request)
        return RenderResponse.model_validate(data)

    def preview(self, resume: dict[str, Any], theme: str) -> PreviewResponse:
        data = self._client.post("/resume/preview", json={"resume": resume, "theme": theme})
        return PreviewResponse.model_validate(data)

    def themes(self) -> Any:
        return self._client.get("/resume/themes")

    def import_rx(self, data: dict[str, Any]) -> Any:
        return self._client.post("/resume/import/rx-resume", json=data)

    def export_rx(self, data: dict[str, Any]) -> Any:
        return self._client.post("/resume/export/rx-resume", json=data)

    def create_master(self, request: dict[str, Any]) -> MasterResume:
        data = self._client.post("/resume/master", json=request)
        return MasterResume.model_validate(data)

    def list_masters(self) -> MasterResumeList:
        data = self._client.get("/resume/master")
        return MasterResumeList.model_validate(data)

    def get_master(self, master_id: str) -> MasterResume:
        data = self._client.get(f"/resume/master/{master_id}")
        return MasterResume.model_validate(data)

    def update_master(self, master_id: str, request: dict[str, Any]) -> MasterResume:
        data = self._client.put(f"/resume/master/{master_id}", json=request)
        return MasterResume.model_validate(data)

    def delete_master(self, master_id: str) -> None:
        self._client.delete(f"/resume/master/{master_id}")


class AsyncResumeResource(AsyncResource):
    """Asynchronous resume resource."""

    async def parse(
        self, file: str | bytes | IO[bytes], *, mode: str | None = None
    ) -> ParseResumeResponse:
        if isinstance(file, str):
            p = Path(file)
            files = {"file": (p.name, p.read_bytes())}
        elif isinstance(file, bytes):
            files = {"file": ("resume", file)}
        else:
            files = {"file": ("resume", file)}
        data_dict: dict[str, Any] = {}
        if mode:
            data_dict["mode"] = mode
        data = await self._client.post("/resume/parse", files=files, data=data_dict or None)
        return ParseResumeResponse.model_validate(data)

    async def validate(self, resume: dict[str, Any]) -> ValidateResumeResponse:
        data = await self._client.post("/resume/validate", json={"resume": resume})
        return ValidateResumeResponse.model_validate(data)

    async def render(self, request: dict[str, Any]) -> RenderResponse:
        data = await self._client.post("/resume/render", json=request)
        return RenderResponse.model_validate(data)

    async def preview(self, resume: dict[str, Any], theme: str) -> PreviewResponse:
        data = await self._client.post("/resume/preview", json={"resume": resume, "theme": theme})
        return PreviewResponse.model_validate(data)

    async def themes(self) -> Any:
        return await self._client.get("/resume/themes")

    async def import_rx(self, data: dict[str, Any]) -> Any:
        return await self._client.post("/resume/import/rx-resume", json=data)

    async def export_rx(self, data: dict[str, Any]) -> Any:
        return await self._client.post("/resume/export/rx-resume", json=data)

    async def create_master(self, request: dict[str, Any]) -> MasterResume:
        data = await self._client.post("/resume/master", json=request)
        return MasterResume.model_validate(data)

    async def list_masters(self) -> MasterResumeList:
        data = await self._client.get("/resume/master")
        return MasterResumeList.model_validate(data)

    async def get_master(self, master_id: str) -> MasterResume:
        data = await self._client.get(f"/resume/master/{master_id}")
        return MasterResume.model_validate(data)

    async def update_master(self, master_id: str, request: dict[str, Any]) -> MasterResume:
        data = await self._client.put(f"/resume/master/{master_id}", json=request)
        return MasterResume.model_validate(data)

    async def delete_master(self, master_id: str) -> None:
        await self._client.delete(f"/resume/master/{master_id}")
