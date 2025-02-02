import pytest
import httpx
from httpx import ASGITransport
from main import app

@pytest.mark.asyncio
@pytest.mark.integration
async def test_api_integration():
    """Test full API integration with actual endpoints"""
    async with httpx.AsyncClient(
        transport=ASGITransport(app=app),
        base_url="http://testserver"
    ) as client:
        # Test ping endpoint
        response = await client.get("/ping")
        assert response.status_code == 200
        
        # Test ask endpoint
        test_prompt = "Explain quantum computing in simple terms"
        response = await client.post("/ask", json={"prompt": test_prompt})
        assert response.status_code == 200
        assert "quantum" in response.json()["response"].lower() 