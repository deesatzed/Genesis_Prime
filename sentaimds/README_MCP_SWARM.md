# MCP Server Swarm

## Overview

The MCP (Master Control Program) Server Swarm is a distributed system for programming troubleshooting and feature implementation guidance. It consists of multiple nodes that work together to provide a reliable and scalable service for programming applications like Cursor, Windsurf, and Cline.

## Architecture

The MCP Server Swarm is built with the following components:

1. **Node Management**: Configuration and state management for swarm nodes
2. **Discovery Service**: Node registration, discovery, and health monitoring
3. **Knowledge Repository**: Storage and retrieval of programming knowledge
4. **Knowledge Synchronization**: Synchronization of knowledge across nodes
5. **API Service**: External interface for client applications

## Setup and Installation

### Prerequisites

- Python 3.8 or higher
- Conda environment (optional but recommended)

### Installation

1. Clone the repository:
   ```bash
   git clone <repository-url>
   cd sentient-ai-poc
   ```

2. Create and activate a conda environment (optional):
   ```bash
   conda create -n mcp-swarm python=3.11
   conda activate mcp-swarm
   ```

3. Install the package in development mode:
   ```bash
   pip install -e .
   ```

## Running the MCP Swarm

### Starting a Single Node

To start a single node:

```bash
python -m mcp_swarm.main
```

You can specify configuration options:

```bash
python -m mcp_swarm.main --config ./path/to/config.json --log-dir ./logs
```

### Starting a Swarm

To start a swarm with multiple nodes (for testing):

```bash
python run_swarm.py
```

Options:
- `--leader-port PORT`: Port for the leader node (default: 9001)
- `--worker-start-port PORT`: Starting port for worker nodes (default: 9002)
- `--num-workers N`: Number of worker nodes to start (default: 2)
- `--log-dir DIR`: Directory for log files (default: ./logs)
- `--debug`: Enable debug logging

## Running Tests

To run the tests:

```bash
python -m pytest tests/swarm/test_swarm_basic.py -v
```

## Configuration

The MCP Server Swarm can be configured using environment variables or a configuration file.

### Environment Variables

- `MCP_NODE_ID`: Unique identifier for the node
- `MCP_NODE_NAME`: Human-readable name for the node
- `MCP_NODE_ROLE`: Role of the node (leader or worker)
- `MCP_API_HOST`: Host for the API service
- `MCP_API_PORT`: Port for the API service
- `MCP_DISCOVERY_HOSTS`: Comma-separated list of discovery hosts
- `MCP_REPOSITORY_PATH`: Path to the knowledge repository
- `MCP_LOG_LEVEL`: Logging level (debug, info, warning, error)

### Configuration File

Example configuration file:

```json
{
  "swarm_name": "mcp-swarm",
  "discovery_hosts": ["localhost:9001"],
  "leader_election_timeout_ms": 5000,
  "heartbeat_interval_ms": 1000,
  "sync_interval_seconds": 60,
  "specializations": ["python", "javascript", "general"],
  "max_concurrent_requests": 100,
  "max_memory_percent": 80.0,
  "agno_config": {
    "agent_config_path": "./config/agents",
    "max_agents": 10,
    "default_model": "gpt-4o"
  }
}
```

## API Endpoints

The MCP Server Swarm provides the following API endpoints:

- `/health`: Health check endpoint
- `/status`: Node status information
- `/knowledge/search`: Search for knowledge items
- `/knowledge/item/{item_id}`: Get, update, or delete a knowledge item
- `/knowledge/add`: Add a new knowledge item

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## License

[Specify your license here]
