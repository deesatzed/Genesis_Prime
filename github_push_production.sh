#!/bin/bash

# Genesis Prime V3 - Production GitHub Push Script
# This script pushes only the essential files needed to run the application

set -e  # Exit on any error

echo "🚀 Genesis Prime V3 - Production GitHub Push"
echo "============================================="

# Check if we're in the right directory
if [ ! -d "apps/gp_b_core" ] || [ ! -d "apps/option1_mono_agent" ]; then
    echo "❌ Error: Must be run from the Gen_Prime_V3-main root directory"
    echo "Current directory: $(pwd)"
    exit 1
fi

# Check if git is initialized
if [ ! -d ".git" ]; then
    echo "📦 Initializing git repository..."
    git init
    echo "✅ Git repository initialized"
fi

# Create .gitignore if it doesn't exist
if [ ! -f ".gitignore" ]; then
    echo "📝 Creating .gitignore..."
    cat > .gitignore << 'EOF'
# Dependencies
node_modules/
__pycache__/
*.pyc
*.pyo
*.pyd
.Python
env/
venv/
.venv/
pip-log.txt
pip-delete-this-directory.txt

# Build outputs
.next/
out/
build/
dist/

# Environment files
.env
.env.local
.env.development.local
.env.test.local
.env.production.local

# Logs
*.log
logs/

# Runtime data
pids/
*.pid
*.seed
*.pid.lock

# Coverage directory used by tools like istanbul
coverage/

# IDE files
.vscode/
.idea/
*.swp
*.swo
*~

# OS generated files
.DS_Store
.DS_Store?
._*
.Spotlight-V100
.Trashes
ehthumbs.db
Thumbs.db

# Backup files
*_backup_*
backup_*
*.backup

# Temporary files
tmp/
temp/
*.tmp

# Cache
.cache/
.npm/
.eslintcache

# Optional npm cache directory
.npm

# Optional REPL history
.node_repl_history

# Output of 'npm pack'
*.tgz

# Yarn Integrity file
.yarn-integrity

# dotenv environment variables file
.env

# Conda environments
.conda/

# Jupyter Notebook
.ipynb_checkpoints

# pyenv
.python-version

# Exclude large directories not needed for production
amm-production-bld-20250520/
Gen_Prime_V2-main/
genesis_prime_production_backup/
infrastructure/
libs/
option1_mono_agent_PriorVersion/
CLEANBUILD/Screenshots/
apps/gp_b_core_backup_*/

# Exclude documentation that's not essential
*_NOTES.md
*_ANALYSIS.md
SESSION_*.md
BACKUP_*.md
CURRENT_*.md
REMAINING_*.md
EOF
    echo "✅ .gitignore created"
fi

# Stage essential files
echo "📁 Staging essential application files..."

# Core application files
git add README.md
git add DEPLOYMENT_GUIDE.md
git add error_logWS.md

# Backend files (Genesis Prime Consciousness)
echo "  📦 Adding backend files..."
git add apps/option1_mono_agent/main.py
git add apps/option1_mono_agent/iit_enhanced_agents.py
git add apps/option1_mono_agent/requirements.txt
git add apps/option1_mono_agent/prompts/

# Frontend files (Dashboard)
echo "  🎨 Adding frontend files..."
git add apps/gp_b_core/package.json
git add apps/gp_b_core/package-lock.json
git add apps/gp_b_core/next.config.js
git add apps/gp_b_core/tailwind.config.ts
git add apps/gp_b_core/tsconfig.json
git add apps/gp_b_core/components.json
git add apps/gp_b_core/postcss.config.js

# Frontend source code
git add apps/gp_b_core/app/
git add apps/gp_b_core/components/
git add apps/gp_b_core/lib/
git add apps/gp_b_core/hooks/

# Configuration files
echo "  ⚙️  Adding configuration files..."
git add CLEANBUILD/FEATURE_MIGRATION_CHECKLIST.md
git add CLEANBUILD/TROUBLESHOOTING_SESSION_20250610.md

# Check if there are any changes to commit
if git diff --staged --quiet; then
    echo "⚠️  No changes to commit"
    exit 0
fi

# Show what will be committed
echo ""
echo "📋 Files to be committed:"
git diff --staged --name-only | sed 's/^/  ✓ /'

echo ""
read -p "🤔 Continue with commit? (y/N): " -n 1 -r
echo
if [[ ! $REPLY =~ ^[Yy]$ ]]; then
    echo "❌ Commit cancelled"
    exit 1
fi

# Get commit message
echo ""
echo "📝 Enter commit message (or press Enter for default):"
read -r COMMIT_MSG

if [ -z "$COMMIT_MSG" ]; then
    COMMIT_MSG="feat: Genesis Prime V3 production release

- Complete multi-agent consciousness system
- Genesis Prime consciousness integration
- Real-time swarm intelligence dashboard
- Activity monitoring and token tracking
- Interactive stimulus and behavior controls
- Comprehensive documentation and deployment guides

Status: Production Ready ✅
Version: 3.0.0"
fi

# Commit changes
echo "💾 Committing changes..."
git commit -m "$COMMIT_MSG"
echo "✅ Changes committed successfully"

# Check for remote repository
if ! git remote get-url origin > /dev/null 2>&1; then
    echo ""
    echo "🔗 No remote repository configured."
    echo "To add a remote repository:"
    echo "  git remote add origin <repository-url>"
    echo "  git push -u origin main"
    exit 0
fi

# Push to remote
echo ""
read -p "🚀 Push to remote repository? (y/N): " -n 1 -r
echo
if [[ $REPLY =~ ^[Yy]$ ]]; then
    echo "📤 Pushing to remote repository..."
    
    # Get current branch
    CURRENT_BRANCH=$(git branch --show-current)
    
    # Push to remote
    if git push origin "$CURRENT_BRANCH"; then
        echo "✅ Successfully pushed to remote repository"
        echo ""
        echo "🎉 Genesis Prime V3 deployment package ready!"
        echo ""
        echo "📊 Repository Statistics:"
        echo "  📁 Total files committed: $(git ls-files | wc -l)"
        echo "  📦 Backend files: $(git ls-files | grep -c "apps/option1_mono_agent/")"
        echo "  🎨 Frontend files: $(git ls-files | grep -c "apps/gp_b_core/")"
        echo "  📚 Documentation files: $(git ls-files | grep -c "\.md$")"
        echo ""
        echo "🔗 Next steps:"
        echo "  1. Clone repository on target system"
        echo "  2. Follow DEPLOYMENT_GUIDE.md for setup"
        echo "  3. Configure environment variables"
        echo "  4. Start backend and frontend services"
        echo ""
        echo "📖 Quick start:"
        echo "  git clone <repository-url>"
        echo "  cd Gen_Prime_V3-main"
        echo "  # Follow README.md instructions"
    else
        echo "❌ Failed to push to remote repository"
        echo "💡 You may need to set up authentication or check repository permissions"
        exit 1
    fi
else
    echo "⏸️  Commit created but not pushed to remote"
    echo "💡 To push later: git push origin $(git branch --show-current)"
fi

echo ""
echo "✨ Genesis Prime V3 production package complete!"
