# Dont Block Ping Demo - FastAPI

A FastAPI-based service demonstrating basic health checks and blocking/non-blocking behavior.

## Features

- 🚀 FastAPI web server
- ✅ /ping health check endpoint

- 🔒 Environment-based configuration
- 🧪 Comprehensive test suite

## Quick Start

### Prerequisites

- Python 3.12+
- UV package manager (<https://github.com/astral-sh/uv>)

### Installation

    uv pip install .  # Install from pyproject.toml

For development with live reload:
    uv pip install -e .[dev]

### Running the Server

    uv run uvicorn main:app --reload

## API Reference

### GET /ping

Health check endpoint

Response:
    {
      "status": "ok",
      "message": "pong"
    }

### GET /sleep/{seconds}

Test endpoint that blocks for given seconds

Response:
    {
      "status": "ok",
      "slept": 5
    }

Example: `curl -X GET http://localhost:8000/ping`

## Testing

Run the main suite of interest:
    uv run pytest tests/test_api.py

Run all tests (unit + integration):
    uv run pytest tests/ -v

Run unit tests only:
    uv run pytest tests/ -m unit -v --cov=main --cov-report=html --cov-report=term

Run integration tests:
    # First start the server in one terminal:
    uv run uvicorn main:app --reload

    # Then in another terminal:
    uv run pytest tests/ -m integration -v --cov=main --cov-append

Tests include:

- Environment variable validation
- Endpoint response checks
- Full service integration tests

## Contributing

1. Clone the repository
2. Create a new branch
3. Add tests for new features
4. Submit a pull request

## License

MIT License - see LICENSE for details
