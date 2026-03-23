"""Base resource class for sync and async resources."""

from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from llmconveyors._http import AsyncHTTPClient, SyncHTTPClient


class SyncResource:
    """Base class for synchronous API resources."""

    def __init__(self, client: SyncHTTPClient) -> None:
        self._client = client


class AsyncResource:
    """Base class for asynchronous API resources."""

    def __init__(self, client: AsyncHTTPClient) -> None:
        self._client = client
