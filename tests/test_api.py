import pytest
import httpx
import asyncio
import time


SECONDS_TO_SLEEP = 5
FAST_RESPONSE = SECONDS_TO_SLEEP - 2


@pytest.mark.asyncio
@pytest.mark.integration
async def test_ping_blocked_by_sync_sleeping():
    """Verify server handles concurrent requests even with blocking sleep"""
    async with httpx.AsyncClient(
        base_url="http://localhost:8000", timeout=60.0
    ) as client:
        # Start sleep request first
        sleep_task = asyncio.create_task(client.get(f"/sleep/{SECONDS_TO_SLEEP}"))
        await asyncio.sleep(0.1)  # Allow request to reach server

        # Test ping response time
        start_time = time.time()
        ping_response = await client.get("/ping")
        elapsed_time = time.time() - start_time

        assert ping_response.status_code == 200
        assert elapsed_time > FAST_RESPONSE, (
            f"Ping response unexpectedly fast, server may not be blocking. Request took {elapsed_time} seconds"
        )

        # Cleanup
        await sleep_task
        assert sleep_task.result().status_code == 200


@pytest.mark.asyncio
@pytest.mark.integration
async def test_ping_not_blocked_by_async_sleeping():
    """Verify server handles concurrent requests even with blocking sleep"""
    async with httpx.AsyncClient(
        base_url="http://localhost:8000", timeout=60.0
    ) as client:
        # Start sleep request first
        sleep_task = asyncio.create_task(client.get(f"/async-sleep/{SECONDS_TO_SLEEP}"))
        await asyncio.sleep(0.1)  # Allow request to reach server

        # Test ping response time
        start_time = time.time()
        ping_response = await client.get("/ping")
        elapsed_time = time.time() - start_time

        assert ping_response.status_code == 200
        assert elapsed_time < FAST_RESPONSE, (
            f"Ping response delayed, server is blocking. Request took {elapsed_time} seconds"
        )

        # Cleanup
        await sleep_task
        assert sleep_task.result().status_code == 200
