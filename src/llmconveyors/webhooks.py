"""Webhook signature verification and event parsing.

Security requirements:
- HMAC-SHA256 with constant-time comparison (hmac.compare_digest)
- Accept raw bytes only for payload (not decoded string)
- Strip sha256= prefix from signature header
"""

from __future__ import annotations

import hashlib
import hmac
import json
from typing import Any

from llmconveyors.errors import WebhookSignatureError
from llmconveyors.models.webhooks import (
    ALLOWED_WEBHOOK_EVENTS,
    GenerationAwaitingInputEvent,
    GenerationCompletedEvent,
    GenerationFailedEvent,
    WebhookEvent,
)


def verify_signature(
    payload: bytes,
    signature: str,
    secret: str,
) -> bool:
    """Verify a webhook signature using HMAC-SHA256.

    Args:
        payload: Raw request body bytes. MUST be bytes, not str.
        signature: Value of X-Webhook-Signature header (with or without sha256= prefix).
        secret: Webhook signing secret.

    Returns:
        True if signature is valid, False otherwise.
    """
    if not payload or not signature or not secret:
        return False

    # Strip sha256= prefix if present
    sig = signature.removeprefix("sha256=")

    expected = hmac.new(
        secret.encode("utf-8"),
        payload,
        hashlib.sha256,
    ).hexdigest()

    # Constant-time comparison to prevent timing attacks
    return hmac.compare_digest(sig, expected)


def parse_webhook_event(body: dict[str, Any]) -> WebhookEvent:
    """Parse a webhook event payload into a typed event.

    Args:
        body: Parsed JSON body of the webhook request.

    Returns:
        A typed WebhookEvent (GenerationCompletedEvent, GenerationFailedEvent,
        or GenerationAwaitingInputEvent).

    Raises:
        ValueError: If the event type is unknown or required fields are missing.
    """
    # Validate required fields
    required = ("event", "generationId", "sessionId", "agentType", "timestamp", "data")
    missing = [f for f in required if f not in body]
    if missing:
        msg = f"Webhook payload missing required fields: {', '.join(missing)}"
        raise ValueError(msg)

    event_type = body["event"]
    if event_type not in ALLOWED_WEBHOOK_EVENTS:
        msg = f"Unknown webhook event type: {event_type}"
        raise ValueError(msg)

    if event_type == "generation.completed":
        return GenerationCompletedEvent.model_validate(body)
    if event_type == "generation.failed":
        return GenerationFailedEvent.model_validate(body)
    if event_type == "generation.awaiting_input":
        return GenerationAwaitingInputEvent.model_validate(body)

    # Should not reach here given the allowlist check above
    msg = f"Unhandled webhook event type: {event_type}"
    raise ValueError(msg)


def construct_event(
    payload: bytes,
    sig_header: str,
    secret: str,
) -> WebhookEvent:
    """Verify signature and parse a webhook event in one step.

    Args:
        payload: Raw request body bytes.
        sig_header: Value of X-Webhook-Signature header.
        secret: Webhook signing secret.

    Returns:
        A typed WebhookEvent.

    Raises:
        WebhookSignatureError: If signature verification fails.
        ValueError: If event parsing fails.
    """
    if not verify_signature(payload, sig_header, secret):
        raise WebhookSignatureError("Webhook signature verification failed")

    body = json.loads(payload)
    return parse_webhook_event(body)
