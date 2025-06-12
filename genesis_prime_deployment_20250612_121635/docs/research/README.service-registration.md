# Sentient AI PoC - Service Registration Fix

This document explains how to fix the service registration issue in the Sentient AI PoC Docker deployment.

## Problem

The issue is that services (Reasoning Server, Memory Server, Personality Server) are not automatically registering with the MCP Hub, causing the system to operate in a degraded mode where requests fail with errors like:

```
No available reasoning server
```

## Solution

The solution is to manually register the services with the MCP Hub using the provided scripts:

1. `service-register.sh` - A script that registers all services with the MCP Hub
2. `docker-test.sh` - A test script that verifies service registration and runs a basic question test

## How to Use

### Deploying with Docker

1. Build the Docker images:
   ```bash
   # Make sure you're in the sentient-ai-poc directory
   cd /home/o2satz/CascadeProjects/Chorus_April/chorus_one/sentient-ai-poc
   
   # Build the images
   ./docker-run.sh build
   ```

2. Start the services:
   ```bash
   ./docker-run.sh start
   ```

3. Register the services with the MCP Hub:
   ```bash
   ./service-register.sh
   ```

4. Test that everything is working:
   ```bash
   ./docker-test.sh
   ```

### Understanding the Registration Process

In a microservices architecture, services need to register themselves with a central registry (in this case, the MCP Hub) so that they can be discovered and used by other services.

The registration process involves:

1. The service starting up and becoming available
2. The service sending a registration request to the MCP Hub with its:
   - ID
   - Name
   - Type (reasoning, memory, personality)
   - URL
   - Capabilities (what it can do)

3. The MCP Hub storing this information and using it to route requests

In our Docker deployment, the services are available at their container names (e.g., `reasoning-server:12500`) within the Docker network.

## Technical Details

### Service Registration Payload

For example, the Reasoning Server registers with this payload:

```json
{
  "id": "reasoning_server_1",
  "name": "Reasoning Server",
  "type": "reasoning",
  "url": "http://reasoning-server:12500",
  "capabilities": ["generate_response"]
}
```

### MCP Hub Server Registration Endpoint

The MCP Hub exposes an endpoint for service registration:

```
POST /api/servers/register
```

### Service-to-Service Communication

In a Docker Compose setup:
- Each service can reach other services using their container names as hostnames
- For example, the Reasoning Server is available at `http://reasoning-server:12500` within the network

## Long-Term Improvements

For a more robust solution:

1. Implement automatic service registration on startup
   - Each service could register itself when it starts
   - This would be done in the service's code

2. Implement health checks and heartbeats
   - Services would regularly send heartbeats to the MCP Hub
   - The MCP Hub would monitor service health and update status

3. Use a dedicated service discovery tool
   - For larger deployments, consider tools like Consul or etcd
   - These provide more advanced service discovery features

## Troubleshooting

If services fail to register:

1. Check that all services are running:
   ```bash
   docker-compose ps
   ```

2. Check the logs for each service:
   ```bash
   docker-compose logs mcp-hub
   docker-compose logs reasoning-server
   docker-compose logs memory-server
   docker-compose logs personality-server
   ```

3. Try manually registering a service:
   ```bash
   curl -X POST -H "Content-Type: application/json" -d '{
     "id": "reasoning_server_1",
     "name": "Reasoning Server",
     "type": "reasoning",
     "url": "http://reasoning-server:12500",
     "capabilities": ["generate_response"]
   }' http://localhost:11400/api/servers/register
   ```

4. Verify registered services:
   ```bash
   curl http://localhost:11400/api/servers/list
   ```