# Chorus One - Sentient AI PoC Setup and Testing Guide

## Project Overview

The Sentient AI Proof of Concept (PoC) is a distributed system for intelligent conversational agents, with the MCP Hub as the central orchestration component. This guide provides comprehensive instructions for setting up, running, and testing the system.

> **DOCKER-BASED DEPLOYMENT (RECOMMENDED)**
>
> We provide a Docker-based deployment method that eliminates symbolic link issues and permission problems:
>
> ```bash
> # Quick start with Docker
> ./docker-run.sh build  # Build images with your user permissions
> ./docker-run.sh start  # Start all services
> ./service-register.sh  # Register services with MCP Hub (IMPORTANT!)
> ./docker-test.sh       # Verify that everything is working
> ```
>
> See [README.docker.md](README.docker.md) for complete instructions and [README.service-registration.md](README.service-registration.md) for details on service registration.
>
> **The instructions below are for manual setup without Docker.**

## Environment Setup

### Python Environment

```bash
# Create conda environment
conda create -n mcp-env python=3.13
conda activate mcp-env

# Install dependencies
cd /home/o2satz/CascadeProjects/Chorus_April/chorus_one/sentient-ai-poc
pip install -r requirements.txt
```

### Required Environment Variables

```bash
# Core service URLs
export MCP_HUB_URL=http://localhost:11400
export REASONING_SERVER_URL=http://localhost:12500
export MEMORY_SERVER_URL=http://localhost:13600
export PERSONALITY_SERVER_URL=http://localhost:14700

# Email configuration (for notifications)
export EMAIL_HOST=smtp.example.com
export EMAIL_PORT=587
export EMAIL_USERNAME=user@example.com
export EMAIL_PASSWORD=password

# Logging configuration
export LOG_LEVEL=DEBUG
```

## Docker Setup

```bash
# Build Docker images
cd /home/o2satz/CascadeProjects/Chorus_April/chorus_one/sentient-ai-poc
docker-compose build

# Start containers
docker-compose up -d

# Stop containers
docker-compose down

# View logs
docker-compose logs -f
```

## Running the Services

### Before Starting Any Services

Always kill any existing servers to avoid port conflicts:

```bash
# Kill MCP Hub server
pkill -f "python run_server.py"

# Kill error demo server
pkill -f "run_error_demo"

# Kill all Python servers (use with caution)
pkill -f "python.*uvicorn"
```

### Starting the MCP Hub Server

```bash
cd /home/o2satz/CascadeProjects/Chorus_April/chorus_one/sentient-ai-poc
python run_server.py
```

### Running the Error Handling Demo

```bash
cd /home/o2satz/CascadeProjects/Chorus_April/chorus_one/sentient-ai-poc
python run_error_demo.py
```

## Setting up the Reasoning Server

This server handles the reasoning and inference logic for the conversational agents.

### Dependencies

*   Python packages listed in `reasoning_server/requirements.txt`.

### Environment Variables

Ensure the following variables are set in your root `.env` file:

```dotenv
REASONING_SERVER_HOST=127.0.0.1
REASONING_SERVER_PORT=12500
```

### Python Dependencies

Navigate to the project root (`sentient-ai-poc`) and install:

```bash
# Activate your virtual environment (e.g., mcp-env) first
source ../mcp-env/bin/activate 
pip install -r reasoning_server/requirements.txt
```

### Running the Reasoning Server

From the project root (`sentient-ai-poc`):

```bash
# Standard run
python -m uvicorn reasoning_server.api.main:app --port 12500 --host 0.0.0.0

# Development with auto-reload
python -m uvicorn reasoning_server.api.main:app --reload --port 12500 --host 0.0.0.0
```

The server will be available at `http://localhost:12500` and the API docs at `http://localhost:12500/docs`.

## Setting up the Memory Server

This server handles persistent storage of question-response pairs using PostgreSQL and the pgvector extension.

### Dependencies

*   PostgreSQL Database (v16+ recommended) with `pgvector` extension enabled.
*   Python packages listed in `memory_server/requirements.txt`.

### Database Setup (Docker Example)

1.  Pull the `pgvector` image:
    ```bash
    docker pull agnohq/pgvector:16
    ```
2.  Run the container, mapping host port 5532 to container port 5432 (adjust password and volume name as needed):
    ```bash
    docker run -d \
      --name pgvector_memory \
      -e POSTGRES_DB=memory_db \
      -e POSTGRES_USER=memory_user \
      -e POSTGRES_PASSWORD=YOUR_SECURE_PASSWORD \
      -e PGDATA=/var/lib/postgresql/data/pgdata \
      -v pgvolume_memory:/var/lib/postgresql/data \
      -p 5532:5432 \
      agnohq/pgvector:16
    ```
3.  Verify connection (you might need `postgresql-client` installed):
    ```bash
    psql -h 127.0.0.1 -p 5532 -U memory_user -d memory_db
    # Enter password when prompted
    # Check extension: \dx
    # Quit: \q
    ```

### Environment Variables

Ensure the following variables are set in your root `.env` file, matching your database setup:

```dotenv
MEMORY_DB_HOST=127.0.0.1
MEMORY_DB_PORT=5532
MEMORY_DB_USER=memory_user
MEMORY_DB_PASSWORD=YOUR_SECURE_PASSWORD
MEMORY_DB_NAME=memory_db
```

**Important:** If your password contains special characters (like `@`), ensure it is properly URL-encoded in `memory_server/database.py` using `urllib.parse.quote_plus()`. This was necessary to resolve connection issues.

### Python Dependencies

Navigate to the project root (`sentient-ai-poc`) and install:

```bash
# Activate your virtual environment (e.g., mcp-env) first
source ../mcp-env/bin/activate 
pip install -r memory_server/requirements.txt
```

### Running the Memory Server

From the project root (`sentient-ai-poc`):

```bash
# Standard run
python -m uvicorn memory_server.api.main:app --port 13600 --host 0.0.0.0

# Development with auto-reload
# Note: --reload might have issues with environment variable loading or network sockets.
# If encountering connection problems, try running without --reload first.
python -m uvicorn memory_server.api.main:app --reload --port 13600 --host 0.0.0.0
```

The server will be available at `http://localhost:13600` and the API docs at `http://localhost:13600/docs`.

## Setting up the MCP Hub

This server acts as the central orchestration component, handling requests and routing them to the appropriate services.

### Dependencies

*   Python packages listed in `mcp-hub/requirements.txt`.

### Environment Variables

Ensure the following variables are set in your root `.env` file:

```dotenv
MCP_HUB_HOST=127.0.0.1
MCP_HUB_PORT=11400
```

### Python Dependencies

Navigate to the project root (`sentient-ai-poc`) and install:

```bash
# Activate your virtual environment (e.g., mcp-env) first
source ../mcp-env/bin/activate 
pip install -r mcp-hub/requirements.txt
```

### Running the MCP Hub

From the project root (`sentient-ai-poc`):

```bash
# Standard run
python -m uvicorn mcp_hub.api.main:app --port 11400 --host 0.0.0.0

# Development with auto-reload
python -m uvicorn mcp_hub.api.main:app --reload --port 11400 --host 0.0.0.0
```

The server will be available at `http://localhost:11400` and the API docs at `http://localhost:11400/docs`.

## Testing

### Running Automated Tests

```bash
# Run all tests
cd /home/o2satz/CascadeProjects/Chorus_April/chorus_one/sentient-ai-poc
pytest tests/

# Run specific test file
pytest tests/test_server_registry.py

# Run with verbose output
pytest -v tests/
```

### Testing Error Handling

```bash
# Run the error handling demo server
python run_error_demo.py

# In a separate terminal, run the error tests
python test_all_errors.py
python test_404_endpoint.py
```

### Available Test Endpoints

| Endpoint | Description | Expected Status |
|----------|-------------|----------------|
| `/health` | Health check endpoint | 200 OK |
| `/api/query` | Query processing endpoint | 200 OK |
| `/api/question` | Legacy question answering endpoint | 200 OK |
| `/error/validation` | Validation error test | 400 Bad Request |
| `/error/resource` | Resource not found test | 404 Not Found |
| `/error/service` | Service error test | 500 Internal Server Error |
| `/error/http` | HTTP exception test | 404 Not Found |
| `/error/uncaught` | Uncaught exception test | 500 Internal Server Error |

## Project Structure

```
sentient-ai-poc/
├── mcp-hub/               # MCP Hub service
│   ├── api/               # API endpoints
│   │   ├── error_handlers.py  # Error handling
│   │   └── main.py        # Main FastAPI application
│   ├── controllers/       # Business logic controllers
│   └── services/          # Services (registry, router, etc.)
├── shared/                # Shared utilities
│   └── utils/
│       ├── config.py      # Configuration utilities
│       └── error_handling.py  # Error handling utilities
├── tests/                 # Test suite
├── run_server.py          # MCP Hub server runner
├── run_error_demo.py      # Error handling demo
├── test_all_errors.py     # Error handling tests
└── test_404_endpoint.py   # 404 error test
```

## Common Issues and Solutions

### Service Registration Issues

**Issue**: Services are not registered with the MCP Hub, causing errors like "No available reasoning server"

**Solution**: Manually register services using the `service-register.sh` script:

```bash
# Using the helper script (recommended)
./service-register.sh

# Or manually for individual services
curl -X POST -H "Content-Type: application/json" -d '{
  "id": "reasoning_server_1",
  "name": "Reasoning Server",
  "type": "reasoning",
  "url": "http://localhost:12500",
  "capabilities": ["generate_response"]
}' http://localhost:11400/api/servers/register
```

### Module Import Issues

**Issue**: Python cannot import modules with hyphenated names (e.g., `mcp-hub`).

**Solution**: The `run_server.py` script creates symbolic links from hyphenated directories to underscore-named modules:

```bash
# Manual fix if needed
cd /home/o2satz/CascadeProjects/Chorus_April/chorus_one/sentient-ai-poc
ln -s mcp-hub mcp_hub
```

> **Note**: The Docker deployment handles this issue automatically with a custom entrypoint script.

### Server Not Picking Up Changes

**Issue**: Server doesn't reflect code changes after modifications.

**Solution**: Restart the server completely:

```bash
pkill -f "python run_server.py"
python run_server.py
```

### Datetime Serialization Issues

**Issue**: JSON serialization errors with datetime objects.

**Solution**: Use the DateTimeEncoder class for serialization:

```python
from shared.utils.serialization import DateTimeEncoder
import json

# Serialize with datetime support
json_data = json.dumps(data, cls=DateTimeEncoder)
```

## Key Documentation Files

- `PROJECT_STATUS.md` - Current project status and next steps
- `docs/error_handling.md` - Error handling system documentation
- `Fixed_Errors_1.md` - Log of fixed errors and solutions
- `TROUBLESHOOTING_CONTEXT.md` - Context for troubleshooting issues

## Lessons Learned

1. **Error Handling**:
   - Always return proper Response objects (JSONResponse, HTMLResponse) from FastAPI exception handlers
   - Add custom handlers for common HTTP status codes (404, 500)
   - Test all error scenarios thoroughly
   - Ensure consistent error response formats across all endpoints
   - Use the ServiceException class hierarchy for structured error handling

2. **Server Setup**:
   - Use symbolic links for Python modules with hyphenated names
   - Set all required environment variables before starting servers
   - Kill existing servers before starting new ones to avoid port conflicts

3. **Testing Approach**:
   - Create dedicated test endpoints for specific scenarios
   - Use both automated tests and manual verification
   - Test non-happy paths explicitly (errors, edge cases)
   - Use docker-test.sh to verify service registration and basic API functionality

4. **API Design**:
   - Support multiple endpoint naming patterns for backward compatibility
   - Use flexible request processing with proper validation
   - Handle different client formats by accepting generic request bodies when needed

## Next Steps

1. **Complete Health Monitoring System**
   - Implement periodic health checks
   - Add automatic deregistration for unhealthy servers

2. **Implement Authentication for Server Registration**
   - Add API key or token-based authentication
   - Secure credential storage and validation

3. **Enhance Request Routing**
   - Complete load balancing implementation
   - Add circuit breaker pattern for handling failures

4. **Performance Optimization**
   - Profile application to identify bottlenecks
   - Optimize database queries and caching

5. **Documentation and Deployment**
   - Complete API documentation
   - Create deployment guides for different environments
