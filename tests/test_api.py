import pytest
import httpx
import asyncio
import time


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


@pytest.mark.asyncio
@pytest.mark.integration
async def test_ping_not_blocked():
    """Verify server handles concurrent requests without blocking"""
    async with httpx.AsyncClient(base_url="http://localhost:8000") as client:
        # Start long-running request
        ask_task = asyncio.create_task(
            client.post(
                "/ask",
                json={"prompt": "Explain quantum computing in exhaustive detail"},
            )
        )

        # Immediately test ping response time
        start_time = time.time()
        ping_response = await client.get("/ping")
        elapsed_time = time.time() - start_time

        assert ping_response.status_code == 200
        assert elapsed_time < 1.0, "Ping response delayed, possible blocking"

        # Cleanup - wait for ask request to complete
        await ask_task
        assert ask_task.result().status_code == 200
