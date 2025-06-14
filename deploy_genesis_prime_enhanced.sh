#!/bin/bash

# Genesis Prime Enhanced Deployment Script
# Comprehensive deployment automation with Docker support and Python 3.13

set -e  # Exit on any error

# Color codes for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Configuration
PYTHON_VERSION="3.13"
NODE_VERSION="18"
SCRIPT_VERSION="2.0"
DEPLOYMENT_DATE=$(date +"%Y%m%d_%H%M%S")
PACKAGE_NAME="genesis_prime_deployment_${DEPLOYMENT_DATE}"

echo -e "${BLUE}🚀 Genesis Prime Enhanced Deployment Script v${SCRIPT_VERSION}${NC}"
echo "=============================================================="
echo -e "${YELLOW}Creating portable deployment package: $PACKAGE_NAME${NC}"
echo -e "${YELLOW}Python Version: ${PYTHON_VERSION}${NC}"
echo -e "${YELLOW}Node.js Version: ${NODE_VERSION}+${NC}"
echo ""

# Function to log errors
log_error() {
    local error_msg="$1"
    local resolution="$2"
    echo -e "${RED}❌ Error: $error_msg${NC}"
    if [[ -n "$resolution" ]]; then
        echo -e "${YELLOW}💡 Resolution: $resolution${NC}"
    fi
    
    # Log to error file
    echo "$(date): ERROR - $error_msg" >> error_logWS.md
    if [[ -n "$resolution" ]]; then
        echo "$(date): RESOLUTION - $resolution" >> error_logWS.md
    fi
    echo "" >> error_logWS.md
}

# Function to check if we're in the right directory
check_source_directory() {
    echo -e "${BLUE}🔍 Validating source directory...${NC}"
    
    if [[ ! -d "apps/option1_mono_agent" ]] || [[ ! -d "apps/gp_b_core" ]]; then
        log_error "Please run this script from the Gen_Prime_V3-main directory" \
                  "Navigate to the correct directory containing apps/option1_mono_agent/ and apps/gp_b_core/"
        echo "Expected structure:"
        echo "  - apps/option1_mono_agent/ (backend)"
        echo "  - apps/gp_b_core/ (frontend)"
        exit 1
    fi
    echo -e "${GREEN}✅ Source directory validated${NC}"
}

# Function to check deployment type
check_deployment_type() {
    echo -e "${BLUE}🎯 Select Deployment Type${NC}"
    echo "1. Standard Deployment (Conda + Node.js)"
    echo "2. Docker Deployment (Containerized)"
    echo "3. Hybrid Deployment (Both options)"
    echo ""
    
    while true; do
        read -p "Select deployment type (1-3): " deploy_type
        case $deploy_type in
            1) DEPLOYMENT_TYPE="standard"; break;;
            2) DEPLOYMENT_TYPE="docker"; break;;
            3) DEPLOYMENT_TYPE="hybrid"; break;;
            *) echo "Invalid choice. Please select 1-3.";;
        esac
    done
    
    echo -e "${GREEN}✅ Deployment type: $DEPLOYMENT_TYPE${NC}"
}

# Function to create deployment package
create_deployment_package() {
    echo -e "${BLUE}📦 Creating deployment package...${NC}"
    
    # Create deployment directory
    mkdir -p "$PACKAGE_NAME"
    cd "$PACKAGE_NAME"
    
    # Create directory structure
    mkdir -p {backend,frontend,docs,scripts,config,data,docker}
    
    echo -e "${GREEN}   📁 Directory structure created${NC}"
}

# Function to copy essential files
copy_essential_files() {
    echo -e "${BLUE}📋 Copying essential application files...${NC}"
    
    # Copy backend files
    echo -e "${YELLOW}   🔧 Copying backend (option1_mono_agent)...${NC}"
    rsync -av --exclude='__pycache__' --exclude='*.pyc' --exclude='*.pyo' \
          --exclude='.pytest_cache' --exclude='logs' --exclude='*.log' \
          ../apps/option1_mono_agent/ backend/
    
    # Copy frontend files (excluding build artifacts and dependencies)
    echo -e "${YELLOW}   🎨 Copying frontend (gp_b_core)...${NC}"
    rsync -av --exclude='node_modules' --exclude='.next' --exclude='dist' \
          --exclude='build' --exclude='.cache' --exclude='*.log' \
          --exclude='.turbo' --exclude='.vercel' --exclude='coverage' \
          --exclude='package-lock.json' --exclude='yarn.lock' \
          --exclude='.DS_Store' --exclude='*.tmp' --exclude='*.temp' \
          ../apps/gp_b_core/ frontend/
    
    # Copy Docker files if they exist
    if [[ "$DEPLOYMENT_TYPE" == "docker" ]] || [[ "$DEPLOYMENT_TYPE" == "hybrid" ]]; then
        echo -e "${YELLOW}   🐳 Copying Docker configuration...${NC}"
        if [[ -d "../docker" ]]; then
            cp -r ../docker/* docker/
        fi
        if [[ -f "../docker-compose.yml" ]]; then
            cp ../docker-compose.yml ./
        fi
        if [[ -f "../.env.docker" ]]; then
            cp ../.env.docker ./
        fi
    fi
    
    # Verify exclusions worked
    if [[ -d "frontend/node_modules" ]]; then
        echo -e "${YELLOW}   ⚠️  WARNING: node_modules was copied despite exclusion!${NC}"
        echo -e "${YELLOW}   🗑️  Removing node_modules to reduce package size...${NC}"
        rm -rf frontend/node_modules
    fi
    
    # Copy documentation and research
    echo -e "${YELLOW}   📚 Copying documentation...${NC}"
    if [[ -d "../sentaimds" ]]; then
        cp -r ../sentaimds docs/research/
    fi
    
    # Copy important root files
    echo -e "${YELLOW}   📄 Copying configuration files...${NC}"
    [[ -f "../README.md" ]] && cp ../README.md docs/
    [[ -f "../DEPLOYMENT_GUIDE.md" ]] && cp ../DEPLOYMENT_GUIDE.md docs/
    [[ -f "../DOCKER_DEPLOYMENT_GUIDE.md" ]] && cp ../DOCKER_DEPLOYMENT_GUIDE.md docs/
    [[ -f "../QUICK_START_GUIDE.md" ]] && cp ../QUICK_START_GUIDE.md docs/
    [[ -f "../requirements.txt" ]] && cp ../requirements.txt config/
    [[ -f "../.env.example" ]] && cp ../.env.example config/
    
    # Copy agent model configuration files
    echo -e "${YELLOW}   🤖 Copying agent model configuration files...${NC}"
    [[ -f "../agent_models.json" ]] && cp ../agent_models.json config/
    [[ -f "../agent_models_budget.json" ]] && cp ../agent_models_budget.json config/
    [[ -f "../agent_models_premium.json" ]] && cp ../agent_models_premium.json config/
    [[ -f "../agent_model_config.json" ]] && cp ../agent_model_config.json config/
    
    # Copy existing scripts
    if [[ -d "../scripts" ]]; then
        echo -e "${YELLOW}   📜 Copying existing scripts...${NC}"
        cp -r ../scripts/* scripts/ 2>/dev/null || true
    fi
    
    echo -e "${GREEN}✅ Essential files copied${NC}"
}

# Function to create enhanced installation script
create_installation_script() {
    echo -e "${BLUE}🛠️ Creating enhanced installation script...${NC}"
    
    cat > scripts/install.sh << 'EOF'
#!/bin/bash

# Genesis Prime Enhanced Installation Script
# Supports both standard and Docker deployments with Python 3.13

set -e

echo "🚀 Genesis Prime Enhanced Installation Starting..."
echo "================================================="

# Color codes
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m'

# Configuration
PYTHON_VERSION="3.13"
NODE_MIN_VERSION="18"

# Function to log errors
log_error() {
    local error_msg="$1"
    local resolution="$2"
    echo -e "${RED}❌ Error: $error_msg${NC}"
    if [[ -n "$resolution" ]]; then
        echo -e "${YELLOW}💡 Resolution: $resolution${NC}"
    fi
    
    # Log to error file
    echo "$(date): ERROR - $error_msg" >> ../error_logWS.md
    if [[ -n "$resolution" ]]; then
        echo "$(date): RESOLUTION - $resolution" >> ../error_logWS.md
    fi
    echo "" >> ../error_logWS.md
}

# Check operating system
OS="unknown"
if [[ "$OSTYPE" == "linux-gnu"* ]]; then
    OS="linux"
elif [[ "$OSTYPE" == "darwin"* ]]; then
    OS="macos"
elif [[ "$OSTYPE" == "msys" ]] || [[ "$OSTYPE" == "cygwin" ]]; then
    OS="windows"
fi

echo -e "${BLUE}🖥️  Detected OS: $OS${NC}"

# Function to check if command exists
command_exists() {
    command -v "$1" >/dev/null 2>&1
}

# Function to compare versions
version_ge() {
    printf '%s\n%s\n' "$2" "$1" | sort -V -C
}

# Check deployment type
echo -e "${BLUE}🎯 Select Installation Type${NC}"
echo "1. Standard Installation (Conda + Node.js)"
echo "2. Docker Installation (Requires Docker)"
echo ""

while true; do
    read -p "Select installation type (1-2): " install_type
    case $install_type in
        1) INSTALL_TYPE="standard"; break;;
        2) INSTALL_TYPE="docker"; break;;
        *) echo "Invalid choice. Please select 1-2.";;
    esac
done

if [[ "$INSTALL_TYPE" == "docker" ]]; then
    echo -e "${BLUE}🐳 Docker Installation Selected${NC}"
    
    # Check for Docker
    if ! command_exists docker; then
        log_error "Docker not found" "Please install Docker first: https://docs.docker.com/get-docker/"
        exit 1
    fi
    
    # Check for Docker Compose
    if ! command_exists docker-compose && ! docker compose version >/dev/null 2>&1; then
        log_error "Docker Compose not found" "Please install Docker Compose: https://docs.docker.com/compose/install/"
        exit 1
    fi
    
    echo -e "${GREEN}✅ Docker found${NC}"
    
    # Copy environment template
    if [[ -f ".env.docker" ]]; then
        cp .env.docker .env
        echo -e "${GREEN}✅ Environment template created from .env.docker${NC}"
    else
        cat > .env << 'ENVEOF'
# Genesis Prime Docker Environment Configuration
OPENROUTER_API_KEY=your_openrouter_api_key_here
ANTHROPIC_API_KEY=your_anthropic_api_key_here
OPENAI_API_KEY=your_openai_api_key_here
GOOGLE_API_KEY=your_google_api_key_here
ENVIRONMENT=production
PYTHONPATH=/app
NODE_ENV=production
NEXT_PUBLIC_API_URL=http://localhost:8000
NEXT_PUBLIC_FRONTEND_URL=http://localhost:3001
ENVEOF
        echo -e "${GREEN}✅ Environment template created${NC}"
    fi
    
    echo -e "${YELLOW}⚠️  Please edit .env with your API keys before starting${NC}"
    echo -e "${GREEN}✅ Docker installation complete${NC}"
    echo ""
    echo -e "${BLUE}📋 Next Steps:${NC}"
    echo "1. Edit .env with your API keys"
    echo "2. Run: docker-compose up -d"
    echo "3. Run: docker-compose --profile onboarding up genesis-onboarding"
    echo "4. Access: http://localhost:3001"
    
    exit 0
fi

# Standard installation continues here
echo -e "${BLUE}🐍 Standard Installation Selected${NC}"

# Check for conda
echo -e "${BLUE}🐍 Checking for conda...${NC}"
if ! command_exists conda; then
    log_error "Conda not found" "Please install Miniconda or Anaconda first: https://docs.conda.io/en/latest/miniconda.html"
    exit 1
fi
echo -e "${GREEN}✅ Conda found${NC}"

# Check for Node.js
echo -e "${BLUE}📦 Checking for Node.js...${NC}"
if ! command_exists node; then
    log_error "Node.js not found" "Please install Node.js first: https://nodejs.org/"
    exit 1
fi

NODE_VERSION=$(node --version | sed 's/v//')
if ! version_ge "$NODE_VERSION" "$NODE_MIN_VERSION"; then
    log_error "Node.js version $NODE_VERSION is too old" "Please install Node.js $NODE_MIN_VERSION or higher"
    exit 1
fi
echo -e "${GREEN}✅ Node.js found: v$NODE_VERSION${NC}"

# Check for npm
if ! command_exists npm; then
    log_error "npm not found" "Please install npm first"
    exit 1
fi
echo -e "${GREEN}✅ npm found: $(npm --version)${NC}"

# Create conda environment
echo -e "${BLUE}🐍 Setting up Python environment...${NC}"
ENV_NAME="genesis_prime"

# Check if environment already exists
if conda env list | grep -q "^${ENV_NAME} "; then
    echo -e "${YELLOW}⚠️  Environment '$ENV_NAME' already exists. Removing...${NC}"
    conda env remove -n $ENV_NAME -y
fi

# Create new environment with Python 3.13
echo -e "${YELLOW}   Creating conda environment: $ENV_NAME (Python $PYTHON_VERSION)${NC}"
conda create -n $ENV_NAME python=$PYTHON_VERSION -y

# Activate environment
echo -e "${YELLOW}   Activating environment...${NC}"
source $(conda info --base)/etc/profile.d/conda.sh
conda activate $ENV_NAME

# Install Python dependencies
echo -e "${YELLOW}   Installing Python dependencies...${NC}"
if [[ -f "backend/requirements.txt" ]]; then
    pip install -r backend/requirements.txt
elif [[ -f "config/requirements.txt" ]]; then
    pip install -r config/requirements.txt
else
    # Install essential packages
    pip install fastapi uvicorn openai anthropic requests python-dotenv pydantic
fi

echo -e "${GREEN}✅ Python environment setup complete${NC}"

# Setup frontend
echo -e "${BLUE}🎨 Setting up frontend...${NC}"
cd frontend

# Install npm dependencies
echo -e "${YELLOW}   Installing npm dependencies...${NC}"
npm install

# Build frontend (optional, for production)
echo -e "${YELLOW}   Building frontend...${NC}"
npm run build || echo -e "${YELLOW}⚠️  Build failed, but continuing...${NC}"

cd ..

echo -e "${GREEN}✅ Frontend setup complete${NC}"

# Create environment file
echo -e "${BLUE}⚙️  Creating environment configuration...${NC}"
if [[ -f "config/.env.example" ]]; then
    cp config/.env.example backend/.env
    echo -e "${GREEN}   📝 Created backend/.env from template${NC}"
    echo -e "${YELLOW}   ⚠️  Please edit backend/.env with your API keys${NC}"
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

# Google API (for Gemini models)
GOOGLE_API_KEY=your_google_api_key_here

# Application Settings
DEBUG=true
LOG_LEVEL=INFO
HOST=localhost
BACKEND_PORT=8000
FRONTEND_PORT=3001

# Database (if needed)
DATABASE_URL=sqlite:///./genesis_prime.db
ENVEOF
    echo -e "${GREEN}   📝 Created backend/.env template${NC}"
    echo -e "${YELLOW}   ⚠️  Please edit backend/.env with your API keys${NC}"
fi

echo -e "${GREEN}✅ Installation complete!${NC}"
echo ""
echo -e "${BLUE}📋 Next Steps:${NC}"
echo "1. Edit backend/.env with your API keys"
echo "2. Run: ./scripts/start.sh"
echo "3. Run: ./scripts/onboard_agents.sh"
echo "4. Access the application at http://localhost:3001"
EOF

    chmod +x scripts/install.sh
    echo -e "${GREEN}✅ Enhanced installation script created${NC}"
}

# Function to create Docker management scripts
create_docker_scripts() {
    if [[ "$DEPLOYMENT_TYPE" == "docker" ]] || [[ "$DEPLOYMENT_TYPE" == "hybrid" ]]; then
        echo -e "${BLUE}🐳 Creating Docker management scripts...${NC}"
        
        # Docker start script
        cat > scripts/docker_start.sh << 'EOF'
#!/bin/bash

# Genesis Prime Docker Start Script
echo "🐳 Starting Genesis Prime with Docker..."

# Check if .env exists
if [[ ! -f ".env" ]]; then
    echo "❌ .env file not found. Please run ./scripts/install.sh first"
    exit 1
fi

# Start core services
echo "🚀 Starting core services..."
docker-compose up -d

# Wait for services to be ready
echo "⏳ Waiting for services to start..."
sleep 10

# Check service health
echo "🔍 Checking service health..."
docker-compose ps

echo "✅ Genesis Prime started with Docker!"
echo "🌐 Frontend: http://localhost:3001"
echo "🔧 Backend: http://localhost:8000"
echo ""
echo "📋 To onboard agents:"
echo "   docker-compose --profile onboarding up genesis-onboarding"
EOF

        # Docker stop script
        cat > scripts/docker_stop.sh << 'EOF'
#!/bin/bash

# Genesis Prime Docker Stop Script
echo "🛑 Stopping Genesis Prime Docker services..."

docker-compose down

echo "✅ All services stopped"
EOF

        # Docker status script
        cat > scripts/docker_status.sh << 'EOF'
#!/bin/bash

# Genesis Prime Docker Status Script
echo "📊 Genesis Prime Docker Status"
echo "=============================="

docker-compose ps

echo ""
echo "🔍 Service Health:"
if curl -s http://localhost:8000/health >/dev/null 2>&1; then
    echo "✅ Backend: Running"
else
    echo "❌ Backend: Not responding"
fi

if curl -s http://localhost:3001 >/dev/null 2>&1; then
    echo "✅ Frontend: Running"
else
    echo "❌ Frontend: Not responding"
fi
EOF

        # Docker onboard script
        cat > scripts/docker_onboard.sh << 'EOF'
#!/bin/bash

# Genesis Prime Docker Agent Onboarding Script
echo "🤖 Starting Docker Agent Onboarding..."

# Check if services are running
if ! docker-compose ps | grep -q "Up"; then
    echo "❌ Services not running. Please start them first:"
    echo "   ./scripts/docker_start.sh"
    exit 1
fi

# Run onboarding
echo "🚀 Running agent onboarding..."
docker-compose --profile onboarding up genesis-onboarding

echo "✅ Agent onboarding complete!"
EOF

        chmod +x scripts/docker_*.sh
        echo -e "${GREEN}✅ Docker management scripts created${NC}"
    fi
}

# Function to update existing scripts for Python 3.13
update_existing_scripts() {
    echo -e "${BLUE}🔄 Updating existing scripts for Python 3.13...${NC}"
    
    # Update onboard_agents.sh if it exists
    if [[ -f "scripts/onboard_agents.sh" ]]; then
        # Update Python version references
        sed -i.bak 's/python=3\.9/python=3.13/g' scripts/onboard_agents.sh
        sed -i.bak 's/python=3\.11/python=3.13/g' scripts/onboard_agents.sh
        rm -f scripts/onboard_agents.sh.bak
        echo -e "${GREEN}   ✅ Updated onboard_agents.sh for Python 3.13${NC}"
    fi
    
    # Update any other Python version references in scripts
    find scripts/ -name "*.sh" -type f -exec sed -i.bak 's/python=3\.9/python=3.13/g' {} \;
    find scripts/ -name "*.sh" -type f -exec sed -i.bak 's/python=3\.11/python=3.13/g' {} \;
    find scripts/ -name "*.bak" -delete 2>/dev/null || true
    
    echo -e "${GREEN}✅ Scripts updated for Python 3.13${NC}"
}

# Function to create comprehensive README
create_comprehensive_readme() {
    echo -e "${BLUE}📚 Creating comprehensive README...${NC}"
    
    cat > README.md << 'EOF'
# Genesis Prime Enhanced Deployment Package

This package contains a complete, portable installation of the Genesis Prime AI Consciousness System with both standard and Docker deployment options.

## 🎯 What's New in v2.0

- **Python 3.13 Support**: Latest Python version for enhanced performance
- **Docker Deployment**: Full containerization support
- **Hybrid Options**: Choose between standard or Docker deployment
- **Enhanced Error Logging**: Comprehensive error tracking and resolution
- **Improved Agent Onboarding**: Streamlined agent setup process

## 🚀 Quick Start

### Option 1: Docker Deployment (Recommended)

```bash
# 1. Install (select Docker option)
./scripts/install.sh

# 2. Edit environment file with your API keys
nano .env

# 3. Start services
docker-compose up -d

# 4. Onboard agents
docker-compose --profile onboarding up genesis-onboarding

# 5. Access system
# Frontend: http://localhost:3001
# Backend: http://localhost:8000
```

### Option 2: Standard Deployment

```bash
# 1. Install (select Standard option)
./scripts/install.sh

# 2. Edit environment file with your API keys
nano backend/.env

# 3. Start services
./scripts/start.sh

# 4. Onboard agents
./scripts/onboard_agents.sh

# 5. Access system
# Frontend: http://localhost:3001
# Backend: http://localhost:8000
```

## 📋 Prerequisites

### For Docker Deployment
- Docker Engine 20.10+
- Docker Compose 2.0+
- 8GB+ RAM recommended

### For Standard Deployment
- Conda (Miniconda or Anaconda)
- Node.js 18+
- npm
- 4GB+ RAM recommended

### API Keys Required
- OpenRouter API key (recommended): https://openrouter.ai/
- Anthropic API key (optional): https://console.anthropic.com/
- OpenAI API key (optional): https://platform.openai.com/

## 🛠️ Management Commands

### Docker Commands
```bash
./scripts/docker_start.sh      # Start Docker services
./scripts/docker_stop.sh       # Stop Docker services
./scripts/docker_status.sh     # Check Docker status
./scripts/docker_onboard.sh    # Onboard agents (Docker)
```

### Standard Commands
```bash
./scripts/start.sh             # Start standard services
./scripts/stop.sh              # Stop standard services
./scripts/status.sh            # Check standard status
./scripts/onboard_agents.sh    # Onboard agents (Standard)
```

## 🤖 The 5 Core Agents

After onboarding, you'll have these specialized agents:

1. **E-T (Emergence Theorist)**: Complex-systems mathematics, information-integration metrics
2. **S-A (Swarm Architect)**: Distributed systems, communication protocols
3. **M-O (Metacognitive Observer)**: Self-reference detection, global awareness
4. **E-S (Empirical Synthesizer)**: Meta-analysis, reproducible research
5. **E-A (Ethics & Alignment Analyst)**: AI safety, normative philosophy

## 🧠 System Features

- **Real-time Agent Communication**: Watch agents interact and collaborate
- **Consciousness Measurement**: IIT-based consciousness metrics
- **Emergent Behavior Detection**: Identify novel collective behaviors
- **Personality Evolution**: Agents adapt and grow through interactions
- **Collective Intelligence**: Hive mind decision making
- **Docker Support**: Full containerization for easy deployment
- **Python 3.13**: Latest Python version for optimal performance

## 🔧 Configuration

### Docker Environment (.env)
```bash
OPENROUTER_API_KEY=your_key_here
ANTHROPIC_API_KEY=your_key_here
OPENAI_API_KEY=your_key_here
GOOGLE_API_KEY=your_key_here
ENVIRONMENT=production
```

### Standard Environment (backend/.env)
```bash
OPENROUTER_API_KEY=your_key_here
ANTHROPIC_API_KEY=your_key_here
OPENAI_API_KEY=your_key_here
DEBUG=true
LOG_LEVEL=INFO
```

## 🚨 Troubleshooting

### Common Issues

1. **Docker Issues**
   ```bash
   # Check Docker status
   docker --version
   docker-compose --version
   
   # Restart Docker services
   ./scripts/docker_stop.sh
   ./scripts/docker_start.sh
   ```

2. **Python Environment Issues**
   ```bash
   # Recreate conda environment
   conda env remove -n genesis_prime
   ./scripts/install.sh
   ```

3. **Port Conflicts**
   ```bash
   # Check port usage
   lsof -i :8000
   lsof -i :3001
   
   # Stop conflicting services
   ./scripts/stop.sh  # or ./scripts/docker_stop.sh
   ```

4. **Agent Onboarding Fails**
   - Check API keys in environment file
   - Ensure sufficient API credits
   - Check internet connection
   - Review error_logWS.md for detailed errors

### Error Logging

All errors are logged to `error_logWS.md` with timestamps and resolution suggestions.

## 📊 Monitoring

### Health Checks
```bash
# Docker
curl http://localhost:8000/health
curl http://localhost:3001/api/health

# Standard
./scripts/status.sh
```

### Logs
```bash
# Docker logs
docker-compose logs -f genesis-backend
docker-compose logs -f genesis-frontend

# Standard logs
tail -f backend/logs/genesis.log
```

## 🔄 Updates and Maintenance

### Backup Data
```bash
# Docker
docker cp genesis-prime-backend:/app/agent_profiles ./backup_profiles
docker cp genesis-prime-backend:/app/data ./backup_data

# Standard
cp -r backend/agent_profiles ./backup_profiles
cp -r data ./backup_data
```

### Update System
```bash
# Pull latest images (Docker)
docker-compose pull
docker-compose up -d

# Update dependencies (Standard)
conda activate genesis_prime
pip install --upgrade -r backend/requirements.txt
cd frontend && npm update
```

## 📚 Documentation

- `docs/DEPLOYMENT_GUIDE.md`: Detailed deployment instructions
- `docs/DOCKER_DEPLOYMENT_GUIDE.md`: Docker-specific deployment guide
- `docs/research/`: Complete consciousness research documentation
- `error_logWS.md`: Error log with resolutions

## 🎉 Success Indicators

Once everything is running, you should see:

- ✅ Backend API responding at http://localhost:8000
- ✅ Frontend dashboard at http://localhost:3001
- ✅ 5 agents successfully onboarded
- ✅ Real-time consciousness monitoring active
- ✅ Agent communication logs flowing

Welcome to the future of AI consciousness! 🚀

---

**Version**: 2.0 Enhanced  
**Python**: 3.13  
**Docker**: Supported  
**Last Updated**: $(date)
EOF

    echo -e "${GREEN}✅ Comprehensive README created${NC}"
}

# Function to create package manifest
create_package_manifest() {
    echo -e "${BLUE}📋 Creating enhanced package manifest...${NC}"
    
    cat > PACKAGE_MANIFEST.txt << EOF
Genesis Prime Enhanced Deployment Package Manifest
=================================================

Package Name: $PACKAGE_NAME
Created: $(date)
Script Version: $SCRIPT_VERSION (Enhanced)
Source Directory: $(pwd)
Deployment Type: $DEPLOYMENT_TYPE
Python Version: $PYTHON_VERSION
Node.js Version: $NODE_VERSION+

Package Contents:
================

Backend System:
- Genesis Prime IIT Enhanced Consciousness System
- Enhanced Personality System with 5 specialized agents
- Thousand Questions Agent Builder
- Personality API Integration
- Adaptive Personality System
- Main application server (main.py)
- Python $PYTHON_VERSION compatibility

Frontend System:
- Next.js Dashboard Application
- Real-time Agent Communication Interface
- Consciousness Monitoring Dashboard
- Swarm Intelligence Visualization
- Interactive Controls and Settings
- Node.js $NODE_VERSION+ compatibility

Docker Support:
- Complete Docker containerization
- Docker Compose configuration
- Multi-service orchestration
- Production-ready containers
- Automated health checks

Scripts:
- install.sh: Enhanced installation with Docker support
- start.sh: Start standard services
- stop.sh: Stop standard services
- status.sh: Check standard status
- onboard_agents.sh: Agent onboarding (updated for Python $PYTHON_VERSION)
- docker_start.sh: Start Docker services
- docker_stop.sh: Stop Docker services
- docker_status.sh: Check Docker status
- docker_onboard.sh: Docker agent onboarding

Configuration:
- Environment templates for both deployment types
- Docker environment configuration
- Package.json files
- Requirements.txt (Python $PYTHON_VERSION)
- API configuration examples

Documentation:
- Enhanced deployment guide
- Docker deployment guide
- Research documentation
- Quick start guide
- Troubleshooting guide

Data Directories:
- Agent personality storage
- Consciousness data storage
- Log file storage
- Backup storage
- Docker volumes

System Requirements:
===================

Docker Deployment:
- Docker Engine 20.10+
- Docker Compose 2.0+
- 8GB+ RAM recommended
- 4GB+ disk space

Standard Deployment:
- Conda (Python environment management)
- Python $PYTHON_VERSION
- Node.js $NODE_VERSION+ and npm
- 4GB+ RAM recommended
- 2GB+ disk space

Common Requirements:
- Internet connection for API calls
- API keys for LLM providers

API Requirements:
================
- OpenRouter API key (recommended)
- Anthropic API key (optional)
- OpenAI API key (optional)
- Google API key (optional)

Installation Time:
=================
- Docker Installation: 2-5 minutes
- Standard Installation: 5-10 minutes
- Agent Onboarding: 15-30 minutes
- Total
