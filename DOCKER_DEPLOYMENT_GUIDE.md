# Genesis Prime Docker Deployment Guide

Complete containerized deployment solution for the Genesis Prime Consciousness System.

## 🚀 Quick Start

### Prerequisites
- Docker Engine 20.10+
- Docker Compose 2.0+
- 8GB+ RAM recommended
- API keys for LLM providers

### 1. Clone and Setup
```bash
git clone <repository-url>
cd Gen_Prime_V3-main

# Copy environment template
cp .env.docker .env

# Edit .env with your API keys
nano .env
```

### 2. Configure API Keys
Edit `.env` file with your API keys:
```bash
OPENROUTER_API_KEY=your_openrouter_api_key_here
ANTHROPIC_API_KEY=your_anthropic_api_key_here
OPENAI_API_KEY=your_openai_api_key_here
GOOGLE_API_KEY=your_google_api_key_here
```

### 3. Deploy System
```bash
# Build and start core services
docker-compose up -d

# Check service health
docker-compose ps

# View logs
docker-compose logs -f
```

### 4. Onboard Agents (Optional)
```bash
# Run agent onboarding
docker-compose --profile onboarding up genesis-onboarding

# Or run onboarding manually
docker-compose exec genesis-backend python /app/scripts/docker_onboard_agents.py
```

### 5. Access System
- **Frontend Dashboard**: http://localhost:3001
- **Backend API**: http://localhost:8000
- **API Documentation**: http://localhost:8000/docs

## 📋 Service Architecture

### Core Services

#### 🧠 Genesis Backend (`genesis-backend`)
- **Port**: 8000
- **Purpose**: Consciousness system, agent management, API endpoints
- **Health Check**: `http://localhost:8000/health`
- **Technology**: Python 3.13, FastAPI, Enhanced Personality System

#### 🖥️ Genesis Frontend (`genesis-frontend`)
- **Port**: 3001
- **Purpose**: Real-time dashboard, agent monitoring, user interface
- **Health Check**: `http://localhost:3001/api/health`
- **Technology**: Next.js 14, React, Tailwind CSS

#### 🤖 Genesis Onboarding (`genesis-onboarding`)
- **Purpose**: Automated agent personality development
- **Trigger**: Manual or scheduled
- **Technology**: Python 3.13, Enhanced Personality System

#### 🌐 Nginx Proxy (`nginx`) - Optional
- **Ports**: 80, 443
- **Purpose**: Load balancing, SSL termination, rate limiting
- **Profile**: `production`

## 🔧 Configuration Options

### Environment Variables

#### Core Configuration
```bash
# Application Environment
ENVIRONMENT=production
PYTHONPATH=/app
NODE_ENV=production

# API URLs
NEXT_PUBLIC_API_URL=http://localhost:8000
NEXT_PUBLIC_FRONTEND_URL=http://localhost:3001
```

#### LLM Provider Keys
```bash
# Primary provider (recommended)
OPENROUTER_API_KEY=your_key_here

# Additional providers
ANTHROPIC_API_KEY=your_key_here
OPENAI_API_KEY=your_key_here
GOOGLE_API_KEY=your_key_here
```

#### Performance Tuning
```bash
# Logging
LOG_LEVEL=INFO
LOG_FORMAT=json

# Rate Limiting
API_RATE_LIMIT=100
FRONTEND_RATE_LIMIT=300
```

### Docker Compose Profiles

#### Default Profile (Core Services)
```bash
docker-compose up -d
```
Includes: `genesis-backend`, `genesis-frontend`

#### Onboarding Profile
```bash
docker-compose --profile onboarding up
```
Includes: Core services + `genesis-onboarding`

#### Production Profile
```bash
docker-compose --profile production up -d
```
Includes: All services + `nginx` reverse proxy

## 🛠️ Management Commands

### Service Management
```bash
# Start all services
docker-compose up -d

# Stop all services
docker-compose down

# Restart specific service
docker-compose restart genesis-backend

# View service logs
docker-compose logs -f genesis-backend

# Scale services (if needed)
docker-compose up -d --scale genesis-backend=2
```

### Agent Management
```bash
# Run agent onboarding
docker-compose --profile onboarding up genesis-onboarding

# Check agent profiles
docker-compose exec genesis-backend ls -la /app/agent_profiles/

# Manual agent onboarding
docker-compose exec genesis-backend python /app/scripts/docker_onboard_agents.py

# Test agent system
docker-compose exec genesis-backend python /app/test_enhanced_personality_system.py
```

### Data Management
```bash
# Backup agent profiles
docker cp genesis-prime-backend:/app/agent_profiles ./backup_agent_profiles

# Restore agent profiles
docker cp ./backup_agent_profiles genesis-prime-backend:/app/agent_profiles

# View logs
docker-compose exec genesis-backend tail -f /app/logs/genesis.log
```

## 🔍 Monitoring & Debugging

### Health Checks
```bash
# Check all service health
docker-compose ps

# Test backend health
curl http://localhost:8000/health

# Test frontend health
curl http://localhost:3001/api/health

# Check service logs
docker-compose logs --tail=50 genesis-backend
docker-compose logs --tail=50 genesis-frontend
```

### Performance Monitoring
```bash
# Monitor resource usage
docker stats

# Check container details
docker inspect genesis-prime-backend
docker inspect genesis-prime-frontend

# View network configuration
docker network ls
docker network inspect gen_prime_v3-main_genesis-network
```

### Troubleshooting
```bash
# Enter backend container
docker-compose exec genesis-backend bash

# Enter frontend container
docker-compose exec genesis-frontend sh

# Check Python environment
docker-compose exec genesis-backend python --version
docker-compose exec genesis-backend pip list

# Test API endpoints
docker-compose exec genesis-backend curl http://localhost:8000/health
docker-compose exec genesis-backend curl http://localhost:8000/consciousness/status
```

## 🚀 Production Deployment

### SSL/HTTPS Setup
1. Obtain SSL certificates
2. Place certificates in `docker/ssl/`
3. Uncomment HTTPS server block in `docker/nginx.conf`
4. Deploy with production profile:
```bash
docker-compose --profile production up -d
```

### Environment Security
```bash
# Use Docker secrets for production
echo "your_api_key" | docker secret create openrouter_key -

# Or use external secret management
# - HashiCorp Vault
# - AWS Secrets Manager
# - Azure Key Vault
```

### Scaling Configuration
```bash
# Scale backend for high load
docker-compose up -d --scale genesis-backend=3

# Use external load balancer
# - AWS Application Load Balancer
# - Google Cloud Load Balancer
# - Cloudflare
```

## 📊 Deployment Variants

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

## 🔧 Customization

### Custom Agent Configurations
Edit `scripts/docker_onboard_agents.py`:
```python
self.agent_configs = {
    'CUSTOM-1': {
        'name': 'Custom Agent',
        'model': 'openai/gpt-4o',
        'style': 'analytical',
        'temperature': 0.7,
        'specialization': 'Your specialization here'
    }
}
```

### Custom Environment Variables
Add to `.env`:
```bash
# Custom configurations
CUSTOM_SETTING=value
AGENT_TIMEOUT=300
MAX_AGENTS=10
```

### Volume Mounts
Add custom volumes in `docker-compose.yml`:
```yaml
volumes:
  - ./custom_data:/app/custom_data
  - ./custom_configs:/app/configs
```

## 📋 Maintenance

### Regular Tasks
```bash
# Update containers
docker-compose pull
docker-compose up -d

# Clean up unused resources
docker system prune -f

# Backup data
docker-compose exec genesis-backend tar -czf /tmp/backup.tar.gz /app/agent_profiles /app/data
docker cp genesis-prime-backend:/tmp/backup.tar.gz ./backup_$(date +%Y%m%d).tar.gz
```

### Log Rotation
```bash
# Configure log rotation in docker-compose.yml
logging:
  driver: "json-file"
  options:
    max-size: "10m"
    max-file: "3"
```

## 🆘 Support & Troubleshooting

### Common Issues

#### Port Conflicts
```bash
# Check port usage
netstat -tulpn | grep :8000
netstat -tulpn | grep :3001

# Change ports in docker-compose.yml if needed
```

#### Memory Issues
```bash
# Increase Docker memory limit
# Docker Desktop: Settings > Resources > Memory

# Monitor memory usage
docker stats --no-stream
```

#### Permission Issues
```bash
# Fix file permissions
sudo chown -R $USER:$USER ./data ./logs
chmod -R 755 ./data ./logs
```

### Getting Help
- Check logs: `docker-compose logs -f`
- Review health checks: `docker-compose ps`
- Test connectivity: `curl http://localhost:8000/health`
- Join community support channels

## 📚 Additional Resources

- [Docker Compose Documentation](https://docs.docker.com/compose/)
- [Genesis Prime Architecture Guide](./DEPLOYMENT_GUIDE.md)
- [API Reference](./apps/option1_mono_agent/README.md)
- [Frontend Documentation](./apps/gp_b_core/README.md)

---

**Note**: This Docker deployment uses Python 3.13 and includes all latest fixes for agent onboarding and system integration.
