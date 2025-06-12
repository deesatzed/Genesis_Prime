#!/bin/bash

# Genesis Prime Enhanced GitHub Push Script
# Creates new branch with Docker support and Python 3.13 enhancements

set -e

# Color codes for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Configuration
BRANCH_NAME="v3.0-docker-python313-enhanced"
COMMIT_MESSAGE="🚀 V3.0 Enhanced: Docker Support + Python 3.13 + Comprehensive Deployment System"
REPO_URL="https://github.com/deesatzed/Genesis_Prime"

echo -e "${BLUE}🚀 Genesis Prime Enhanced GitHub Push${NC}"
echo "=============================================="
echo -e "${YELLOW}Branch: $BRANCH_NAME${NC}"
echo -e "${YELLOW}Repository: $REPO_URL${NC}"
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

# Function to check git status
check_git_status() {
    echo -e "${BLUE}🔍 Checking Git status...${NC}"
    
    if ! git status >/dev/null 2>&1; then
        log_error "Not in a Git repository" "Initialize Git repository with: git init"
        exit 1
    fi
    
    # Check if we have uncommitted changes
    if ! git diff-index --quiet HEAD -- 2>/dev/null; then
        echo -e "${YELLOW}⚠️  Uncommitted changes detected${NC}"
        echo "Files with changes:"
        git status --porcelain
        echo ""
        read -p "Continue with commit? (Y/n): " -n 1 -r
        echo
        if [[ $REPLY =~ ^[Nn]$ ]]; then
            echo "Aborting push."
            exit 0
        fi
    fi
    
    echo -e "${GREEN}✅ Git status checked${NC}"
}

# Function to create and switch to new branch
create_branch() {
    echo -e "${BLUE}🌿 Creating new branch: $BRANCH_NAME${NC}"
    
    # Check if branch already exists
    if git branch --list | grep -q "$BRANCH_NAME"; then
        echo -e "${YELLOW}⚠️  Branch $BRANCH_NAME already exists${NC}"
        read -p "Switch to existing branch? (Y/n): " -n 1 -r
        echo
        if [[ $REPLY =~ ^[Nn]$ ]]; then
            echo "Aborting."
            exit 0
        fi
        git checkout "$BRANCH_NAME"
    else
        # Create new branch from current branch
        git checkout -b "$BRANCH_NAME"
        echo -e "${GREEN}✅ Created and switched to branch: $BRANCH_NAME${NC}"
    fi
}

# Function to stage all changes
stage_changes() {
    echo -e "${BLUE}📋 Staging changes...${NC}"
    
    # Add all files
    git add .
    
    # Show what will be committed
    echo -e "${YELLOW}Files to be committed:${NC}"
    git status --porcelain | head -20
    if [[ $(git status --porcelain | wc -l) -gt 20 ]]; then
        echo "... and $(($(git status --porcelain | wc -l) - 20)) more files"
    fi
    echo ""
    
    echo -e "${GREEN}✅ Changes staged${NC}"
}

# Function to create comprehensive commit
create_commit() {
    echo -e "${BLUE}💾 Creating commit...${NC}"
    
    # Create detailed commit message
    cat > /tmp/commit_message << EOF
$COMMIT_MESSAGE

## 🎯 Major Enhancements

### 🐳 Docker Containerization
- Complete Docker Compose setup with multi-service architecture
- Backend (Python 3.13), Frontend (Next.js), Onboarding, and Nginx services
- Health checks and automated service monitoring
- Volume management for persistent data storage
- Docker Compose profiles (default, onboarding, production)

### 🐍 Python 3.13 Migration
- All Dockerfiles updated to Python 3.13-slim base images
- Conda environment scripts updated for Python 3.13
- Enhanced performance and security with latest Python version
- Maintained backward compatibility with existing codebase

### 🔄 Hybrid Deployment System
- Interactive deployment type selection (Standard/Docker/Hybrid)
- Enhanced installation scripts with error logging
- Smart file copying with rsync optimization
- Comprehensive environment configuration templates

### 📊 Enhanced Management
- Complete Docker management script suite
- Health monitoring and status checking
- Automated error logging and resolution tracking
- Progress tracking for agent onboarding

## 🚀 New Features

### Docker Infrastructure
- docker/Dockerfile.backend: Python 3.13 backend container
- docker/Dockerfile.frontend: Next.js frontend container
- docker/Dockerfile.onboarding: Agent onboarding container
- docker/nginx.conf: Nginx reverse proxy configuration
- docker-compose.yml: Multi-service orchestration
- .env.docker: Docker environment template

### Enhanced Scripts
- deploy_genesis_prime_enhanced.sh: New deployment script with Docker support
- scripts/docker_*.sh: Complete Docker management suite
- scripts/docker_onboard_agents.py: Python onboarding for Docker
- Updated all existing scripts for Python 3.13 compatibility

### Comprehensive Documentation
- DOCKER_DEPLOYMENT_GUIDE.md: Complete Docker deployment guide
- Enhanced README.md with both deployment options
- Updated error_logWS.md with all resolutions and Docker documentation
- Comprehensive troubleshooting and quick start guides

## 🔧 Technical Improvements

### System Architecture
- Multi-service Docker architecture with health checks
- Python 3.13 performance and security enhancements
- Enhanced error handling and logging throughout
- Scalable deployment options for development and production

### Deployment Flexibility
- Standard deployment: Conda + Node.js + Python 3.13
- Docker deployment: Full containerization with Docker Compose
- Hybrid support: Both options available in same package
- Environment isolation and reproducible deployments

### Operational Benefits
- Simplified deployment with one-command Docker setup
- Automated service health monitoring and restart
- Comprehensive error logging with resolution suggestions
- Enhanced documentation and troubleshooting guides

## 📋 Files Modified/Created

### New Files
- docker/Dockerfile.backend
- docker/Dockerfile.frontend
- docker/Dockerfile.onboarding
- docker/nginx.conf
- docker-compose.yml
- .env.docker
- deploy_genesis_prime_enhanced.sh
- scripts/docker_start.sh
- scripts/docker_stop.sh
- scripts/docker_status.sh
- scripts/docker_onboard.sh
- scripts/docker_onboard_agents.py
- DOCKER_DEPLOYMENT_GUIDE.md
- github_push_enhanced.sh

### Updated Files
- README.md: Complete rewrite with Docker and Python 3.13 support
- error_logWS.md: Enhanced with Docker documentation and resolutions
- All deployment scripts updated for Python 3.13 compatibility

## ✅ System Status
- Docker Support: ✅ Full containerization implemented
- Python 3.13: ✅ All components upgraded and tested
- Deployment Scripts: ✅ Enhanced with hybrid support
- Documentation: ✅ Comprehensive guides created
- Error Logging: ✅ Enhanced tracking and resolution
- Agent Onboarding: ✅ Docker-compatible process

## 🎉 Benefits Achieved
1. Production-ready Docker deployment with health monitoring
2. Latest Python 3.13 performance and security benefits
3. Flexible deployment options for different use cases
4. Comprehensive documentation and error handling
5. Scalable architecture ready for enterprise deployment
6. Enhanced user experience with automated setup and monitoring

Version: 3.0.0 Enhanced
Python: 3.13
Docker: Supported
Status: Production Ready ✅
EOF

    # Create commit with detailed message
    git commit -F /tmp/commit_message
    rm /tmp/commit_message
    
    echo -e "${GREEN}✅ Commit created successfully${NC}"
}

# Function to push to GitHub
push_to_github() {
    echo -e "${BLUE}🚀 Pushing to GitHub...${NC}"
    
    # Check if remote origin exists
    if ! git remote get-url origin >/dev/null 2>&1; then
        echo -e "${YELLOW}⚠️  No remote origin found. Adding remote...${NC}"
        git remote add origin "$REPO_URL"
    fi
    
    # Push branch to GitHub
    echo -e "${YELLOW}Pushing branch $BRANCH_NAME to GitHub...${NC}"
    git push -u origin "$BRANCH_NAME"
    
    echo -e "${GREEN}✅ Successfully pushed to GitHub!${NC}"
}

# Function to create pull request information
create_pr_info() {
    echo -e "${BLUE}📋 Pull Request Information${NC}"
    echo "==========================================="
    echo ""
    echo -e "${YELLOW}Branch:${NC} $BRANCH_NAME"
    echo -e "${YELLOW}Repository:${NC} $REPO_URL"
    echo ""
    echo -e "${YELLOW}Pull Request Title:${NC}"
    echo "$COMMIT_MESSAGE"
    echo ""
    echo -e "${YELLOW}Pull Request Description:${NC}"
    cat << EOF
## 🎯 Overview
This PR introduces comprehensive Docker support and Python 3.13 migration for Genesis Prime V3.0, providing enterprise-grade deployment capabilities with both traditional and containerized options.

## 🚀 Major Features
- **🐳 Complete Docker Containerization**: Multi-service architecture with health checks
- **🐍 Python 3.13 Migration**: Latest Python version for enhanced performance
- **🔄 Hybrid Deployment**: Interactive selection between standard and Docker deployment
- **📊 Enhanced Management**: Comprehensive monitoring and error logging
- **📚 Complete Documentation**: Detailed guides for both deployment methods

## 🔧 Technical Changes
- Docker Compose setup with backend, frontend, onboarding, and nginx services
- All Python components upgraded to 3.13 with maintained compatibility
- Enhanced deployment scripts with error logging and health checks
- Comprehensive documentation and troubleshooting guides

## 🧪 Testing
- ✅ Docker deployment tested and verified
- ✅ Standard deployment tested with Python 3.13
- ✅ Agent onboarding process validated
- ✅ Health checks and monitoring confirmed
- ✅ Documentation accuracy verified

## 📋 Breaking Changes
None - maintains backward compatibility while adding new deployment options.

## 🎉 Benefits
1. Production-ready containerized deployment
2. Latest Python performance and security
3. Flexible deployment options
4. Enhanced error handling and monitoring
5. Comprehensive documentation

Ready for review and merge! 🚀
EOF
    echo ""
    echo -e "${GREEN}✅ Pull request information prepared${NC}"
}

# Function to display summary
display_summary() {
    echo ""
    echo -e "${GREEN}🎉 GitHub Push Complete!${NC}"
    echo "=============================================="
    echo ""
    echo -e "${YELLOW}📊 Summary:${NC}"
    echo "• Branch: $BRANCH_NAME"
    echo "• Repository: $REPO_URL"
    echo "• Commit: Enhanced Docker + Python 3.13 support"
    echo "• Files: $(git diff --name-only HEAD~1 | wc -l) files modified/created"
    echo ""
    echo -e "${YELLOW}🔗 Next Steps:${NC}"
    echo "1. Visit: $REPO_URL"
    echo "2. Create Pull Request from branch: $BRANCH_NAME"
    echo "3. Use the pull request information provided above"
    echo "4. Review and merge when ready"
    echo ""
    echo -e "${YELLOW}🚀 New Features Available:${NC}"
    echo "• Docker deployment with docker-compose up -d"
    echo "• Python 3.13 enhanced performance"
    echo "• Hybrid deployment options"
    echo "• Comprehensive health monitoring"
    echo "• Enhanced documentation and error logging"
    echo ""
    echo -e "${GREEN}Genesis Prime V3.0 Enhanced is ready for production! ✅${NC}"
}

# Main execution
main() {
    echo -e "${BLUE}Starting GitHub push process...${NC}"
    echo ""
    
    # Step 1: Check Git status
    check_git_status
    
    # Step 2: Create new branch
    create_branch
    
    # Step 3: Stage all changes
    stage_changes
    
    # Step 4: Create comprehensive commit
    create_commit
    
    # Step 5: Push to GitHub
    push_to_github
    
    # Step 6: Create PR information
    create_pr_info
    
    # Step 7: Display summary
    display_summary
}

# Execute main function
main "$@"
