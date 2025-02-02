import pytest
from fastapi.testclient import TestClient
from main import app


@pytest.fixture
def client():
    """Fixture for FastAPI TestClient"""
    return TestClient(app)


def test_ping_route(client):
    """Test the ping endpoint"""
    response = client.get("/ping")
    assert response.status_code == 200
    assert response.json() == {"status": "ok", "message": "pong"}


def test_main_execution():
    """Test the main module execution"""
    import main

    assert hasattr(main, "app")  # Basic sanity check
