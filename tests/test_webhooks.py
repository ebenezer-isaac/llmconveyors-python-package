"""Tests for webhook signature verification and event parsing."""

from __future__ import annotations

import hashlib
import hmac
import json

import pytest

from llmconveyors.errors import WebhookSignatureError
from llmconveyors.models.webhooks import (
    GenerationAwaitingInputEvent,
    GenerationCompletedEvent,
    GenerationFailedEvent,
)
from llmconveyors.webhooks import construct_event, parse_webhook_event, verify_signature


def _sign(payload: bytes, secret: str) -> str:
    return "sha256=" + hmac.new(secret.encode(), payload, hashlib.sha256).hexdigest()


class TestVerifySignature:
    def test_valid_signature_with_prefix(self):
        payload = b'{"event":"generation.completed"}'
        secret = "whsec_test123"
        sig = _sign(payload, secret)
        assert verify_signature(payload, sig, secret) is True

    def test_valid_signature_without_prefix(self):
        payload = b'{"event":"generation.completed"}'
        secret = "whsec_test123"
        raw_sig = hmac.new(secret.encode(), payload, hashlib.sha256).hexdigest()
        assert verify_signature(payload, raw_sig, secret) is True

    def test_invalid_signature(self):
        payload = b'{"event":"generation.completed"}'
        assert verify_signature(payload, "sha256=deadbeef", "secret") is False

    def test_empty_payload_returns_false(self):
        assert verify_signature(b"", "sha256=abc", "secret") is False

    def test_empty_signature_returns_false(self):
        assert verify_signature(b"payload", "", "secret") is False

    def test_empty_secret_returns_false(self):
        assert verify_signature(b"payload", "sha256=abc", "") is False

    def test_tampered_payload(self):
        payload = b'{"event":"generation.completed"}'
        secret = "whsec_test123"
        sig = _sign(payload, secret)
        tampered = b'{"event":"generation.failed"}'
        assert verify_signature(tampered, sig, secret) is False


class TestParseWebhookEvent:
    def test_generation_completed(self):
        body = {
            "event": "generation.completed",
            "generationId": "gen-1",
            "sessionId": "sess-1",
            "agentType": "job-hunter",
            "timestamp": "2026-01-01T00:00:00Z",
            "data": {"status": "completed", "artifacts": [{"type": "cv"}]},
        }
        event = parse_webhook_event(body)
        assert isinstance(event, GenerationCompletedEvent)
        assert event.data.status == "completed"

    def test_generation_failed(self):
        body = {
            "event": "generation.failed",
            "generationId": "gen-1",
            "sessionId": "sess-1",
            "agentType": "job-hunter",
            "timestamp": "2026-01-01T00:00:00Z",
            "data": {"status": "failed", "error": "Out of credits"},
        }
        event = parse_webhook_event(body)
        assert isinstance(event, GenerationFailedEvent)
        assert event.data.error == "Out of credits"

    def test_generation_awaiting_input(self):
        body = {
            "event": "generation.awaiting_input",
            "generationId": "gen-1",
            "sessionId": "sess-1",
            "agentType": "job-hunter",
            "timestamp": "2026-01-01T00:00:00Z",
            "data": {
                "status": "awaiting_input",
                "interactionData": {"candidates": [], "recommendedTargetId": "c1"},
            },
        }
        event = parse_webhook_event(body)
        assert isinstance(event, GenerationAwaitingInputEvent)

    def test_missing_required_fields(self):
        with pytest.raises(ValueError, match="missing required fields"):
            parse_webhook_event({"event": "generation.completed"})

    def test_unknown_event_type(self):
        body = {
            "event": "unknown.event",
            "generationId": "gen-1",
            "sessionId": "sess-1",
            "agentType": "job-hunter",
            "timestamp": "2026-01-01T00:00:00Z",
            "data": {},
        }
        with pytest.raises(ValueError, match="Unknown webhook event type"):
            parse_webhook_event(body)


class TestConstructEvent:
    def test_full_roundtrip(self):
        body = {
            "event": "generation.completed",
            "generationId": "gen-1",
            "sessionId": "sess-1",
            "agentType": "job-hunter",
            "timestamp": "2026-01-01T00:00:00Z",
            "data": {"status": "completed", "artifacts": []},
        }
        payload = json.dumps(body).encode()
        secret = "whsec_test"
        sig = _sign(payload, secret)

        event = construct_event(payload, sig, secret)
        assert isinstance(event, GenerationCompletedEvent)

    def test_invalid_signature_raises(self):
        payload = b'{"event":"generation.completed"}'
        with pytest.raises(WebhookSignatureError):
            construct_event(payload, "sha256=bad", "secret")
