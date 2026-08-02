from fastapi.testclient import TestClient

from toni_backend.config import Settings, get_settings
from toni_backend.main import app


def no_key_settings() -> Settings:
    return Settings(openai_api_key=None, app_env="test")


app.dependency_overrides[get_settings] = no_key_settings
client = TestClient(app)


def test_health() -> None:
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json() == {
        "status": "ok",
        "environment": "test",
        "api_key_configured": False,
    }


def test_agent_catalog_includes_toni_and_specialists() -> None:
    response = client.get("/v1/agents")
    assert response.status_code == 200
    keys = {agent["key"] for agent in response.json()}
    assert {"toni", "tilo", "tim", "jan", "pia", "marika", "ben"} <= keys


def test_run_requires_api_key() -> None:
    response = client.post("/v1/runs", json={"message": "Bewerte das Projekt."})
    assert response.status_code == 503
    assert response.json()["detail"] == "OPENAI_API_KEY ist nicht konfiguriert."


def test_unknown_specialist_is_rejected() -> None:
    response = client.post(
        "/v1/runs",
        json={"message": "Bewerte das Projekt.", "requested_specialists": ["unbekannt"]},
    )
    assert response.status_code == 422

