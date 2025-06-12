#!/bin/bash

# Genesis Prime Status Script
# Checks the status of backend and frontend services

echo "📊 Genesis Prime System Status"
echo "=============================="

# Function to check service status
check_service() {
    local port=$1
    local service_name=$2
    local url="http://localhost:$port"
    
    if curl -s "$url" >/dev/null 2>&1; then
        echo "✅ $service_name: Running on port $port"
        return 0
    else
        echo "❌ $service_name: Not running on port $port"
        return 1
    fi
}

# Check backend
check_service 8000 "Backend"
BACKEND_STATUS=$?

# Check frontend
check_service 3001 "Frontend"
FRONTEND_STATUS=$?

echo ""

# Overall status
if [[ $BACKEND_STATUS -eq 0 ]] && [[ $FRONTEND_STATUS -eq 0 ]]; then
    echo "🎉 System Status: FULLY OPERATIONAL"
    echo ""
    echo "🔗 Access URLs:"
    echo "   Frontend: http://localhost:3001"
    echo "   Backend:  http://localhost:8000"
elif [[ $BACKEND_STATUS -eq 0 ]] || [[ $FRONTEND_STATUS -eq 0 ]]; then
    echo "⚠️  System Status: PARTIALLY RUNNING"
    echo ""
    echo "🔧 To start missing services:"
    echo "   ./scripts/start.sh"
else
    echo "❌ System Status: NOT RUNNING"
    echo ""
    echo "🚀 To start the system:"
    echo "   ./scripts/start.sh"
fi

# Check for PID files
echo ""
echo "📋 Process Information:"
if [[ -f ".backend_pid" ]]; then
    BACKEND_PID=$(cat .backend_pid)
    if kill -0 "$BACKEND_PID" 2>/dev/null; then
        echo "   Backend PID: $BACKEND_PID (running)"
    else
        echo "   Backend PID: $BACKEND_PID (not running)"
        rm -f .backend_pid
    fi
else
    echo "   Backend PID: Not tracked"
fi

if [[ -f ".frontend_pid" ]]; then
    FRONTEND_PID=$(cat .frontend_pid)
    if kill -0 "$FRONTEND_PID" 2>/dev/null; then
        echo "   Frontend PID: $FRONTEND_PID (running)"
    else
        echo "   Frontend PID: $FRONTEND_PID (not running)"
        rm -f .frontend_pid
    fi
else
    echo "   Frontend PID: Not tracked"
fi
