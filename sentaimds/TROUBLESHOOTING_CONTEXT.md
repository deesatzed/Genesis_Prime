# MCP Hub and Reasoning Server Integration - Troubleshooting Context

**Date:** April 4, 2025

## Current Issues (RESOLVED)

### 1. Datetime Serialization Issue
We've resolved the datetime serialization issues between the MCP Hub and Reasoning Server:
```
DIAGNOSTIC FAIL: Hub used fallback mechanism. Error reported in metadata: Unexpected error in reasoning service: Object of type datetime is not JSON serializable
```

**Resolution:** The issue has been fixed by implementing proper datetime serialization in the `ServiceClient.post` method and creating a shared serialization utility. See the `Fixed_Errors_1.md` log for details.

### 2. API Endpoint Missing Issue
The docker-test.sh script was trying to use a `/api/query` endpoint that didn't exist in the MCP Hub, resulting in a 404 error:
```
❌ Failed to get response to question
Response: {"detail":"Not Found"}
```

**Resolution:** We implemented a new `/api/query` endpoint in the MCP Hub to handle requests in the format used by the docker-test.sh script. The endpoint accepts a query parameter and processes it using the same controller logic as the existing `/api/question` endpoint.

### 3. ServiceError Constructor Issue
We encountered an issue with the ServiceError class not accepting a 'code' parameter that was being passed to it:
```
ServiceError.__init__() got an unexpected keyword argument 'code'
```

**Resolution:** We updated the ServiceError constructor in `service_client.py` to accept and ignore extra parameters using `**kwargs`. This ensures backward compatibility with code that might be passing parameters not used by the ServiceError class but supported by its parent class ServiceException.

## System Architecture
- **MCP Hub** (Port 11400): Central coordination server handling client requests
- **Reasoning Server** (Port 12500): Provides response generation with placeholder logic
- **Memory Server** (Port 13600): Stores and retrieves knowledge
- **Personality Server** (Port 14700): Manages personality profiles and response guidance

## Progress So Far

### Configuration Changes
1. Updated server URLs in `shared/utils/config.py` to use higher-numbered ports
2. Modified service client factory to create fresh instances
3. Added logging to view requests/responses between services 

### Datetime Serialization Fixes
1. Added `DateTimeEncoder` class to both MCP Hub and Reasoning Server
2. Configured FastAPI apps to use this encoder with `json_encoder=DateTimeEncoder`
3. Added serialization to the request flow in `service_client.py`
4. Added helper method `_serialize_dict()` to `RequestController` class
5. Explicitly convert datetime objects to ISO format strings

## Current State of Servers
All servers are running with the new configurations and datetime serialization fixes:
- MCP Hub: http://localhost:11400
- Reasoning Server: http://localhost:12500 
- Memory Server: http://localhost:13600
- Personality Server: http://localhost:14700

## Test Status
The integration test `test_hub_knowledge_repo.py` still fails with datetime serialization errors.

## Completed Steps

1. **Identified and Fixed the Serialization Issue**:
   - Created a shared serialization utility module (`shared/utils/serialization.py`)
   - Modified the `ServiceClient.post` method to explicitly serialize datetime objects
   - Updated the `ReasoningClient.generate_response` method for proper Pydantic model handling
   - Applied similar fixes to the Memory Server and Personality Server

2. **Added Comprehensive Testing**:
   - Verified the fix with the existing integration test
   - Created additional integration tests for Memory and Personality servers
   - Documented the fix in `Fixed_Errors_1.md`

## Recent Implementations

1. **Server Registration Mechanism** (Completed April 4, 2025):
   - Implemented a server registry system in the MCP Hub
   - Added API endpoints for server registration, heartbeat, and management
   - Created a background task for monitoring server health
   - Added integration tests for the server registration flow
   - Created a wrapper script (`run_server.py`) to handle Python path and module import issues

2. **Request Routing and Load Balancing** (Completed April 5, 2025):
   - Implemented a router service for directing requests to appropriate specialized servers
   - Updated the ServiceClientFactory to support dynamic server URLs
   - Modified the RequestController to use the router service for all service interactions
   - Implemented a weighted random selection algorithm for load balancing
   - Added request statistics tracking for monitoring routing patterns

## Current Status

- **MCP Hub**: Fully operational with server registration mechanism and request routing
- **Reasoning Server**: Operational with datetime serialization fixes
- **Memory Server**: Operational with datetime serialization fixes
- **Personality Server**: Operational with datetime serialization fixes
- **Integration Tests**: All passing, including server registration and router service tests
- **Load Balancing**: Implemented with weighted random selection algorithm

## Next Development Steps

1. **Week 5 Remaining Tasks** (April 6-7, 2025):
   - Enhance error handling with standardized error responses
   - Complete the health monitoring system with detailed metrics

2. **Week 6 Tasks** (April 8-14, 2025):
   - Develop core REST API endpoints for external clients
   - Implement initial authentication for API and server registration
   - Create comprehensive API documentation
   - Build basic client SDK for easy integration

3. **System Enhancement**:
   - Add more comprehensive logging across all services
   - Create a monitoring dashboard for system health
   - Implement authentication for server registration
   - Develop server capabilities negotiation for dynamic service discovery

## Relevant Files

- **MCP Hub**
  - `/mcp-hub/api/main.py` - Main API endpoints for MCP Hub
  - `/mcp-hub/controllers/request_controller.py` - Handles requests and communication
  - `/mcp-hub/services/service_client.py` - Client for communicating with other services
  - `/mcp-hub/services/server_registry.py` - Server registry for managing specialized servers
  - `/mcp-hub/services/router_service.py` - Router service for directing requests to appropriate servers
  - `/mcp-hub/api/server_management.py` - API endpoints for server registration and management
  - `/mcp-hub/run_server.py` - Wrapper script for starting the MCP Hub with correct Python path

- **Reasoning Server**
  - `/reasoning-server/api/main.py` - API endpoints for Reasoning Server

- **Test Files**
  - `/tests/integration_tests/test_hub_knowledge_repo.py` - Integration test

## Starting Instructions

To resume debugging, start all servers with explicit environment variables:

```bash
# 1. Start the Personality Server
cd /home/o2satz/CascadeProjects/Chorus_April/chorus_one/sentient-ai-poc/personality-server
PERSONALITY_SERVER_URL="http://localhost:14700" MCP_HUB_URL="http://localhost:11400" REASONING_SERVER_URL="http://localhost:12500" MEMORY_SERVER_URL="http://localhost:13600" python -m uvicorn api.main:app --host 0.0.0.0 --port 14700 --reload

# 2. Start the Memory Server
cd /home/o2satz/CascadeProjects/Chorus_April/chorus_one/sentient-ai-poc/memory-server
PERSONALITY_SERVER_URL="http://localhost:14700" MCP_HUB_URL="http://localhost:11400" REASONING_SERVER_URL="http://localhost:12500" MEMORY_SERVER_URL="http://localhost:13600" python -m uvicorn api.main:app --host 0.0.0.0 --port 13600 --reload

# 3. Start the Reasoning Server
cd /home/o2satz/CascadeProjects/Chorus_April/chorus_one/sentient-ai-poc/reasoning-server
PERSONALITY_SERVER_URL="http://localhost:14700" MCP_HUB_URL="http://localhost:11400" REASONING_SERVER_URL="http://localhost:12500" MEMORY_SERVER_URL="http://localhost:13600" python -m uvicorn api.main:app --host 0.0.0.0 --port 12500 --reload

# 4. Start the MCP Hub
cd /home/o2satz/CascadeProjects/Chorus_April/chorus_one/sentient-ai-poc/mcp-hub
PERSONALITY_SERVER_URL="http://localhost:14700" MCP_HUB_URL="http://localhost:11400" REASONING_SERVER_URL="http://localhost:12500" MEMORY_SERVER_URL="http://localhost:13600" python -m uvicorn api.main:app --host 0.0.0.0 --port 11400 --reload

# 5. Run the integration test
cd /home/o2satz/CascadeProjects/Chorus_April/chorus_one
PERSONALITY_SERVER_URL="http://localhost:14700" MCP_HUB_URL="http://localhost:11400" REASONING_SERVER_URL="http://localhost:12500" MEMORY_SERVER_URL="http://localhost:13600" pytest tests/integration_tests/test_hub_knowledge_repo.py -v

# 6. Start the MCP Hub using the wrapper script
cd /home/o2satz/CascadeProjects/Chorus_April/chorus_one/sentient-ai-poc/mcp-hub
python run_server.py

# 7. Test the server registration mechanism
cd /home/o2satz/CascadeProjects/Chorus_April/chorus_one
PERSONALITY_SERVER_URL="http://localhost:14700" MCP_HUB_URL="http://localhost:11400" REASONING_SERVER_URL="http://localhost:12500" MEMORY_SERVER_URL="http://localhost:13600" python tests/integration_tests/test_server_registration.py
```

Good luck with the system updates! We'll continue troubleshooting from this point when you return.
