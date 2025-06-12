# Chorus One / Sentient AI POC - Next Build & Test Steps

## Overview

Based on review of the current project status, this document outlines the next concrete steps for moving the Chorus One / Sentient AI POC project forward. Following these steps in order will ensure methodical progress toward completing the remaining features.

## Current Build Status Issues

Several issues were identified during our initial build attempt:

1. Missing requirements in service config files - Package requirements for each service aren't consistent
2. Module import errors in Docker containers - particularly with python-dotenv vs python_dotenv naming
3. Symbolic linking issues within containers
4. Service registration errors with the MCP Hub

These issues need to be addressed first before proceeding with feature development.

## Pre-requisites

- Conda environment with Python 3.12 (`mcp-env`)
- Docker and Docker Compose for containerized testing
- PostgreSQL with pgvector extension (when not using Docker)

## Next Steps in Priority Order

### 1. Fix Docker Build Configuration Issues

- [ ] Update all service requirements.txt files to have consistent package naming
- [ ] Modify Dockerfiles to ensure proper symbolic linking between services
- [ ] Fix package import issues in all service modules
- [ ] Configure proper service registration with MCP Hub

```bash
# Check Docker container logs for specific errors
docker-compose logs mcp-hub
docker-compose logs reasoning-server
docker-compose logs memory-server
docker-compose logs personality-server

# Ensure proper symbolic links are created in Docker containers
docker-compose exec mcp-hub ls -la /app

# Verify proper Python package installation
docker-compose exec reasoning-server pip list
```

### 2. Complete Thousand Questions Processing System

- [ ] Implement the full asynchronous batch processor in `thousand_questions_processor.py`
- [ ] Add progress tracking and error handling to the batch processor
- [ ] Create a test suite for the Thousand Questions processor
- [ ] Integrate Thousand Questions data with the Memory Server's knowledge repository

```bash
# Testing the Thousand Questions parser
cd /home/o2satz/CascadeProjects/Chorus_April/chorus_one/sentient-ai-poc
python -m memory_server.thousand_questions.parser --verbose

# Run the batch processor once implemented
python thousand_questions_processor.py
```

### 2. Complete Memory Server Integration

- [ ] Extend Memory Server with knowledge graph capabilities
- [ ] Implement vector similarity search for knowledge retrieval
- [ ] Verify PostgreSQL and pgvector integration
- [ ] Test Memory Server integration with MCP Hub

```bash
# Start Memory Server
cd /home/o2satz/CascadeProjects/Chorus_April/chorus_one/sentient-ai-poc
python -m uvicorn memory_server.api.main:app --port 13600 --host 0.0.0.0

# Run Memory Server integration tests
pytest tests/integration_tests/test_memory_server.py
```

### 3. Implement Health Monitoring System

- [ ] Complete periodic health checks for registered servers
- [ ] Add automatic deregistration for unhealthy servers
- [ ] Create monitoring dashboard for system health
- [ ] Test failover mechanisms

```bash
# Start Docker environment for testing
./docker-run.sh build
./docker-run.sh start
./service-register.sh

# Test health monitoring endpoints
curl http://localhost:11400/api/health
curl http://localhost:11400/api/servers/health
```

### 4. Implement Authentication for Server Registration

- [ ] Add API key or token-based authentication
- [ ] Implement secure storage and validation of credentials
- [ ] Create test suite for authentication system

```bash
# Test authentication for server registration (once implemented)
curl -X POST -H "Content-Type: application/json" -H "Authorization: Bearer TEST_TOKEN" \
  -d '{
    "id": "reasoning_server_1",
    "name": "Reasoning Server",
    "type": "reasoning",
    "url": "http://localhost:12500",
    "capabilities": ["generate_response"]
  }' http://localhost:11400/api/servers/register
```

### 5. Enhance Request Routing

- [ ] Complete load balancing implementation
- [ ] Add circuit breaker pattern for handling server failures
- [ ] Implement request retry mechanisms
- [ ] Test request routing with multiple server instances

```bash
# Start multiple instances for load balancing testing
docker-compose up -d --scale reasoning-server=3
./service-register.sh

# Test load balancing (once implemented)
for i in {1..10}; do
  curl -X POST -H "Content-Type: application/json" \
    -d '{"query": "Test question", "category": "general"}' \
    http://localhost:11400/api/query
done
```

### 6. Performance Optimization

- [ ] Profile the application to identify bottlenecks
- [ ] Optimize database queries and implement caching
- [ ] Implement connection pooling for external services
- [ ] Run performance tests and document results

```bash
# Run performance tests (after optimization)
python -m tests.performance_tests.test_response_generation
python -m tests.performance_tests.test_memory_retrieval
```

### 7. Complete Personality Server Implementation

- [ ] Implement personality profile generation
- [ ] Add response guidance based on personality traits
- [ ] Create test suite for Personality Server
- [ ] Integrate Personality Server with MCP Hub workflow

```bash
# Start Personality Server
cd /home/o2satz/CascadeProjects/Chorus_April/chorus_one/sentient-ai-poc
python -m uvicorn personality_server.api.main:app --port 14700 --host 0.0.0.0

# Test Personality Server integration
pytest tests/integration_tests/test_personality_server.py
```

### 8. Comprehensive System Testing

- [ ] Create end-to-end test suite for full system
- [ ] Test all error scenarios and edge cases
- [ ] Verify Docker deployment workflow
- [ ] Document any issues or limitations found

```bash
# Run complete test suite
cd /home/o2satz/CascadeProjects/Chorus_April/chorus_one/sentient-ai-poc
pytest tests/

# Run Docker-based test
./docker-test.sh
```

## Documentation Updates

- [ ] Update PROJECT_STATUS.md with progress
- [ ] Create API documentation for all services
- [ ] Update deployment guides for different environments
- [ ] Document lessons learned and best practices

## Build Verification

After completing each step, verify the build status using:

```bash
# Start the entire system with Docker
./docker-run.sh build
./docker-run.sh start
./service-register.sh

# Verify system status
curl http://localhost:11400/status

# Test a basic query
curl -X POST -H "Content-Type: application/json" \
  -d '{"query": "How do you know that you exist?", "category": "philosophy"}' \
  http://localhost:11400/api/query
```