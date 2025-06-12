#!/bin/bash

# Test Genesis Prime Backup Script (without sudo)
# This version creates a backup without requiring sudo privileges

set -euo pipefail

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
PURPLE='\033[0;35m'
CYAN='\033[0;36m'
NC='\033[0m'

log_info() {
    echo -e "${BLUE}[INFO]${NC} $1"
}

log_success() {
    echo -e "${GREEN}[SUCCESS]${NC} $1"
}

log_warning() {
    echo -e "${YELLOW}[WARNING]${NC} $1"
}

log_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

print_banner() {
    echo -e "${CYAN}"
    cat << 'EOF'
╔══════════════════════════════════════════════════════════════╗
║               GENESIS PRIME BACKUP TEST                     ║
║                  (No Sudo Required)                         ║
╚══════════════════════════════════════════════════════════════╝
EOF
    echo -e "${NC}"
}

main() {
    print_banner
    
    BACKUP_DATE=$(date +"%Y%m%d_%H%M%S")
    BACKUP_ID="genesis_prime_test_backup_${BACKUP_DATE}"
    SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
    DEST_DIR="$HOME/Desktop/genesis_prime_test_backups/$BACKUP_ID"
    
    log_info "Creating test backup without sudo..."
    log_info "Source: $SCRIPT_DIR"
    log_info "Destination: $DEST_DIR"
    
    # Create destination
    mkdir -p "$DEST_DIR"/{core,security,frontend,database,cloud_tools,tests,documentation,config}
    
    # Count and copy core files
    local core_count=0
    for file in agent.py genesis_prime_hive.py emergence_engine.py iit_enhanced_agents.py; do
        if [[ -f "$SCRIPT_DIR/$file" ]]; then
            cp "$SCRIPT_DIR/$file" "$DEST_DIR/core/"
            ((core_count++))
        fi
    done
    
    # Copy security files
    local security_count=0
    for file in gph_security_*.py blockchain_security_*.py; do
        if [[ -f "$SCRIPT_DIR/$file" ]]; then
            cp "$SCRIPT_DIR/$file" "$DEST_DIR/security/"
            ((security_count++))
        fi
    done
    
    # Copy documentation
    local doc_count=0
    for file in "$SCRIPT_DIR"/*.md; do
        if [[ -f "$file" ]]; then
            cp "$file" "$DEST_DIR/documentation/"
            ((doc_count++))
        fi
    done
    
    # Copy config files
    local config_count=0
    for file in requirements.txt Dockerfile docker-compose.yml; do
        if [[ -f "$SCRIPT_DIR/$file" ]]; then
            cp "$SCRIPT_DIR/$file" "$DEST_DIR/config/"
            ((config_count++))
        fi
    done
    
    # Create simple deployment script
    cat > "$DEST_DIR/quick_deploy.sh" << 'EOF'
#!/bin/bash
echo "🚀 Genesis Prime Quick Test Deploy"
echo "=================================="

if [[ -f "config/requirements.txt" ]]; then
    echo "📦 Installing dependencies..."
    pip install -r config/requirements.txt
fi

if [[ -f "core/agent.py" ]]; then
    echo "✅ Core agent found"
fi

if [[ -f "security/gph_security_production.py" ]]; then
    echo "🛡️ Production security found"
fi

echo "Test deployment complete!"
EOF
    
    chmod +x "$DEST_DIR/quick_deploy.sh"
    
    # Create manifest
    cat > "$DEST_DIR/TEST_MANIFEST.json" << EOF
{
    "test_backup": {
        "backup_id": "$BACKUP_ID",
        "created": "$(date)",
        "source": "$SCRIPT_DIR",
        "destination": "$DEST_DIR"
    },
    "file_counts": {
        "core_files": $core_count,
        "security_files": $security_count,
        "documentation": $doc_count,
        "config_files": $config_count,
        "total_files": $(find "$DEST_DIR" -type f | wc -l)
    }
}
EOF
    
    # Summary
    local total_files=$(find "$DEST_DIR" -type f | wc -l)
    local backup_size=$(du -sh "$DEST_DIR" | cut -f1)
    
    echo
    log_success "Test backup completed!"
    echo "=============================="
    echo "Files backed up: $total_files"
    echo "Core files: $core_count"
    echo "Security files: $security_count"
    echo "Documentation: $doc_count"
    echo "Config files: $config_count"
    echo "Size: $backup_size"
    echo "Location: $DEST_DIR"
    echo
    echo "Test deployment: cd '$DEST_DIR' && ./quick_deploy.sh"
    
    log_info "Ready to run full sudo backup with: sudo ./backup_genesis_prime.sh"
}

main "$@"