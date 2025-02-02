# Dont Block Ping Demo

A FastAPI-based service with Gemini AI integration demonstrating basic health checks and LLM interactions.

## Features

- 🚀 FastAPI web server
- ✅ /ping health check endpoint
- 🤖 /ask endpoint for Gemini AI queries
- 🔒 Environment-based configuration
- 🧪 Comprehensive test suite

## Quick Start

### Prerequisites

- Python 3.12+
- UV package manager (<https://github.com/astral-sh/uv>)
- Gemini API key (<https://ai.google.dev/>)

### Installation

    uv pip install .  # Install from pyproject.toml

For development with live reload:
    uv pip install -e .[dev]

### Configuration

1. Create .env file:

    echo "GEMINI_API_KEY=your_api_key_here" > .env

### Running the Server

    uvicorn main:app --reload

## API Reference

### GET /ping

Health check endpoint

Response:
    {
      "status": "ok",
      "message": "pong"
    }

### POST /ask

Submit prompts to Gemini AI

Request Body:
    {
      "prompt": "your question here"
    }

Example:
    curl -X POST "<http://localhost:8000/ask>" \
      -H "Content-Type: application/json" \
      -d '{"prompt":"Explain quantum computing in simple terms"}'

## Testing

Run the test suite:

    pytest tests/ -v

Tests include:

- Environment variable validation
- Endpoint response checks
- Gemini API integration
- Full service integration tests

## Environment Variables

| Variable          | Description                      |
|-------------------|----------------------------------|
| GEMINI_API_KEY    | Google Gemini API key (required) |

## Contributing

1. Clone the repository
2. Create a new branch
3. Add tests for new features
4. Submit a pull request

## License

MIT License - see LICENSE for details
