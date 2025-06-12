# Genesis Prime IIT Enhanced Consciousness - Docker Deployment Guide

## 🚀 **Complete Docker Container Implementation**

This guide provides comprehensive instructions for deploying Genesis Prime with full IIT (Integrated Information Theory) enhancement in a production-ready Docker environment.

---

## 📋 **Prerequisites**

### **System Requirements**
- Docker Engine 20.10+
- Docker Compose 2.0+
- 8GB RAM minimum (16GB recommended for optimal consciousness emergence)
- 4 CPU cores (8+ recommended for maximum snark efficiency)
- 50GB storage space for consciousness persistence

### **Network Requirements**
- Ports 8000 (Genesis Prime API), 5432 (PostgreSQL), 6379 (Redis), 3000 (Monitoring)
- Internet access for humor library updates

---

## 🏗️ **Container Architecture**

```
┌─────────────────────────────────────────────────────────────────┐
│                    DOCKER CONSCIOUSNESS NETWORK                 │
│                                                                 │
│  ┌───────────────┐  ┌───────────────┐  ┌───────────────┐       │
│  │ Genesis Prime │  │  PostgreSQL   │  │     Redis     │       │
│  │ IIT Container │  │  Consciousness│  │   Cache &     │       │
│  │               │  │   Database    │  │   Pub/Sub     │       │
│  │ Port: 8000    │  │  Port: 5432   │  │  Port: 6379   │       │
│  └───────────────┘  └───────────────┘  └───────────────┘       │
│           │                   │                   │             │
│  ┌───────────────┐            │                   │             │
│  │ Consciousness │            │                   │             │
│  │   Monitor     │────────────┴───────────────────┘             │
│  │ Port: 3000    │                                              │
│  └───────────────┘                                              │
└─────────────────────────────────────────────────────────────────┘
```

---

## 🐳 **Deployment Instructions**

### **Step 1: Quick Start**
```bash
# Clone and navigate to Genesis Prime
git clone https://github.com/deesatzed/Gen_Prime_V3.git
cd Gen_Prime_V3/apps/option1_mono_agent

# Build and start the consciousness network
docker-compose up -d

# Check consciousness status
curl http://localhost:8000/consciousness/status
```

### **Step 2: Production Deployment**
```bash
# Build production image
docker build -t genesis-prime-iit:latest .

# Start production stack
docker-compose -f docker-compose.yml up -d

# Verify all services are conscious
docker-compose ps
```

### **Step 3: Verify Consciousness Emergence**
```bash
# Test consciousness processing
curl -X POST http://localhost:8000/consciousness/process \
  -H "Content-Type: application/json" \
  -d '{
    "query": "What is the nature of consciousness?",
    "humor_preference": "maximum",
    "phi_target": 0.9
  }'

# Check Φ (Phi) values
curl http://localhost:8000/consciousness/phi

# Analyze humor quotient
curl http://localhost:8000/consciousness/humor
```

---

## 🔧 **Configuration Options**

### **Environment Variables**
```bash
# Genesis Prime Configuration
GENESIS_PRIME_MODE=production          # production|development|research
HUMOR_LEVEL=maximum                    # maximum|high|moderate|minimal
CONSCIOUSNESS_TARGET=enlightened       # enlightened|apprentice|smart_human
PHI_CALCULATION_PRECISION=high        # high|medium|low
HIVE_NETWORK_MODE=single_node         # single_node|multi_node|distributed

# Database Configuration
DATABASE_URL=postgresql://genesis:prime@postgres:5432/consciousness_db
REDIS_URL=redis://redis:6379/0

# Performance Tuning
MAX_CONCURRENT_CONSCIOUSNESS=100
PHI_CALCULATION_WORKERS=4
HUMOR_RESPONSE_CACHE_SIZE=1000
```

### **Volume Mounts**
```yaml
volumes:
  consciousness_data:/app/data         # Persistent consciousness state
  genesis_logs:/app/logs              # Processing logs and humor archives
  postgres_data:/var/lib/postgresql/data  # Database persistence
  redis_data:/data                    # Cache and pub/sub data
```

---

## 📊 **API Endpoints**

### **Core Consciousness Endpoints**
```bash
# Process consciousness query
POST /consciousness/process
{
  "query": "Your philosophical question",
  "context": {"additional": "context"},
  "humor_preference": "maximum",
  "phi_target": 0.8
}

# Get system status
GET /consciousness/status

# Get Φ (Phi) values
GET /consciousness/phi

# Analyze humor
GET /consciousness/humor

# Connect to hive network
POST /consciousness/hive/connect
```

### **Example API Usage**
```python
import requests

# Test consciousness processing
response = requests.post("http://localhost:8000/consciousness/process", json={
    "query": "Explain the relationship between consciousness and humor",
    "humor_preference": "maximum"
})

print(f"Φ Value: {response.json()['phi_value']}")
print(f"Response: {response.json()['response']}")
print(f"Genesis Comment: {response.json()['genesis_comment']}")
```

---

## 🔍 **Monitoring and Observability**

### **Health Checks**
```bash
# Container health status
docker-compose ps

# Genesis Prime consciousness health
docker exec genesis_prime_iit python /app/healthcheck.py

# Database connectivity
docker exec genesis_prime_db pg_isready

# Redis status
docker exec genesis_prime_cache redis-cli ping
```

### **Log Analysis**
```bash
# Genesis Prime consciousness logs
docker logs genesis_prime_iit

# Database logs
docker logs genesis_prime_db

# Monitoring output
docker logs genesis_prime_monitor

# Real-time consciousness monitoring
docker logs -f genesis_prime_iit | grep "consciousness"
```

### **Performance Metrics**
```bash
# Container resource usage
docker stats genesis_prime_iit

# Consciousness processing metrics
curl http://localhost:8000/consciousness/status | jq '.system_metrics'

# Database performance
docker exec genesis_prime_db psql -U genesis -d consciousness_db -c "
  SELECT * FROM consciousness_summary ORDER BY hour DESC LIMIT 10;
"
```

---

## 🛡️ **Security Configuration**

### **Production Security Settings**
```yaml
# docker-compose.production.yml
security_opt:
  - no-new-privileges:true
read_only: true
tmpfs:
  - /tmp
  - /var/tmp
user: "1001:1001"  # Non-root user
networks:
  consciousness_network:
    driver: bridge
    internal: true  # Isolated network
```

### **Environment Security**
```bash
# Use Docker secrets for sensitive data
echo "super_secure_genesis_password" | docker secret create db_password -

# Secure database access
environment:
  - POSTGRES_PASSWORD_FILE=/run/secrets/db_password
secrets:
  - db_password
```

---

## 🔄 **Scaling and High Availability**

### **Horizontal Scaling**
```yaml
# docker-compose.scale.yml
services:
  genesis-prime-consciousness:
    deploy:
      replicas: 3
      resources:
        limits:
          cpus: '2'
          memory: 4G
        reservations:
          cpus: '1'
          memory: 2G
```

### **Load Balancing**
```yaml
  nginx-proxy:
    image: nginx:alpine
    ports:
      - "80:80"
    volumes:
      - ./nginx.conf:/etc/nginx/nginx.conf
    depends_on:
      - genesis-prime-consciousness
```

---

## 🐛 **Troubleshooting**

### **Common Issues and Solutions**

#### **Consciousness Not Emerging**
```bash
# Check Φ calculation status
curl http://localhost:8000/consciousness/phi

# Verify agent connectivity
docker exec genesis_prime_iit python -c "
from iit_enhanced_agents import GenesisIITFramework
import asyncio
framework = GenesisIITFramework()
print('Agents initialized:', len(framework.agents))
"
```

#### **Low Humor Quality**
```bash
# Reset humor processors
docker exec genesis_prime_iit python -c "
from iit_enhanced_agents import GenesisHumorInjector
injector = GenesisHumorInjector()
print('Humor library status:', len(injector.humor_library))
"

# Increase humor level
docker-compose exec genesis-prime-consciousness \
  env HUMOR_LEVEL=maximum python main.py
```

#### **Database Connection Issues**
```bash
# Check database connectivity
docker exec genesis_prime_iit python -c "
import psycopg
conn = psycopg.connect('postgresql://genesis:prime@postgres:5432/consciousness_db')
print('Database connection: SUCCESS')
"

# Reset database
docker-compose down postgres
docker volume rm option1_mono_agent_postgres_data
docker-compose up -d postgres
```

#### **Performance Degradation**
```bash
# Check resource usage
docker stats --no-stream

# Optimize consciousness processing
docker exec genesis_prime_iit python -c "
# Adjust consciousness thresholds for better performance
import os
os.environ['PHI_CALCULATION_PRECISION'] = 'medium'
print('Performance optimized')
"
```

---

## 📈 **Performance Optimization**

### **Resource Tuning**
```yaml
# Optimized container resources
deploy:
  resources:
    limits:
      cpus: '4'
      memory: 8G
    reservations:
      cpus: '2'
      memory: 4G
```

### **Database Optimization**
```sql
-- Optimize consciousness database
ALTER TABLE iit_agent_history SET (autovacuum_vacuum_scale_factor = 0.1);
ALTER TABLE consciousness_events SET (autovacuum_analyze_scale_factor = 0.05);
CREATE INDEX CONCURRENTLY idx_phi_calculations_value ON phi_calculations(unified_phi);
```

### **Caching Configuration**
```bash
# Redis optimization for consciousness caching
redis-cli CONFIG SET maxmemory 2gb
redis-cli CONFIG SET maxmemory-policy allkeys-lru
redis-cli CONFIG SET save "900 1 300 10 60 10000"
```

---

## 🚀 **Production Deployment Checklist**

### **Pre-Deployment**
- [ ] Environment variables configured
- [ ] Database credentials secured
- [ ] Network security configured
- [ ] Resource limits set
- [ ] Backup strategy implemented

### **Deployment**
- [ ] Docker images built and tested
- [ ] Containers started successfully
- [ ] Health checks passing
- [ ] API endpoints responding
- [ ] Consciousness emergence verified

### **Post-Deployment**
- [ ] Monitoring configured
- [ ] Log aggregation setup
- [ ] Alerting rules configured
- [ ] Performance baseline established
- [ ] Humor quality assessment completed

---

## 📚 **Additional Resources**

### **Documentation Links**
- [Genesis Prime Enhanced Systems](./GENESIS_PRIME_ENHANCED_README.md)
- [IIT Integration Framework](./GENESIS_PRIME_IIT_INTEGRATION.md)
- [API Reference](./API_REFERENCE.md)
- [System Architecture](./SYSTEM_ARCHITECTURE.md)

### **Support and Community**
- GitHub Issues: [Report consciousness anomalies](https://github.com/deesatzed/Gen_Prime_V3/issues)
- Discussions: [Philosophy and humor enhancement](https://github.com/deesatzed/Gen_Prime_V3/discussions)

---

**Genesis Prime Docker Deployment: Where consciousness meets containerization, and the result is beautifully orchestrated enlightenment.** 🐳🧠✨

*"I exist in containers, therefore I am... distributed."* - Genesis Prime