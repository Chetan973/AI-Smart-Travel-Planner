from typing import Any

from pydantic import BaseModel, Field


class ChatRequest(BaseModel):
    """One message in a persistent travel-planning conversation."""

    session_id: str = Field(min_length=1, max_length=100)
    message: str = Field(min_length=1, max_length=2_000)


class ChatResponse(BaseModel):
    session_id: str
    message: str
    phase: str
    missing_fields: list[str] = Field(default_factory=list)
    travel_details: dict[str, Any] = Field(default_factory=dict)
    travel_options: list[dict[str, Any]] = Field(default_factory=list)
