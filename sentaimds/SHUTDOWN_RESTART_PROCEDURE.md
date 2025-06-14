# Project Shutdown and Restart Procedure

This document outlines the steps to safely shut down the development environment for updates/restarts and resume work seamlessly.

## Docker-Based Deployment (Recommended)

### Shutting Down Docker Containers

To stop all running containers:

```bash
cd /home/o2satz/CascadeProjects/Chorus_April/chorus_one/sentient-ai-poc
./docker-run.sh stop
# OR
docker-compose down
```

To stop and remove all containers, networks, and volumes:

```bash
cd /home/o2satz/CascadeProjects/Chorus_April/chorus_one/sentient-ai-poc
docker-compose down -v
```

### Cleaning Up Docker Environment

If you encounter issues or need to start fresh:

```bash
# Remove all containers, networks, and optionally prune the system
cd /home/o2satz/CascadeProjects/Chorus_April/chorus_one/sentient-ai-poc
docker-compose down -v
docker system prune -f

# For a complete rebuild
./docker-run.sh build
```

### Starting Docker Containers

To start all services:

```bash
cd /home/o2satz/CascadeProjects/Chorus_April/chorus_one/sentient-ai-poc
./docker-run.sh start
```

### Registering Services with MCP Hub

After starting the containers, register all services:

```bash
cd /home/o2satz/CascadeProjects/Chorus_April/chorus_one/sentient-ai-poc
./service-register.sh
```

### Testing the System

To test if the system is functioning correctly:

```bash
cd /home/o2satz/CascadeProjects/Chorus_April/chorus_one/sentient-ai-poc
./docker-test.sh
```

## Manual Deployment (Legacy)

### Stopping Individual Servers

If you need to stop individual servers:

```bash
# Kill MCP Hub
pkill -f "python.*mcp.*hub"

# Kill Reasoning Server
pkill -f "python.*reasoning.*server"

# Kill Memory Server
pkill -f "python.*memory.*server"

# Kill Personality Server
pkill -f "python.*personality.*server"

# Kill all Python-based servers
pkill -f "python.*uvicorn"
```

### Starting Individual Servers

Start these servers in the following order:

#### 1. MCP Hub Server

```bash
cd /home/o2satz/CascadeProjects/Chorus_April/chorus_one/sentient-ai-poc
python -m uvicorn mcp_hub.api.main:app --host 0.0.0.0 --port 11400 --reload
```

#### 2. Reasoning Server

```bash
cd /home/o2satz/CascadeProjects/Chorus_April/chorus_one/sentient-ai-poc
python -m uvicorn reasoning_server.api.main:app --host 0.0.0.0 --port 12500 --reload
```

#### 3. Memory Server

```bash
cd /home/o2satz/CascadeProjects/Chorus_April/chorus_one/sentient-ai-poc
python -m uvicorn memory_server.api.main:app --host 0.0.0.0 --port 13600 --reload
```

#### 4. Personality Server

```bash
cd /home/o2satz/CascadeProjects/Chorus_April/chorus_one/sentient-ai-poc
python -m uvicorn personality_server.api.main:app --host 0.0.0.0 --port 14700 --reload
```

## Git Version Control Procedures

### Before Shutdown

1. **Save All File Changes:**
   * Ensure all open files in your editor are saved.

2. **Commit Code Changes to Git:**
   ```bash
   cd /home/o2satz/CascadeProjects/Chorus_April/chorus_one/sentient-ai-poc
   git status
   git add .
   git commit -m "Your descriptive message about the changes"
   ```

3. **(Optional) Push to Remote Repository:**
   ```bash
   git push origin master  # Replace with your branch name if different
   ```

### After Restart

1. **Navigate to Project Directory:**
   ```bash
   cd /home/o2satz/CascadeProjects/Chorus_April/chorus_one/sentient-ai-poc
   ```

2. **Activate Virtual Environment:**
   ```bash
   source ../mcp-env/bin/activate
   ```

3. **(Optional) Pull Remote Changes:**
   ```bash
   git pull origin master  # Replace with your branch name
   ```

4. **Regain Context:**
   ```bash
   git log -1  # Check last commit
   git status  # Check working directory status
   ```

## Troubleshooting Common Issues

### Docker Container Not Starting

If containers fail to start:

1. Check if the port is already in use:
   ```bash
   netstat -tulnp | grep -E '11400|12500|13600|14700|5000'
   ```

2. Remove any existing containers:
   ```bash
   docker-compose down -v
   ```

3. Check logs for errors:
   ```bash
   docker-compose logs mcp-hub
   docker-compose logs reasoning-server
   ```

### Service Registration Failures

If services fail to register with the MCP Hub:

1. Verify all services are running:
   ```bash
   docker-compose ps
   ```

2. Check if services are accessible:
   ```bash
   curl http://localhost:11400/health
   curl http://localhost:12500/health
   ```

3. Check MCP Hub logs for specific errors:
   ```bash
   docker-compose logs mcp-hub | tail -n 50
   ```

### Known Issues

- KeyError in logging system: Sometimes there's a KeyError related to "Attempt to overwrite 'message' in LogRecord" in the shared/utils/error_handling.py module.
- Fix by removing duplicate log message parameter in the error handling code.