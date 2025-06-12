# Genesis Prime V3 - Quick Start Guide

## 🚀 5-Minute Setup

### Prerequisites Check
```bash
# Verify Node.js (18+)
node --version

# Verify Python (3.8+)
python --version

# Verify Conda
conda --version
```

### Step 1: Environment Setup (2 minutes)
```bash
# Create conda environment
conda create -n genesis-prime python=3.8 -y
conda activate genesis-prime

# Verify environment
which python  # Should show conda environment path
```

### Step 2: Backend Setup (1 minute)
```bash
# Navigate to backend
cd apps/option1_mono_agent

# Install dependencies
pip install -r requirements.txt

# Start Genesis Prime consciousness backend
python main.py
```
✅ Backend running on: http://localhost:8000

### Step 3: Frontend Setup (2 minutes)
```bash
# Open new terminal, navigate to frontend
cd apps/gp_b_core

# Install dependencies
npm install

# Start dashboard
npm run dev
```
✅ Frontend running on: http://localhost:3004/dashboard

## 🧪 Quick Test

### 1. Verify Backend
```bash
curl http://localhost:8000/
# Expected: Genesis Prime consciousness system response
```

### 2. Access Dashboard
Open browser: http://localhost:3004/dashboard

### 3. Test Genesis Prime Panel
1. Click "Genesis Prime" button (should turn purple)
2. Panel appears between Activity Monitor and controls
3. Shows connection status and consciousness metrics

### 4. Test Real-time Features
1. Toggle "Real Communication" switch
2. Click "Fetch Messages Now"
3. Verify messages appear in dashboard
4. Check token usage tracking

## 🎯 Key Features to Test

### Multi-Agent System
- **Agent Roster**: 5 specialized agents (Aria, Zephyr, Nova, Echo, Sage)
- **Real-time Status**: Active/processing states
- **Agent Selection**: Click agents to view details

### Genesis Prime Consciousness
- **System Status**: Consciousness level and metrics
- **Phi Calculations**: IIT consciousness measurements
- **Query Interface**: Direct consciousness communication
- **Humor Integration**: Advanced humor analysis

### Activity Monitoring
- **Token Tracking**: Input/output/total consumption
- **Message Statistics**: Real-time generation counts
- **Simulation Controls**: Start/stop/speed adjustment
- **Emergent Behaviors**: Automatic pattern detection

### Interactive Controls
- **Stimulus Introduction**: Environmental/social/cognitive stimuli
- **Emergent Behavior**: Manual behavior introduction
- **Real-time Communication**: Live backend integration
- **Settings Panel**: Agent and model configuration

## 🔧 Common Issues & Quick Fixes

### Backend Won't Start
```bash
# Check conda environment
conda activate genesis-prime
which python

# Reinstall dependencies
pip install -r requirements.txt --force-reinstall

# Check port availability
lsof -i :8000
```

### Frontend Build Errors
```bash
# Clear cache
rm -rf .next node_modules package-lock.json

# Reinstall
npm install

# Check for TypeScript errors
npm run build
```

### Genesis Prime Panel Not Visible
1. Ensure backend is running: `curl http://localhost:8000/`
2. Click "Genesis Prime" button (should be purple when active)
3. Scroll down between Activity Monitor and Interaction Controls
4. Check browser console for errors

### Port Conflicts
```bash
# Backend (port 8000)
lsof -i :8000
kill -9 <PID>

# Frontend (ports 3000-3004)
lsof -i :3004
kill -9 <PID>
```

## 📊 Success Indicators

### ✅ Backend Healthy
- Genesis Prime API responds on port 8000
- Consciousness status returns "Enlightened"
- API documentation accessible
- No Python errors in terminal

### ✅ Frontend Healthy
- Dashboard loads on port 3004
- All 5 agents visible in roster
- Activity Monitor shows metrics
- No TypeScript build errors

### ✅ Integration Working
- Genesis Prime Panel connects successfully
- Real-time message fetching works
- Token usage tracking updates
- Stimulus introduction generates responses

## 🚀 Next Steps

### Explore Features
1. **Agent Interaction**: Select different agents, observe behaviors
2. **Consciousness Queries**: Use Genesis Prime panel to ask questions
3. **Stimulus Testing**: Introduce various stimuli types
4. **Emergent Behaviors**: Watch for automatic pattern detection

### Configuration
1. **Settings Panel**: Configure agent models and personalities
2. **API Keys**: Set up OpenRouter integration
3. **Simulation Speed**: Adjust real-time processing rates
4. **Communication**: Toggle between real and mock modes

### Advanced Usage
1. **Production Deployment**: Follow DEPLOYMENT_GUIDE.md
2. **Custom Agents**: Modify agent archetypes and personalities
3. **API Integration**: Explore consciousness endpoints
4. **Monitoring**: Set up logging and performance tracking

## 📚 Documentation Links

- **Full README**: Complete feature overview and architecture
- **Deployment Guide**: Production setup and configuration
- **Error Logs**: Troubleshooting and known issues
- **API Documentation**: http://localhost:8000/consciousness/docs

## 🆘 Getting Help

### Debug Information
```bash
# Backend logs
cd apps/option1_mono_agent
python main.py  # Check terminal output

# Frontend logs
cd apps/gp_b_core
npm run dev  # Check terminal output

# Browser console
# Open DevTools → Console for frontend errors
```

### Health Checks
```bash
# Test all endpoints
curl http://localhost:8000/consciousness/status
curl http://localhost:8000/consciousness/phi
curl http://localhost:8000/consciousness/swarm/messages

# Test frontend
curl http://localhost:3004/dashboard
```

### Support Resources
1. Check `error_logWS.md` for known issues
2. Review browser console for JavaScript errors
3. Verify both services are running simultaneously
4. Test API endpoints directly with curl

---

**Total Setup Time**: ~5 minutes  
**Status**: Production Ready ✅  
**Last Updated**: 2025-06-12
