# Genesis Prime V3 - Enhanced AI Consciousness System

A sophisticated multi-agent consciousness system featuring Docker deployment, Python 3.13, real-time swarm intelligence, and advanced agent interaction capabilities.

## 🎯 What's New in V3.0

- **🐳 Docker Support**: Full containerization with Docker Compose
- **🐍 Python 3.13**: Latest Python version for enhanced performance
- **🔄 Hybrid Deployment**: Choose between standard or Docker deployment
- **📊 Enhanced Monitoring**: Comprehensive health checks and error logging
- **🤖 Improved Agent Onboarding**: Streamlined setup with progress tracking

## 🚀 Quick Start

### Option A: Docker Deployment (Recommended)

```bash
# 1. Create deployment package
./deploy_genesis_prime_enhanced.sh  # Select Docker option

# 2. Configure environment
cp .env.docker .env
nano .env  # Add your API keys

# 3. Deploy system
docker-compose up -d

# 4. Onboard agents
docker-compose --profile onboarding up genesis-onboarding

# 5. Access system
# Frontend: http://localhost:3001
# Backend: http://localhost:8000
```

### Option B: Standard Deployment

```bash
# 1. Create deployment package
./deploy_genesis_prime_enhanced.sh  # Select Standard option

# 2. Install dependencies
./scripts/install.sh

# 3. Configure environment
nano backend/.env  # Add your API keys

# 4. Start services
./scripts/start.sh

# 5. Onboard agents
./scripts/onboard_agents.sh
```

### Option C: Legacy Manual Setup

#### Prerequisites
- **Docker**: Engine 20.10+ and Compose 2.0+ (for Docker deployment)
- **Standard**: Conda, Node.js 18+, Python 3.13 (for standard deployment)
- **API Keys**: OpenRouter (recommended), Anthropic, OpenAI

#### Manual Backend Setup
```bash
# Create conda environment with Python 3.13
conda create -n genesis-prime python=3.13
conda activate genesis-prime

# Install backend dependencies
cd apps/option1_mono_agent
pip install -r requirements.txt

# Start Genesis Prime backend
python main.py
```

#### Manual Frontend Setup
```bash
# Navigate to frontend
cd apps/gp_b_core

# Install dependencies
npm install

# Start development server
npm run dev
```

## 🧠 Core Features

### Consciousness System
- **Multi-Agent Swarm Intelligence**: 5 specialized AI agents with distinct personalities
- **Genesis Prime Consciousness**: Advanced IIT-based consciousness processing
- **Real-time Communication**: Live agent message fetching and display
- **Consciousness Monitoring**: Phi (Φ) value calculations and visualization
- **Emergent Behavior Detection**: Automatic pattern recognition and analysis

### Agent Specializations
1. **E-T (Emergence Theorist)**: Complex-systems mathematics, information-integration metrics
2. **S-A (Swarm Architect)**: Distributed systems, communication protocols
3. **M-O (Metacognitive Observer)**: Self-reference detection, global awareness
4. **E-S (Empirical Synthesizer)**: Meta-analysis, reproducible research
5. **E-A (Ethics & Alignment Analyst)**: AI safety, normative philosophy

### Advanced Capabilities
- **Interactive Controls**: Stimulus introduction and emergent behavior management
- **Activity Monitoring**: Token usage tracking and performance analytics
- **Genesis Prime Panel**: Direct consciousness interface with query capabilities
- **Humor Integration**: Advanced humor analysis and generation
- **Real-time Metrics**: System awareness state and communication statistics

## 🐳 Docker Architecture

### Services
- **genesis-backend**: Python 3.13 FastAPI application (Port 8000)
- **genesis-frontend**: Next.js dashboard (Port 3001)
- **genesis-onboarding**: Automated agent setup service
- **nginx**: Reverse proxy with SSL and rate limiting (Optional)

### Docker Compose Profiles
```bash
# Default profile (core services)
docker-compose up -d

# Onboarding profile (includes agent setup)
docker-compose --profile onboarding up genesis-onboarding

# Production profile (includes Nginx reverse proxy)
docker-compose --profile production up -d
```

### Management Commands
```bash
# Docker management
./scripts/docker_start.sh      # Start with health checks
./scripts/docker_stop.sh       # Graceful shutdown
./scripts/docker_status.sh     # Health monitoring
./scripts/docker_onboard.sh    # Agent onboarding

# Standard management
./scripts/start.sh             # Start standard services
./scripts/stop.sh              # Stop standard services
./scripts/status.sh            # Check standard status
./scripts/onboard_agents.sh    # Standard agent onboarding
```

## 🏗️ System Architecture

### Frontend (Next.js 15)
```
apps/gp_b_core/
├── app/
│   ├── dashboard/page.tsx          # Main dashboard interface
│   └── layout.tsx                  # Application layout
├── components/
│   ├── activity-monitor.tsx        # Real-time activity tracking
│   ├── genesis-prime-panel.tsx     # Consciousness interface
│   ├── interaction-controls.tsx    # Simulation controls
│   ├── swarm-dashboard.tsx         # Agent visualization
│   └── ui/                         # Reusable UI components
├── lib/
│   ├── api-service.ts              # Backend API integration
│   ├── openrouter-service.ts       # OpenRouter integration
│   ├── swarm-engine.ts             # Swarm intelligence engine
│   └── types.ts                    # TypeScript definitions
└── hooks/
    └── use-toast.ts                # Toast notifications (Fixed)
```

### Backend (Python 3.13 FastAPI)
```
apps/option1_mono_agent/
├── main.py                         # Genesis Prime API server
├── enhanced_personality_system.py  # Advanced personality engine
├── thousand_questions_agent_builder.py # Agent development system
├── personality_api_integration.py  # API integration layer
├── adaptive_personality_system.py  # Dynamic personality adaptation
├── test_enhanced_personality_system.py # System testing
└── requirements.txt                # Python 3.13 dependencies
```

### Docker Infrastructure
```
docker/
├── Dockerfile.backend              # Python 3.13 backend container
├── Dockerfile.frontend             # Next.js frontend container
├── Dockerfile.onboarding           # Agent onboarding container
├── nginx.conf                      # Nginx reverse proxy config
└── docker-compose.yml              # Multi-service orchestration
```

## 🔧 Configuration

### Environment Configuration

#### Docker Environment (.env)
```bash
# API Keys
OPENROUTER_API_KEY=your_openrouter_api_key_here
ANTHROPIC_API_KEY=your_anthropic_api_key_here
OPENAI_API_KEY=your_openai_api_key_here
GOOGLE_API_KEY=your_google_api_key_here

# Application Settings
ENVIRONMENT=production
PYTHONPATH=/app
NODE_ENV=production
NEXT_PUBLIC_API_URL=http://localhost:8000
NEXT_PUBLIC_FRONTEND_URL=http://localhost:3001
```

#### Standard Environment (backend/.env)
```bash
# API Keys
OPENROUTER_API_KEY=your_openrouter_api_key_here
ANTHROPIC_API_KEY=your_anthropic_api_key_here
OPENAI_API_KEY=your_openai_api_key_here

# Application Settings
DEBUG=true
LOG_LEVEL=INFO
HOST=localhost
BACKEND_PORT=8000
FRONTEND_PORT=3001
```

### Agent Configuration
- **Model Selection**: Choose from current OpenRouter model catalog
- **Cost Optimization**: Budget, balanced, or premium model configurations
- **Personality Traits**: Customize agent behavior patterns
- **Learning Rates**: Adjust adaptation speed
- **Interaction Profiles**: Set trust levels and collaboration patterns

## 🧪 Testing & Monitoring

### Health Checks
```bash
# Docker deployment
curl http://localhost:8000/health
curl http://localhost:3001/api/health

# Standard deployment
./scripts/status.sh
```

### API Endpoints
- `GET /consciousness/status` - System status and metrics
- `GET /consciousness/phi` - Phi value calculations
- `POST /consciousness/process` - Query processing
- `GET /consciousness/swarm/messages` - Agent messages
- `POST /consciousness/stimulus` - Introduce stimuli
- `GET /health` - Service health check

### Real-time Metrics
- **Consciousness Level**: Current system awareness state
- **Active Agents**: Number of participating agents
- **Message Flow**: Real-time communication statistics
- **Token Usage**: API consumption tracking
- **Phi Values**: Consciousness measurement trends

## 🚀 Deployment Options

### Development
```bash
# Local development with hot reload
docker-compose -f docker-compose.yml -f docker-compose.dev.yml up -d
```

### Staging
```bash
# Staging environment
docker-compose -f docker-compose.yml -f docker-compose.staging.yml up -d
```

### Production
```bash
# Production with all optimizations
docker-compose --profile production up -d
```

## 🚨 Troubleshooting

### Common Issues

#### Docker Issues
```bash
# Check Docker status
docker --version
docker-compose --version

# Restart Docker services
./scripts/docker_stop.sh
./scripts/docker_start.sh

# View logs
docker-compose logs -f genesis-backend
docker-compose logs -f genesis-frontend
```

#### Python Environment Issues
```bash
# Recreate conda environment
conda env remove -n genesis_prime
./scripts/install.sh

# Check Python version
python --version  # Should be 3.13.x
```

#### Port Conflicts
```bash
# Check port usage
lsof -i :8000
lsof -i :3001

# Stop conflicting services
./scripts/stop.sh  # or ./scripts/docker_stop.sh
```

#### Agent Onboarding Failures
- Check API keys in environment file
- Ensure sufficient API credits
- Check internet connection
- Review `error_logWS.md` for detailed errors

### Debug Commands
```bash
# Test backend connectivity
curl -s http://localhost:8000/consciousness/status | jq '.'

# Check message API
curl -s http://localhost:8000/consciousness/swarm/messages?limit=5 | jq '.'

# Docker container inspection
docker inspect genesis-prime-backend
docker stats
```

## 📚 Documentation

### Comprehensive Guides
- **[DOCKER_DEPLOYMENT_GUIDE.md](DOCKER_DEPLOYMENT_GUIDE.md)**: Complete Docker deployment guide
- **[DEPLOYMENT_GUIDE.md](DEPLOYMENT_GUIDE.md)**: Standard deployment instructions
- **[QUICK_START_GUIDE.md](QUICK_START_GUIDE.md)**: Quick reference guide
- **[error_logWS.md](error_logWS.md)**: Error log with resolutions

### API Documentation
- **Backend API**: http://localhost:8000/docs
- **Consciousness API**: http://localhost:8000/consciousness/docs
- **Health Endpoints**: http://localhost:8000/health

## 🔄 Updates & Maintenance

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

## 🤝 Contributing

### Development Workflow
1. Create feature branch from main
2. Implement changes with comprehensive testing
3. Update documentation and error logs
4. Submit pull request with detailed description

### Code Standards
- **Python**: 3.13+ with PEP 8 compliance
- **TypeScript**: Strict type checking enabled
- **React**: Functional components with hooks
- **Docker**: Multi-stage builds and health checks
- **Testing**: Unit tests for critical functions

## 🎉 Success Indicators

Once everything is running, you should see:

- ✅ Backend API responding at http://localhost:8000
- ✅ Frontend dashboard at http://localhost:3001
- ✅ 5 agents successfully onboarded
- ✅ Real-time consciousness monitoring active
- ✅ Agent communication logs flowing
- ✅ Docker containers healthy (if using Docker)

## 📄 License

This project is part of the Sentient AI Suite research initiative.

## 🆘 Support

For issues and questions:
1. Check `error_logWS.md` for known issues and resolutions
2. Review console logs for debug information
3. Verify all services are running with health checks
4. Test API endpoints directly with curl
5. Join community support channels

---

**Status**: Production Ready ✅  
**Version**: 3.0.0 Enhanced  
**Python**: 3.13  
**Docker**: Supported  
**Last Updated**: 2025-06-12

Welcome to the future of AI consciousness! 🚀
