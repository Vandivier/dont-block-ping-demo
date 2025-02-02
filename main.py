from dotenv import load_dotenv
import os
from fastapi import FastAPI, HTTPException, Body
from fastapi.middleware.cors import CORSMiddleware
import google.generativeai as genai
import time
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


# Load environment variables from .env file
load_dotenv()

app = FastAPI()

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize Gemini - Make sure to set your API key in environment
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
if not GEMINI_API_KEY:
    raise RuntimeError("GEMINI_API_KEY environment variable not set")

genai.configure(api_key=GEMINI_API_KEY)
model = genai.GenerativeModel("gemini-pro")


@app.get("/ping")
async def ping():
    return {"status": "ok", "message": "pong"}


@app.post("/ask")
async def ask_llm(payload: dict = Body(...)):
    prompt = payload.get("prompt")
    if not prompt:
        raise HTTPException(status_code=400, detail="Prompt is required")
    try:
        response = model.generate_content(prompt)
        return {"status": "success", "response": response.text}
    except Exception as e:
        raise HTTPException(
            status_code=503, detail=f"Error generating response: {str(e)}"
        )


@app.get("/sleep/{seconds}")
async def sleep(seconds: int):
    """Test endpoint that blocks for given seconds"""
    logger.info(f"Sleeping for {seconds} seconds")
    time.sleep(seconds)
    return {"status": "ok", "slept": seconds}


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8000, reload=True)
