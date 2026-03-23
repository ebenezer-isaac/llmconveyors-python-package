"""Main client classes: LLMConveyors (sync) and AsyncLLMConveyors (async)."""

from __future__ import annotations

from typing import Any

from llmconveyors._constants import DEFAULT_BASE_URL, DEFAULT_MAX_RETRIES, DEFAULT_TIMEOUT
from llmconveyors._http import AsyncHTTPClient, SyncHTTPClient
from llmconveyors.resources.agents import AgentsResource, AsyncAgentsResource
from llmconveyors.resources.ats import AsyncATSResource, ATSResource
from llmconveyors.resources.auth import AsyncAuthResource, AuthResource
from llmconveyors.resources.content import AsyncContentResource, ContentResource
from llmconveyors.resources.documents import AsyncDocumentsResource, DocumentsResource
from llmconveyors.resources.health import AsyncHealthResource, HealthResource
from llmconveyors.resources.logging import AsyncLoggingResource, LoggingResource
from llmconveyors.resources.privacy import AsyncPrivacyResource, PrivacyResource
from llmconveyors.resources.referral import AsyncReferralResource, ReferralResource
from llmconveyors.resources.resume import AsyncResumeResource, ResumeResource
from llmconveyors.resources.sessions import AsyncSessionsResource, SessionsResource
from llmconveyors.resources.settings import AsyncSettingsResource, SettingsResource
from llmconveyors.resources.shares import AsyncSharesResource, SharesResource
from llmconveyors.resources.streaming import AsyncStreamingResource, StreamingResource
from llmconveyors.resources.upload import AsyncUploadResource, UploadResource


class LLMConveyors:
    """Synchronous LLM Conveyors SDK client.

    Usage:
        client = LLMConveyors(api_key="llmc_...")
        # or
        with LLMConveyors(api_key="llmc_...") as client:
            ...
    """

    def __init__(
        self,
        api_key: str | None = None,
        *,
        base_url: str = DEFAULT_BASE_URL,
        timeout: float = DEFAULT_TIMEOUT,
        max_retries: int = DEFAULT_MAX_RETRIES,
    ) -> None:
        self._http = SyncHTTPClient(
            api_key=api_key,
            base_url=base_url,
            timeout=timeout,
            max_retries=max_retries,
        )

        # Wire up all 15 resource namespaces
        self.agents = AgentsResource(self._http)
        self.stream = StreamingResource(self._http)
        self.sessions = SessionsResource(self._http)
        self.upload = UploadResource(self._http)
        self.resume = ResumeResource(self._http)
        self.ats = ATSResource(self._http)
        self.settings = SettingsResource(self._http)
        self.privacy = PrivacyResource(self._http)
        self.auth = AuthResource(self._http)
        self.documents = DocumentsResource(self._http)
        self.logging = LoggingResource(self._http)
        self.health = HealthResource(self._http)
        self.content = ContentResource(self._http)
        self.shares = SharesResource(self._http)
        self.referral = ReferralResource(self._http)

        # Wire streaming ↔ agents for run() orchestration
        self.agents._set_stream_resource(self.stream)

    def close(self) -> None:
        """Close the underlying HTTP client."""
        self._http.close()

    def __enter__(self) -> LLMConveyors:
        return self

    def __exit__(self, *args: Any) -> None:
        self.close()


class AsyncLLMConveyors:
    """Asynchronous LLM Conveyors SDK client.

    Usage:
        async with AsyncLLMConveyors(api_key="llmc_...") as client:
            ...
    """

    def __init__(
        self,
        api_key: str | None = None,
        *,
        base_url: str = DEFAULT_BASE_URL,
        timeout: float = DEFAULT_TIMEOUT,
        max_retries: int = DEFAULT_MAX_RETRIES,
    ) -> None:
        self._http = AsyncHTTPClient(
            api_key=api_key,
            base_url=base_url,
            timeout=timeout,
            max_retries=max_retries,
        )

        self.agents = AsyncAgentsResource(self._http)
        self.stream = AsyncStreamingResource(self._http)
        self.sessions = AsyncSessionsResource(self._http)
        self.upload = AsyncUploadResource(self._http)
        self.resume = AsyncResumeResource(self._http)
        self.ats = AsyncATSResource(self._http)
        self.settings = AsyncSettingsResource(self._http)
        self.privacy = AsyncPrivacyResource(self._http)
        self.auth = AsyncAuthResource(self._http)
        self.documents = AsyncDocumentsResource(self._http)
        self.logging = AsyncLoggingResource(self._http)
        self.health = AsyncHealthResource(self._http)
        self.content = AsyncContentResource(self._http)
        self.shares = AsyncSharesResource(self._http)
        self.referral = AsyncReferralResource(self._http)

        self.agents._set_stream_resource(self.stream)

    async def close(self) -> None:
        await self._http.close()

    async def __aenter__(self) -> AsyncLLMConveyors:
        return self

    async def __aexit__(self, *args: Any) -> None:
        await self.close()
