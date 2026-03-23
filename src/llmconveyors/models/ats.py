"""ATS scoring models.

IMPORTANT: The response uses `overallScore` (NOT `score`) and `grade`.
There is NO `dimensions` object — that was a FICTITIOUS schema.
The actual response has `breakdown`, `matchedKeywords`, `missingKeywords`, etc.
"""

from __future__ import annotations

from typing import Any

from pydantic import Field

from llmconveyors.models.common import APIModel, Grade

# ---------------------------------------------------------------------------
# Request
# ---------------------------------------------------------------------------


class ATSScoreRequest(APIModel):
    """Request body for POST /ats/score."""

    resume_text: str
    job_description: str
    job_title: str | None = None


# ---------------------------------------------------------------------------
# Response
# ---------------------------------------------------------------------------


class ATSScoreResponse(APIModel):
    """Response from POST /ats/score.

    CORRECT schema from docs SSOT. DO NOT use the old
    {score, dimensions, suggestions} schema — it was wrong.
    """

    overall_score: int = Field(ge=0, le=100)
    grade: Grade
    breakdown: dict[str, Any]
    matched_keywords: list[dict[str, Any]]
    missing_keywords: list[str]
    suggestions: list[str]

    # Optional enriched fields
    semantic_insights: dict[str, Any] | None = None
    reasoning: str | None = None
    enriched_suggestions: list[dict[str, Any]] | None = None
    enriched_missing_keywords: list[dict[str, Any]] | None = None
    keyword_confidences: list[dict[str, Any]] | None = None
    domain_intelligence: dict[str, Any] | None = None
