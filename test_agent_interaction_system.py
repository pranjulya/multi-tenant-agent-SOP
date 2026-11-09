from fastapi.testclient import TestClient

import agent_interaction_system as app_module
from agent_interaction_system import app


def setup_function():
    app_module.tenant_data.clear()


def test_blank_tenant_id_is_rejected():
    client = TestClient(app)
    for tenant_id in ("", "   ", "\t"):
        response = client.post(
            "/agent/interact",
            json={"tenant_id": tenant_id, "message": "hello"},
        )
        assert response.status_code == 422, tenant_id
        assert tenant_id.strip() not in app_module.tenant_data
        assert "" not in app_module.tenant_data


def test_blank_message_is_rejected():
    client = TestClient(app)
    response = client.post(
        "/agent/interact",
        json={"tenant_id": "tenant1", "message": "  "},
    )
    assert response.status_code == 422
    assert "tenant1" not in app_module.tenant_data


def test_valid_interaction_is_isolated_per_tenant():
    client = TestClient(app)
    first = client.post(
        "/agent/interact",
        json={"tenant_id": "tenant1", "message": "hello"},
    )
    second = client.post(
        "/agent/interact",
        json={"tenant_id": "tenant2", "message": "ping"},
    )
    assert first.status_code == 200
    assert second.status_code == 200
    history1 = client.get("/agent/history/tenant1")
    history2 = client.get("/agent/history/tenant2")
    assert history1.status_code == 200
    assert history2.status_code == 200
    assert len(history1.json()["history"]) == 1
    assert len(history2.json()["history"]) == 1
    assert history1.json()["history"][0]["message"] == "hello"
    assert history2.json()["history"][0]["message"] == "ping"
