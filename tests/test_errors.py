"""Tests for error hierarchy and parse_error_response."""

from __future__ import annotations

from llmconveyors.errors import (
    AIProviderError,
    ConcurrentGenerationLimitError,
    ConflictError,
    ForbiddenError,
    GenerationTimeoutError,
    InsufficientCreditsError,
    InsufficientScopeError,
    InternalError,
    LLMConveyorsError,
    NetworkError,
    NotFoundError,
    RateLimitError,
    ServerRestartingError,
    SessionDeletedError,
    StreamError,
    StreamNotFoundError,
    TimeoutError,
    UnauthorizedError,
    UnknownAgentError,
    ValidationError,
    WebhookSignatureError,
    parse_error_response,
)


class TestErrorHierarchy:
    def test_base_error_attrs(self):
        exc = LLMConveyorsError(
            "test",
            status_code=400,
            code="TEST",
            hint="fix it",
            request_id="req-123",
        )
        assert exc.message == "test"
        assert exc.status_code == 400
        assert exc.code == "TEST"
        assert exc.hint == "fix it"
        assert exc.request_id == "req-123"

    def test_is_retryable_for_retryable_codes(self):
        exc = RateLimitError("rate limited", code="RATE_LIMITED")
        assert exc.is_retryable is True

    def test_is_retryable_for_non_retryable_codes(self):
        exc = ValidationError("bad input")
        assert exc.is_retryable is False

    def test_insufficient_scope_is_forbidden(self):
        assert issubclass(InsufficientScopeError, ForbiddenError)

    def test_unknown_agent_is_not_found(self):
        assert issubclass(UnknownAgentError, NotFoundError)

    def test_concurrent_gen_limit_is_conflict(self):
        """CONCURRENT_GENERATION_LIMIT is 409, not 429."""
        assert issubclass(ConcurrentGenerationLimitError, ConflictError)
        assert ConcurrentGenerationLimitError.status_code == 409

    def test_rate_limit_error_has_retry_after(self):
        exc = RateLimitError("limited", retry_after=30.0)
        assert exc.retry_after == 30.0

    def test_all_error_classes_are_llmconveyors_errors(self):
        classes = [
            ValidationError, UnauthorizedError, InsufficientCreditsError,
            ForbiddenError, InsufficientScopeError, NotFoundError,
            UnknownAgentError, ConflictError, ConcurrentGenerationLimitError,
            RateLimitError, InternalError, AIProviderError,
            GenerationTimeoutError, ServerRestartingError, StreamNotFoundError,
            StreamError, SessionDeletedError, NetworkError, TimeoutError,
            WebhookSignatureError,
        ]
        for cls in classes:
            assert issubclass(cls, LLMConveyorsError)


class TestParseErrorResponse:
    def test_nested_envelope_parsing(self, error_envelope):
        """Error envelope is NESTED: body['error']['code']."""
        body = error_envelope("VALIDATION_ERROR", "companyName is required")
        exc = parse_error_response(400, body)
        assert isinstance(exc, ValidationError)
        assert exc.message == "companyName is required"
        assert exc.code == "VALIDATION_ERROR"
        assert exc.request_id == "test-request-id"

    def test_code_dispatch_over_status(self, error_envelope):
        """INSUFFICIENT_SCOPE (403) dispatches by code, not just status."""
        body = error_envelope("INSUFFICIENT_SCOPE", "Key lacks scope")
        exc = parse_error_response(403, body)
        assert isinstance(exc, InsufficientScopeError)

    def test_concurrent_gen_limit_409(self, error_envelope):
        """CONCURRENT_GENERATION_LIMIT is dispatched by code on 409."""
        body = error_envelope("CONCURRENT_GENERATION_LIMIT", "Too many concurrent")
        exc = parse_error_response(409, body)
        assert isinstance(exc, ConcurrentGenerationLimitError)
        assert exc.is_retryable is True

    def test_unknown_agent_404(self, error_envelope):
        body = error_envelope("UNKNOWN_AGENT", "No such agent")
        exc = parse_error_response(404, body)
        assert isinstance(exc, UnknownAgentError)

    def test_rate_limited_with_retry_after(self, error_envelope):
        body = error_envelope("RATE_LIMITED", "Too many requests")
        headers = {"Retry-After": "60", "X-RateLimit-Limit": "10",
                   "X-RateLimit-Remaining": "0", "X-RateLimit-Reset": "1711152000"}
        exc = parse_error_response(429, body, headers=headers)
        assert isinstance(exc, RateLimitError)
        assert exc.retry_after == 60.0
        assert exc.rate_limit_info is not None
        assert exc.rate_limit_info.limit == 10

    def test_hint_preserved(self, error_envelope):
        body = error_envelope("INSUFFICIENT_CREDITS", "No credits", hint="Top up at ...")
        exc = parse_error_response(402, body)
        assert exc.hint == "Top up at ..."

    def test_fallback_to_status_code(self):
        """Unknown code falls back to status code mapping."""
        body = {"success": False, "error": {"code": "UNKNOWN_CODE", "message": "wat"}}
        exc = parse_error_response(500, body)
        assert isinstance(exc, InternalError)

    def test_all_17_codes_mapped(self, error_envelope):
        """Every documented error code maps to a specific exception class."""
        code_to_class = {
            ("VALIDATION_ERROR", 400): ValidationError,
            ("UNAUTHORIZED", 401): UnauthorizedError,
            ("INSUFFICIENT_CREDITS", 402): InsufficientCreditsError,
            ("FORBIDDEN", 403): ForbiddenError,
            ("INSUFFICIENT_SCOPE", 403): InsufficientScopeError,
            ("NOT_FOUND", 404): NotFoundError,
            ("UNKNOWN_AGENT", 404): UnknownAgentError,
            ("CONFLICT", 409): ConflictError,
            ("CONCURRENT_GENERATION_LIMIT", 409): ConcurrentGenerationLimitError,
            ("RATE_LIMITED", 429): RateLimitError,
            ("INTERNAL_ERROR", 500): InternalError,
            ("AI_PROVIDER_ERROR", 502): AIProviderError,
            ("GENERATION_TIMEOUT", 504): GenerationTimeoutError,
            ("SERVER_RESTARTING", 0): ServerRestartingError,
            ("STREAM_NOT_FOUND", 0): StreamNotFoundError,
            ("STREAM_ERROR", 0): StreamError,
            ("SESSION_DELETED", 0): SessionDeletedError,
        }
        for (code, status), expected_cls in code_to_class.items():
            body = error_envelope(code, f"Test {code}")
            exc = parse_error_response(status or 400, body)
            assert isinstance(exc, expected_cls), (
                f"{code} -> {type(exc).__name__} != {expected_cls.__name__}"
            )
