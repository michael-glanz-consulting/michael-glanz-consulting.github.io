from typing import Any

from pydantic import BaseModel, Field, field_validator

from .role_catalog import ROLE_BY_KEY


class RunRequest(BaseModel):
    message: str = Field(min_length=3, max_length=20_000)
    project_context: dict[str, Any] = Field(default_factory=dict)
    requested_specialists: list[str] | None = None

    @field_validator("requested_specialists")
    @classmethod
    def validate_specialists(cls, value: list[str] | None) -> list[str] | None:
        if value is None:
            return value
        normalized = list(dict.fromkeys(key.lower().strip() for key in value))
        unknown = sorted(set(normalized) - set(ROLE_BY_KEY))
        if unknown:
            allowed = ", ".join(ROLE_BY_KEY)
            raise ValueError(f"Unbekannte Fachagenten: {', '.join(unknown)}. Erlaubt: {allowed}")
        if not normalized:
            raise ValueError("Mindestens ein Fachagent muss ausgewählt werden.")
        return normalized


class RunResponse(BaseModel):
    run_id: str
    coordinator: str = "Toni"
    model: str
    output: str


class AgentInfo(BaseModel):
    key: str
    name: str
    responsibility: str


class HealthResponse(BaseModel):
    status: str
    environment: str
    api_key_configured: bool

