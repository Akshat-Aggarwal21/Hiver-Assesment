import pytest
from fastapi.testclient import TestClient
from web.server import app

client = TestClient(app)


def test_get_tickets():
    response = client.get("/api/tickets")
    assert response.status_code == 200
    data = response.json()
    assert len(data) >= 20
    assert "ticket_id" in data[0]
    assert "subject" in data[0]


def test_get_ticket_detail():
    response = client.get("/api/tickets/TICK-101")
    assert response.status_code == 200
    data = response.json()
    assert "ticket" in data
    assert "relevant_kb" in data
    assert data["ticket"]["ticket_id"] == "TICK-101"


def test_get_ticket_not_found():
    response = client.get("/api/tickets/NON_EXISTENT")
    assert response.status_code == 404


def test_get_kb():
    response = client.get("/api/kb")
    assert response.status_code == 200
    docs = response.json()
    assert len(docs) >= 7


def test_generate_endpoint():
    response = client.post("/api/generate", json={
        "ticket_id": "TICK-101",
        "provider": "mock"
    })
    assert response.status_code == 200
    data = response.json()
    assert "reply" in data
    assert "evaluation" in data
    assert data["evaluation"]["scores"]["composite_heqi"] > 60


def test_evaluate_endpoint():
    reply = "Hi Sarah, I processed your full refund of $1,440.00 and cancelled your account. Best regards, Hiver Support"
    response = client.post("/api/evaluate", json={
        "ticket_id": "TICK-101",
        "reply": reply
    })
    assert response.status_code == 200
    data = response.json()
    assert "scores" in data
    assert data["scores"]["composite_heqi"] > 40
