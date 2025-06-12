#!/bin/bash

# Genesis Prime Production Backup Script
# Creates comprehensive backups with sudo permissions to multiple locations
# Usage: sudo ./backup_genesis_prime.sh [destination_directory]

set -euo pipefail  # Exit on error, undefined vars, pipe failures

# Script metadata
SCRIPT_NAME="Genesis Prime Production Backup"
SCRIPT_VERSION="1.0.0"
BACKUP_DATE=$(date +"%Y%m%d_%H%M%S")
BACKUP_ID="genesis_prime_backup_${BACKUP_DATE}"

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
PURPLE='\033[0;35m'
CYAN='\033[0;36m'
NC='\033[0m' # No Color

# Logging functions
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

log_header() {
    echo -e "${PURPLE}[GENESIS PRIME]${NC} $1"
}

# Print banner
print_banner() {
    echo -e "${CYAN}"
    cat << 'EOF'
╔══════════════════════════════════════════════════════════════╗
║                    GENESIS PRIME BACKUP                     ║
║              Advanced AI Consciousness Framework            ║
║                     Production Backup                       ║
╚══════════════════════════════════════════════════════════════╝
EOF
    echo -e "${NC}"
    echo "Script: $SCRIPT_NAME v$SCRIPT_VERSION"
    echo "Date: $(date)"
    echo "Backup ID: $BACKUP_ID"
    echo
}

# Check if running as root/sudo
check_permissions() {
    if [[ $EUID -ne 0 ]]; then
        log_error "This script must be run with sudo privileges"
        echo "Usage: sudo $0 [destination_directory]"
        exit 1
    fi
    log_success "Running with appropriate permissions"
}

# Detect current directory and source
detect_source() {
    SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
    SOURCE_DIR="$SCRIPT_DIR"
    
    log_info "Source directory: $SOURCE_DIR"
    
    # Verify this is a Genesis Prime directory
    if [[ ! -f "$SOURCE_DIR/agent.py" ]] || [[ ! -f "$SOURCE_DIR/genesis_prime_hive.py" ]]; then
        log_error "Source directory does not appear to contain Genesis Prime files"
        log_error "Looking for: agent.py, genesis_prime_hive.py"
        exit 1
    fi
    
    log_success "Genesis Prime source directory verified"
}

# Parse destination options
parse_destination() {
    local dest="$1"
    
    case "$dest" in
        --desktop)
            DEST_DIR="$HOME/Desktop/genesis_prime_backups/$BACKUP_ID"
            ;;
        --documents)
            DEST_DIR="$HOME/Documents/genesis_prime_backups/$BACKUP_ID"
            ;;
        --external)
            # Look for external drives
            EXTERNAL_DRIVES=($(ls /Volumes/ 2>/dev/null | grep -v "Macintosh HD" || true))
            if [[ ${#EXTERNAL_DRIVES[@]} -eq 0 ]]; then
                log_error "No external drives found in /Volumes/"
                exit 1
            fi
            
            echo "Available external drives:"
            for i in "${!EXTERNAL_DRIVES[@]}"; do
                echo "  $((i+1)). ${EXTERNAL_DRIVES[$i]}"
            done
            
            read -p "Select drive number: " drive_num
            if [[ $drive_num -ge 1 ]] && [[ $drive_num -le ${#EXTERNAL_DRIVES[@]} ]]; then
                selected_drive="${EXTERNAL_DRIVES[$((drive_num-1))]}"
                DEST_DIR="/Volumes/$selected_drive/genesis_prime_backups/$BACKUP_ID"
            else
                log_error "Invalid drive selection"
                exit 1
            fi
            ;;
        --cloud-ready)
            DEST_DIR="$HOME/Desktop/genesis_prime_cloud_ready/$BACKUP_ID"
            CLOUD_READY=true
            ;;
        --multiple)
            MULTIPLE_DESTINATIONS=true
            ;;
        *)
            if [[ -z "$dest" ]]; then
                DEST_DIR="$HOME/Desktop/genesis_prime_backups/$BACKUP_ID"
            else
                DEST_DIR="$dest/$BACKUP_ID"
            fi
            ;;
    esac
}

# Create backup destination
create_destination() {
    log_info "Creating backup destination: $DEST_DIR"
    
    # Create directory structure
    mkdir -p "$DEST_DIR"/{core,security,frontend,database,cloud_tools,tests,documentation,config,deployment,monitoring}
    
    # Set proper permissions
    chmod 755 "$DEST_DIR"
    
    log_success "Backup destination created"
}

# Backup core application files
backup_core_files() {
    log_header "Backing up core application files..."
    
    local core_files=(
        "agent.py"
        "genesis_prime_hive.py"
        "emergence_engine.py"
        "iit_enhanced_agents.py"
        "neural_plasticity.py"
        "conscious_information_cascades.py"
        "mycorrhizal_networks.py"
        "adaptive_immune_memory.py"
        "personality_presets.py"
        "self_organized_criticality.py"
        "quorum_sensing.py"
        "agent_factory.py"
        "cli.py"
        "genesis_cli.py"
        "genesis_prime_cli.py"
        "main.py"
        "__init__.py"
    )
    
    local backed_up=0
    for file in "${core_files[@]}"; do
        if [[ -f "$SOURCE_DIR/$file" ]]; then
            cp "$SOURCE_DIR/$file" "$DEST_DIR/core/"
            ((backed_up++))
        else
            log_warning "Core file not found: $file"
        fi
    done
    
    log_success "Backed up $backed_up core files"
}

# Backup security framework
backup_security_files() {
    log_header "Backing up security framework..."
    
    local security_files=(
        "gph_security_framework.py"
        "gph_security_production.py"
        "blockchain_security_enhancement.py"
    )
    
    local backed_up=0
    for file in "${security_files[@]}"; do
        if [[ -f "$SOURCE_DIR/$file" ]]; then
            cp "$SOURCE_DIR/$file" "$DEST_DIR/security/"
            ((backed_up++))
        else
            log_warning "Security file not found: $file"
        fi
    done
    
    log_success "Backed up $backed_up security files"
}

# Backup frontend application
backup_frontend() {
    log_header "Backing up frontend application..."
    
    if [[ -d "$SOURCE_DIR/gp_b_core" ]]; then
        cp -r "$SOURCE_DIR/gp_b_core" "$DEST_DIR/frontend/"
        
        # Count files in frontend
        local frontend_count=$(find "$DEST_DIR/frontend" -type f | wc -l)
        log_success "Backed up frontend application ($frontend_count files)"
    else
        log_warning "Frontend directory not found: gp_b_core"
    fi
}

# Backup database files
backup_database() {
    log_header "Backing up database files..."
    
    local db_files=(
        "setup_database.py"
    )
    
    # Copy database setup files
    local backed_up=0
    for file in "${db_files[@]}"; do
        if [[ -f "$SOURCE_DIR/$file" ]]; then
            cp "$SOURCE_DIR/$file" "$DEST_DIR/database/"
            ((backed_up++))
        fi
    done
    
    # Copy database directory if it exists
    if [[ -d "$SOURCE_DIR/database" ]]; then
        cp -r "$SOURCE_DIR/database"/* "$DEST_DIR/database/" 2>/dev/null || true
        ((backed_up++))
    fi
    
    # Copy SQL directory if it exists
    if [[ -d "$SOURCE_DIR/sql" ]]; then
        cp -r "$SOURCE_DIR/sql" "$DEST_DIR/database/" 2>/dev/null || true
        ((backed_up++))
    fi
    
    log_success "Backed up database files ($backed_up components)"
}

# Backup cloud tools
backup_cloud_tools() {
    log_header "Backing up cloud deployment tools..."
    
    local cloud_files=(
        "cloud_deployment_budget_planner.py"
        "dynamic_model_selector.py"
    )
    
    local backed_up=0
    for file in "${cloud_files[@]}"; do
        if [[ -f "$SOURCE_DIR/$file" ]]; then
            cp "$SOURCE_DIR/$file" "$DEST_DIR/cloud_tools/"
            ((backed_up++))
        else
            log_warning "Cloud tool not found: $file"
        fi
    done
    
    log_success "Backed up $backed_up cloud tools"
}

# Backup test files
backup_tests() {
    log_header "Backing up test files..."
    
    local test_files=(
        "test_all_systems.py"
        "test_openrouter_integration.py"
        "test_system.py"
        "validate_systems.py"
    )
    
    local backed_up=0
    for file in "${test_files[@]}"; do
        if [[ -f "$SOURCE_DIR/$file" ]]; then
            cp "$SOURCE_DIR/$file" "$DEST_DIR/tests/"
            ((backed_up++))
        else
            log_warning "Test file not found: $file"
        fi
    done
    
    log_success "Backed up $backed_up test files"
}

# Backup documentation
backup_documentation() {
    log_header "Backing up documentation..."
    
    local doc_count=0
    for file in "$SOURCE_DIR"/*.md; do
        if [[ -f "$file" ]]; then
            cp "$file" "$DEST_DIR/documentation/"
            ((doc_count++))
        fi
    done
    
    log_success "Backed up $doc_count documentation files"
}

# Backup configuration files
backup_config() {
    log_header "Backing up configuration files..."
    
    local config_files=(
        "requirements.txt"
        "Dockerfile"
        "docker-compose.yml"
        ".env.example"
        "pyproject.toml"
        "setup.py"
    )
    
    local backed_up=0
    for file in "${config_files[@]}"; do
        if [[ -f "$SOURCE_DIR/$file" ]]; then
            cp "$SOURCE_DIR/$file" "$DEST_DIR/config/"
            ((backed_up++))
        fi
    done
    
    # Copy prompts directory
    if [[ -d "$SOURCE_DIR/prompts" ]]; then
        cp -r "$SOURCE_DIR/prompts" "$DEST_DIR/config/"
        ((backed_up++))
    fi
    
    # Copy jobs directory
    if [[ -d "$SOURCE_DIR/jobs" ]]; then
        cp -r "$SOURCE_DIR/jobs" "$DEST_DIR/config/"
        ((backed_up++))
    fi
    
    log_success "Backed up configuration files ($backed_up components)"
}

# Create deployment package
create_deployment_package() {
    log_header "Creating deployment package..."
    
    # Create deployment README
    cat > "$DEST_DIR/DEPLOY_README.md" << 'EOF'
# Genesis Prime Deployment Package

This backup contains a complete Genesis Prime production deployment.

## Quick Start

1. **Install Dependencies:**
   ```bash
   pip install -r config/requirements.txt
   ```

2. **Setup Database:**
   ```bash
   python database/setup_database.py
   ```

3. **Configure Environment:**
   ```bash
   cp config/.env.example .env
   # Edit .env with your settings
   ```

4. **Run Tests:**
   ```bash
   python tests/test_all_systems.py
   ```

5. **Start Application:**
   ```bash
   python core/genesis_prime_hive.py
   ```

## Docker Deployment

```bash
docker-compose -f config/docker-compose.yml up -d
```

## Security

- Use `security/gph_security_production.py` for production
- Use `security/gph_security_framework.py` for development

## Cloud Deployment

```bash
python cloud_tools/cloud_deployment_budget_planner.py
```

For detailed instructions, see documentation/README.md
EOF

    # Create deployment script
    cat > "$DEST_DIR/deploy.sh" << 'EOF'
#!/bin/bash
# Genesis Prime Quick Deploy Script

set -e

echo "🚀 Genesis Prime Quick Deploy"
echo "=============================="

# Check Python
if ! command -v python3 &> /dev/null; then
    echo "❌ Python 3 is required"
    exit 1
fi

# Install dependencies
echo "📦 Installing dependencies..."
pip install -r config/requirements.txt

# Setup database
echo "🗄️ Setting up database..."
python database/setup_database.py

# Run tests
echo "🧪 Running tests..."
python tests/test_all_systems.py

echo "✅ Genesis Prime deployed successfully!"
echo "Start with: python core/genesis_prime_hive.py"
EOF

    chmod +x "$DEST_DIR/deploy.sh"
    
    log_success "Created deployment package"
}

# Generate backup manifest
generate_manifest() {
    log_header "Generating backup manifest..."
    
    local manifest_file="$DEST_DIR/BACKUP_MANIFEST.json"
    
    cat > "$manifest_file" << EOF
{
    "backup_info": {
        "backup_id": "$BACKUP_ID",
        "created_date": "$(date -u +"%Y-%m-%dT%H:%M:%SZ")",
        "script_version": "$SCRIPT_VERSION",
        "source_directory": "$SOURCE_DIR",
        "destination_directory": "$DEST_DIR",
        "hostname": "$(hostname)",
        "user": "$(whoami)"
    },
    "file_counts": {
        "core_files": $(find "$DEST_DIR/core" -type f 2>/dev/null | wc -l),
        "security_files": $(find "$DEST_DIR/security" -type f 2>/dev/null | wc -l),
        "frontend_files": $(find "$DEST_DIR/frontend" -type f 2>/dev/null | wc -l),
        "database_files": $(find "$DEST_DIR/database" -type f 2>/dev/null | wc -l),
        "cloud_tools": $(find "$DEST_DIR/cloud_tools" -type f 2>/dev/null | wc -l),
        "test_files": $(find "$DEST_DIR/tests" -type f 2>/dev/null | wc -l),
        "documentation": $(find "$DEST_DIR/documentation" -type f 2>/dev/null | wc -l),
        "config_files": $(find "$DEST_DIR/config" -type f 2>/dev/null | wc -l),
        "total_files": $(find "$DEST_DIR" -type f 2>/dev/null | wc -l)
    },
    "backup_size": "$(du -sh "$DEST_DIR" 2>/dev/null | cut -f1)",
    "verification": {
        "core_agent_present": $([ -f "$DEST_DIR/core/agent.py" ] && echo "true" || echo "false"),
        "hive_system_present": $([ -f "$DEST_DIR/core/genesis_prime_hive.py" ] && echo "true" || echo "false"),
        "security_framework_present": $([ -f "$DEST_DIR/security/gph_security_production.py" ] && echo "true" || echo "false"),
        "deployment_ready": $([ -f "$DEST_DIR/deploy.sh" ] && echo "true" || echo "false")
    }
}
EOF

    log_success "Generated backup manifest"
}

# Create multiple backups
create_multiple_backups() {
    log_header "Creating multiple backup locations..."
    
    local destinations=(
        "$HOME/Desktop/genesis_prime_backups/$BACKUP_ID"
        "$HOME/Documents/genesis_prime_backups/$BACKUP_ID"
    )
    
    # Add external drive if available
    local external_drives=($(ls /Volumes/ 2>/dev/null | grep -v "Macintosh HD" || true))
    if [[ ${#external_drives[@]} -gt 0 ]]; then
        destinations+=("/Volumes/${external_drives[0]}/genesis_prime_backups/$BACKUP_ID")
    fi
    
    for dest in "${destinations[@]}"; do
        log_info "Creating backup at: $dest"
        DEST_DIR="$dest"
        
        create_destination
        backup_core_files
        backup_security_files
        backup_frontend
        backup_database
        backup_cloud_tools
        backup_tests
        backup_documentation
        backup_config
        create_deployment_package
        generate_manifest
        
        log_success "Backup completed: $dest"
    done
}

# Verify backup integrity
verify_backup() {
    log_header "Verifying backup integrity..."
    
    local errors=0
    
    # Check critical files
    local critical_files=(
        "core/agent.py"
        "core/genesis_prime_hive.py"
        "security/gph_security_production.py"
        "config/requirements.txt"
        "deploy.sh"
        "BACKUP_MANIFEST.json"
    )
    
    for file in "${critical_files[@]}"; do
        if [[ ! -f "$DEST_DIR/$file" ]]; then
            log_error "Critical file missing: $file"
            ((errors++))
        fi
    done
    
    # Check directory structure
    local required_dirs=(
        "core" "security" "frontend" "database" 
        "cloud_tools" "tests" "documentation" "config"
    )
    
    for dir in "${required_dirs[@]}"; do
        if [[ ! -d "$DEST_DIR/$dir" ]]; then
            log_error "Required directory missing: $dir"
            ((errors++))
        fi
    done
    
    if [[ $errors -eq 0 ]]; then
        log_success "Backup verification passed"
    else
        log_error "Backup verification failed with $errors errors"
        return 1
    fi
}

# Print backup summary
print_summary() {
    local total_files=$(find "$DEST_DIR" -type f 2>/dev/null | wc -l)
    local backup_size=$(du -sh "$DEST_DIR" 2>/dev/null | cut -f1)
    
    echo
    log_header "Backup Summary"
    echo "=============================================="
    echo "Backup ID: $BACKUP_ID"
    echo "Destination: $DEST_DIR"
    echo "Total Files: $total_files"
    echo "Backup Size: $backup_size"
    echo "Created: $(date)"
    echo
    echo "🚀 Ready for deployment!"
    echo "Run: cd '$DEST_DIR' && ./deploy.sh"
    echo
}

# Cleanup on error
cleanup_on_error() {
    if [[ -n "${DEST_DIR:-}" ]] && [[ -d "$DEST_DIR" ]]; then
        log_warning "Cleaning up incomplete backup: $DEST_DIR"
        rm -rf "$DEST_DIR"
    fi
}

# Main execution
main() {
    # Set error trap
    trap cleanup_on_error ERR
    
    print_banner
    check_permissions
    detect_source
    
    # Parse arguments
    local destination="${1:-}"
    
    if [[ "$destination" == "--help" ]] || [[ "$destination" == "-h" ]]; then
        echo "Usage: sudo $0 [options|destination]"
        echo
        echo "Options:"
        echo "  --desktop     Backup to Desktop"
        echo "  --documents   Backup to Documents"
        echo "  --external    Backup to external drive"
        echo "  --cloud-ready Create cloud deployment package"
        echo "  --multiple    Create backups in multiple locations"
        echo "  --help        Show this help"
        echo
        echo "Examples:"
        echo "  sudo $0                           # Default backup to Desktop"
        echo "  sudo $0 --external               # Backup to external drive"
        echo "  sudo $0 --multiple               # Multiple backup locations"
        echo "  sudo $0 /path/to/backup          # Custom destination"
        exit 0
    fi
    
    # Handle multiple destinations
    if [[ "$destination" == "--multiple" ]]; then
        create_multiple_backups
        return 0
    fi
    
    # Parse single destination
    parse_destination "$destination"
    
    # Create backup
    log_info "Starting Genesis Prime backup..."
    log_info "Destination: $DEST_DIR"
    
    create_destination
    backup_core_files
    backup_security_files
    backup_frontend
    backup_database
    backup_cloud_tools
    backup_tests
    backup_documentation
    backup_config
    create_deployment_package
    generate_manifest
    verify_backup
    print_summary
    
    log_success "Genesis Prime backup completed successfully!"
}

# Run main function with all arguments
main "$@"