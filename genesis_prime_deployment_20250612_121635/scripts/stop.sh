#!/bin/bash

# Genesis Prime Stop Script
# Stops both backend and frontend services

echo "🛑 Stopping Genesis Prime System..."
echo "==================================="

# Function to stop process by PID file
stop_by_pid_file() {
    local pid_file=$1
    local service_name=$2
    
    if [[ -f "$pid_file" ]]; then
        local pid=$(cat "$pid_file")
        if kill -0 "$pid" 2>/dev/null; then
            echo "   Stopping $service_name (PID: $pid)..."
            kill "$pid"
            sleep 2
            if kill -0 "$pid" 2>/dev/null; then
                echo "   Force stopping $service_name..."
                kill -9 "$pid"
            fi
        fi
        rm -f "$pid_file"
    fi
}

# Stop by PID files
stop_by_pid_file ".backend_pid" "backend"
stop_by_pid_file ".frontend_pid" "frontend"

# Stop by process name (backup method)
echo "🔍 Stopping any remaining processes..."
pkill -f "python.*main.py" 2>/dev/null || true
pkill -f "npm.*run.*dev" 2>/dev/null || true

# Wait a moment
sleep 2

# Check if processes are stopped
BACKEND_STOPPED=true
FRONTEND_STOPPED=true

if lsof -Pi :8000 -sTCP:LISTEN -t >/dev/null 2>&1; then
    BACKEND_STOPPED=false
fi

if lsof -Pi :3001 -sTCP:LISTEN -t >/dev/null 2>&1; then
    FRONTEND_STOPPED=false
fi

if [[ "$BACKEND_STOPPED" == true ]] && [[ "$FRONTEND_STOPPED" == true ]]; then
    echo "✅ Genesis Prime System stopped successfully"
else
    echo "⚠️  Some processes may still be running:"
    [[ "$BACKEND_STOPPED" == false ]] && echo "   - Backend still running on port 8000"
    [[ "$FRONTEND_STOPPED" == false ]] && echo "   - Frontend still running on port 3001"
fi
