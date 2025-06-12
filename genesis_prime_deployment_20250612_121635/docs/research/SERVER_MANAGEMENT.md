# Sentient AI POC Server Management Guide

This document provides comprehensive instructions for managing all servers in the Sentient AI Proof of Concept system.

> **IMPORTANT:** A Docker-based deployment method is now available and recommended. 
> See [README.docker.md](README.docker.md) for instructions on using Docker instead
> of the manual setup described in this document.
>
> ```bash
> # Use Docker for easier deployment (recommended)
> ./docker-run.sh build
> ./docker-run.sh start
> ```

## System Architecture

The Sentient AI POC consists of the following components, each running as a separate server:

| Component | Port | Description | Required |
|-----------|------|-------------|----------|
| MCP Hub | 11400 | Central orchestration server | Yes |
| Reasoning Server | 12500 | Generates responses to questions | Yes |
| Memory Server | 13600 | Stores and retrieves knowledge | Yes |
| Personality Server | 14700 | Manages personality traits | No (optional) |
| Web Interface | 5000 | User-friendly web interface | No (optional) |

## Prerequisites

1. Ensure you have the correct Python environment:
   ```bash
   conda activate mcp-env
   ```

2. Navigate to the project directory:
   ```bash
   cd /home/o2satz/CascadeProjects/Chorus_April/chorus_one/sentient-ai-poc
   ```

3. Create symbolic links for Python modules (required for proper imports):
   ```bash
   ln -sf mcp-hub mcp_hub
   ln -sf memory-server memory_server
   ln -sf personality-server personality_server
   ln -sf reasoning-server reasoning_server
   ```

## Starting and Stopping Servers

### Stopping Existing Servers

Before starting new server instances, always ensure all existing servers are stopped to avoid port conflicts:

```bash
# Kill all Python-based servers
pkill -f "python.*uvicorn"

# Kill the web interface
pkill -f "python app.py"

# Alternatively, kill specific servers
pkill -f "python.*mcp.*hub"
pkill -f "python.*reasoning.*server"
pkill -f "python.*memory.*server"
pkill -f "python.*personality.*server"
```

### Starting Core Servers

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

#### 4. Personality Server (Optional)

```bash
cd /home/o2satz/CascadeProjects/Chorus_April/chorus_one/sentient-ai-poc
python -m uvicorn personality_server.api.main:app --host 0.0.0.0 --port 14700 --reload
```

### Starting the Web Interface

The web interface provides a user-friendly way to interact with the system:

```bash
cd /home/o2satz/CascadeProjects/Chorus_April/chorus_one/sentient-ai-poc/web-interface
python app.py
```

The web interface will be available at http://localhost:5000

## Verifying Server Status

### Check Individual Server Health

```bash
# Check MCP Hub health
curl http://localhost:11400/health

# Check Reasoning Server health
curl http://localhost:12500/health

# Check Memory Server health
curl http://localhost:13600/health

# Check Personality Server health (if running)
curl http://localhost:14700/health
```

### Check MCP Hub Status

```bash
# Check overall system status
curl http://localhost:11400/status

# Check registered servers
curl http://localhost:11400/api/servers
```

### Using the CLI Demo Tool

The CLI demo tool provides a convenient way to check system health and functionality:

```bash
# Check system health
python cli_demo.py --health

# Test a question
python cli_demo.py -q "How do you know that you exist?" -c "philosophy"
```

## Common Issues and Solutions

### Module Import Errors

**Issue**: `ModuleNotFoundError: No module named 'mcp_hub.services.server_registry'`

**Solution**:
1. Ensure symbolic links are created correctly:
   ```bash
   ln -sf mcp-hub mcp_hub
   ln -sf memory-server memory_server
   ln -sf personality-server personality_server
   ln -sf reasoning-server reasoning_server
   ```

2. Add the project root to the Python path:
   ```bash
   export PYTHONPATH="$PYTHONPATH:/home/o2satz/CascadeProjects/Chorus_April/chorus_one/sentient-ai-poc"
   ```

### Server Not Responding

**Issue**: Requests to server endpoints return connection refused

**Solution**:
1. Check if the server is running:
   ```bash
   ps aux | grep -E 'uvicorn|python' | grep -v grep
   ```

2. Check if the port is in use:
   ```bash
   netstat -tulnp | grep -E '11400|12500|13600|14700|5000'
   ```

3. Restart the server if needed.

### Datetime Serialization Issues

**Issue**: JSON serialization errors with datetime objects

**Solution**:
1. Check that both the MCP Hub and Reasoning Server are using the same serialization approach
2. Verify that the DateTimeEncoder class is being used for all JSON serialization
3. Restart both the MCP Hub and Reasoning Server

### Web Interface Shows "Offline" Status

**Issue**: Web interface shows system status as "Offline" even though servers are running

**Solution**:
1. Check the MCP Hub URL in the web interface configuration:
   ```bash
   grep -r "MCP_HUB_URL" web-interface/
   ```

2. Ensure it's set to `http://localhost:11400`

3. Restart the web interface

## Advanced Server Management

### Running Servers in the Background

To run servers in the background and keep them running after closing the terminal:

```bash
# Start MCP Hub in the background
nohup python -m uvicorn mcp_hub.api.main:app --host 0.0.0.0 --port 11400 --reload > mcp_hub.log 2>&1 &

# Start Reasoning Server in the background
nohup python -m uvicorn reasoning_server.api.main:app --host 0.0.0.0 --port 12500 --reload > reasoning_server.log 2>&1 &

# Start Memory Server in the background
nohup python -m uvicorn memory_server.api.main:app --host 0.0.0.0 --port 13600 --reload > memory_server.log 2>&1 &

# Start Web Interface in the background
cd web-interface && nohup python app.py > web_interface.log 2>&1 &
```

### Viewing Server Logs

```bash
# View MCP Hub logs
tail -f mcp_hub.log

# View Reasoning Server logs
tail -f reasoning_server.log

# View Memory Server logs
tail -f memory_server.log

# View Web Interface logs
tail -f web_interface.log
```

### Monitoring Server Performance

```bash
# Monitor CPU and memory usage of all Python processes
watch -n 1 'ps aux | grep -E "python|uvicorn" | grep -v grep'

# Monitor network connections
watch -n 1 'netstat -tulnp | grep -E "11400|12500|13600|14700|5000"'
```

## Customizing Server Behavior

### Enhancing Reasoning Server Responses

The Reasoning Server has been enhanced to provide more detailed responses for common questions. To add or modify these responses:

1. Edit the `generate_response` function in `/home/o2satz/CascadeProjects/Chorus_April/chorus_one/sentient-ai-poc/reasoning_server/api/main.py`

2. Modify the `responses` dictionary to add new question-answer pairs:
   ```python
   responses = {
       "new question pattern": "Detailed response for this question",
       # Add more responses here
   }
   ```

3. Restart the Reasoning Server to apply changes

### Thousand Questions Processing

The Thousand Questions processing system is used to populate the AI's knowledge base and personality profile by processing answers to a comprehensive set of questions. To work with this system:

1. **Processing Questions Dataset**:
   ```bash
   # Navigate to the project directory
   cd /home/o2satz/CascadeProjects/Chorus_April/chorus_one/sentient-ai-poc
   
   # Run the Thousand Questions parser
   python -m memory_server.thousand_questions.parser
   ```

2. **Running Batch Processing** (when implemented):
   ```bash
   # Run the batch processor
   cd /home/o2satz/CascadeProjects/Chorus_April/chorus_one/sentient-ai-poc
   python -m thousand_questions_processor
   ```

3. **Viewing Processed Data**:
   ```bash
   # Check the processed questions
   cd /home/o2satz/CascadeProjects/Chorus_April/chorus_one/sentient-ai-poc
   python -c "import json; f=open('path/to/processed_questions.json'); data=json.load(f); print(f'Processed {len(data.get(\'questions\', []))} questions');"
   ```

4. **Updating Personality Profile**:
   ```bash
   # Generate personality profile from responses
   cd /home/o2satz/CascadeProjects/Chorus_April/chorus_one/sentient-ai-poc
   python -m narrative_forge.thousand_questions
   ```

### Configuring Server Logging

To adjust logging levels for better debugging:

1. Edit the logging configuration in each server's main.py file
2. Change the logging level to DEBUG for more detailed logs:
   ```python
   logging.basicConfig(
       level=logging.DEBUG,
       format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
   )
   ```
3. Restart the server to apply changes

## Thousand Questions Management

### Monitoring Progress

To monitor the progress of Thousand Questions processing:

```bash
# Check processing logs
tail -f thousand_questions_processing.log

# View current progress statistics
cat processed_responses.json | grep -A5 metadata
```

### Troubleshooting Thousand Questions Processing

Common issues when processing Thousand Questions:

1. **Parser Failures**:
   - Check file paths in configuration
   - Verify questions data file format
   - Look for syntax errors in the parser code

2. **Batch Processing Errors**:
   - Check MCP Hub and Memory Server are running
   - Verify correct URLs are configured
   - Look for timeouts or connection issues in logs

3. **Knowledge Integration Issues**:
   - Verify Memory Server database is accessible
   - Check knowledge format compatibility
   - Look for serialization errors in logs

## Conclusion

This guide covers the essential operations for managing the Sentient AI POC servers. For more detailed information about specific components, refer to the README.md and DEMO_GUIDE.md files.

For any issues not covered in this guide, check the Fixed_Errors_1.md log for previously successful solutions before attempting new approaches.
