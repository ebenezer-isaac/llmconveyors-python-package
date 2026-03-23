"""Upload request/response models."""

from __future__ import annotations

from typing import Any

from pydantic import Field

from llmconveyors.models.common import APIModel

# ---------------------------------------------------------------------------
# Resume upload
# ---------------------------------------------------------------------------


class ResumeUploadMetadata(APIModel):
    """Metadata from resume upload."""

    extraction_method: str | None = None
    passes: int | None = None
    confidence: float | dict[str, Any] | None = None  # Can be float or {overall, extraction, validation}
    usage: dict[str, Any] | None = None
    model: str | None = None


class ResumeUploadResponse(APIModel):
    """Response from POST /upload/resume."""

    ok: bool
    normalized: dict[str, Any]
    file_size: int
    metadata: ResumeUploadMetadata | None = None


# ---------------------------------------------------------------------------
# Job description upload
# ---------------------------------------------------------------------------


class JobDescriptionMetadata(APIModel):
    """Metadata from job description extraction."""

    city: str | None = None
    country: str | None = None
    keywords: list[str] | None = None
    is_remote: bool | None = None
    grounded_extraction: bool | None = None


class JobDescriptionResponse(APIModel):
    """Response from POST /upload/job and POST /upload/job-text."""

    job_description: str
    company_name: str
    job_title: str
    company_website: str | None = None
    was_url: bool = False
    job_url: str | None = None
    email_addresses: list[str] = Field(default_factory=list)
    metadata: JobDescriptionMetadata | None = None
    processed: bool = False
    degraded: bool = False


# ---------------------------------------------------------------------------
# Job text request
# ---------------------------------------------------------------------------


class JobTextRequest(APIModel):
    """Request body for POST /upload/job-text.

    At least one of text or url must be provided.
    """

    text: str | None = Field(None, max_length=50_000)
    url: str | None = Field(None, max_length=2048)
