"""Typed exception hierarchy for the LLM Conveyors SDK.

Error codes and HTTP status mappings are derived from the API documentation (SSOT).
The API error envelope is NESTED: body["error"]["code"], NOT flat body["code"].
"""

from __future__ import annotations

from typing import Any

# ---------------------------------------------------------------------------
# Error codes
# ---------------------------------------------------------------------------

RETRYABLE_CODES: frozenset[str] = frozenset(
    {
        "RATE_LIMITED",
        "CONCURRENT_GENERATION_LIMIT",
        "AI_PROVIDER_ERROR",
        "GENERATION_TIMEOUT",
        "SERVER_RESTARTING",
        "STREAM_ERROR",
    }
)

# ---------------------------------------------------------------------------
# Base exception
# ---------------------------------------------------------------------------


class LLMConveyorsError(Exception):
    """Base exception for all SDK errors."""

    status_code: int = 0
    code: str = ""

    def __init__(
        self,
        message: str,
        *,
        status_code: int = 0,
        code: str = "",
        hint: str | None = None,
        details: dict[str, Any] | None = None,
        request_id: str | None = None,
        timestamp: str | None = None,
        path: str | None = None,
    ) -> None:
        super().__init__(message)
        self.message = message
        if status_code:
            self.status_code = status_code
        if code:
            self.code = code
        self.hint = hint
        self.details = details
        self.request_id = request_id
        self.timestamp = timestamp
        self.path = path

    @property
    def is_retryable(self) -> bool:
        return self.code in RETRYABLE_CODES

    def __repr__(self) -> str:
        parts = [f"{type(self).__name__}({self.message!r}"]
        if self.code:
            parts.append(f", code={self.code!r}")
        if self.status_code:
            parts.append(f", status={self.status_code}")
        parts.append(")")
        return "".join(parts)


# ---------------------------------------------------------------------------
# HTTP 4xx errors
# ---------------------------------------------------------------------------


class ValidationError(LLMConveyorsError):
    """Invalid input parameters (400 / VALIDATION_ERROR)."""

    status_code = 400
    code = "VALIDATION_ERROR"


class UnauthorizedError(LLMConveyorsError):
    """Missing or invalid API key (401 / UNAUTHORIZED)."""

    status_code = 401
    code = "UNAUTHORIZED"


class InsufficientCreditsError(LLMConveyorsError):
    """Not enough credits to start generation (402 / INSUFFICIENT_CREDITS)."""

    status_code = 402
    code = "INSUFFICIENT_CREDITS"


class ForbiddenError(LLMConveyorsError):
    """Access denied to resource (403 / FORBIDDEN)."""

    status_code = 403
    code = "FORBIDDEN"


class InsufficientScopeError(ForbiddenError):
    """API key lacks required scope (403 / INSUFFICIENT_SCOPE)."""

    code = "INSUFFICIENT_SCOPE"


class NotFoundError(LLMConveyorsError):
    """Resource not found (404 / NOT_FOUND)."""

    status_code = 404
    code = "NOT_FOUND"


class UnknownAgentError(NotFoundError):
    """Unrecognized agent type (404 / UNKNOWN_AGENT)."""

    code = "UNKNOWN_AGENT"


class ConflictError(LLMConveyorsError):
    """Resource state conflict (409 / CONFLICT)."""

    status_code = 409
    code = "CONFLICT"


class ConcurrentGenerationLimitError(ConflictError):
    """Maximum concurrent generation limit reached (409 / CONCURRENT_GENERATION_LIMIT).

    NOTE: This is HTTP 409 (Conflict), NOT 429. Confirmed from backend source.
    Retry after ~5 seconds.
    """

    code = "CONCURRENT_GENERATION_LIMIT"


class RateLimitError(LLMConveyorsError):
    """Too many requests (429 / RATE_LIMITED)."""

    status_code = 429
    code = "RATE_LIMITED"

    def __init__(
        self,
        message: str,
        *,
        retry_after: float | None = None,
        rate_limit_info: RateLimitInfo | None = None,
        **kwargs: Any,
    ) -> None:
        super().__init__(message, **kwargs)
        self.retry_after = retry_after
        self.rate_limit_info = rate_limit_info


# ---------------------------------------------------------------------------
# HTTP 5xx errors
# ---------------------------------------------------------------------------


class InternalError(LLMConveyorsError):
    """Unexpected server error (500 / INTERNAL_ERROR)."""

    status_code = 500
    code = "INTERNAL_ERROR"


class AIProviderError(LLMConveyorsError):
    """Upstream AI provider failure (502 / AI_PROVIDER_ERROR)."""

    status_code = 502
    code = "AI_PROVIDER_ERROR"


class GenerationTimeoutError(LLMConveyorsError):
    """Generation exceeded maximum time limit (504 / GENERATION_TIMEOUT)."""

    status_code = 504
    code = "GENERATION_TIMEOUT"


# ---------------------------------------------------------------------------
# SSE streaming errors (no HTTP status — delivered inside SSE stream)
# ---------------------------------------------------------------------------


class ServerRestartingError(LLMConveyorsError):
    """Server restarting — reconnect after delay (SSE / SERVER_RESTARTING)."""

    code = "SERVER_RESTARTING"


class StreamNotFoundError(LLMConveyorsError):
    """SSE stream not found or already closed (SSE / STREAM_NOT_FOUND). Non-retryable."""

    code = "STREAM_NOT_FOUND"


class StreamError(LLMConveyorsError):
    """Unexpected SSE stream error (SSE / STREAM_ERROR)."""

    code = "STREAM_ERROR"


class SessionDeletedError(LLMConveyorsError):
    """Session deleted during generation (SSE / SESSION_DELETED). Non-retryable."""

    code = "SESSION_DELETED"


# ---------------------------------------------------------------------------
# Client-side errors (not from the API)
# ---------------------------------------------------------------------------


class NetworkError(LLMConveyorsError):
    """Transport-level failure (DNS, connection refused, etc.)."""

    code = "NETWORK_ERROR"


class TimeoutError(LLMConveyorsError):  # noqa: A001
    """Client-side request or polling timeout."""

    code = "TIMEOUT"


class WebhookSignatureError(LLMConveyorsError):
    """Webhook signature verification failed."""

    code = "WEBHOOK_SIGNATURE_ERROR"


# ---------------------------------------------------------------------------
# Rate limit info
# ---------------------------------------------------------------------------


class RateLimitInfo:
    """Parsed rate limit headers from API response."""

    __slots__ = ("limit", "remaining", "reset")

    def __init__(self, limit: int, remaining: int, reset: int) -> None:
        self.limit = limit
        self.remaining = remaining
        self.reset = reset  # Unix timestamp (seconds)


# ---------------------------------------------------------------------------
# Error code → exception class mapping
# ---------------------------------------------------------------------------

_CODE_MAP: dict[str, type[LLMConveyorsError]] = {
    "VALIDATION_ERROR": ValidationError,
    "UNAUTHORIZED": UnauthorizedError,
    "INSUFFICIENT_CREDITS": InsufficientCreditsError,
    "FORBIDDEN": ForbiddenError,
    "INSUFFICIENT_SCOPE": InsufficientScopeError,
    "NOT_FOUND": NotFoundError,
    "UNKNOWN_AGENT": UnknownAgentError,
    "CONFLICT": ConflictError,
    "CONCURRENT_GENERATION_LIMIT": ConcurrentGenerationLimitError,
    "RATE_LIMITED": RateLimitError,
    "INTERNAL_ERROR": InternalError,
    "AI_PROVIDER_ERROR": AIProviderError,
    "GENERATION_TIMEOUT": GenerationTimeoutError,
    "SERVER_RESTARTING": ServerRestartingError,
    "STREAM_NOT_FOUND": StreamNotFoundError,
    "STREAM_ERROR": StreamError,
    "SESSION_DELETED": SessionDeletedError,
}

_STATUS_CODE_MAP: dict[int, type[LLMConveyorsError]] = {
    400: ValidationError,
    401: UnauthorizedError,
    402: InsufficientCreditsError,
    403: ForbiddenError,
    404: NotFoundError,
    409: ConflictError,
    429: RateLimitError,
    500: InternalError,
    502: AIProviderError,
    504: GenerationTimeoutError,
}


def _parse_rate_limit_headers(
    headers: dict[str, str] | None,
) -> tuple[float | None, RateLimitInfo | None]:
    """Extract Retry-After and rate limit info from response headers."""
    if not headers:
        return None, None

    retry_after: float | None = None
    raw = headers.get("retry-after") or headers.get("Retry-After")
    if raw:
        try:
            retry_after = float(raw)
        except (ValueError, TypeError):
            pass

    rate_limit_info: RateLimitInfo | None = None
    limit_raw = headers.get("x-ratelimit-limit") or headers.get("X-RateLimit-Limit")
    remaining_raw = headers.get("x-ratelimit-remaining") or headers.get(
        "X-RateLimit-Remaining"
    )
    reset_raw = headers.get("x-ratelimit-reset") or headers.get("X-RateLimit-Reset")
    if limit_raw and remaining_raw and reset_raw:
        try:
            rate_limit_info = RateLimitInfo(
                limit=int(limit_raw),
                remaining=int(remaining_raw),
                reset=int(reset_raw),
            )
        except (ValueError, TypeError):
            pass

    return retry_after, rate_limit_info


def parse_error_response(
    status_code: int,
    body: dict[str, Any],
    *,
    headers: dict[str, str] | None = None,
) -> LLMConveyorsError:
    """Parse an API error response into a typed exception.

    The API error envelope is NESTED:
    {
      "success": false,
      "error": {"code": "...", "message": "...", "hint": "...", "details": {}},
      "requestId": "...",
      "timestamp": "...",
      "path": "..."
    }
    """
    # Extract from nested envelope
    error_obj = body.get("error", {})
    if isinstance(error_obj, str):
        # Fallback: some errors might just have a string error field
        error_obj = {"code": "", "message": error_obj}

    code = error_obj.get("code", "") or ""
    message = error_obj.get("message", "") or f"HTTP {status_code}"
    hint = error_obj.get("hint")
    details = error_obj.get("details")

    request_id = body.get("requestId")
    timestamp = body.get("timestamp")
    path = body.get("path")

    # Dispatch by code string FIRST (handles same-status-code collisions)
    exc_cls = _CODE_MAP.get(code)

    # Fall back to status code if code is unknown
    if exc_cls is None:
        exc_cls = _STATUS_CODE_MAP.get(status_code, LLMConveyorsError)

    common_kwargs: dict[str, Any] = {
        "status_code": status_code,
        "code": code,
        "hint": hint,
        "details": details,
        "request_id": request_id,
        "timestamp": timestamp,
        "path": path,
    }

    if exc_cls is RateLimitError or issubclass(exc_cls, RateLimitError):
        retry_after, rate_limit_info = _parse_rate_limit_headers(headers)
        return RateLimitError(
            message,
            retry_after=retry_after,
            rate_limit_info=rate_limit_info,
            **common_kwargs,
        )

    return exc_cls(message, **common_kwargs)
