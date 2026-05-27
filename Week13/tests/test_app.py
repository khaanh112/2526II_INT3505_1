import pathlib
import sys

import pytest

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[1]))

from app import api_keys, app, developers, usage_events


@pytest.fixture(autouse=True)
def clean_state():
    developers.clear()
    api_keys.clear()
    usage_events.clear()
    yield
    developers.clear()
    api_keys.clear()
    usage_events.clear()


@pytest.fixture
def client():
    app.config.update(TESTING=True)
    return app.test_client()


def register(client, plan="free"):
    return client.post("/api/developers/register", json={
        "name": "Minh",
        "email": "minh@example.com",
        "plan": plan
    })


def test_portal_exposes_product_links(client):
    response = client.get("/")

    assert response.status_code == 200
    payload = response.get_json()
    assert payload["links"]["register"] == "/api/developers/register"
    assert payload["links"]["analytics"] == "/api/analytics/kpis"


def test_register_developer_and_call_sandbox(client):
    register_response = register(client, plan="growth")
    api_key = register_response.get_json()["api_key"]

    sandbox_response = client.get(
        "/api/sandbox/weather?city=Hanoi",
        headers={"X-API-Key": api_key}
    )

    assert register_response.status_code == 201
    assert sandbox_response.status_code == 200
    payload = sandbox_response.get_json()
    assert payload["data"]["city"] == "Hanoi"
    assert payload["served_for"]["plan"] == "growth"


def test_analytics_tracks_developer_call_volume_and_error_rate(client):
    register(client)
    client.get("/api/sandbox/weather")

    kpi_response = client.get("/api/analytics/kpis")

    assert kpi_response.status_code == 200
    payload = kpi_response.get_json()
    assert payload["developer_registrations"] == 1
    assert payload["call_volume"] == 2
    assert payload["error_count"] == 1
    assert payload["error_rate"] == 0.5
