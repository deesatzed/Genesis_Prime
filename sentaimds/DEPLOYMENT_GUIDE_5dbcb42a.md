# Genesis Prime V3 - Deployment Guide

## 🚀 Production Deployment

### System Requirements
- **OS**: Linux/macOS/Windows
- **Node.js**: 18.0.0 or higher
- **Python**: 3.8 or higher
- **Memory**: 4GB RAM minimum, 8GB recommended
- **Storage**: 2GB free space
- **Network**: Internet connection for model API access

### Environment Setup

#### 1. Create Conda Environment
```bash
# Create isolated Python environment
conda create -n genesis-prime python=3.8
conda activate genesis-prime

# Verify Python version
python --version  # Should show Python 3.8.x
```

#### 2. Clone and Setup Repository
```bash
# Clone repository
git clone <repository-url>
cd Gen_Prime_V3-main

# Verify directory structure
ls -la apps/
# Should show: gp_b_core/ and option1_mono_agent/
```

### Backend Deployment (Genesis Prime Consciousness)

#### 1. Install Dependencies
```bash
cd apps/option1_mono_agent
pip install -r requirements.txt
```

#### 2. Environment Configuration
```bash
# Create .env file
cat > .env << EOF
OPENROUTER_API_KEY=your_openrouter_api_key_here
ENVIRONMENT=production
LOG_LEVEL=INFO
HOST=0.0.0.0
PORT=8000
EOF
```

#### 3. Start Backend Service
```bash
# Development mode
python main.py

# Production mode (with gunicorn)
pip install gunicorn
gunicorn -w 4 -k uvicorn.workers.UvicornWorker main:app --bind 0.0.0.0:8000
```

#### 4. Verify Backend
```bash
# Health check
curl http://localhost:8000/
# Expected: {"message":"Genesis Prime IIT Enhanced Consciousness System"...}

# API documentation
curl http://localhost:8000/consciousness/docs
# Should return OpenAPI documentation
```

### Frontend Deployment (Dashboard)

#### 1. Install Dependencies
```bash
cd apps/gp_b_core
npm install
```

#### 2. Environment Configuration
```bash
# Create .env.local file
cat > .env.local << EOF
NEXT_PUBLIC_API_URL=http://localhost:8000
NODE_ENV=production
EOF
```

#### 3. Build and Start
```bash
# Build for production
npm run build

# Start production server
npm start
# Or for development
npm run dev
```

#### 4. Verify Frontend
```bash
# Check build output
ls -la .next/
# Should show compiled application

# Test accessibility
curl http://localhost:3004/dashboard
# Should return HTML dashboard
```

### Docker Deployment (Optional)

#### 1. Backend Dockerfile
```dockerfile
# apps/option1_mono_agent/Dockerfile
FROM python:3.8-slim

WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt

COPY . .
EXPOSE 8000

CMD ["python", "main.py"]
```

#### 2. Frontend Dockerfile
```dockerfile
# apps/gp_b_core/Dockerfile
FROM node:18-alpine

WORKDIR /app
COPY package*.json ./
RUN npm ci --only=production

COPY . .
RUN npm run build

EXPOSE 3000
CMD ["npm", "start"]
```

#### 3. Docker Compose
```yaml
# docker-compose.yml
version: '3.8'
services:
  backend:
    build: ./apps/option1_mono_agent
    ports:
      - "8000:8000"
    environment:
      - OPENROUTER_API_KEY=${OPENROUTER_API_KEY}
    
  frontend:
    build: ./apps/gp_b_core
    ports:
      - "3004:3000"
    environment:
      - NEXT_PUBLIC_API_URL=http://backend:8000
    depends_on:
      - backend
```

### Production Monitoring

#### 1. Health Checks
```bash
# Backend health
curl -f http://localhost:8000/consciousness/status || exit 1

# Frontend health
curl -f http://localhost:3004/dashboard || exit 1
```

#### 2. Log Monitoring
```bash
# Backend logs
tail -f apps/option1_mono_agent/logs/genesis-prime.log

# Frontend logs (PM2 example)
pm2 logs genesis-frontend
```

#### 3. Performance Monitoring
```bash
# System resources
htop

# Network connections
netstat -tulpn | grep :8000
netstat -tulpn | grep :3004
```

### Security Configuration

#### 1. API Key Management
```bash
# Store API keys securely
export OPENROUTER_API_KEY="your_secure_key"

# Use environment files (not committed to git)
echo "OPENROUTER_API_KEY=your_key" > .env
echo ".env" >> .gitignore
```

#### 2. Network Security
```bash
# Firewall rules (example for Ubuntu)
sudo ufw allow 8000/tcp  # Backend API
sudo ufw allow 3004/tcp  # Frontend dashboard
sudo ufw enable
```

#### 3. HTTPS Configuration (Production)
```nginx
# nginx configuration example
server {
    listen 443 ssl;
    server_name your-domain.com;
    
    ssl_certificate /path/to/cert.pem;
    ssl_certificate_key /path/to/key.pem;
    
    location / {
        proxy_pass http://localhost:3004;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
    }
    
    location /api/ {
        proxy_pass http://localhost:8000/;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
    }
}
```

### Troubleshooting

#### Common Issues

**Port Already in Use**
```bash
# Find process using port
lsof -i :8000
lsof -i :3004

# Kill process if needed
kill -9 <PID>
```

**Permission Denied**
```bash
# Fix file permissions
chmod +x apps/option1_mono_agent/main.py
chmod -R 755 apps/gp_b_core/
```

**Module Not Found**
```bash
# Reinstall dependencies
cd apps/option1_mono_agent
pip install -r requirements.txt --force-reinstall

cd ../gp_b_core
rm -rf node_modules package-lock.json
npm install
```

**API Connection Failed**
```bash
# Check backend status
curl -v http://localhost:8000/consciousness/status

# Check network connectivity
ping localhost
telnet localhost 8000
```

### Performance Optimization

#### 1. Backend Optimization
```bash
# Use production ASGI server
pip install uvicorn[standard]
uvicorn main:app --host 0.0.0.0 --port 8000 --workers 4

# Enable caching
pip install redis
# Configure Redis caching in application
```

#### 2. Frontend Optimization
```bash
# Enable compression
npm install compression

# Optimize build
npm run build -- --analyze

# Use CDN for static assets
# Configure in next.config.js
```

### Backup and Recovery

#### 1. Configuration Backup
```bash
# Backup configuration files
tar -czf config-backup-$(date +%Y%m%d).tar.gz \
  apps/option1_mono_agent/.env \
  apps/gp_b_core/.env.local \
  apps/gp_b_core/components.json
```

#### 2. Application State Backup
```bash
# Backup agent configurations
cp apps/gp_b_core/lib/config-service.ts config-backup/
cp -r apps/option1_mono_agent/prompts/ config-backup/
```

#### 3. Recovery Procedure
```bash
# Stop services
pkill -f "python main.py"
pkill -f "npm.*dev"

# Restore from backup
tar -xzf config-backup-YYYYMMDD.tar.gz

# Restart services
cd apps/option1_mono_agent && python main.py &
cd apps/gp_b_core && npm run dev &
```

### Maintenance

#### 1. Regular Updates
```bash
# Update Python dependencies
pip list --outdated
pip install -r requirements.txt --upgrade

# Update Node.js dependencies
npm outdated
npm update
```

#### 2. Log Rotation
```bash
# Setup logrotate for backend logs
sudo cat > /etc/logrotate.d/genesis-prime << EOF
/path/to/logs/*.log {
    daily
    rotate 30
    compress
    delaycompress
    missingok
    notifempty
}
EOF
```

#### 3. Health Monitoring
```bash
# Create monitoring script
cat > monitor.sh << EOF
#!/bin/bash
if ! curl -f http://localhost:8000/consciousness/status > /dev/null 2>&1; then
    echo "Backend down, restarting..."
    cd apps/option1_mono_agent && python main.py &
fi

if ! curl -f http://localhost:3004/dashboard > /dev/null 2>&1; then
    echo "Frontend down, restarting..."
    cd apps/gp_b_core && npm run dev &
fi
EOF

chmod +x monitor.sh
# Add to crontab: */5 * * * * /path/to/monitor.sh
```

---

**Status**: Production Ready ✅  
**Last Updated**: 2025-06-12  
**Version**: 3.0.0
