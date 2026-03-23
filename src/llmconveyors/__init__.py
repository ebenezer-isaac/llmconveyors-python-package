"""LLM Conveyors Python SDK.

Official Python client for the LLM Conveyors AI Agent Platform API.
"""

from llmconveyors._version import __version__
from llmconveyors.client import AsyncLLMConveyors, LLMConveyors
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
)
from llmconveyors.webhooks import construct_event, parse_webhook_event, verify_signature

__all__ = [
    # Version
    "__version__",
    # Clients
    "LLMConveyors",
    "AsyncLLMConveyors",
    # Errors
    "LLMConveyorsError",
    "ValidationError",
    "UnauthorizedError",
    "InsufficientCreditsError",
    "ForbiddenError",
    "InsufficientScopeError",
    "NotFoundError",
    "UnknownAgentError",
    "ConflictError",
    "ConcurrentGenerationLimitError",
    "RateLimitError",
    "InternalError",
    "AIProviderError",
    "GenerationTimeoutError",
    "ServerRestartingError",
    "StreamNotFoundError",
    "StreamError",
    "SessionDeletedError",
    "NetworkError",
    "TimeoutError",
    "WebhookSignatureError",
    # Webhooks
    "verify_signature",
    "construct_event",
    "parse_webhook_event",
]
