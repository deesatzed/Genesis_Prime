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
