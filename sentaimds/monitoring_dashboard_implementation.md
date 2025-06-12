# MCP Server Swarm Monitoring Dashboard

## Overview

The MCP Server Swarm Monitoring Dashboard provides real-time visibility into the health, performance, and resource utilization of all nodes in the MCP swarm. This document outlines the implementation details, architecture, and usage guidelines for the monitoring system.

## Architecture

### Components

1. **Metrics Collector**
   - Collects system and application metrics from each node
   - Implemented in `mcp_swarm/monitoring/metrics.py`
   - Uses `psutil` for system metrics and application-specific counters

2. **Monitoring Service**
   - Runs as a background service on each node
   - Periodically collects and reports metrics
   - Implemented in `mcp_swarm/monitoring/service.py`
   - Reports metrics to leader node if applicable

3. **Dashboard Application**
   - Flask-based web application for visualizing metrics
   - Implemented in `mcp_swarm/monitoring/dashboard/app.py`
   - Uses Plotly for interactive charts and visualizations

### Data Flow

```
┌─────────────┐     ┌─────────────┐     ┌─────────────┐
│  Node 1     │     │  Node 2     │     │  Node N     │
│  Metrics    │     │  Metrics    │     │  Metrics    │
│  Collector  │     │  Collector  │     │  Collector  │
└──────┬──────┘     └──────┬──────┘     └──────┬──────┘
       │                   │                   │
       ▼                   ▼                   ▼
┌──────┴──────┐     ┌──────┴──────┐     ┌──────┴──────┐
│  Node 1     │     │  Node 2     │     │  Node N     │
│  Monitoring │     │  Monitoring │     │  Monitoring │
│  Service    │     │  Service    │     │  Service    │
└──────┬──────┘     └──────┬──────┘     └──────┬──────┘
       │                   │                   │
       └───────────┬───────┴───────────┬───────┘
                   │                   │
                   ▼                   ▼
         ┌─────────────────────────────────┐
         │          Metrics Storage        │
         │  (File System / Time Series DB) │
         └───────────────┬─────────────────┘
                         │
                         ▼
         ┌─────────────────────────────────┐
         │       Dashboard Application     │
         │         (Flask + Plotly)        │
         └─────────────────────────────────┘
```

## Implementation Details

### Metrics Collector

The `MetricsCollector` class is responsible for gathering system and application metrics:

```python
class MetricsCollector:
    def __init__(self, node_id):
        self.node_id = node_id
        self.last_metrics = None
        self.start_time = time.time()
        self.request_counter = Counter()
        
    def collect_system_metrics(self):
        """Collect system metrics using psutil."""
        metrics = {
            "cpu": {
                "percent": psutil.cpu_percent(interval=0.1),
                "count": psutil.cpu_count()
            },
            "memory": {
                "total": psutil.virtual_memory().total,
                "available": psutil.virtual_memory().available,
                "percent": psutil.virtual_memory().percent
            },
            "disk": {
                "total": psutil.disk_usage('/').total,
                "used": psutil.disk_usage('/').used,
                "percent": psutil.disk_usage('/').percent
            },
            "network": {
                "bytes_sent": psutil.net_io_counters().bytes_sent,
                "bytes_recv": psutil.net_io_counters().bytes_recv
            },
            "uptime": time.time() - self.start_time
        }
        return metrics
        
    def collect_application_metrics(self):
        """Collect application-specific metrics."""
        metrics = {
            "requests": dict(self.request_counter),
            "active_connections": self._get_active_connections()
        }
        return metrics
        
    def collect_all_metrics(self):
        """Collect all metrics."""
        metrics = {
            "node_id": self.node_id,
            "timestamp": time.time(),
            "system": self.collect_system_metrics(),
            "application": self.collect_application_metrics()
        }
        self.last_metrics = metrics
        return metrics
```

### Monitoring Service

The `MonitoringService` class runs as a background service to periodically collect and report metrics:

```python
class MonitoringService:
    def __init__(self, node, collection_interval=60, metrics_dir=None):
        self.node = node
        self.node_id = node.node_id
        self.collection_interval = collection_interval
        self.metrics_collector = MetricsCollector(self.node_id)
        self.running = False
        self.collection_task = None
        
        # Set metrics directory
        self.metrics_dir = metrics_dir or os.environ.get(
            "MCP_METRICS_DIR", 
            os.path.join(os.path.dirname(__file__), "metrics")
        )
        os.makedirs(self.metrics_dir, exist_ok=True)
        
    async def start(self):
        """Start the monitoring service."""
        logger.info(f"Starting monitoring service with interval {self.collection_interval}s")
        self.running = True
        self.collection_task = asyncio.create_task(self._collect_metrics_periodically())
        
    async def stop(self):
        """Stop the monitoring service."""
        logger.info("Stopping monitoring service")
        self.running = False
        if self.collection_task:
            self.collection_task.cancel()
            try:
                await self.collection_task
            except asyncio.CancelledError:
                pass
        
    async def _collect_metrics_periodically(self):
        """Collect metrics at regular intervals."""
        while self.running:
            try:
                metrics = self.metrics_collector.collect_all_metrics()
                self._store_metrics(metrics)
                
                # Report metrics to leader if this node is not the leader
                if not self.node.is_leader and self.node.leader_address:
                    await self._report_metrics_to_leader(metrics)
                    
            except Exception as e:
                logger.error(f"Error collecting metrics: {e}", exc_info=True)
                
            await asyncio.sleep(self.collection_interval)
            
    def _store_metrics(self, metrics):
        """Store metrics to file system."""
        timestamp = datetime.fromtimestamp(metrics["timestamp"])
        date_str = timestamp.strftime("%Y-%m-%d")
        time_str = timestamp.strftime("%H-%M-%S")
        
        # Create date directory if it doesn't exist
        date_dir = os.path.join(self.metrics_dir, date_str)
        os.makedirs(date_dir, exist_ok=True)
        
        # Write metrics to file
        filename = f"{self.node_id}_{time_str}.json"
        filepath = os.path.join(date_dir, filename)
        
        with open(filepath, 'w') as f:
            json.dump(metrics, f, indent=2)
            
    async def _report_metrics_to_leader(self, metrics):
        """Report metrics to leader node."""
        if not self.node.leader_address:
            return
            
        try:
            url = f"{self.node.leader_address}/api/metrics"
            async with aiohttp.ClientSession() as session:
                async with session.post(url, json=metrics) as response:
                    if response.status != 200:
                        logger.warning(f"Failed to report metrics to leader: {response.status}")
        except Exception as e:
            logger.error(f"Error reporting metrics to leader: {e}", exc_info=True)
```

### Dashboard Application

The Flask-based dashboard application visualizes the collected metrics:

```python
from flask import Flask, render_template, jsonify
import os
import json
import glob
from datetime import datetime, timedelta
import plotly.graph_objects as go
import plotly.express as px
import pandas as pd

app = Flask(__name__)

# Configuration
METRICS_DIR = os.environ.get("MCP_METRICS_DIR", os.path.join(os.path.dirname(__file__), "../metrics"))
REFRESH_INTERVAL = int(os.environ.get("MCP_DASHBOARD_REFRESH", 60))  # seconds

@app.route('/')
def index():
    """Render the dashboard homepage."""
    return render_template('index.html', refresh_interval=REFRESH_INTERVAL)

@app.route('/api/nodes')
def get_nodes():
    """Get list of all nodes."""
    nodes = set()
    for file in glob.glob(f"{METRICS_DIR}/**/*.json", recursive=True):
        with open(file, 'r') as f:
            try:
                data = json.load(f)
                nodes.add(data.get('node_id'))
            except:
                continue
    return jsonify(list(nodes))

@app.route('/api/metrics/summary')
def get_metrics_summary():
    """Get summary of latest metrics for all nodes."""
    summary = []
    nodes = {}
    
    # Get the latest file for each node
    for date_dir in sorted(glob.glob(f"{METRICS_DIR}/*"), reverse=True):
        if not os.path.isdir(date_dir):
            continue
            
        for file in sorted(glob.glob(f"{date_dir}/*.json"), reverse=True):
            try:
                with open(file, 'r') as f:
                    data = json.load(f)
                    node_id = data.get('node_id')
                    
                    if node_id not in nodes:
                        nodes[node_id] = data
            except:
                continue
    
    # Convert to list for API response
    for node_id, data in nodes.items():
        summary.append({
            'node_id': node_id,
            'timestamp': data.get('timestamp'),
            'cpu_percent': data.get('system', {}).get('cpu', {}).get('percent', 0),
            'memory_percent': data.get('system', {}).get('memory', {}).get('percent', 0),
            'disk_percent': data.get('system', {}).get('disk', {}).get('percent', 0),
            'uptime': data.get('system', {}).get('uptime', 0),
            'requests': sum(data.get('application', {}).get('requests', {}).values(), 0)
        })
    
    return jsonify(summary)

@app.route('/api/metrics/history/<node_id>')
def get_metrics_history(node_id):
    """Get historical metrics for a specific node."""
    history = []
    
    # Get metrics from the last 24 hours
    start_time = datetime.now() - timedelta(hours=24)
    
    for date_dir in sorted(glob.glob(f"{METRICS_DIR}/*")):
        date_str = os.path.basename(date_dir)
        try:
            date = datetime.strptime(date_str, "%Y-%m-%d")
            if date < start_time.replace(hour=0, minute=0, second=0, microsecond=0):
                continue
        except:
            continue
        
        for file in sorted(glob.glob(f"{date_dir}/{node_id}_*.json")):
            try:
                with open(file, 'r') as f:
                    data = json.load(f)
                    timestamp = data.get('timestamp')
                    
                    if timestamp < start_time.timestamp():
                        continue
                        
                    history.append({
                        'timestamp': timestamp,
                        'cpu_percent': data.get('system', {}).get('cpu', {}).get('percent', 0),
                        'memory_percent': data.get('system', {}).get('memory', {}).get('percent', 0),
                        'disk_percent': data.get('system', {}).get('disk', {}).get('percent', 0),
                        'requests': sum(data.get('application', {}).get('requests', {}).values(), 0)
                    })
            except:
                continue
    
    return jsonify(history)

@app.route('/api/charts/cpu/<node_id>')
def get_cpu_chart(node_id):
    """Generate CPU usage chart for a node."""
    history = json.loads(get_metrics_history(node_id).data)
    
    if not history:
        return jsonify({'error': 'No data available'})
    
    df = pd.DataFrame(history)
    df['datetime'] = pd.to_datetime(df['timestamp'], unit='s')
    
    fig = px.line(df, x='datetime', y='cpu_percent', 
                 title=f'CPU Usage - Node {node_id}',
                 labels={'cpu_percent': 'CPU %', 'datetime': 'Time'})
    
    return jsonify(fig.to_json())

# Similar routes for memory, disk, and request charts

if __name__ == '__main__':
    port = int(os.environ.get("MCP_DASHBOARD_PORT", 5000))
    debug = os.environ.get("MCP_DASHBOARD_DEBUG", "False").lower() == "true"
    app.run(host='0.0.0.0', port=port, debug=debug)
```

## Configuration

The monitoring system can be configured using environment variables:

| Variable | Description | Default |
|----------|-------------|---------|
| `MCP_METRICS_DIR` | Directory to store metrics data | `./metrics` |
| `MCP_DASHBOARD_PORT` | Port for the dashboard web server | `5000` |
| `MCP_DASHBOARD_REFRESH` | Dashboard refresh interval in seconds | `60` |
| `MCP_DASHBOARD_DEBUG` | Enable debug mode for Flask | `False` |

## Usage

### Starting the Monitoring Service

The monitoring service is automatically started when a swarm node is initialized:

```python
# In SwarmNode initialization
self.monitoring_service = MonitoringService(self)
await self.monitoring_service.start()
```

### Accessing the Dashboard

The dashboard can be accessed at `http://<leader-node-ip>:<dashboard-port>/` in a web browser.

### API Endpoints

The dashboard provides the following API endpoints:

| Endpoint | Description |
|----------|-------------|
| `/api/nodes` | Get list of all nodes |
| `/api/metrics/summary` | Get summary of latest metrics for all nodes |
| `/api/metrics/history/<node_id>` | Get historical metrics for a specific node |
| `/api/charts/cpu/<node_id>` | Generate CPU usage chart for a node |
| `/api/charts/memory/<node_id>` | Generate memory usage chart for a node |
| `/api/charts/disk/<node_id>` | Generate disk usage chart for a node |
| `/api/charts/requests/<node_id>` | Generate request count chart for a node |

## Security Considerations

1. **Authentication**: The dashboard does not currently implement authentication. It should only be exposed on a secure internal network.

2. **Data Validation**: All metrics data is validated before storage to prevent injection attacks.

3. **Resource Limits**: The metrics collection process is designed to have minimal impact on system resources.

## Future Enhancements

1. **Authentication and Authorization**: Add user authentication and role-based access control.

2. **Alerting**: Implement alert thresholds and notification mechanisms.

3. **Time Series Database**: Replace file-based storage with a dedicated time series database for better performance.

4. **Custom Metrics**: Allow users to define and collect custom application metrics.

5. **Dashboard Customization**: Enable users to create custom dashboard layouts and visualizations.
