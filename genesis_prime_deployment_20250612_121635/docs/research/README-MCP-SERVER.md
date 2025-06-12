# MCP Server Quick Reference

MCP (Model Control Protocol) server builds now include these improvements:

1. **Standalone Operation**: No need for amm_project package, all required modules are included
2. **Easier Startup**: New wrapper script handles paths and configuration automatically
3. **Robust Error Handling**: Better error recovery and logging
4. **Metadata Support**: Properly handles optional metadata field
5. **Complete Documentation**: Detailed guides on usage and troubleshooting
6. **GUI Integration**: Launch and manage MCP servers directly from the GUI
7. **Import Fix**: Automatic import fixing script for standalone MCP servers
8. **Network Access**: Binds to 0.0.0.0 by default for better accessibility

## Quick Start

### Option 1: Easy Server Start

```bash
# Start the most recently built MCP server on port 8000
./start_mcp.sh

# Start on a specific port
./start_mcp.sh 9000
```

### Option 2: Manual Start

```bash
cd /path/to/mcp/build
python start_server.py --host 0.0.0.0 --port 8000
```

### Fixing Import Issues

If you encounter import errors:

```bash
# Fix imports in a specific MCP server build
python fix_imports.py /path/to/mcp/build
```

## Testing the API

Basic health check:
```bash
curl -X GET http://localhost:8000/health
```

Send a query:
```bash
curl -X POST http://localhost:8000/generate \
  -H "Content-Type: application/json" \
  -d '{
    "query": "Hello, how are you?",
    "parameters": {},
    "context": {}
  }'
```

## For Complete Documentation

See the following guide files:
- MCP_SERVER_GUIDE.md - Complete guide for MCP server usage
- running_mcp_server.md - Detailed runtime options and examples
- FIXED_ISSUES.md - Documentation of fixes and improvements
