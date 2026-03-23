"""Pydantic models for the LLM Conveyors API."""

from llmconveyors.models.agents import (
    AgentBilling,
    AgentCapabilities,
    B2BSalesGenerateRequest,
    GenerateCVRequest,
    GenerateCVResponse,
    GenerateResponse,
    InteractRequest,
    InteractResponse,
    JobHunterGenerateRequest,
    JobStatusResponse,
    ManifestResponse,
    RunResult,
)
from llmconveyors.models.ats import ATSScoreRequest, ATSScoreResponse
from llmconveyors.models.auth import ExportDataResponse
from llmconveyors.models.common import (
    AgentType,
    AIModel,
    APIModel,
    GenerationMode,
    Grade,
    JobStatus,
    LogLevel,
    RenderFormat,
    ResearchMode,
    ResumeTheme,
    SessionLogRole,
    Tier,
)
from llmconveyors.models.content import (
    DeleteGenerationParams,
    SaveContentRequest,
    SaveContentResponse,
)
from llmconveyors.models.health import HealthResponse
from llmconveyors.models.logging import SendLogRequest
from llmconveyors.models.privacy import Consent
from llmconveyors.models.referral import ReferralCode, ReferralStats, SetVanityCodeRequest
from llmconveyors.models.resume import (
    MasterResume,
    MasterResumeCreate,
    MasterResumeList,
    MasterResumeUpdate,
    ParseResumeResponse,
    PreviewRequest,
    PreviewResponse,
    RenderRequest,
    RenderResponse,
    ValidateResumeRequest,
    ValidateResumeResponse,
)
from llmconveyors.models.sessions import (
    AppendLogRequest,
    Session,
    SessionCreate,
    SessionHydration,
    SessionInitResponse,
)
from llmconveyors.models.settings import (
    APIKeyCreate,
    APIKeyInfo,
    APIKeyRotate,
    APIKeyUsage,
    BYOKeySet,
    BYOKeyStatus,
    Preferences,
    Profile,
    UsageLog,
    UsageSummary,
    WebhookSecretResponse,
)
from llmconveyors.models.shares import (
    PublicShare,
    ShareCreate,
    ShareCreateResponse,
    ShareStats,
    ShareVisitStats,
)
from llmconveyors.models.streaming import (
    ChunkEvent,
    CompleteEvent,
    HeartbeatEvent,
    LogEvent,
    ProgressEvent,
    SSEErrorEvent,
    StreamEvent,
)
from llmconveyors.models.upload import (
    JobDescriptionResponse,
    JobTextRequest,
    ResumeUploadResponse,
)
from llmconveyors.models.webhooks import (
    GenerationAwaitingInputEvent,
    GenerationCompletedEvent,
    GenerationFailedEvent,
    WebhookEvent,
)

__all__ = [
    # Common types
    "AIModel",
    "AgentType",
    "APIModel",
    "GenerationMode",
    "Grade",
    "JobStatus",
    "LogLevel",
    "RenderFormat",
    "ResearchMode",
    "ResumeTheme",
    "SessionLogRole",
    "Tier",
    # Agents
    "AgentBilling",
    "AgentCapabilities",
    "B2BSalesGenerateRequest",
    "GenerateCVRequest",
    "GenerateCVResponse",
    "GenerateResponse",
    "InteractRequest",
    "InteractResponse",
    "JobHunterGenerateRequest",
    "JobStatusResponse",
    "ManifestResponse",
    "RunResult",
    # ATS
    "ATSScoreRequest",
    "ATSScoreResponse",
    # Auth
    "ExportDataResponse",
    # Content
    "DeleteGenerationParams",
    "SaveContentRequest",
    "SaveContentResponse",
    # Health
    "HealthResponse",
    # Logging
    "SendLogRequest",
    # Privacy
    "Consent",
    # Referral
    "ReferralCode",
    "ReferralStats",
    "SetVanityCodeRequest",
    # Resume
    "MasterResume",
    "MasterResumeCreate",
    "MasterResumeList",
    "MasterResumeUpdate",
    "ParseResumeResponse",
    "PreviewRequest",
    "PreviewResponse",
    "RenderRequest",
    "RenderResponse",
    "ValidateResumeRequest",
    "ValidateResumeResponse",
    # Sessions
    "AppendLogRequest",
    "Session",
    "SessionCreate",
    "SessionHydration",
    "SessionInitResponse",
    # Settings
    "APIKeyCreate",
    "APIKeyInfo",
    "APIKeyRotate",
    "APIKeyUsage",
    "BYOKeySet",
    "BYOKeyStatus",
    "Preferences",
    "Profile",
    "UsageLog",
    "UsageSummary",
    "WebhookSecretResponse",
    # Shares
    "PublicShare",
    "ShareCreate",
    "ShareCreateResponse",
    "ShareStats",
    "ShareVisitStats",
    # Streaming
    "ChunkEvent",
    "CompleteEvent",
    "HeartbeatEvent",
    "LogEvent",
    "ProgressEvent",
    "SSEErrorEvent",
    "StreamEvent",
    # Upload
    "JobDescriptionResponse",
    "JobTextRequest",
    "ResumeUploadResponse",
    # Webhooks
    "GenerationAwaitingInputEvent",
    "GenerationCompletedEvent",
    "GenerationFailedEvent",
    "WebhookEvent",
]
