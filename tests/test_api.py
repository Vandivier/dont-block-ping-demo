import pytest
import httpx

@pytest.mark.asyncio
@pytest.mark.integration
async def test_api_integration():
    """Test full API integration with actual running server"""
    async with httpx.AsyncClient(base_url="http://localhost:8000") as client:
        # Test ping endpoint
        response = await client.get("/ping")
        assert response.status_code == 200
        
        # Test ask endpoint
        test_prompt = "Explain quantum computing in simple terms"
        response = await client.post("/ask", json={"prompt": test_prompt})
        assert response.status_code == 200
        assert "quantum" in response.json()["response"].lower() 