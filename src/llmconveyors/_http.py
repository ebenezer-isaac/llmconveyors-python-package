"""HTTP transport layer with retry, envelope unwrapping, and error handling.

Provides both sync and async clients wrapping httpx.
"""

from __future__ import annotations

import logging
import os
import random
import time
from typing import IO, Any

import httpx

from llmconveyors._constants import (
    API_KEY_ENV_VAR,
    API_KEY_PREFIX,
    CONCURRENT_LIMIT_DELAY,
    DEFAULT_BASE_URL,
    DEFAULT_MAX_RETRIES,
    DEFAULT_TIMEOUT,
    RETRY_BASE_DELAY,
    RETRY_JITTER_MAX,
    RETRY_MAX_DELAY,
)
from llmconveyors._version import __version__
from llmconveyors.errors import (
    ConcurrentGenerationLimitError,
    LLMConveyorsError,
    NetworkError,
    RateLimitError,
    TimeoutError,
    parse_error_response,
)

logger = logging.getLogger("llmconveyors")

FileInput = str | bytes | IO[bytes]

# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------


def _resolve_api_key(api_key: str | None) -> str:
    """Resolve API key from argument or environment variable."""
    key = api_key or os.environ.get(API_KEY_ENV_VAR, "")
    if not key:
        msg = (
            f"API key is required. Pass api_key= or set the {API_KEY_ENV_VAR} "
            "environment variable."
        )
        raise ValueError(msg)
    if not key.startswith(API_KEY_PREFIX):
        msg = f"API key must start with '{API_KEY_PREFIX}' prefix."
        raise ValueError(msg)
    return key


def _build_headers(api_key: str) -> dict[str, str]:
    """Build default request headers."""
    return {
        "X-API-Key": api_key,
        "User-Agent": f"llmconveyors-python/{__version__}",
        "Accept": "application/json",
    }


def _compute_backoff(attempt: int, base: float = RETRY_BASE_DELAY) -> float:
    """Exponential backoff with jitter: base * 2^attempt + random jitter."""
    delay = min(base * (2**attempt), RETRY_MAX_DELAY)
    jitter = random.uniform(0, RETRY_JITTER_MAX)  # noqa: S311
    return delay + jitter


def _is_json_response(response: httpx.Response) -> bool:
    """Check if response has JSON content type."""
    ct = response.headers.get("content-type", "")
    return "application/json" in ct


def _unwrap_response(response: httpx.Response) -> Any:
    """Unwrap API envelope, handling JSON/binary/empty responses."""
    # 204 No Content
    if response.status_code == 204:
        return None

    # Non-JSON (binary responses like PDF downloads)
    if not _is_json_response(response):
        return response.content

    body = response.json()

    # Error envelope
    if response.status_code >= 400:
        headers_dict = dict(response.headers)
        raise parse_error_response(response.status_code, body, headers=headers_dict)

    # Success envelope: {"success": true, "data": ...}
    if isinstance(body, dict) and body.get("success") is True and "data" in body:
        return body["data"]

    # Passthrough (some endpoints return raw data without envelope)
    return body


def _should_retry(exc: LLMConveyorsError, attempt: int, max_retries: int) -> bool:
    """Determine if a request should be retried."""
    if attempt >= max_retries:
        return False
    return exc.is_retryable


def _get_retry_delay(exc: LLMConveyorsError, attempt: int) -> float:
    """Compute retry delay based on error type."""
    if isinstance(exc, RateLimitError) and exc.retry_after is not None:
        return exc.retry_after + random.uniform(0, RETRY_JITTER_MAX)  # noqa: S311
    if isinstance(exc, ConcurrentGenerationLimitError):
        return CONCURRENT_LIMIT_DELAY + random.uniform(0, RETRY_JITTER_MAX)  # noqa: S311
    return _compute_backoff(attempt)


# ---------------------------------------------------------------------------
# Sync HTTP client
# ---------------------------------------------------------------------------


class SyncHTTPClient:
    """Synchronous HTTP client wrapping httpx.Client."""

    def __init__(
        self,
        api_key: str | None = None,
        base_url: str = DEFAULT_BASE_URL,
        timeout: float = DEFAULT_TIMEOUT,
        max_retries: int = DEFAULT_MAX_RETRIES,
    ) -> None:
        self._api_key = _resolve_api_key(api_key)
        self._base_url = base_url.rstrip("/")
        self._max_retries = max_retries
        self._client = httpx.Client(
            base_url=self._base_url,
            headers=_build_headers(self._api_key),
            timeout=timeout,
        )

    def close(self) -> None:
        self._client.close()

    def __enter__(self) -> SyncHTTPClient:
        return self

    def __exit__(self, *args: Any) -> None:
        self.close()

    # -- Convenience methods --

    def get(self, path: str, *, params: dict[str, Any] | None = None) -> Any:
        return self._request("GET", path, params=params)

    def post(
        self,
        path: str,
        *,
        json: Any = None,
        files: dict[str, Any] | None = None,
        data: dict[str, Any] | None = None,
    ) -> Any:
        return self._request("POST", path, json=json, files=files, data=data)

    def put(self, path: str, *, json: Any = None) -> Any:
        return self._request("PUT", path, json=json)

    def delete(self, path: str, *, params: dict[str, Any] | None = None) -> Any:
        return self._request("DELETE", path, params=params)

    def stream(self, path: str, *, params: dict[str, Any] | None = None,
               headers: dict[str, str] | None = None,
               timeout: float | None = None) -> httpx.Response:
        """Start a streaming GET request (for SSE). Returns the raw response."""
        return self._client.stream(
            "GET",
            path,
            params=params,
            headers=headers,
            timeout=timeout,
        )

    # -- Core request method with retry --

    def _request(
        self,
        method: str,
        path: str,
        *,
        json: Any = None,
        params: dict[str, Any] | None = None,
        files: dict[str, Any] | None = None,
        data: dict[str, Any] | None = None,
    ) -> Any:
        last_exc: LLMConveyorsError | None = None

        for attempt in range(self._max_retries + 1):
            try:
                response = self._client.request(
                    method,
                    path,
                    json=json,
                    params=params,
                    files=files,
                    data=data,
                )
                return _unwrap_response(response)
            except LLMConveyorsError as exc:
                last_exc = exc
                if not _should_retry(exc, attempt, self._max_retries):
                    raise
                delay = _get_retry_delay(exc, attempt)
                logger.info(
                    "Retrying %s %s (attempt %d/%d) after %.1fs: %s",
                    method, path, attempt + 1, self._max_retries, delay, exc.code,
                )
                time.sleep(delay)
            except httpx.TimeoutException as exc:
                raise TimeoutError(str(exc)) from exc
            except httpx.HTTPError as exc:
                raise NetworkError(str(exc)) from exc

        # Should not reach here, but just in case
        if last_exc is not None:
            raise last_exc
        msg = "Request failed with no error captured"
        raise LLMConveyorsError(msg)


# ---------------------------------------------------------------------------
# Async HTTP client
# ---------------------------------------------------------------------------


class AsyncHTTPClient:
    """Asynchronous HTTP client wrapping httpx.AsyncClient."""

    def __init__(
        self,
        api_key: str | None = None,
        base_url: str = DEFAULT_BASE_URL,
        timeout: float = DEFAULT_TIMEOUT,
        max_retries: int = DEFAULT_MAX_RETRIES,
    ) -> None:
        self._api_key = _resolve_api_key(api_key)
        self._base_url = base_url.rstrip("/")
        self._max_retries = max_retries
        self._client = httpx.AsyncClient(
            base_url=self._base_url,
            headers=_build_headers(self._api_key),
            timeout=timeout,
        )

    async def close(self) -> None:
        await self._client.aclose()

    async def __aenter__(self) -> AsyncHTTPClient:
        return self

    async def __aexit__(self, *args: Any) -> None:
        await self.close()

    # -- Convenience methods --

    async def get(self, path: str, *, params: dict[str, Any] | None = None) -> Any:
        return await self._request("GET", path, params=params)

    async def post(
        self,
        path: str,
        *,
        json: Any = None,
        files: dict[str, Any] | None = None,
        data: dict[str, Any] | None = None,
    ) -> Any:
        return await self._request("POST", path, json=json, files=files, data=data)

    async def put(self, path: str, *, json: Any = None) -> Any:
        return await self._request("PUT", path, json=json)

    async def delete(self, path: str, *, params: dict[str, Any] | None = None) -> Any:
        return await self._request("DELETE", path, params=params)

    def stream(self, path: str, *, params: dict[str, Any] | None = None,
               headers: dict[str, str] | None = None,
               timeout: float | None = None) -> Any:
        """Start a streaming GET request (for SSE). Returns async context manager."""
        return self._client.stream(
            "GET",
            path,
            params=params,
            headers=headers,
            timeout=timeout,
        )

    # -- Core request method with retry --

    async def _request(
        self,
        method: str,
        path: str,
        *,
        json: Any = None,
        params: dict[str, Any] | None = None,
        files: dict[str, Any] | None = None,
        data: dict[str, Any] | None = None,
    ) -> Any:
        import asyncio

        last_exc: LLMConveyorsError | None = None

        for attempt in range(self._max_retries + 1):
            try:
                response = await self._client.request(
                    method,
                    path,
                    json=json,
                    params=params,
                    files=files,
                    data=data,
                )
                return _unwrap_response(response)
            except LLMConveyorsError as exc:
                last_exc = exc
                if not _should_retry(exc, attempt, self._max_retries):
                    raise
                delay = _get_retry_delay(exc, attempt)
                logger.info(
                    "Retrying %s %s (attempt %d/%d) after %.1fs: %s",
                    method, path, attempt + 1, self._max_retries, delay, exc.code,
                )
                await asyncio.sleep(delay)
            except httpx.TimeoutException as exc:
                raise TimeoutError(str(exc)) from exc
            except httpx.HTTPError as exc:
                raise NetworkError(str(exc)) from exc

        if last_exc is not None:
            raise last_exc
        msg = "Request failed with no error captured"
        raise LLMConveyorsError(msg)
