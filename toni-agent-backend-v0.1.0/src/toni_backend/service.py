import json
from uuid import uuid4

from agents import Runner

from .agent_factory import build_toni
from .config import Settings
from .schemas import RunRequest, RunResponse


def _build_input(request: RunRequest) -> str:
    context = json.dumps(request.project_context, ensure_ascii=False, indent=2, default=str)
    return (
        "PROJEKTKONTEXT\n"
        f"{context if request.project_context else 'Kein zusätzlicher Kontext übergeben.'}\n\n"
        "AUFTRAG\n"
        f"{request.message}"
    )


async def run_toni(request: RunRequest, settings: Settings) -> RunResponse:
    toni = build_toni(settings, request.requested_specialists)
    result = await Runner.run(toni, _build_input(request), max_turns=10)

    return RunResponse(
        run_id=str(uuid4()),
        model=settings.openai_model,
        output=str(result.final_output),
    )

