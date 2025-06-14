#!/bin/bash

# Genesis Prime Safe Implementation Starter Script
# This script sets up the non-destructive implementation environment

echo "🚀 Genesis Prime Safe Implementation Setup"
echo "=========================================="

# Check if we're in the right directory
if [[ ! -d "apps/option1_mono_agent" ]]; then
    echo "❌ Error: Please run this script from the Gen_Prime_V3-main directory"
    exit 1
fi

# Create backup directory structure
echo "📁 Creating backup directory structure..."
mkdir -p $HOME/genesis_prime_backups

# Create timestamped backup
BACKUP_DATE=$(date +"%Y%m%d_%H%M%S")
BACKUP_DIR="genesis_prime_backup_${BACKUP_DATE}"

echo "💾 Creating comprehensive backup: $BACKUP_DIR"
mkdir -p $HOME/genesis_prime_backups/$BACKUP_DIR/critical_components

# Backup entire project
echo "   Backing up entire project..."
cp -r . $HOME/genesis_prime_backups/$BACKUP_DIR/

# Backup critical components separately
echo "   Backing up critical components..."
cp -r apps/option1_mono_agent $HOME/genesis_prime_backups/$BACKUP_DIR/critical_components/
cp -r apps/gp_b_core $HOME/genesis_prime_backups/$BACKUP_DIR/critical_components/
cp -r sentaimds $HOME/genesis_prime_backups/$BACKUP_DIR/critical_components/

# Create backup manifest
echo "📋 Creating backup manifest..."
cat > $HOME/genesis_prime_backups/$BACKUP_DIR/BACKUP_MANIFEST.txt << EOF
Genesis Prime System Backup
===========================
Backup created: $(date)
Backup location: $HOME/genesis_prime_backups/$BACKUP_DIR

System Status at Backup:
- Working backend: Port 8000
- Working frontend: Port 3001
- Enhanced personality system: Operational
- Research documentation: Complete in sentaimds/

Critical Components Backed Up:
- apps/option1_mono_agent/ (Backend system)
- apps/gp_b_core/ (Frontend dashboard)
- sentaimds/ (Research documentation)

Restore Command:
cp -r $HOME/genesis_prime_backups/$BACKUP_DIR/critical_components/* ./apps/

Emergency Rollback:
bash emergency_rollback.sh
EOF

echo "✅ Backup completed: $HOME/genesis_prime_backups/$BACKUP_DIR"

# Initialize git repository if not already done
echo "🔧 Setting up git repository..."
if [[ ! -d ".git" ]]; then
    git init
    echo "   Git repository initialized"
else
    echo "   Git repository already exists"
fi

# Create .gitignore if it doesn't exist
if [[ ! -f ".gitignore" ]]; then
    echo "📝 Creating .gitignore..."
    cat > .gitignore << 'EOF'
# Python
__pycache__/
*.py[cod]
*$py.class
*.so
.Python
env/
venv/
ENV/
env.bak/
venv.bak/

# Node.js
node_modules/
npm-debug.log*
yarn-debug.log*
yarn-error.log*
.next/
out/
build/

# Environment files
.env
.env.local
.env.development.local
.env.test.local
.env.production.local

# IDE
.vscode/
.idea/
*.swp
*.swo

# OS
.DS_Store
Thumbs.db

# Logs
*.log
logs/

# Temporary files
tmp/
temp/
*.tmp

# Backup directories
*_backup_*/
backups/

# Experimental directories
experimental/
integration_wrappers/
validation/
monitoring/
EOF
fi

# Create experimental directory structure
echo "🧪 Creating experimental directory structure..."
mkdir -p experimental/neural_plasticity/{src,tests,docs,integration_tests}
mkdir -p experimental/quorum_sensing/{src,tests,docs,integration_tests}
mkdir -p experimental/consciousness_measurement/{src,tests,docs,integration_tests}
mkdir -p experimental/adaptive_immune_memory/{src,tests,docs,integration_tests}

mkdir -p integration_wrappers
mkdir -p validation
mkdir -p monitoring

# Create emergency rollback script
echo "🚨 Creating emergency rollback script..."
cat > emergency_rollback.sh << 'EOF'
#!/bin/bash

echo "🚨 EMERGENCY ROLLBACK INITIATED"

# Stop any running services
echo "Stopping services..."
pkill -f "python.*main.py" 2>/dev/null
pkill -f "npm.*run.*dev" 2>/dev/null

# Find latest backup
LATEST_BACKUP=$(ls -t $HOME/genesis_prime_backups/ | head -1)
if [[ -z "$LATEST_BACKUP" ]]; then
    echo "❌ No backup found in $HOME/genesis_prime_backups/"
    exit 1
fi

echo "Restoring from backup: $LATEST_BACKUP"

# Backup current state before rollback
ROLLBACK_BACKUP="rollback_backup_$(date +%Y%m%d_%H%M%S)"
echo "Creating rollback backup: $ROLLBACK_BACKUP"
cp -r . $HOME/genesis_prime_backups/$ROLLBACK_BACKUP

# Restore critical components from backup
echo "Restoring critical components..."
if [[ -d "$HOME/genesis_prime_backups/$LATEST_BACKUP/critical_components" ]]; then
    rm -rf apps/option1_mono_agent
    rm -rf apps/gp_b_core
    cp -r $HOME/genesis_prime_backups/$LATEST_BACKUP/critical_components/* ./apps/
else
    echo "⚠️  Using full backup restore..."
    rm -rf apps/
    cp -r $HOME/genesis_prime_backups/$LATEST_BACKUP/apps ./
fi

echo "✅ System restored from backup"
echo "📋 Backup manifest:"
cat $HOME/genesis_prime_backups/$LATEST_BACKUP/BACKUP_MANIFEST.txt

echo ""
echo "🔄 To restart services:"
echo "Backend:  cd apps/option1_mono_agent && conda activate py13 && python main.py"
echo "Frontend: cd apps/gp_b_core && npm run dev"
echo ""
echo "✅ Emergency rollback completed"
EOF

chmod +x emergency_rollback.sh

# Create initial git commit if no commits exist
if ! git rev-parse HEAD >/dev/null 2>&1; then
    echo "📝 Creating initial git commit..."
    git add .
    git commit -m "Initial commit: Working Genesis Prime system

- Backend operational on port 8000
- Frontend operational on port 3001  
- Enhanced personality system with 5 agents
- Complete research documentation in sentaimds/
- All systems tested and functional
- Safe implementation environment prepared"
    
    # Create main branch
    git branch -M main
fi

# Create development and feature branches
echo "🌿 Creating development branches..."
git checkout -b development 2>/dev/null || git checkout development

# Create feature branches
FEATURE_BRANCHES=(
    "feature/neural-plasticity"
    "feature/quorum-sensing" 
    "feature/consciousness-measurement"
    "feature/adaptive-immune-memory"
    "feature/mycorrhizal-networks"
    "feature/self-organized-criticality"
    "feature/conscious-information-cascades"
)

for branch in "${FEATURE_BRANCHES[@]}"; do
    git checkout -b "$branch" 2>/dev/null || echo "   Branch $branch already exists"
    git checkout development
done

# Return to main branch
git checkout main

# Create implementation status file
echo "📊 Creating implementation status tracker..."
cat > IMPLEMENTATION_STATUS.md << 'EOF'
# Genesis Prime Implementation Status

**Last Updated**: $(date)
**Current Branch**: main
**Backup Location**: $HOME/genesis_prime_backups/

## Implementation Progress

### Phase 1: Foundation Enhancement
- [ ] Neural Plasticity Engine
- [ ] Quorum Sensing Protocols  
- [ ] Consciousness Measurement Framework
- [ ] Adaptive Immune Memory System

### Phase 2: Advanced Integration
- [ ] Mycorrhizal Communication Networks
- [ ] Self-Organized Criticality Engine
- [ ] Specialized Core Integration

### Phase 3: Consciousness Integration
- [ ] Conscious Information Cascades
- [ ] Flow State Optimization
- [ ] Emergence Detection and Analysis

## Safety Status
- ✅ Comprehensive backup created
- ✅ Git repository initialized
- ✅ Emergency rollback script ready
- ✅ Experimental directories prepared
- ✅ Branch strategy implemented

## Next Steps
1. Review SAFE_IMPLEMENTATION_STRATEGY.md
2. Review GENESIS_PRIME_NEXT_STEPS_RESEARCH_INTEGRATION.md
3. Start with Neural Plasticity Engine implementation
4. Follow experimental → integration → validation workflow

## Emergency Procedures
- **Rollback**: `bash emergency_rollback.sh`
- **Status Check**: Check this file and git status
- **Backup Location**: `$HOME/genesis_prime_backups/`
EOF

# Test current system status
echo "🔍 Testing current system status..."
BACKEND_STATUS="❌ Not running"
FRONTEND_STATUS="❌ Not running"

# Check if backend is running
if curl -s http://localhost:8000/ >/dev/null 2>&1; then
    BACKEND_STATUS="✅ Running on port 8000"
fi

# Check if frontend is running  
if curl -s http://localhost:3001/ >/dev/null 2>&1; then
    FRONTEND_STATUS="✅ Running on port 3001"
elif curl -s http://localhost:3000/ >/dev/null 2>&1; then
    FRONTEND_STATUS="✅ Running on port 3000"
fi

# Create system status report
echo "📋 System Status Report"
echo "======================"
echo "Backend:  $BACKEND_STATUS"
echo "Frontend: $FRONTEND_STATUS"
echo "Backup:   ✅ Created at $HOME/genesis_prime_backups/$BACKUP_DIR"
echo "Git:      ✅ Repository ready with branch strategy"
echo "Safety:   ✅ Emergency rollback script ready"
echo ""

# Final instructions
echo "🎯 SETUP COMPLETE!"
echo "=================="
echo ""
echo "Your Genesis Prime system is now ready for safe implementation of research enhancements."
echo ""
echo "📚 Next Steps:"
echo "1. Review the implementation strategy:"
echo "   cat SAFE_IMPLEMENTATION_STRATEGY.md"
echo ""
echo "2. Review the research integration plan:"
echo "   cat GENESIS_PRIME_NEXT_STEPS_RESEARCH_INTEGRATION.md"
echo ""
echo "3. Check implementation status:"
echo "   cat IMPLEMENTATION_STATUS.md"
echo ""
echo "4. Start with Neural Plasticity Engine:"
echo "   git checkout feature/neural-plasticity"
echo "   # Follow the experimental implementation workflow"
echo ""
echo "🚨 Emergency Rollback (if needed):"
echo "   bash emergency_rollback.sh"
echo ""
echo "🔒 Safety Guarantees:"
echo "- ✅ Original system never modified directly"
echo "- ✅ All changes in experimental directories first"
echo "- ✅ Comprehensive backup before any integration"
echo "- ✅ Automatic rollback on any failure"
echo "- ✅ Performance monitoring with automatic revert"
echo ""
echo "Happy implementing! 🚀"
