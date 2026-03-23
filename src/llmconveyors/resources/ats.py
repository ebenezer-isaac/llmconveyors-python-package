"""ATS scoring resource."""

from __future__ import annotations

from typing import Any

from llmconveyors.models.ats import ATSScoreResponse
from llmconveyors.resources._base import AsyncResource, SyncResource


class ATSResource(SyncResource):
    def score(self, request: dict[str, Any]) -> ATSScoreResponse:
        data = self._client.post("/ats/score", json=request)
        return ATSScoreResponse.model_validate(data)


class AsyncATSResource(AsyncResource):
    async def score(self, request: dict[str, Any]) -> ATSScoreResponse:
        data = await self._client.post("/ats/score", json=request)
        return ATSScoreResponse.model_validate(data)
