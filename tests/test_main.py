import os
import pytest
from fastapi.testclient import TestClient
from main import app


@pytest.fixture
def client():
    """Fixture for FastAPI TestClient"""
    return TestClient(app)


def test_environment_variables_loaded():
    """Test that environment variables are properly loaded"""
    assert os.getenv("GEMINI_API_KEY") is not None, (
        "GEMINI_API_KEY should be set in .env"
    )


def test_ping_route(client):
    """Test the ping endpoint"""
    response = client.get("/ping")
    assert response.status_code == 200
    assert response.json() == {"status": "ok", "message": "pong"}


@pytest.mark.asyncio
@pytest.mark.unit
async def test_gemini_response():
    """Test basic Gemini API interaction"""
    from main import model

    response = await model.generate_content_async("Say 'hello world'")
    assert "hello" in response.text.lower()


def test_missing_api_key(monkeypatch):
    """Test missing GEMINI_API_KEY environment variable"""
    monkeypatch.delenv("GEMINI_API_KEY", raising=False)
    with pytest.raises(RuntimeError) as exc_info:
        from main import GEMINI_API_KEY  # noqa: F401
    assert "GEMINI_API_KEY environment variable not set" in str(exc_info.value)


@pytest.mark.asyncio
@pytest.mark.unit
async def test_ask_endpoint_error_handling(mocker, client):
    """Test error handling in ask endpoint"""
    # Test missing prompt
    response = client.post("/ask", json={})
    assert response.status_code == 400
    assert "Prompt is required" in response.json()["detail"]

    # Mock Gemini API failure
    mocker.patch("main.model.generate_content", side_effect=Exception("API Error"))
    response = client.post("/ask", json={"prompt": "test"})
    assert response.status_code == 503
    assert "Error generating response" in response.json()["detail"]


def test_cors_headers(client):
    """Test CORS headers are properly set"""
    response = client.options("/ping")
    assert response.headers["access-control-allow-origin"] == "*"
    assert response.headers["access-control-allow-methods"] == "*"


def test_main_execution():
    """Test the main module execution"""
    import main

    assert hasattr(main, "app")  # Basic sanity check
