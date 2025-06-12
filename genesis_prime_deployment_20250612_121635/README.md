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
