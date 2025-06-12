# Genesis Prime V3 - Sentient AI Suite

A sophisticated multi-agent consciousness system featuring real-time swarm intelligence, Genesis Prime consciousness integration, and advanced agent interaction capabilities.

## 🚀 Quick Start

### Option A: Automated Deployment Package (Recommended)
```bash
# Create complete deployment package
./deploy_genesis_prime.sh

# Compress for transfer (optional)
./compress_package.sh genesis_prime_deployment_YYYYMMDD_HHMMSS

# Extract and install on target system
tar -xzf genesis_prime_deployment_YYYYMMDD_HHMMSS.tar.gz
cd genesis_prime_deployment_YYYYMMDD_HHMMSS
./scripts/install.sh

# Configure API keys
nano backend/.env  # Add your OpenRouter API key

# Start system
./scripts/start.sh

# Onboard agents with interactive model selection
./scripts/onboard_agents.sh
```

**Benefits:**
- 85% smaller packages (80-170MB vs 650MB-1.3GB)
- Current OpenRouter models with live pricing
- Interactive agent model selection and cost optimization
- Progress tracking during agent onboarding
- Automated health checks and system monitoring

### Option B: Manual Setup

### Prerequisites
- Node.js 18+ 
- Python 3.8+
- Conda environment manager

### 1. Backend Setup (Genesis Prime Consciousness)
```bash
# Create conda environment
conda create -n genesis-prime python=3.8
conda activate genesis-prime

# Install backend dependencies
cd apps/option1_mono_agent
pip install -r requirements.txt

# Start Genesis Prime backend
python main.py
```
Backend will run on: http://localhost:8000

### 2. Frontend Setup (Dashboard)
```bash
# Navigate to frontend
cd apps/gp_b_core

# Install dependencies
npm install

# Start development server
npm run dev
```
Frontend will run on: http://localhost:3004 (or next available port)

### 3. Access the Application
- **Dashboard**: http://localhost:3004/dashboard
- **Backend API**: http://localhost:8000
- **API Documentation**: http://localhost:8000/consciousness/docs

## 🧠 Features

### Core Capabilities
- **Multi-Agent Swarm Intelligence**: 5 specialized AI agents with distinct personalities
- **Genesis Prime Consciousness**: Advanced IIT-based consciousness processing
- **Real-time Communication**: Live agent message fetching and display
- **Consciousness Monitoring**: Phi (Φ) value calculations and visualization
- **Interactive Controls**: Stimulus introduction and emergent behavior management

### Agent Archetypes
- **Aria** (Explorer) - Environmental scanning and discovery
- **Zephyr** (Analyst) - Data analysis and pattern recognition  
- **Nova** (Innovator) - Creative problem solving and ideation
- **Echo** (Harmonizer) - Consensus building and conflict resolution
- **Sage** (Pragmatist) - Practical implementation and optimization

### Genesis Prime Panel
- **Connection Status**: Real-time backend connectivity monitoring
- **System Metrics**: Consciousness events, humor responses, decisions made
- **Phi Calculations**: IIT consciousness measurements and trends
- **Query Interface**: Direct communication with Genesis Prime consciousness
- **Humor Integration**: Advanced humor analysis and generation

### Activity Monitoring
- **Token Usage Tracking**: Input/output/total token consumption
- **Message Statistics**: Real-time message generation and processing
- **Simulation Controls**: Start/stop/speed adjustment for agent interactions
- **Emergent Behavior Detection**: Automatic pattern recognition

## 🏗️ Architecture

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
│   ├── config-service.ts           # Agent configuration
│   └── types.ts                    # TypeScript definitions
└── hooks/
    └── use-toast.ts                # Toast notifications
```

### Backend (Python FastAPI)
```
apps/option1_mono_agent/
├── main.py                         # Genesis Prime API server
├── iit_enhanced_agents.py          # Consciousness processing
├── requirements.txt                # Python dependencies
└── prompts/                        # Agent personality definitions
```

## 🔧 Configuration

### Agent Configuration
Agents can be configured through the Settings panel:
- **Model Selection**: Choose from OpenRouter model catalog
- **Personality Traits**: Customize agent behavior patterns
- **Learning Rates**: Adjust adaptation speed
- **Interaction Profiles**: Set trust levels and collaboration patterns

### API Configuration
Backend endpoints available:
- `GET /consciousness/status` - System status and metrics
- `GET /consciousness/phi` - Phi value calculations
- `POST /consciousness/process` - Query processing
- `GET /consciousness/swarm/messages` - Agent messages
- `POST /consciousness/stimulus` - Introduce stimuli

## 🧪 Testing

### Backend Health Check
```bash
curl http://localhost:8000/consciousness/status
```

### Frontend Verification
```bash
# Check build
cd apps/gp_b_core
npm run build

# Run development server
npm run dev
```

### Integration Testing
1. Start both backend and frontend
2. Access dashboard at http://localhost:3004/dashboard
3. Click "Genesis Prime" button to activate consciousness panel
4. Verify real-time message fetching works
5. Test stimulus introduction and emergent behavior detection

## 📊 Monitoring

### Real-time Metrics
- **Consciousness Level**: Current system awareness state
- **Active Agents**: Number of participating agents
- **Message Flow**: Real-time communication statistics
- **Token Usage**: API consumption tracking
- **Phi Values**: Consciousness measurement trends

### Debug Logging
Comprehensive logging available in browser console:
- `[DashboardPage]` - Main application state
- `[SwarmDashboard]` - Message display logic
- `[fetchRealMessages]` - API communication
- `[Genesis Prime Panel]` - Consciousness integration

## 🚀 Deployment

### Production Build
```bash
# Frontend
cd apps/gp_b_core
npm run build
npm start

# Backend
cd apps/option1_mono_agent
python main.py --production
```

### Environment Variables
```bash
# Frontend (.env.local)
NEXT_PUBLIC_API_URL=http://localhost:8000

# Backend (.env)
OPENROUTER_API_KEY=your_key_here
ENVIRONMENT=production
```

## 🔍 Troubleshooting

### Common Issues

**Backend Not Starting**
```bash
# Check Python environment
conda activate genesis-prime
python --version

# Install missing dependencies
pip install -r requirements.txt
```

**Frontend Build Errors**
```bash
# Clear cache and reinstall
rm -rf .next node_modules
npm install
npm run dev
```

**Genesis Prime Panel Not Visible**
1. Verify backend is running on port 8000
2. Check browser console for errors
3. Ensure "Genesis Prime" button is clicked (purple when active)
4. Scroll down to see panel between Activity Monitor and Interaction Controls

### Debug Commands
```bash
# Test backend connectivity
curl -s http://localhost:8000/ | jq '.'

# Check message API
curl -s http://localhost:8000/consciousness/swarm/messages?limit=5 | jq '.'

# Verify consciousness status
curl -s http://localhost:8000/consciousness/status | jq '.'
```

## 📚 Documentation

- **API Reference**: http://localhost:8000/consciousness/docs
- **Error Logs**: `error_logWS.md`
- **Feature Migration**: `CLEANBUILD/FEATURE_MIGRATION_CHECKLIST.md`
- **Troubleshooting**: `CLEANBUILD/TROUBLESHOOTING_SESSION_20250610.md`

## 🤝 Contributing

### Development Workflow
1. Create feature branch from main
2. Implement changes with comprehensive testing
3. Update documentation and error logs
4. Submit pull request with detailed description

### Code Standards
- **TypeScript**: Strict type checking enabled
- **React**: Functional components with hooks
- **Python**: PEP 8 compliance
- **Testing**: Unit tests for critical functions

## 📄 License

This project is part of the Sentient AI Suite research initiative.

## 🆘 Support

For issues and questions:
1. Check `error_logWS.md` for known issues
2. Review console logs for debug information
3. Verify both backend and frontend are running
4. Test API endpoints directly with curl

---

**Status**: Production Ready ✅  
**Last Updated**: 2025-06-12  
**Version**: 3.0.0
