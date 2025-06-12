# Authentication and Monitoring for MCP Server Swarm

This document describes the authentication, authorization, and monitoring capabilities implemented in the MCP Server Swarm.

## Authentication System

The MCP Server Swarm uses JWT (JSON Web Tokens) for authentication. This provides a stateless, secure way to authenticate users and nodes in the swarm.

### User Roles

The system supports three user roles:

1. **Admin** - Full access to all endpoints, including node management, knowledge management, and metrics
2. **User** - Access to read knowledge items and basic node information
3. **Node** - Special role for swarm nodes to communicate with each other

### Authentication Flow

1. Users authenticate through the `/api/auth/login` endpoint with username and password
2. Nodes authenticate through the `/api/auth/node/token` endpoint (requires admin token)
3. The system returns a JWT token that must be included in subsequent requests
4. Tokens have a configurable expiration time (default: 30 minutes)

### Environment Variables

- `MCP_JWT_SECRET` - Secret key for signing JWT tokens
- `MCP_TOKEN_EXPIRE` - Token expiration time in minutes
- `MCP_ADMIN_PASSWORD` - Password for the admin user
- `MCP_USER_PASSWORD` - Password for the regular user

### API Endpoints

- `POST /api/auth/login` - Login with username and password
- `POST /api/auth/token` - OAuth2-compatible token endpoint
- `POST /api/auth/node/token` - Get a token for a node (admin only)
- `GET /api/auth/me` - Get information about the current user

## Monitoring System

The monitoring system collects and reports metrics about node health, performance, and resource usage.

### Metrics Collected

#### System Metrics
- CPU usage (percent and count)
- Memory usage (total, available, used, percent)
- Disk usage (total, free, used, percent)
- Network connections
- System information (platform, uptime)

#### Application Metrics
- Process CPU and memory usage
- Thread count and open files
- Request count and error count
- API response times

### Metrics Collection

- Metrics are collected periodically (default: every 60 seconds)
- Metrics are stored in JSON files in the `metrics` directory
- Worker nodes report metrics to the leader node

### Environment Variables

- `MCP_METRICS_INTERVAL` - Metrics collection interval in seconds

### API Endpoints

- `GET /api/metrics/health` - Health check (no authentication required)
- `GET /api/metrics/system` - Get system metrics (admin or node)
- `GET /api/metrics/application` - Get application metrics (admin or node)
- `GET /api/metrics/all` - Get all metrics (admin or node)
- `POST /api/metrics/report` - Report metrics from a worker node (node only)
- `GET /api/metrics/nodes` - Get metrics for all nodes in the swarm (admin only)

## Integration with Swarm Components

### SwarmNode Integration

The `SwarmNode` class has been updated to initialize and manage the monitoring service. The monitoring service is started during node initialization and stopped during cleanup.

### API Service Integration

The API service uses middleware to:
1. Authenticate requests using JWT tokens
2. Track request metrics (endpoint, status code, duration)
3. Apply role-based access control to endpoints

### Discovery Service Integration

The discovery service now includes token-based authentication for node registration and communication. When a node registers with the leader, it receives a node token that it can use for subsequent requests.

## Testing

Comprehensive tests have been implemented to verify the functionality of the authentication and monitoring systems:

- `test_security.py` - Tests for JWT token creation, validation, and role-based access control
- `test_monitoring.py` - Tests for metrics collection, reporting, and the monitoring service
- `test_auth_monitoring_integration.py` - Integration tests for authentication and monitoring

## Example Usage

### Authenticating as an Admin

```python
import requests

# Login
response = requests.post(
    "http://localhost:8000/api/auth/login",
    json={"username": "admin", "password": "admin-password"}
)
token = response.json()["access_token"]

# Use the token for authenticated requests
headers = {"Authorization": f"Bearer {token}"}
response = requests.get(
    "http://localhost:8000/api/metrics/all",
    headers=headers
)
metrics = response.json()
```

### Viewing Node Metrics

```python
import requests

# Login as admin
response = requests.post(
    "http://localhost:8000/api/auth/login",
    json={"username": "admin", "password": "admin-password"}
)
token = response.json()["access_token"]

# Get metrics for all nodes
headers = {"Authorization": f"Bearer {token}"}
response = requests.get(
    "http://localhost:8000/api/metrics/nodes",
    headers=headers
)
node_metrics = response.json()
```

## Security Considerations

1. Always use HTTPS in production environments
2. Keep the JWT secret key secure and rotate it periodically
3. Use strong passwords for admin and user accounts
4. Consider implementing rate limiting for authentication endpoints
5. Monitor failed authentication attempts for potential security breaches
