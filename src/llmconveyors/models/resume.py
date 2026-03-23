"""Resume operation models."""

from __future__ import annotations

from typing import Any

from pydantic import Field

from llmconveyors.models.common import APIModel, RenderFormat, ResumeTheme

# ---------------------------------------------------------------------------
# Parse
# ---------------------------------------------------------------------------


class ParseResumeResponse(APIModel):
    """Response from POST /resume/parse."""

    resume: dict[str, Any]
    metadata: dict[str, Any] | None = None


# ---------------------------------------------------------------------------
# Validate
# ---------------------------------------------------------------------------


class ValidateResumeRequest(APIModel):
    """Request body for POST /resume/validate."""

    resume: dict[str, Any]


class ValidateResumeResponse(APIModel):
    """Response from POST /resume/validate."""

    valid: bool
    errors: list[dict[str, Any]] | None = None
    warnings: list[dict[str, Any]] | None = None
    coerced: dict[str, Any] | None = None


# ---------------------------------------------------------------------------
# Render
# ---------------------------------------------------------------------------


class RenderRequest(APIModel):
    """Request body for POST /resume/render."""

    resume: dict[str, Any]
    theme: ResumeTheme
    format: RenderFormat | None = None


class RenderResponse(APIModel):
    """Response from POST /resume/render (PDF format)."""

    pdf: str  # Base64-encoded PDF bytes
    page_count: int | None = None
    theme: str
    mime_type: str
    cache_hit: bool


# ---------------------------------------------------------------------------
# Preview
# ---------------------------------------------------------------------------


class PreviewRequest(APIModel):
    """Request body for POST /resume/preview."""

    resume: dict[str, Any]
    theme: ResumeTheme


class PreviewResponse(APIModel):
    """Response from POST /resume/preview."""

    html: str


# ---------------------------------------------------------------------------
# Master resume
# ---------------------------------------------------------------------------


class MasterResumeCreate(APIModel):
    """Request body for POST /resume/master."""

    label: str
    raw_text: str = Field(min_length=1, max_length=100_000)
    structured: dict[str, Any] | None = None
    is_default: bool | None = None


class MasterResumeUpdate(APIModel):
    """Request body for PUT /resume/master/:id."""

    label: str | None = None
    raw_text: str | None = Field(None, min_length=1, max_length=100_000)
    structured: dict[str, Any] | None = None
    is_default: bool | None = None


class MasterResume(APIModel):
    """A master resume object."""

    id: str
    label: str
    raw_text: str = ""
    structured: dict[str, Any] | None = None
    is_default: bool = False
    created_at: str | None = None
    updated_at: str | None = None


class MasterResumeList(APIModel):
    """Response from GET /resume/master."""

    resumes: list[MasterResume]
    total: int
