import pytest
import httpx
import asyncio
import time


@pytest.mark.asyncio
@pytest.mark.integration
async def test_api_integration():
    """Test full API integration with actual running server"""
    async with httpx.AsyncClient(base_url="http://localhost:8000", timeout=60.0) as client:
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
    async with httpx.AsyncClient(base_url="http://localhost:8000", timeout=60.0) as client:
        # Start long-running request
        ask_task = asyncio.create_task(
            client.post(
                "/ask",
                json={"prompt": "Fill in the blank: Please Excuse My Dear Aunt _____."},
            )
        )

        # Immediately test ping response time
        start_time = time.time()
        ping_response = await client.get("/ping")
        elapsed_time = time.time() - start_time

        assert ping_response.status_code == 200
        assert elapsed_time < 1.0, "Ping response delayed, possible blocking"

        # Cleanup - wait for ask request to complete
        result = await ask_task

        assert result.status_code == 200
        assert result.json()["response"] == "Sally", f"Response should be 'Sally' but got {result.json()['response']}"


@pytest.mark.asyncio
@pytest.mark.integration
async def test_ping_not_blocked_by_sleeping():
    """Verify server handles concurrent requests even with blocking sleep"""
    async with httpx.AsyncClient(base_url="http://localhost:8000", timeout=60.0) as client:
        wait_seconds = 5
        fast_response = wait_seconds - 2
        
        # Start sleep request first
        sleep_task = asyncio.create_task(client.get(f"/sleep/{wait_seconds}"))
        await asyncio.sleep(0.1)  # Allow request to reach server

        # Test ping response time
        start_time = time.time()
        ping_response = await client.get("/ping")
        elapsed_time = time.time() - start_time
        
        assert ping_response.status_code == 200
        assert elapsed_time < fast_response, \
            f"Ping response delayed, server is blocking. Request took {elapsed_time} seconds"
        
        # Cleanup
        await sleep_task
        assert sleep_task.result().status_code == 200

