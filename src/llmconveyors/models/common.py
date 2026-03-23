"""Shared types, enums, and base model configuration."""

from __future__ import annotations

from typing import Literal

from pydantic import BaseModel, ConfigDict


def _to_camel(name: str) -> str:
    """Convert snake_case to camelCase for API field aliases."""
    parts = name.split("_")
    return parts[0] + "".join(word.capitalize() for word in parts[1:])


class APIModel(BaseModel):
    """Base model with camelCase alias support for all API models."""

    model_config = ConfigDict(
        alias_generator=_to_camel,
        populate_by_name=True,
    )


# ---------------------------------------------------------------------------
# Literal types (used across multiple modules)
# ---------------------------------------------------------------------------

AgentType = Literal["job-hunter", "b2b-sales"]

JobStatus = Literal["queued", "processing", "completed", "failed", "awaiting_input"]

LogLevel = Literal["debug", "info", "success", "warn", "error"]

ResumeTheme = Literal[
    "even",
    "stackoverflow",
    "class",
    "professional",
    "elegant",
    "macchiato",
    "react",
    "academic",
]

Tier = Literal["free", "byo"]

AIModel = Literal["flash", "pro"]

GenerationMode = Literal["standard", "cold_outreach"]

ResearchMode = Literal["parallel", "sequential"]

RenderFormat = Literal["pdf", "html"]

Grade = Literal["A", "B", "C", "D", "F"]

SessionLogRole = Literal["user", "assistant", "system", "tool", "status"]
