import os
import pytest
from fastapi.testclient import TestClient
from main import app

client = TestClient(app)

def test_environment_variables_loaded():
    """Test that environment variables are properly loaded"""
    assert os.getenv("GEMINI_API_KEY") is not None, "GEMINI_API_KEY should be set in .env"

def test_ping_route():
    """Test the ping endpoint"""
    response = client.get("/ping")
    assert response.status_code == 200
    assert response.json() == {"status": "ok", "message": "pong"}

@pytest.mark.asyncio
@pytest.mark.unit
async def test_gemini_integration():
    """Test basic Gemini API interaction"""
    from main import model
    response = await model.generate_content_async("Say 'hello world'")
    assert "hello" in response.text.lower() 