"""Agent request/response models."""

from __future__ import annotations

from typing import Any

from pydantic import Field

from llmconveyors.models.common import (
    AgentType,
    AIModel,
    APIModel,
    GenerationMode,
    JobStatus,
    ResearchMode,
    ResumeTheme,
    Tier,
)

# ---------------------------------------------------------------------------
# Generate requests
# ---------------------------------------------------------------------------


class JobHunterGenerateRequest(APIModel):
    """Request body for POST /agents/job-hunter/generate."""

    # Required
    company_name: str
    job_title: str
    company_website: str
    contact_email: str
    generic_email: str
    job_source_url: str

    # Optional
    session_id: str | None = None
    generation_id: str | None = None
    master_resume_id: str | None = None
    tier: Tier | None = None
    model: AIModel | None = None
    job_description: str | None = None
    webhook_url: str | None = Field(None, max_length=2048)
    auto_select_contacts: bool | None = None
    skip_research_cache: bool | None = None
    mode: GenerationMode | None = None
    theme: ResumeTheme | None = None
    contact_name: str | None = None
    contact_title: str | None = None
    original_cv: str | None = Field(None, alias="originalCV")
    extensive_cv: str | None = Field(None, alias="extensiveCV")
    cv_strategy: str | None = Field(None, alias="cvStrategy")
    cover_letter_strategy: str | None = None
    cold_email_strategy: str | None = None
    recon_strategy: str | None = None
    specific_core: str | None = None
    company_profile: str | None = None
    email_addresses: str | None = None


class B2BSalesGenerateRequest(APIModel):
    """Request body for POST /agents/b2b-sales/generate."""

    # Required
    company_name: str
    company_website: str
    skip_research_cache: bool

    # Optional
    session_id: str | None = None
    generation_id: str | None = None
    master_resume_id: str | None = None
    tier: Tier | None = None
    model: AIModel | None = None
    user_company_context: str | None = None
    target_company_context: str | None = None
    contact_name: str | None = None
    contact_title: str | None = None
    contact_email: str | None = None
    sales_strategy: str | None = None
    recon_strategy: str | None = None
    company_research: str | None = None
    research_mode: ResearchMode | None = None
    sender_name: str | None = None
    webhook_url: str | None = Field(None, max_length=2048)


# ---------------------------------------------------------------------------
# Generate responses
# ---------------------------------------------------------------------------


class GenerateResponse(APIModel):
    """Response from POST /agents/:type/generate (202 Accepted).

    All 5 fields are ALWAYS present — never optional.
    """

    job_id: str
    generation_id: str
    session_id: str
    status: str  # Always "queued"
    stream_url: str


class InteractRequest(APIModel):
    """Request body for POST /agents/:type/interact.

    All 4 fields are required.
    """

    generation_id: str
    session_id: str
    interaction_type: str
    interaction_data: dict[str, Any]


class InteractResponse(APIModel):
    """Response from POST /agents/:type/interact (202 Accepted).

    NOTE: This is DIFFERENT from GenerateResponse.
    Returns a NEW jobId and streamUrl for Phase B.
    """

    success: bool
    job_id: str
    stream_url: str


# ---------------------------------------------------------------------------
# Status
# ---------------------------------------------------------------------------


class JobStatusResponse(APIModel):
    """Response from GET /agents/:type/status/:jobId."""

    job_id: str
    generation_id: str
    session_id: str
    agent_type: AgentType
    status: JobStatus
    progress: int = 0
    current_step: str = ""

    # Optional — present depending on status
    failed_reason: str | None = None
    interaction_data: dict[str, Any] | None = None
    logs: list[dict[str, Any]] | None = None
    artifacts: list[dict[str, Any]] | None = None
    created_at: str | None = None
    completed_at: str | None = None


# ---------------------------------------------------------------------------
# Manifest
# ---------------------------------------------------------------------------


class AgentBilling(APIModel):
    """Billing info from agent manifest."""

    minimum_credits: int
    maximum_credits: int | None = None


class AgentCapabilities(APIModel):
    """Capabilities from agent manifest."""

    supports_phasing: bool = False
    has_artifact_versioning: bool = False


class ManifestResponse(APIModel):
    """Response from GET /agents/:type/manifest."""

    agent_type: AgentType
    label: str
    description: str
    skills: list[str]
    billing: AgentBilling
    capabilities: AgentCapabilities
    input_fields: list[dict[str, Any]] = Field(default_factory=list)
    interaction_types: list[dict[str, Any]] = Field(default_factory=list)


# ---------------------------------------------------------------------------
# Generate CV (separate synchronous endpoint)
# ---------------------------------------------------------------------------


class GenerateCVRequest(APIModel):
    """Request body for POST /agents/job-hunter/generate-cv (synchronous)."""

    prompt: str


class GenerateCVResponse(APIModel):
    """Response from POST /agents/job-hunter/generate-cv (200 OK, synchronous)."""

    resume: dict[str, Any]
    model: str
    usage: dict[str, Any] | None = None
    warning: str | None = None


# ---------------------------------------------------------------------------
# High-level helper types
# ---------------------------------------------------------------------------


class RunResult(APIModel):
    """Result from the high-level agents.run() orchestration method."""

    success: bool
    artifacts: list[dict[str, Any]] = Field(default_factory=list)
    warnings: list[str] = Field(default_factory=list)
    session_id: str = ""
    generation_id: str = ""
