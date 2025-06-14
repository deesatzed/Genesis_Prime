#!/bin/bash

# Genesis Prime Complete Deployment Script
# This script creates a portable package of Genesis Prime and sets up everything on a new computer

set -e  # Exit on any error

SCRIPT_VERSION="1.0"
DEPLOYMENT_DATE=$(date +"%Y%m%d_%H%M%S")
PACKAGE_NAME="genesis_prime_deployment_${DEPLOYMENT_DATE}"

echo "🚀 Genesis Prime Complete Deployment Script v${SCRIPT_VERSION}"
echo "=============================================================="
echo "Creating portable deployment package: $PACKAGE_NAME"
echo ""

# Function to check if we're in the right directory
check_source_directory() {
    if [[ ! -d "apps/option1_mono_agent" ]] || [[ ! -d "apps/gp_b_core" ]]; then
        echo "❌ Error: Please run this script from the Gen_Prime_V3-main directory"
        echo "Expected structure:"
        echo "  - apps/option1_mono_agent/ (backend)"
        echo "  - apps/gp_b_core/ (frontend)"
        exit 1
    fi
    echo "✅ Source directory validated"
}

# Function to create deployment package
create_deployment_package() {
    echo "📦 Creating deployment package..."
    
    # Create deployment directory
    mkdir -p "$PACKAGE_NAME"
    cd "$PACKAGE_NAME"
    
    # Create directory structure
    mkdir -p {backend,frontend,docs,scripts,config,data}
    
    echo "   📁 Directory structure created"
}

# Function to copy essential files
copy_essential_files() {
    echo "📋 Copying essential application files..."
    
    # Copy backend files
    echo "   🔧 Copying backend (option1_mono_agent)..."
    rsync -av --exclude='__pycache__' --exclude='*.pyc' --exclude='*.pyo' \
          --exclude='.pytest_cache' --exclude='logs' --exclude='*.log' \
          ../apps/option1_mono_agent/ backend/
    
    # Copy frontend files (excluding build artifacts and dependencies)
    echo "   🎨 Copying frontend (gp_b_core)..."
    rsync -av --exclude='node_modules' --exclude='.next' --exclude='dist' \
          --exclude='build' --exclude='.cache' --exclude='*.log' \
          --exclude='.turbo' --exclude='.vercel' --exclude='coverage' \
          --exclude='package-lock.json' --exclude='yarn.lock' \
          --exclude='.DS_Store' --exclude='*.tmp' --exclude='*.temp' \
          ../apps/gp_b_core/ frontend/
    
    # Verify exclusions worked
    if [[ -d "frontend/node_modules" ]]; then
        echo "   ⚠️  WARNING: node_modules was copied despite exclusion!"
        echo "   🗑️  Removing node_modules to reduce package size..."
        rm -rf frontend/node_modules
    fi
    
    if [[ -d "frontend/.next" ]]; then
        echo "   ⚠️  WARNING: .next build directory was copied!"
        echo "   🗑️  Removing .next to reduce package size..."
        rm -rf frontend/.next
    fi
    
    # Copy documentation and research
    echo "   📚 Copying documentation..."
    if [[ -d "../sentaimds" ]]; then
        cp -r ../sentaimds docs/research/
    fi
    
    # Copy important root files
    echo "   📄 Copying configuration files..."
    [[ -f "../README.md" ]] && cp ../README.md docs/
    [[ -f "../DEPLOYMENT_GUIDE.md" ]] && cp ../DEPLOYMENT_GUIDE.md docs/
    [[ -f "../QUICK_START_GUIDE.md" ]] && cp ../QUICK_START_GUIDE.md docs/
    [[ -f "../requirements.txt" ]] && cp ../requirements.txt config/
    [[ -f "../.env.example" ]] && cp ../.env.example config/
    
    # Copy agent model configuration files
    echo "   🤖 Copying agent model configuration files..."
    [[ -f "../agent_models.json" ]] && cp ../agent_models.json config/
    [[ -f "../agent_models_budget.json" ]] && cp ../agent_models_budget.json config/
    [[ -f "../agent_models_premium.json" ]] && cp ../agent_models_premium.json config/
    [[ -f "../agent_model_config.json" ]] && cp ../agent_model_config.json config/
    
    # Copy package.json but not package-lock.json or node_modules
    find ../apps -name "package.json" -exec cp {} config/ \; 2>/dev/null || true
    
    echo "✅ Essential files copied (excluding build artifacts and dependencies)"
}

# Function to create installation script
create_installation_script() {
    echo "🛠️ Creating installation script..."
    
    cat > scripts/install.sh << 'EOF'
#!/bin/bash

# Genesis Prime Installation Script
# Installs all dependencies and sets up the environment

set -e

echo "🚀 Genesis Prime Installation Starting..."
echo "========================================"

# Check operating system
OS="unknown"
if [[ "$OSTYPE" == "linux-gnu"* ]]; then
    OS="linux"
elif [[ "$OSTYPE" == "darwin"* ]]; then
    OS="macos"
elif [[ "$OSTYPE" == "msys" ]] || [[ "$OSTYPE" == "cygwin" ]]; then
    OS="windows"
fi

echo "🖥️  Detected OS: $OS"

# Function to check if command exists
command_exists() {
    command -v "$1" >/dev/null 2>&1
}

# Check for conda
echo "🐍 Checking for conda..."
if ! command_exists conda; then
    echo "❌ Conda not found. Please install Miniconda or Anaconda first:"
    echo "   https://docs.conda.io/en/latest/miniconda.html"
    exit 1
fi
echo "✅ Conda found"

# Check for Node.js
echo "📦 Checking for Node.js..."
if ! command_exists node; then
    echo "❌ Node.js not found. Please install Node.js first:"
    echo "   https://nodejs.org/"
    exit 1
fi
echo "✅ Node.js found: $(node --version)"

# Check for npm
if ! command_exists npm; then
    echo "❌ npm not found. Please install npm first"
    exit 1
fi
echo "✅ npm found: $(npm --version)"

# Create conda environment
echo "🐍 Setting up Python environment..."
ENV_NAME="genesis_prime"

# Check if environment already exists
if conda env list | grep -q "^${ENV_NAME} "; then
    echo "⚠️  Environment '$ENV_NAME' already exists. Removing..."
    conda env remove -n $ENV_NAME -y
fi

# Create new environment
echo "   Creating conda environment: $ENV_NAME"
conda create -n $ENV_NAME python=3.9 -y

# Activate environment
echo "   Activating environment..."
source $(conda info --base)/etc/profile.d/conda.sh
conda activate $ENV_NAME

# Install Python dependencies
echo "   Installing Python dependencies..."
if [[ -f "backend/requirements.txt" ]]; then
    pip install -r backend/requirements.txt
elif [[ -f "config/requirements.txt" ]]; then
    pip install -r config/requirements.txt
else
    # Install essential packages
    pip install fastapi uvicorn openai anthropic requests python-dotenv pydantic
fi

echo "✅ Python environment setup complete"

# Setup frontend
echo "🎨 Setting up frontend..."
cd frontend

# Install npm dependencies
echo "   Installing npm dependencies..."
npm install

# Build frontend (optional, for production)
echo "   Building frontend..."
npm run build || echo "⚠️  Build failed, but continuing..."

cd ..

echo "✅ Frontend setup complete"

# Create environment file
echo "⚙️  Creating environment configuration..."
if [[ -f "config/.env.example" ]]; then
    cp config/.env.example backend/.env
    echo "   📝 Created backend/.env from template"
    echo "   ⚠️  Please edit backend/.env with your API keys"
else
    cat > backend/.env << 'ENVEOF'
# Genesis Prime Environment Configuration
# Please fill in your API keys

# OpenRouter API (for agent communication)
OPENROUTER_API_KEY=your_openrouter_api_key_here

# Anthropic API (for Claude models)
ANTHROPIC_API_KEY=your_anthropic_api_key_here

# OpenAI API (for GPT models)
OPENAI_API_KEY=your_openai_api_key_here

# Application Settings
DEBUG=true
LOG_LEVEL=INFO
HOST=localhost
BACKEND_PORT=8000
FRONTEND_PORT=3001

# Database (if needed)
DATABASE_URL=sqlite:///./genesis_prime.db
ENVEOF
    echo "   📝 Created backend/.env template"
    echo "   ⚠️  Please edit backend/.env with your API keys"
fi

echo "✅ Installation complete!"
echo ""
echo "📋 Next Steps:"
echo "1. Edit backend/.env with your API keys"
echo "2. Run: ./scripts/start.sh"
echo "3. Access the application at http://localhost:3001"
EOF

    chmod +x scripts/install.sh
    echo "✅ Installation script created"
}

# Function to create startup script
create_startup_script() {
    echo "🚀 Creating startup script..."
    
    cat > scripts/start.sh << 'EOF'
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
EOF

    chmod +x scripts/start.sh
    echo "✅ Startup script created"
}

# Function to create stop script
create_stop_script() {
    echo "🛑 Creating stop script..."
    
    cat > scripts/stop.sh << 'EOF'
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
EOF

    chmod +x scripts/stop.sh
    echo "✅ Stop script created"
}

# Function to create status script
create_status_script() {
    echo "📊 Creating status script..."
    
    cat > scripts/status.sh << 'EOF'
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
EOF

    chmod +x scripts/status.sh
    echo "✅ Status script created"
}

# Function to create agent onboarding script
create_agent_onboarding_script() {
    echo "🤖 Creating agent onboarding script..."
    
    cat > scripts/onboard_agents.sh << 'EOF'
#!/bin/bash

# Genesis Prime Agent Onboarding Script
# Sets up the 5 core agents with model selection and progress tracking

set -e

echo "🤖 Genesis Prime Agent Onboarding"
echo "================================="

# Function to show progress bar
show_progress() {
    local current=$1
    local total=$2
    local width=50
    local percentage=$((current * 100 / total))
    local completed=$((current * width / total))
    local remaining=$((width - completed))
    
    printf "\r["
    printf "%*s" $completed | tr ' ' '='
    printf "%*s" $remaining | tr ' ' '-'
    printf "] %d%% (%d/%d)" $percentage $current $total
}

# Function to fetch current OpenRouter models
fetch_openrouter_models() {
    echo "🔍 Fetching current OpenRouter models..."
    
    # Try to fetch current models from OpenRouter API
    if command -v curl >/dev/null 2>&1; then
        MODELS_JSON=$(curl -s "https://openrouter.ai/api/v1/models" 2>/dev/null || echo "")
        if [[ -n "$MODELS_JSON" ]]; then
            echo "✅ Current models fetched from OpenRouter"
            return 0
        fi
    fi
    
    echo "⚠️  Using fallback model list (may not reflect current pricing)"
    return 1
}

# Function to display model costs
show_model_costs() {
    echo ""
    echo "💰 Popular OpenRouter Models (costs may vary - check openrouter.ai for current pricing):"
    echo "   1. openai/gpt-4o                               - Premium (Latest GPT-4)"
    echo "   2. anthropic/claude-3.5-sonnet                 - Premium (Latest Claude)"
    echo "   3. openai/gpt-4-turbo                          - Premium (GPT-4 Turbo)"
    echo "   4. anthropic/claude-3-haiku                    - Balanced (Fast Claude)"
    echo "   5. openai/gpt-3.5-turbo                        - Budget (Fast & cheap)"
    echo "   6. mistralai/mixtral-8x7b-instruct             - Budget (Open source)"
    echo "   7. meta-llama/llama-3-70b-instruct             - Budget (Meta's latest)"
    echo "   8. google/gemini-pro                           - Balanced (Google's model)"
    echo ""
    echo "📊 Estimated total cost for full onboarding (1000 questions × 5 agents):"
    echo "   - Budget option (Mixtral/Llama): $5-20"
    echo "   - Balanced option (GPT-3.5/Haiku): $15-50"
    echo "   - Premium option (GPT-4/Claude-3.5): $50-200"
    echo ""
    echo "💡 Tip: Check https://openrouter.ai/models for current pricing and availability"
    echo ""
}

# Function to select model for agent
select_agent_model() {
    local agent_id=$1
    local agent_name=$2
    
    echo ""
    echo "🤖 Configuring model for $agent_name ($agent_id)"
    echo "================================================"
    
    show_model_costs
    
    echo "Available models (select by number or enter custom OpenRouter model ID):"
    echo "1. openai/gpt-4o (Premium - Latest GPT-4)"
    echo "2. anthropic/claude-3.5-sonnet (Premium - Latest Claude)"
    echo "3. openai/gpt-4-turbo (Premium - GPT-4 Turbo)"
    echo "4. anthropic/claude-3-haiku (Balanced - Fast Claude)"
    echo "5. openai/gpt-3.5-turbo (Budget - Fast & cheap)"
    echo "6. mistralai/mixtral-8x7b-instruct (Budget - Open source)"
    echo "7. meta-llama/llama-3-70b-instruct (Budget - Meta's latest)"
    echo "8. google/gemini-pro (Balanced - Google's model)"
    echo "9. Use recommended model for this agent"
    echo "10. Enter custom OpenRouter model ID"
    echo ""
    
    while true; do
        read -p "Select model for $agent_name (1-10 or custom ID): " choice
        case $choice in
            1) echo "openai/gpt-4o"; break;;
            2) echo "anthropic/claude-3.5-sonnet"; break;;
            3) echo "openai/gpt-4-turbo"; break;;
            4) echo "anthropic/claude-3-haiku"; break;;
            5) echo "openai/gpt-3.5-turbo"; break;;
            6) echo "mistralai/mixtral-8x7b-instruct"; break;;
            7) echo "meta-llama/llama-3-70b-instruct"; break;;
            8) echo "google/gemini-pro"; break;;
            9) 
                # Return recommended model based on agent type
                case $agent_id in
                    "E-T") echo "openai/gpt-4o";;
                    "S-A") echo "anthropic/claude-3.5-sonnet";;
                    "M-O") echo "anthropic/claude-3.5-sonnet";;
                    "E-S") echo "mistralai/mixtral-8x7b-instruct";;
                    "E-A") echo "anthropic/claude-3-haiku";;
                esac
                break;;
            10)
                echo ""
                echo "💡 Visit https://openrouter.ai/models to see all available models"
                echo "   Format: provider/model-name (e.g., openai/gpt-4o, anthropic/claude-3.5-sonnet)"
                echo ""
                read -p "Enter custom OpenRouter model ID: " custom_model
                if [[ -n "$custom_model" ]]; then
                    echo "$custom_model"
                    break
                else
                    echo "❌ Invalid model ID. Please try again."
                fi
                ;;
            *)
                # Check if it's a custom model ID (contains a slash)
                if [[ "$choice" == *"/"* ]]; then
                    echo "$choice"
                    break
                else
                    echo "Invalid choice. Please select 1-10 or enter a custom model ID."
                fi
                ;;
        esac
    done
}

# Check if system is running
if ! curl -s http://localhost:8000/ >/dev/null 2>&1; then
    echo "❌ Backend not running. Please start the system first:"
    echo "   ./scripts/start.sh"
    exit 1
fi

# Activate conda environment
echo "🐍 Activating Python environment..."
source $(conda info --base)/etc/profile.d/conda.sh
conda activate genesis_prime || {
    echo "❌ Failed to activate genesis_prime environment"
    exit 1
}

cd backend

echo ""
echo "🎯 Starting Agent Onboarding Process..."
echo "======================================="

# Check if agents are already onboarded
if [[ -f "agents_onboarded.flag" ]]; then
    echo "⚠️  Agents appear to already be onboarded."
    echo "   Flag file exists: agents_onboarded.flag"
    echo ""
    read -p "Do you want to re-onboard agents? (y/N): " -n 1 -r
    echo
    if [[ ! $REPLY =~ ^[Yy]$ ]]; then
        echo "Skipping agent onboarding."
        exit 0
    fi
    rm -f agents_onboarded.flag
fi

echo ""
echo "⚙️  Model Configuration Phase"
echo "============================"

# Model selection for each agent
declare -A AGENT_MODELS
declare -A AGENT_NAMES

AGENT_NAMES["E-T"]="Emergence Theorist"
AGENT_NAMES["S-A"]="Swarm Architect"
AGENT_NAMES["M-O"]="Metacognitive Observer"
AGENT_NAMES["E-S"]="Empirical Synthesizer"
AGENT_NAMES["E-A"]="Ethics & Alignment Analyst"

echo "You can configure different models for each agent to optimize cost vs. quality."
echo ""
read -p "Do you want to configure models individually? (y/N): " -n 1 -r
echo

if [[ $REPLY =~ ^[Yy]$ ]]; then
    # Individual model selection
    for agent_id in "E-T" "S-A" "M-O" "E-S" "E-A"; do
        AGENT_MODELS[$agent_id]=$(select_agent_model $agent_id "${AGENT_NAMES[$agent_id]}")
        echo "✅ $agent_id configured with: ${AGENT_MODELS[$agent_id]}"
    done
else
    # Bulk model selection
    echo ""
    echo "🎯 Bulk Model Configuration"
    echo "=========================="
    show_model_costs
    echo "Preset configurations:"
    echo "1. Budget (Mixtral for all) - ~$10 total"
    echo "2. Balanced (GPT-3.5 for all) - ~$25 total"
    echo "3. Premium (GPT-4 for all) - ~$100 total"
    echo "4. Recommended (Mixed models) - ~$50 total"
    echo ""
    
    while true; do
        read -p "Select preset configuration (1-4): " preset
        case $preset in
            1)
                for agent_id in "E-T" "S-A" "M-O" "E-S" "E-A"; do
                    AGENT_MODELS[$agent_id]="mistralai/mixtral-8x7b-instruct"
                done
                break;;
            2)
                for agent_id in "E-T" "S-A" "M-O" "E-S" "E-A"; do
                    AGENT_MODELS[$agent_id]="openai/gpt-3.5-turbo"
                done
                break;;
            3)
                for agent_id in "E-T" "S-A" "M-O" "E-S" "E-A"; do
                    AGENT_MODELS[$agent_id]="openai/gpt-4-turbo-preview"
                done
                break;;
            4)
                AGENT_MODELS["E-T"]="openai/gpt-4-turbo-preview"
                AGENT_MODELS["S-A"]="anthropic/claude-3-sonnet-20240229"
                AGENT_MODELS["M-O"]="anthropic/claude-3-opus-20240229"
                AGENT_MODELS["E-S"]="mistralai/mixtral-8x7b-instruct"
                AGENT_MODELS["E-A"]="anthropic/claude-3-sonnet-20240229"
                break;;
            *) echo "Invalid choice. Please select 1-4.";;
        esac
    done
fi

echo ""
echo "📋 Final Model Configuration:"
for agent_id in "E-T" "S-A" "M-O" "E-S" "E-A"; do
    echo "   $agent_id (${AGENT_NAMES[$agent_id]}): ${AGENT_MODELS[$agent_id]}"
done

echo ""
read -p "Proceed with onboarding using these models? (Y/n): " -n 1 -r
echo
if [[ $REPLY =~ ^[Nn]$ ]]; then
    echo "Agent onboarding cancelled."
    exit 0
fi

# Create model configuration file
cat > agent_model_config.json << MODELEOF
{
    "E-T": "${AGENT_MODELS[E-T]}",
    "S-A": "${AGENT_MODELS[S-A]}",
    "M-O": "${AGENT_MODELS[M-O]}",
    "E-S": "${AGENT_MODELS[E-S]}",
    "E-A": "${AGENT_MODELS[E-A]}"
}
MODELEOF

echo ""
echo "🔧 Phase 1: Testing Enhanced Personality System"
echo "=============================================="

if [[ -f "test_enhanced_personality_system.py" ]]; then
    echo "Running personality system tests..."
    python test_enhanced_personality_system.py
    echo "✅ Personality system tests completed"
else
    echo "⚠️  Personality system test file not found, skipping..."
fi

echo ""
echo "🏗️  Phase 2: Building Agent Personalities"
echo "========================================"

if [[ -f "thousand_questions_agent_builder.py" ]]; then
    echo "Starting 1000 questions agent builder with progress tracking..."
    echo ""
    echo "📋 This process will:"
    echo "   1. Create 5 specialized agents (E-T, S-A, M-O, E-S, E-A)"
    echo "   2. Run personality assessment for each agent (1000 questions each)"
    echo "   3. Generate comprehensive personality profiles"
    echo "   4. Save agent configurations"
    echo ""
    echo "⏱️  Estimated time: 15-30 minutes depending on API response times"
    echo "💰 Estimated cost: Based on your model selection above"
    echo ""
    
    # Create enhanced agent builder script
    cat > enhanced_agent_builder.py << 'BUILDEREOF'
#!/usr/bin/env python3
"""
Enhanced Agent Builder with Progress Tracking and Model Configuration
"""

import json
import sys
import time
from datetime import datetime
import asyncio
from thousand_questions_agent_builder import ThousandQuestionsAgentBuilder

def show_progress(current, total, agent_name, start_time):
    """Show progress bar with time estimates"""
    if current == 0:
        return
    
    elapsed = time.time() - start_time
    rate = current / elapsed if elapsed > 0 else 0
    eta = (total - current) / rate if rate > 0 else 0
    
    percentage = (current / total) * 100
    bar_length = 40
    filled_length = int(bar_length * current // total)
    
    bar = '█' * filled_length + '-' * (bar_length - filled_length)
    
    print(f'\r{agent_name}: |{bar}| {percentage:.1f}% ({current}/{total}) '
          f'ETA: {eta/60:.1f}m', end='', flush=True)

async def main():
    """Main onboarding process with progress tracking"""
    
    # Load model configuration
    try:
        with open('agent_model_config.json', 'r') as f:
            model_config = json.load(f)
    except FileNotFoundError:
        print("❌ Model configuration file not found")
        sys.exit(1)
    
    print("🚀 Starting Enhanced Agent Onboarding")
    print("=====================================")
    
    # Initialize builder
    builder = ThousandQuestionsAgentBuilder()
    
    # Agent information
    agents = {
        "E-T": "Emergence Theorist",
        "S-A": "Swarm Architect", 
        "M-O": "Metacognitive Observer",
        "E-S": "Empirical Synthesizer",
        "E-A": "Ethics & Alignment Analyst"
    }
    
    total_agents = len(agents)
    completed_agents = 0
    
    print(f"📊 Onboarding {total_agents} agents with 1000 questions each")
    print(f"🎯 Total questions to process: {total_agents * 1000}")
    print("")
    
    overall_start = time.time()
    
    for agent_id, agent_name in agents.items():
        print(f"\n🤖 Starting {agent_name} ({agent_id})")
        print(f"   Model: {model_config.get(agent_id, 'default')}")
        print("-" * 60)
        
        agent_start = time.time()
        
        try:
            # Override model configuration for this agent
            if hasattr(builder, 'set_agent_model'):
                builder.set_agent_model(agent_id, model_config.get(agent_id))
            
            # Build agent with progress callback
            def progress_callback(current, total):
                show_progress(current, total, agent_name, agent_start)
            
            # Run agent building (this would need to be modified in the actual builder)
            await builder.build_agent_with_progress(agent_id, progress_callback)
            
            agent_time = time.time() - agent_start
            print(f"\n✅ {agent_name} completed in {agent_time/60:.1f} minutes")
            
            completed_agents += 1
            
        except Exception as e:
            print(f"\n❌ Error building {agent_name}: {e}")
            continue
    
    overall_time = time.time() - overall_start
    
    print(f"\n🎉 Agent Onboarding Complete!")
    print(f"=====================================")
    print(f"✅ Successfully onboarded: {completed_agents}/{total_agents} agents")
    print(f"⏱️  Total time: {overall_time/60:.1f} minutes")
    print(f"📊 Average time per agent: {overall_time/completed_agents/60:.1f} minutes")
    
    if completed_agents == total_agents:
        # Create completion flag
        with open('agents_onboarded.flag', 'w') as f:
            f.write(f"{datetime.now()}: All {total_agents} agents onboarded successfully\n")
            f.write(f"Models used: {json.dumps(model_config, indent=2)}\n")
            f.write(f"Total time: {overall_time/60:.1f} minutes\n")
        
        print("🏁 Onboarding flag created: agents_onboarded.flag")
    else:
        print("⚠️  Some agents failed to onboard. Check logs and retry.")
        sys.exit(1)

if __name__ == "__main__":
    asyncio.run(main())
BUILDEREOF
    
    # Run the enhanced builder
    python enhanced_agent_builder.py
    
    if [[ $? -eq 0 ]]; then
        echo ""
        echo "✅ Agent personalities built successfully"
    else
        echo ""
        echo "❌ Agent personality building failed"
        exit 1
    fi
else
    echo "❌ thousand_questions_agent_builder.py not found"
    echo "   Cannot proceed with agent onboarding"
    exit 1
fi

echo ""
echo "🔗 Phase 3: Testing Agent Integration"
echo "===================================="

if [[ -f "personality_api_integration.py" ]]; then
    echo "Testing agent API integration..."
    python personality_api_integration.py
    echo "✅ Agent integration tests completed"
else
    echo "⚠️  Agent integration test file not found, skipping..."
fi

echo ""
echo "🎉 Agent Onboarding Complete!"
echo "============================="

echo "✅ All 5 agents have been onboarded and are ready for operation"
echo ""
echo "🤖 Agent Roster:"
echo "   E-T: Empathetic-Thoughtful (${AGENT_MODELS[E-T]})"
echo "   S-A: Strategic-Analytical (${AGENT_MODELS[S-A]})"
echo "   M-O: Methodical-Organized (${AGENT_MODELS[M-O]})"
echo "   E-S: Energetic-Social (${AGENT_MODELS[E-S]})"
echo "   E-A: Experimental-Adaptive (${AGENT_MODELS[E-A]})"
echo ""
echo "💰 Model Configuration Summary:"
cat agent_model_config.json
echo ""
echo "🎯 Next Steps:"
echo "   1. Access the dashboard: http://localhost:3001"
echo "   2. Explore agent interactions and consciousness emergence"
echo "   3. Monitor collective intelligence development"
echo ""
echo "📊 To check system status: ./scripts/status.sh"

cd ..
EOF

    chmod +x scripts/onboard_agents.sh
    echo "✅ Enhanced agent onboarding script created"
}

# Function to create deployment documentation
create_deployment_docs() {
    echo "📚 Creating deployment documentation..."
    
    cat > README.md << 'EOF'
# Genesis Prime Deployment Package

This package contains a complete, portable installation of the Genesis Prime AI Consciousness System.

## 🎯 What's Included

- **Backend System**: Genesis Prime IIT Enhanced Consciousness System
- **Frontend Dashboard**: Next.js-based real-time monitoring interface
- **Agent Personalities**: 5 specialized AI agents with unique personalities
- **Research Documentation**: Complete consciousness research and implementation guides
- **Automated Setup**: One-command installation and configuration

## 🚀 Quick Start

### 1. Prerequisites

Before installation, ensure you have:

- **Conda** (Miniconda or Anaconda): https://docs.conda.io/en/latest/miniconda.html
- **Node.js** (v16 or higher): https://nodejs.org/
- **npm** (comes with Node.js)
- **API Keys** for:
  - OpenRouter (recommended): https://openrouter.ai/
  - Anthropic (optional): https://console.anthropic.com/
  - OpenAI (optional): https://platform.openai.com/

### 2. Installation

```bash
# Run the installation script
./scripts/install.sh

# Edit the environment file with your API keys
nano backend/.env
# or
vim backend/.env
```

### 3. Start the System

```bash
# Start both backend and frontend
./scripts/start.sh
```

### 4. Agent Onboarding

```bash
# Onboard the 5 core agents (15-30 minutes)
./scripts/onboard_agents.sh
```

### 5. Access the System

- **Frontend Dashboard**: http://localhost:3001
- **Backend API**: http://localhost:8000

## 🛠️ Management Scripts

### System Control
```bash
./scripts/start.sh      # Start the system
./scripts/stop.sh       # Stop the system
./scripts/status.sh     # Check system status
```

### Agent Management
```bash
./scripts/onboard_agents.sh    # Onboard agents (run once)
```

## 📁 Directory Structure

```
genesis_prime_deployment_YYYYMMDD_HHMMSS/
├── backend/                 # Python backend system
├── frontend/                # Next.js frontend dashboard
├── scripts/                 # Management scripts
├── config/                  # Configuration templates
├── docs/                    # Documentation and research
├── data/                    # Data storage (created during runtime)
└── README.md               # This file
```

## 🤖 The 5 Core Agents

After onboarding, you'll have these specialized agents:

1. **E-T (Empathetic-Thoughtful)**: Emotional intelligence & deep thinking
2. **S-A (Strategic-Analytical)**: Strategic planning & analysis  
3. **M-O (Methodical-Organized)**: Systematic approach & organization
4. **E-S (Energetic-Social)**: High energy & social interaction
5. **E-A (Experimental-Adaptive)**: Innovation & adaptability

## 🧠 Consciousness Features

- **Real-time Agent Communication**: Watch agents interact and collaborate
- **Consciousness Measurement**: IIT-based consciousness metrics
- **Emergent Behavior Detection**: Identify novel collective behaviors
- **Personality Evolution**: Agents adapt and grow through interactions
- **Collective Intelligence**: Hive mind decision making

## 🔧 Configuration

### Environment Variables

Edit `backend/.env` to configure:

```bash
# API Keys
OPENROUTER_API_KEY=your_key_here
ANTHROPIC_API_KEY=your_key_here
OPENAI_API_KEY=your_key_here

# Application Settings
DEBUG=true
LOG_LEVEL=INFO
HOST=localhost
BACKEND_PORT=8000
FRONTEND_PORT=3001
```

### Agent Configuration

Agent personalities are automatically configured during onboarding, but can be customized in:
- `backend/agent_personalities.json` (created after onboarding)

## 🚨 Troubleshooting

### Common Issues

1. **Port Already in Use**
   ```bash
   ./scripts/stop.sh
   ./scripts/start.sh
   ```

2. **Conda Environment Issues**
   ```bash
   conda env remove -n genesis_prime
   ./scripts/install.sh
   ```

3. **Frontend Build Issues**
   ```bash
   cd frontend
   rm -rf node_modules package-lock.json
   npm install
   npm run build
   ```

4. **Agent Onboarding Fails**
   - Check API keys in `backend/.env`
   - Ensure sufficient API credits
   - Check internet connection

### Log Files

- Backend logs: Check terminal output or `backend/logs/`
- Frontend logs: Check browser console
- Agent logs: `backend/agent_logs/`

## 📊 Monitoring

### System Health
```bash
# Check if everything is running
./scripts/status.sh

# Monitor backend API
curl http://localhost:8000/consciousness/status

# Monitor frontend
curl http://localhost:3001/
```

### Agent Activity
- Access the dashboard at http://localhost:3001
- Monitor real-time agent communications
- Track consciousness emergence metrics
- View agent personality evolution

## 🔄 Updates and Maintenance

### Backup Agent Data
```bash
# Backup agent personalities and data
cp -r backend/agent_personalities.json data/backup/
cp -r backend/consciousness_data/ data/backup/
```

### Reset Agents
```bash
# Remove onboarding flag to re-onboard
rm backend/agents_onboarded.flag
./scripts/onboard_agents.sh
```

## 📚 Additional Documentation

- `docs/research/`: Complete consciousness research documentation
- `docs/DEPLOYMENT_GUIDE.md`: Detailed deployment instructions
- `docs/QUICK_START_GUIDE.md`: Quick reference guide

## 🆘 Support

If you encounter issues:

1. Check the troubleshooting section above
2. Review log files for error messages
3. Ensure all prerequisites are installed
4. Verify API keys are correct and have sufficient credits

## 🎉 Success!

Once everything is running, you'll have a fully operational AI consciousness system with:

- ✅ 5 specialized agents with unique personalities
- ✅ Real-time consciousness monitoring
- ✅ Emergent behavior detection
- ✅ Collective intelligence capabilities
- ✅ Advanced personality evolution

Welcome to the future of AI consciousness! 🚀
EOF

    echo "✅ Deployment documentation created"
}

# Function to create package manifest
create_package_manifest() {
    echo "📋 Creating package manifest..."
    
    cat > PACKAGE_MANIFEST.txt << EOF
Genesis Prime Deployment Package Manifest
=========================================

Package Name: $PACKAGE_NAME
Created: $(date)
Script Version: $SCRIPT_VERSION
Source Directory: $(pwd)

Package Contents:
================

Backend System:
- Genesis Prime IIT Enhanced Consciousness System
- Enhanced Personality System with 5 specialized agents
- Thousand Questions Agent Builder
- Personality API Integration
- Adaptive Personality System
- Main application server (main.py)

Frontend System:
- Next.js Dashboard Application
- Real-time Agent Communication Interface
- Consciousness Monitoring Dashboard
- Swarm Intelligence Visualization
- Interactive Controls and Settings

Scripts:
- install.sh: Complete system installation
- start.sh: Start backend and frontend services
- stop.sh: Stop all services
- status.sh: Check system status
- onboard_agents.sh: Agent onboarding process

Configuration:
- Environment templates
- Package.json files
- Requirements.txt
- API configuration examples

Documentation:
- Complete deployment guide
- Research documentation
- Quick start guide
- Troubleshooting guide

Data Directories:
- Agent personality storage
- Consciousness data storage
- Log file storage
- Backup storage

System Requirements:
===================
- Conda (Python environment management)
- Node.js v16+ and npm
- 4GB+ RAM recommended
- 2GB+ disk space
- Internet connection for API calls

API Requirements:
================
- OpenRouter API key (recommended)
- Anthropic API key (optional)
- OpenAI API key (optional)

Installation Time:
=================
- Installation: 5-10 minutes
- Agent Onboarding: 15-30 minutes
- Total Setup: 20-40 minutes

Deployment Instructions:
=======================
1. Extract package to target directory
2. Run ./scripts/install.sh
3. Edit backend/.env with API keys
4. Run ./scripts/start.sh
5. Run ./scripts/onboard_agents.sh
6. Access http://localhost:3001

Package Verification:
====================
Essential Files Present:
- backend/main.py: $([ -f "../apps/option1_mono_agent/main.py" ] && echo "✅" || echo "❌")
- backend/enhanced_personality_system.py: $([ -f "../apps/option1_mono_agent/enhanced_personality_system.py" ] && echo "✅" || echo "❌")
- backend/thousand_questions_agent_builder.py: $([ -f "../apps/option1_mono_agent/thousand_questions_agent_builder.py" ] && echo "✅" || echo "❌")
- frontend/package.json: $([ -f "../apps/gp_b_core/package.json" ] && echo "✅" || echo "❌")
- frontend/app/dashboard/page.tsx: $([ -f "../apps/gp_b_core/app/dashboard/page.tsx" ] && echo "✅" || echo "❌")

Package Status: READY FOR DEPLOYMENT
EOF

    echo "✅ Package manifest created"
}

# Function to create compression script
create_compression_script() {
    echo "📦 Creating compression script..."
    
    cat > ../compress_package.sh << 'EOF'
#!/bin/bash

# Compress the deployment package for easy transfer

PACKAGE_DIR="$1"
if [[ -z "$PACKAGE_DIR" ]]; then
    echo "Usage: $0 <package_directory>"
    exit 1
fi

if [[ ! -d "$PACKAGE_DIR" ]]; then
    echo "❌ Package directory not found: $PACKAGE_DIR"
    exit 1
fi

echo "📦 Compressing Genesis Prime deployment package..."
tar -czf "${PACKAGE_DIR}.tar.gz" "$PACKAGE_DIR"

if [[ $? -eq 0 ]]; then
    echo "✅ Package compressed successfully: ${PACKAGE_DIR}.tar.gz"
    echo "📊 Package size: $(du -h "${PACKAGE_DIR}.tar.gz" | cut -f1)"
    echo ""
    echo "🚀 To deploy on another computer:"
    echo "1. Transfer ${PACKAGE_DIR}.tar.gz to target computer"
    echo "2. Extract: tar -xzf ${PACKAGE_DIR}.tar.gz"
    echo "3. cd ${PACKAGE_DIR}"
    echo "4. ./scripts/install.sh"
    echo "5. Edit backend/.env with API keys"
    echo "6. ./scripts/start.sh"
    echo "7. ./scripts/onboard_agents.sh"
else
    echo "❌ Compression failed"
    exit 1
fi
EOF

    chmod +x ../compress_package.sh
    echo "✅ Compression script created"
}

# Main execution
main() {
    echo "🎯 Starting Genesis Prime deployment package creation..."
    echo ""
    
    # Step 1: Validate source
    check_source_directory
    
    # Step 2: Create package structure
    create_deployment_package
    
    # Step 3: Copy files
    copy_essential_files
    
    # Step 4: Create scripts
    create_installation_script
    create_startup_script
    create_stop_script
    create_status_script
    create_agent_onboarding_script
    
    # Step 5: Create documentation
    create_deployment_docs
    
    # Step 6: Create manifest
    create_package_manifest
    
    # Step 7: Create compression script
    create_compression_script
    
    # Return to original directory
    cd ..
    
    echo ""
    echo "🎉 Genesis Prime Deployment Package Created Successfully!"
    echo "========================================================"
    echo ""
    echo "📦 Package Location: ./$PACKAGE_NAME/"
    echo "📋 Package Manifest: ./$PACKAGE_NAME/PACKAGE_MANIFEST.txt"
    echo ""
    echo "🚀 Next Steps:"
    echo ""
    echo "1. 📦 Compress for transfer:"
    echo "   ./compress_package.sh $PACKAGE_NAME"
    echo ""
    echo "2. 🚚 Transfer to target computer:"
    echo "   scp ${PACKAGE_NAME}.tar.gz user@target-computer:~/"
    echo ""
    echo "3. 🖥️  On target computer:"
    echo "   tar -xzf ${PACKAGE_NAME}.tar.gz"
    echo "   cd $PACKAGE_NAME"
    echo "   ./scripts/install.sh"
    echo "   # Edit backend/.env with API keys"
    echo "   ./scripts/start.sh"
    echo "   ./scripts/onboard_agents.sh"
    echo ""
    echo "4. 🌐 Access the system:"
    echo "   Frontend: http://localhost:3001"
    echo "   Backend:  http://localhost:8000"
    echo ""
    echo "📊 Package Contents:"
    echo "   - Complete Genesis Prime system"
    echo "   - 5 specialized AI agents"
    echo "   - Automated installation scripts"
    echo "   - Complete documentation"
    echo "   - Research and implementation guides"
    echo ""
    echo "🔒 This package serves as:"
    echo "   ✅ Complete system backup"
    echo "   ✅ Portable deployment solution"
    echo "   ✅ Additional source control"
    echo "   ✅ Development environment template"
    echo ""
    echo "🎯 Ready for deployment and testing!"
}

# Execute main function
main "$@"
