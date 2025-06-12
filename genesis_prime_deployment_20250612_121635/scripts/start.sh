#!/bin/bash

# Genesis Prime Startup Script
# Starts both backend and frontend services

set -e

echo "🚀 Starting Genesis Prime System..."
echo "=================================="

# Check if .env file exists
if [[ ! -f "backend/.env" ]]; then
    echo "❌ Environment file not found. Please run ./scripts/install.sh first"
    exit 1
fi

# Function to check if port is in use
check_port() {
    local port=$1
    if lsof -Pi :$port -sTCP:LISTEN -t >/dev/null 2>&1; then
        return 0  # Port is in use
    else
        return 1  # Port is free
    fi
}

# Check for conda
if ! command -v conda >/dev/null 2>&1; then
    echo "❌ Conda not found. Please install conda first."
    exit 1
fi

# Activate conda environment
echo "🐍 Activating Python environment..."
source $(conda info --base)/etc/profile.d/conda.sh
conda activate genesis_prime || {
    echo "❌ Failed to activate genesis_prime environment"
    echo "   Please run ./scripts/install.sh first"
    exit 1
}

# Check backend port
BACKEND_PORT=8000
if check_port $BACKEND_PORT; then
    echo "⚠️  Port $BACKEND_PORT is already in use"
    echo "   Attempting to stop existing process..."
    pkill -f "python.*main.py" 2>/dev/null || true
    sleep 2
fi

# Start backend
echo "🔧 Starting backend server..."
cd backend
python main.py &
BACKEND_PID=$!
cd ..

# Wait for backend to start
echo "   Waiting for backend to start..."
for i in {1..30}; do
    if curl -s http://localhost:$BACKEND_PORT/ >/dev/null 2>&1; then
        echo "✅ Backend started successfully on port $BACKEND_PORT"
        break
    fi
    if [[ $i -eq 30 ]]; then
        echo "❌ Backend failed to start after 30 seconds"
        kill $BACKEND_PID 2>/dev/null || true
        exit 1
    fi
    sleep 1
done

# Check frontend port
FRONTEND_PORT=3001
if check_port $FRONTEND_PORT; then
    echo "⚠️  Port $FRONTEND_PORT is already in use"
    echo "   Attempting to stop existing process..."
    pkill -f "npm.*run.*dev" 2>/dev/null || true
    sleep 2
fi

# Start frontend
echo "🎨 Starting frontend server..."
cd frontend
npm run dev &
FRONTEND_PID=$!
cd ..

# Wait for frontend to start
echo "   Waiting for frontend to start..."
for i in {1..60}; do
    if curl -s http://localhost:$FRONTEND_PORT/ >/dev/null 2>&1; then
        echo "✅ Frontend started successfully on port $FRONTEND_PORT"
        break
    fi
    if [[ $i -eq 60 ]]; then
        echo "❌ Frontend failed to start after 60 seconds"
        kill $BACKEND_PID $FRONTEND_PID 2>/dev/null || true
        exit 1
    fi
    sleep 1
done

echo ""
echo "🎉 Genesis Prime System Started Successfully!"
echo "============================================="
echo "🔧 Backend:  http://localhost:$BACKEND_PORT"
echo "🎨 Frontend: http://localhost:$FRONTEND_PORT"
echo ""
echo "📋 Process IDs:"
echo "   Backend PID:  $BACKEND_PID"
echo "   Frontend PID: $FRONTEND_PID"
echo ""
echo "🛑 To stop the system:"
echo "   ./scripts/stop.sh"
echo ""
echo "📊 To check status:"
echo "   ./scripts/status.sh"
echo ""
echo "🔄 The system is now ready for agent onboarding!"

# Save PIDs for stop script
echo "$BACKEND_PID" > .backend_pid
echo "$FRONTEND_PID" > .frontend_pid
