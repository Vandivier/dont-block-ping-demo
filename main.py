import asyncio
from fastapi import FastAPI
import time
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI()


@app.get("/ping")
async def ping():
    return {"status": "ok", "message": "pong"}


@app.get("/async-sleep/{seconds}")
async def asyncio_sleep(seconds: int):
    """Test endpoint that blocks for given seconds"""
    logger.info(f"Sleeping for {seconds} seconds")
    await asyncio.sleep(seconds)
    return {"status": "ok", "slept": seconds}


@app.get("/sleep/{seconds}")
async def sleep(seconds: int):
    """Test endpoint that blocks for given seconds"""
    logger.info(f"Sleeping for {seconds} seconds")
    time.sleep(seconds)
    return {"status": "ok", "slept": seconds}


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8000, reload=True)
