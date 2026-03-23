"""Tests for SSE streaming parser."""

from __future__ import annotations

import pytest

from llmconveyors.errors import ServerRestartingError, SessionDeletedError, StreamNotFoundError
from llmconveyors.models.streaming import (
    ChunkEvent,
    CompleteEvent,
    HeartbeatEvent,
    LogEvent,
    ProgressEvent,
)
from llmconveyors.streaming import parse_sse_lines


def _make_sse_lines(*events: str) -> list[bytes]:
    """Create SSE byte lines from data payloads."""
    lines = []
    for i, event in enumerate(events):
        lines.append(f"id: {i + 1}".encode())
        lines.append(f"data: {event}".encode())
        lines.append(b"")
    return lines


class TestSSEParser:
    def test_progress_event(self):
        lines = _make_sse_lines(
            '{"event":"progress","data":{"jobId":"j1","sessionId":"s1","step":"Research","percent":25}}'
        )
        events = list(parse_sse_lines(iter(lines)))
        assert len(events) == 1
        assert isinstance(events[0], ProgressEvent)
        assert events[0].step == "Research"
        assert events[0].percent == 25

    def test_chunk_event(self):
        lines = _make_sse_lines(
            '{"event":"chunk","data":{"jobId":"j1","sessionId":"s1","chunk":"Hello ","index":0}}'
        )
        events = list(parse_sse_lines(iter(lines)))
        assert len(events) == 1
        assert isinstance(events[0], ChunkEvent)
        assert events[0].chunk == "Hello "
        assert events[0].index == 0

    def test_complete_event_with_artifacts(self):
        lines = _make_sse_lines(
            '{"event":"complete","data":{"jobId":"j1","sessionId":"s1","success":true,"artifacts":[{"type":"cv"}]}}'
        )
        events = list(parse_sse_lines(iter(lines)))
        assert len(events) == 1
        assert isinstance(events[0], CompleteEvent)
        assert events[0].success is True
        assert len(events[0].artifacts) == 1

    def test_complete_event_awaiting_input(self):
        lines = _make_sse_lines(
            '{"event":"complete","data":{"jobId":"j1","sessionId":"s1","success":true,"artifacts":[],"awaitingInput":true,"interactionType":"contact_selection"}}'
        )
        events = list(parse_sse_lines(iter(lines)))
        assert len(events) == 1
        assert isinstance(events[0], CompleteEvent)
        assert events[0].awaiting_input is True
        assert events[0].interaction_type == "contact_selection"

    def test_error_event_raises_stream_not_found(self):
        payload = (
            '{"event":"error","data":{"jobId":"j1","sessionId":"s1",'
            '"code":"STREAM_NOT_FOUND","message":"Not found"}}'
        )
        lines = _make_sse_lines(payload)
        with pytest.raises(StreamNotFoundError):
            list(parse_sse_lines(iter(lines)))

    def test_error_event_raises_server_restarting(self):
        lines = _make_sse_lines(
            '{"event":"error","data":{"jobId":"j1","sessionId":"s1","code":"SERVER_RESTARTING","message":"Restarting"}}'
        )
        with pytest.raises(ServerRestartingError):
            list(parse_sse_lines(iter(lines)))

    def test_error_event_raises_session_deleted(self):
        lines = _make_sse_lines(
            '{"event":"error","data":{"jobId":"j1","sessionId":"s1","code":"SESSION_DELETED","message":"Deleted"}}'
        )
        with pytest.raises(SessionDeletedError):
            list(parse_sse_lines(iter(lines)))

    def test_log_event(self):
        lines = _make_sse_lines(
            '{"event":"log","data":{"messageId":"m1","generationId":"g1","sessionId":"s1","content":"Starting","level":"info","timestamp":"2026-01-01T00:00:00Z"}}'
        )
        events = list(parse_sse_lines(iter(lines)))
        assert len(events) == 1
        assert isinstance(events[0], LogEvent)
        assert events[0].level == "info"

    def test_heartbeat_filtered_by_default(self):
        lines = _make_sse_lines(
            '{"event":"heartbeat","data":{"jobId":"j1","sessionId":"s1","timestamp":"2026-01-01T00:00:00Z"}}'
        )
        events = list(parse_sse_lines(iter(lines)))
        assert len(events) == 0

    def test_heartbeat_included_when_requested(self):
        lines = _make_sse_lines(
            '{"event":"heartbeat","data":{"jobId":"j1","sessionId":"s1","timestamp":"2026-01-01T00:00:00Z"}}'
        )
        events = list(parse_sse_lines(iter(lines), include_heartbeats=True))
        assert len(events) == 1
        assert isinstance(events[0], HeartbeatEvent)

    def test_logs_filtered_when_disabled(self):
        lines = _make_sse_lines(
            '{"event":"log","data":{"messageId":"m1","generationId":"g1","sessionId":"s1","content":"msg","level":"debug","timestamp":"2026-01-01T00:00:00Z"}}'
        )
        events = list(parse_sse_lines(iter(lines), include_logs=False))
        assert len(events) == 0

    def test_unknown_event_skipped_gracefully(self):
        lines = _make_sse_lines(
            '{"event":"unknown_type","data":{"foo":"bar"}}'
        )
        events = list(parse_sse_lines(iter(lines)))
        assert len(events) == 0

    def test_no_event_field_in_wire_format(self):
        """Server sends NO SSE event: field — only id: and data: lines."""
        p = '{"event":"progress","data":{"jobId":"j1","sessionId":"s1",'
        p += '"step":"ATS","percent":50}}'
        c = '{"event":"complete","data":{"jobId":"j1","sessionId":"s1",'
        c += '"success":true,"artifacts":[]}}'
        raw_lines = [
            b"id: 1",
            f"data: {p}".encode(),
            b"",
            b"id: 2",
            f"data: {c}".encode(),
        ]
        events = list(parse_sse_lines(iter(raw_lines)))
        assert len(events) == 2
        assert isinstance(events[0], ProgressEvent)
        assert isinstance(events[1], CompleteEvent)

    def test_bom_stripped_from_first_line(self):
        d = '{"event":"progress","data":{"jobId":"j1","sessionId":"s1","step":"Init","percent":0}}'
        lines = [
            "\ufeffid: 1".encode(),
            f"data: {d}".encode(),
        ]
        events = list(parse_sse_lines(iter(lines)))
        assert len(events) == 1

    def test_malformed_json_skipped(self):
        lines = [b"data: {not valid json}"]
        events = list(parse_sse_lines(iter(lines)))
        assert len(events) == 0

    def test_comment_lines_ignored(self):
        j = '{"event":"progress","data":{"jobId":"j1","sessionId":"s1","step":"X","percent":1}}'
        d = f"data: {j}".encode()
        lines = [b": this is a comment", b"data: {}", d]
        events = list(parse_sse_lines(iter(lines)))
        assert len(events) == 1

    def test_multiple_events_in_sequence(self):
        lines = _make_sse_lines(
            '{"event":"progress","data":{"jobId":"j1","sessionId":"s1","step":"A","percent":10}}',
            '{"event":"chunk","data":{"jobId":"j1","sessionId":"s1","chunk":"text","index":0}}',
            '{"event":"complete","data":{"jobId":"j1","sessionId":"s1","success":true,"artifacts":[]}}',
        )
        events = list(parse_sse_lines(iter(lines)))
        assert len(events) == 3
        assert isinstance(events[0], ProgressEvent)
        assert isinstance(events[1], ChunkEvent)
        assert isinstance(events[2], CompleteEvent)
