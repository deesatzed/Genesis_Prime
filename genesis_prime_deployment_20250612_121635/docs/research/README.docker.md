# Sentient AI PoC - Docker Setup Guide

This document provides instructions for running the Sentient AI Proof of Concept system using Docker containers, which eliminates the need for symbolic links and ensures a consistent environment across different machines.

## Prerequisites

- Docker and Docker Compose installed
- At least 4GB of free RAM
- At least 10GB of free disk space

### User Permissions

The Docker setup automatically uses your current user's UID and GID inside the containers. This ensures that:

1. Files created by the containers are owned by your user, not root
2. You don't need root/sudo privileges to run the containers
3. There are no permission issues when editing files that are mounted into containers

If you're having permission issues:
- Make sure your user is in the docker group: `sudo usermod -aG docker $USER`
- Log out and back in for the group change to take effect
- Run `./docker-run.sh build` to rebuild the images with your current user's UID/GID

## Services Architecture

The Sentient AI PoC consists of the following containerized services:

| Service | Port | Description |
|---------|------|-------------|
| MCP Hub | 11400 | Central orchestration service |
| Reasoning Server | 12500 | Handles AI reasoning and responses |
| Memory Server | 13600 | Manages knowledge storage and retrieval |
| Personality Server | 14700 | Handles personality traits and profiles |
| PostgreSQL (pgvector) | 5532 | Database for the Memory Server |

## Getting Started

### Quick Start

The easiest way to start the system is using the provided scripts:

```bash
# Build and start all services
./docker-run.sh build  # Build Docker images (first time setup)
./docker-run.sh start  # Start all services
./service-register.sh  # Register services with MCP Hub (IMPORTANT!)

# Test that everything is working
./docker-test.sh       # Verify services are registered and working

# Other useful commands
./docker-run.sh status # Check the status of services
./docker-run.sh logs   # View logs from all services
./docker-run.sh stop   # Stop all services
```

### First-Time Setup

When running for the first time, follow these steps:

1. Build the Docker images:
   ```bash
   ./docker-run.sh build
   ```

2. Start all services:
   ```bash
   ./docker-run.sh start
   ```

3. Register services with the MCP Hub (IMPORTANT!):
   ```bash
   ./service-register.sh
   ```

4. Verify everything is working:
   ```bash
   ./docker-test.sh
   ```

> **Note:** The service registration step is crucial for the system to function correctly. Without it, services won't be able to communicate with each other through the MCP Hub.

## Environment Variables

The Docker setup uses environment variables defined in the docker-compose.yml file. If you need to customize these, you can either:

1. Edit the docker-compose.yml file directly
2. Create a .env file in the same directory
3. Pass variables via the command line: `MEMORY_DB_PASSWORD=newpassword docker-compose up -d`

## Accessing Services

After starting the containers, you can access the services at:

- MCP Hub: http://localhost:11400
- MCP Hub API Docs: http://localhost:11400/docs
- Reasoning Server: http://localhost:12500
- Memory Server: http://localhost:13600
- Personality Server: http://localhost:14700

## Testing the System

To run basic health checks on all services:

```bash
./docker-run.sh test
```

For more comprehensive testing:

```bash
# Enter the MCP Hub container
docker exec -it mcp-hub bash

# Run tests inside the container
cd /app
pytest tests/
```

## Working with the Database

The PostgreSQL database with pgvector extension is available at localhost:5532:

```bash
# Connect to the database from the host
psql -h localhost -p 5532 -U memory_user -d memory_db

# View tables
\dt

# Examine the memory_entries table
\d memory_entries
```

## Thousand Questions Processing

To process the Thousand Questions dataset:

```bash
# Enter the MCP Hub container
docker exec -it mcp-hub bash

# Run the processor
python thousand_questions_processor.py
```

## Troubleshooting

### Common Issues

1. **Service fails to start**: Check logs with `docker-compose logs service-name`

2. **Database connection issues**: Ensure the pgvector container is running and healthy with `docker ps` and `docker inspect pgvector | grep Health`

3. **Import errors**: The Docker setup eliminates symbolic link issues by setting PYTHONPATH correctly

4. **Services not registered with MCP Hub**: If you encounter errors like "No available reasoning server", run the service registration script:
   ```bash
   ./service-register.sh
   ```
   Then verify the registration was successful:
   ```bash
   curl http://localhost:11400/api/servers/list
   ```

5. **Service registration fails**: Make sure all services are running properly before attempting registration. Check individual service logs for errors:
   ```bash
   docker-compose logs mcp-hub
   docker-compose logs reasoning-server
   docker-compose logs memory-server
   docker-compose logs personality-server
   ```

### Restarting Services

If a service is not responding correctly:

```bash
# Restart a specific service
docker-compose restart service-name

# Restart all services
./docker-run.sh restart
```

## Advanced Usage

### Building Individual Services

To rebuild a specific service:

```bash
docker-compose build service-name
docker-compose up -d service-name
```

### Accessing Container Shells

```bash
# MCP Hub shell
docker exec -it mcp-hub bash

# Reasoning Server shell
docker exec -it reasoning-server bash

# Memory Server shell
docker exec -it memory-server bash

# Personality Server shell
docker exec -it personality-server bash

# Database shell
docker exec -it pgvector bash
```

### Clearing Data

To remove all data and start fresh:

```bash
./docker-run.sh clean
```

## Development Workflow

For development, the Docker setup mounts the local directory into each container, so changes to the code are immediately available inside the containers. For most changes, you don't need to rebuild the images.

To apply changes:
1. Modify the code on your local machine
2. Restart the affected service: `docker-compose restart service-name`

For dependency changes:
1. Update requirements.txt
2. Rebuild the base image: `docker build -t chorus-base:latest -f Dockerfile.base .`
3. Restart all services: `./docker-run.sh restart`