from toni_backend.schemas import RunRequest
from toni_backend.service import _build_input


def test_build_input_keeps_context_and_task_separate() -> None:
    request = RunRequest(
        message="Erstelle eine Entscheidungsvorlage.",
        project_context={"region": "NRW", "status": "Konzept"},
    )
    result = _build_input(request)
    assert "PROJEKTKONTEXT" in result
    assert '"region": "NRW"' in result
    assert "AUFTRAG" in result
    assert "Erstelle eine Entscheidungsvorlage." in result

