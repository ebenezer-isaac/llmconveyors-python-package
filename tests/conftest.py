"""Shared test fixtures."""

from __future__ import annotations

import pytest


@pytest.fixture
def api_key() -> str:
    return "llmc_test_key_123456789"


@pytest.fixture
def base_url() -> str:
    return "https://api.llmconveyors.com/api/v1"


@pytest.fixture
def success_envelope():
    """Factory for success envelope responses."""
    def _make(data):
        return {"success": True, "data": data}
    return _make


@pytest.fixture
def error_envelope():
    """Factory for error envelope responses."""
    def _make(code: str, message: str, status: int = 400, hint: str = ""):
        return {
            "success": False,
            "error": {
                "code": code,
                "message": message,
                "hint": hint,
                "details": {},
            },
            "requestId": "test-request-id",
            "timestamp": "2026-03-23T00:00:00.000Z",
            "path": "/api/v1/test",
        }
    return _make
