"""Tests for Pydantic models — correct field names, types, and schemas."""

from __future__ import annotations

import pytest

from llmconveyors.models.agents import (
    GenerateResponse,
    InteractResponse,
    JobStatusResponse,
)
from llmconveyors.models.ats import ATSScoreResponse
from llmconveyors.models.sessions import SessionHydration
from llmconveyors.models.streaming import CompleteEvent


class TestGenerateResponse:
    def test_all_five_fields_required(self):
        data = {
            "jobId": "j1",
            "generationId": "g1",
            "sessionId": "s1",
            "status": "queued",
            "streamUrl": "/stream/generation/g1",
        }
        resp = GenerateResponse.model_validate(data)
        assert resp.job_id == "j1"
        assert resp.generation_id == "g1"
        assert resp.session_id == "s1"
        assert resp.status == "queued"
        assert resp.stream_url == "/stream/generation/g1"

    def test_missing_field_raises(self):
        with pytest.raises(Exception):
            GenerateResponse.model_validate({"jobId": "j1"})


class TestInteractResponse:
    def test_correct_shape(self):
        """InteractResponse is {success, jobId, streamUrl} — NOT GenerateResponse shape."""
        data = {"success": True, "jobId": "j2", "streamUrl": "/stream/generation/g2"}
        resp = InteractResponse.model_validate(data)
        assert resp.success is True
        assert resp.job_id == "j2"
        assert resp.stream_url == "/stream/generation/g2"

    def test_no_generation_id_field(self):
        """InteractResponse does NOT have generationId."""
        data = {"success": True, "jobId": "j2", "streamUrl": "/s"}
        resp = InteractResponse.model_validate(data)
        assert not hasattr(resp, "generation_id")


class TestJobStatusResponse:
    def test_all_status_values(self):
        for status in ("queued", "processing", "completed", "failed", "awaiting_input"):
            data = {
                "jobId": "j1",
                "generationId": "g1",
                "sessionId": "s1",
                "agentType": "job-hunter",
                "status": status,
            }
            resp = JobStatusResponse.model_validate(data)
            assert resp.status == status


class TestATSScoreResponse:
    def test_correct_schema(self):
        """Response uses overallScore (not score), has grade, no dimensions."""
        data = {
            "overallScore": 85,
            "grade": "A",
            "breakdown": {"keywords": 90},
            "matchedKeywords": [{"keyword": "python", "found": True}],
            "missingKeywords": ["golang"],
            "suggestions": ["Add more keywords"],
        }
        resp = ATSScoreResponse.model_validate(data)
        assert resp.overall_score == 85
        assert resp.grade == "A"
        assert not hasattr(resp, "score")
        assert not hasattr(resp, "dimensions")


class TestSessionHydration:
    def test_generation_logs_field_name(self):
        """Field is generationLogs, NOT logs."""
        data = {
            "session": {"id": "s1"},
            "artifacts": [],
            "generationLogs": [{"id": "log1"}],
            "activeGeneration": None,
            "cvVersions": [],
            "coverLetterVersions": [],
            "coldEmailVersions": [],
            "atsVersions": [],
        }
        hydration = SessionHydration.model_validate(data)
        assert len(hydration.generation_logs) == 1
        assert hydration.generation_logs[0]["id"] == "log1"


class TestCompleteEvent:
    def test_awaiting_input_is_phase_boundary(self):
        data = {
            "jobId": "j1",
            "sessionId": "s1",
            "success": True,
            "artifacts": [],
            "awaitingInput": True,
            "interactionType": "contact_selection",
            "completedPhase": 0,
        }
        event = CompleteEvent.model_validate(data)
        assert event.awaiting_input is True
        assert event.interaction_type == "contact_selection"
        assert event.completed_phase == 0
