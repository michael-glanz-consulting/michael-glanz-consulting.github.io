from typing import Annotated

from fastapi import Depends, FastAPI, HTTPException, status

from . import __version__
from .config import Settings, get_settings
from .role_catalog import SPECIALIST_ROLES
from .schemas import AgentInfo, HealthResponse, RunRequest, RunResponse
from .service import run_toni

app = FastAPI(
    title="Toni Agent Backend",
    description="Technisches Backend für Toni und das KI-Transformationsteam.",
    version=__version__,
)


@app.get("/health", response_model=HealthResponse, tags=["system"])
async def health(
    settings: Annotated[Settings, Depends(get_settings)],
) -> HealthResponse:
    return HealthResponse(
        status="ok",
        environment=settings.app_env,
        api_key_configured=bool(settings.openai_api_key),
    )


@app.get("/v1/agents", response_model=list[AgentInfo], tags=["agents"])
async def list_agents() -> list[AgentInfo]:
    coordinator = AgentInfo(
        key="toni",
        name="Toni",
        responsibility="Koordination, Synthese und Entscheidungsvorlage",
    )
    specialists = [
        AgentInfo(key=role.key, name=role.name, responsibility=role.responsibility)
        for role in SPECIALIST_ROLES
    ]
    return [coordinator, *specialists]


@app.post("/v1/runs", response_model=RunResponse, tags=["agents"])
async def create_run(
    request: RunRequest,
    settings: Annotated[Settings, Depends(get_settings)],
) -> RunResponse:
    if not settings.openai_api_key:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="OPENAI_API_KEY ist nicht konfiguriert.",
        )
    return await run_toni(request, settings)
