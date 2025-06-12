# Project Handoff Document

**Project:** Sentient AI Proof of Concept  
**Date:** April 11, 2025  
**Status:** In Progress - Implementing Memory Server Enhancements  

## Project Overview

The Sentient AI Proof of Concept (PoC) is a distributed system for intelligent conversational agents, with the MCP Hub serving as the central orchestration component. The system follows a microservices architecture with specialized servers for reasoning, memory, and personality.

## Environment Setup

### System Requirements

- **OS:** Linux
- **Python Version:** 3.12
- **Node Version:** Not applicable (Python-based project)

### Conda Environment

```bash
# Create conda environment
conda create -n mcp-env python=3.12
conda activate mcp-env

# Install dependencies
cd /home/o2satz/CascadeProjects/Chorus_April/chorus_one/sentient-ai-poc
pip install -r requirements.txt
```

### Key Dependencies

- FastAPI
- Uvicorn
- aiohttp (for Thousand Questions processor)
- tqdm (for progress bars)
- pytest (for testing)

### Environment Variables

```
MCP_HUB_URL=http://localhost:11400
REASONING_SERVER_URL=http://localhost:8000
MEMORY_SERVER_URL=http://localhost:13600
PERSONALITY_SERVER_URL=http://localhost:14700
LOG_LEVEL=DEBUG
```

## Project Structure

```
sentient-ai-poc/
├── shared/                        # Shared code used across services
│   ├── models/                    # Pydantic models
│   └── utils/                     # Utility functions
│
├── memory-server/                 # Memory service
│   ├── api/                       # API endpoints
│   ├── models/                    # Service-specific models
│   └── thousand_questions/        # Thousand Questions parser
│
├── thousand_questions_processor.py # Asynchronous batch processor
│
├── personality-server/            # Personality service
│   ├── api/                       # API endpoints
│   └── models/                    # Personality models
│
├── reasoning-server/              # Reasoning service
│   ├── api/                       # API endpoints
│   └── models/                    # Reasoning models
│
├── mcp-hub/                       # MCP Hub central orchestration
│   ├── api/                       # API endpoints
│   ├── controllers/               # Request handling
│   └── services/                  # Service clients
│
├── web-interface/                 # Web interface
│   ├── static/                    # Static assets
│   └── templates/                 # HTML templates
│
└── tests/                         # Test suites
    ├── unit/                      # Unit tests
    └── integration/               # Integration tests
```

## Current Status

### Completed Features

1. **Server Registration System**
   - Implemented ServerRegistry class for managing server instances
   - Created API endpoints for server registration, deregistration, and listing
   - Added validation for server registration requests

2. **Error Handling System**
   - Implemented standardized error responses across all services
   - Created exception handlers for all error types
   - Added custom 404 handler for non-existent endpoints

3. **Basic Infrastructure**
   - Set up FastAPI application structure
   - Implemented CORS middleware
   - Created utility functions for common operations
   
4. **Enhanced Reasoning Responses**
   - Implemented improved response generation for common questions
   - Created a library of detailed responses for philosophical, technical, and general knowledge queries
   - Integrated response generation with the MCP Hub

5. **Thousand Questions Processing**
   - Parser for Thousand Questions dataset implemented
   - Basic categorization and metadata extraction functional
   - Asynchronous batch processor implemented with progress tracking
   - Incremental saving and error handling mechanisms in place

6. **Reasoning Server LLM Integration Debugging**
   - Successfully diagnosed and fixed issues preventing the Reasoning Server from communicating with the OpenRouter LLM.
   - Resolved dependency conflicts, environment variable loading errors, Python import errors (missing __init__.py, incorrect PYTHONPATH/working directory).
   - Verified endpoint functionality with curl requests.

7. **Memory Server Enhancements**
   - Successfully integrated with PostgreSQL (v16) using SQLAlchemy (asyncio) and `asyncpg` driver.
   - Uses `pgvector` Docker image and enables the extension in the database (`memory_db`).
   - Connection issues (`socket.gaierror`) were resolved by URL-encoding the database password containing special characters (`@`).
   - Basic `/store_response` and `/get_knowledge` endpoints function using the database.
   - Currently running successfully on port `13600`.

### In-Progress Features

1. **Memory Server Knowledge Graph**
   - Enhancing Memory Server for knowledge graph storage and retrieval
   - Implementing semantic search capabilities

2. **Personality Profile Generation**
   - Developing system to generate personality profiles from question responses
   - Creating integration with Reasoning Server

3. **Monitoring Interface**
   - Designing tools for monitoring Thousand Questions processing
   - Implementing dashboard components

## Server Startup Sequence

### Prerequisite: Create Symbolic Links

```bash
# Create symbolic links for hyphenated directory names
ln -sf mcp-hub mcp_hub
ln -sf memory-server memory_server
ln -sf personality-server personality_server
ln -sf reasoning-server reasoning_server
```

### Stopping Existing Servers

```bash
# Kill all Python-based servers
pkill -f "python.*uvicorn"

# Alternatively, kill specific servers
pkill -f "python.*mcp.*hub"
pkill -f "run_error_demo"
```

### Starting the Servers

1. **Start the MCP Hub Server (Terminal 1):**
   ```bash
   cd /home/o2satz/CascadeProjects/Chorus_April/chorus_one/sentient-ai-poc
   python -m uvicorn mcp_hub.api.main:app --host 0.0.0.0 --port 11400 --reload
   ```

2. **Start the Reasoning Server (Terminal 2):**
   ```bash
   cd /home/o2satz/CascadeProjects/Chorus_April/chorus_one/sentient-ai-poc
   python -m uvicorn reasoning_server.api.main:app --host 0.0.0.0 --port 8000 --reload
   ```

3. **Start the Memory Server (Terminal 3):**
   ```bash
   cd /home/o2satz/CascadeProjects/Chorus_April/chorus_one/sentient-ai-poc
   python -m uvicorn memory_server.api.main:app --host 0.0.0.0 --port 13600 --reload
   ```

4. **Start the Personality Server (Terminal 4, optional):**
   ```bash
   cd /home/o2satz/CascadeProjects/Chorus_April/chorus_one/sentient-ai-poc
   python -m uvicorn personality_server.api.main:app --host 0.0.0.0 --port 14700 --reload
   ```

5. **Start the Web Interface (Terminal 5, optional):**
   ```bash
   cd /home/o2satz/CascadeProjects/Chorus_April/chorus_one/sentient-ai-poc/web-interface
   python app.py
   ```
   The web interface will be available at http://localhost:5000

## Verifying Server Status

```bash
# Check MCP Hub health
curl http://localhost:11400/health

# Check if servers are registered with MCP Hub
curl http://localhost:11400/api/servers

# Test question answering functionality
curl -X POST http://localhost:11400/api/question \
  -H "Content-Type: application/json" \
  -d '{"text": "What is your purpose?", "category": "identity"}'
```

## Running the Thousand Questions Processor

```bash
# Basic usage
cd /home/o2satz/CascadeProjects/Chorus_April/chorus_one/sentient-ai-poc
python thousand_questions_processor.py

# With custom options
python thousand_questions_processor.py --batch-size=20 --questions-path=/path/to/questions.json --output-path=/path/to/output.json
```

## Testing

### Running Tests

```bash
# Run all tests
cd /home/o2satz/CascadeProjects/Chorus_April/chorus_one/sentient-ai-poc
pytest tests/

# Run specific test file
pytest tests/test_thousand_questions_processor.py
```

## Known Issues and Workarounds

1. **Module Import Issues**
   - **Issue**: Python path and module import issues with hyphenated directories
   - **Workaround**: Use symbolic links and ensure PYTHONPATH includes the project root

2. **Server Not Picking Up Changes**
   - **Issue**: Server sometimes doesn't reflect code changes
   - **Workaround**: Restart the server completely (kill and restart)

3. **Datetime Serialization Issues**
   - **Issue**: JSON serialization issues with datetime objects
   - **Workaround**: Use the DateTimeEncoder class for serialization

## Implementation Plan

The current implementation plan is detailed in the `THOUSAND_QUESTIONS_ROADMAP.md` file. The key phases are:

1. **Phase 1: Core Batch Processing System** (Completed)
   - Asynchronous batch processor for Thousand Questions
   - Progress tracking and error handling
   - Comprehensive logging

2. **Phase 2: Memory Server Enhancements** (In Progress)
   - Knowledge graph capabilities
   - Semantic search for knowledge retrieval
   - Optimized storage format

3. **Phase 3: Personality Profile Integration** (Next)
   - Enhanced personality profiler
   - Profile storage and versioning
   - Integration with Reasoning Server

4. **Phase 4: MCP Hub Integration** (Planned)
   - MCP Hub controller for Thousand Questions
   - Knowledge routing
   - Authentication and security

5. **Phase 5: Monitoring and Management Interface** (Planned)
   - Command-line management tools
   - Web interface components
   - Analytics capabilities

## Documentation

The project includes several documentation files:

1. **README.md** - Overview, setup instructions, and basic usage
2. **DEMO_GUIDE.md** - Instructions for demonstrating the system
3. **SERVER_MANAGEMENT.md** - Procedures for managing servers
4. **SSAI_Workflow_Checklist.md** - Component status and workflow stages
5. **PROJECT_STATUS.md** - Detailed project status and next steps
6. **THOUSAND_QUESTIONS_ROADMAP.md** - Implementation plan for Thousand Questions system

## Next Steps

1. **Complete Memory Server Enhancements**
   - Implement vector search capabilities
   - Integrate with MCP Hub for knowledge retrieval
   - Enhance knowledge graph storage and retrieval

2. **Complete Health Monitoring System**
   - Implement periodic health checks for registered servers
   - Add automatic deregistration for unhealthy servers
   - Create dashboard for monitoring server health

3. **Implement Authentication for Server Registration**
   - Add API key or token-based authentication for server registration
   - Implement secure storage and validation of credentials

## Handoff Notes - April 11, 2025

### Project: MCP Swarm / Sentient AI PoC

### Current Status

*   **MCP Hub:** Basic functionality, connects to Reasoning and Personality servers. Needs integration with Memory Server.
*   **Reasoning Server:** Operational, integrates with shared LLM client, connects via MCP Hub.
*   **Personality Server:** Basic structure exists, needs implementation and integration.
*   **Memory Server:** 
    *   Successfully integrated with PostgreSQL (v16) using SQLAlchemy (asyncio) and `asyncpg` driver.
    *   Uses `pgvector` Docker image and enables the extension in the database (`memory_db`).
    *   Connection issues (`socket.gaierror`) were resolved by URL-encoding the database password containing special characters (`@`).
    *   Basic `/store_response` and `/get_knowledge` endpoints function using the database.
    *   Currently running successfully on port `13600`.
*   **Shared Utilities:** LLM Client (`shared/utils/llm_client.py`) implemented and used by Reasoning Server.

### Recent Accomplishments

*   Integrated PostgreSQL persistence into the Memory Server.
*   Configured database models and asynchronous sessions using SQLAlchemy.
*   Enabled `pgvector` extension.
*   Troubleshot and resolved complex database connection errors related to environment variables, dependencies (`asyncpg`), and password URL encoding.
*   Updated relevant documentation (`README.md`, `SETUP_AND_TESTING.md`, `docs/mcp_swarm_architecture.md`, `PROJECT_STATUS.md`, `Fixed_Errors_1.md`, created `memory_server/README.md`).

### Blockers

*   None specific to the Memory Server's core functionality at this moment.

### Next Steps / Priorities

1.  **Memory Server - Vector Search:**
    *   Choose and integrate a sentence transformer model/library (e.g., `sentence-transformers`) to generate embeddings for questions/responses stored in the Memory Server.
    *   Update the `MemoryEntry` model to include a `vector` column (using `pgvector.sqlalchemy.Vector`).
    *   Modify `/store_response` to generate and save the embedding.
    *   Implement a new endpoint (e.g., `/find_similar`) or modify `/get_knowledge` to perform vector similarity searches using `pgvector` operators (e.g., `<=>`).
2.  **MCP Hub - Memory Integration:**
    *   Add calls to the Memory Server's `/store_response` endpoint from the MCP Hub after a final response is generated.
    *   (Optional/Future) Add calls to the Memory Server's search endpoint from the MCP Hub *before* calling the Reasoning Server to potentially enrich the context.
3.  **Personality Server:** Implement core logic and integrate with MCP Hub.
4.  **Testing:** Add more robust integration tests for the Memory Server database interactions and API endpoints.

### Open Questions / Design Decisions

*   Which embedding model should be used for the Memory Server?
*   How exactly should memory retrieval influence the prompt sent to the Reasoning Server?
*   Error handling strategy across the different services.

## Conclusion

The Sentient AI PoC project has made significant progress, particularly with the implementation of the Thousand Questions processor and Memory Server enhancements. The next phase will focus on enhancing the Memory Server with knowledge graph capabilities, integrating it with the MCP Hub, and implementing personality profile generation from responses.

This handoff document provides a comprehensive overview of the project's current state, environment setup, and implementation plan to ensure a seamless resumption of work after the hardware maintenance.
