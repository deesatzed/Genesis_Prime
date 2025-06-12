#!/bin/bash

# Compress the deployment package for easy transfer

PACKAGE_DIR="$1"
if [[ -z "$PACKAGE_DIR" ]]; then
    echo "Usage: $0 <package_directory>"
    exit 1
fi

if [[ ! -d "$PACKAGE_DIR" ]]; then
    echo "❌ Package directory not found: $PACKAGE_DIR"
    exit 1
fi

echo "📦 Compressing Genesis Prime deployment package..."
tar -czf "${PACKAGE_DIR}.tar.gz" "$PACKAGE_DIR"

if [[ $? -eq 0 ]]; then
    echo "✅ Package compressed successfully: ${PACKAGE_DIR}.tar.gz"
    echo "📊 Package size: $(du -h "${PACKAGE_DIR}.tar.gz" | cut -f1)"
    echo ""
    echo "🚀 To deploy on another computer:"
    echo "1. Transfer ${PACKAGE_DIR}.tar.gz to target computer"
    echo "2. Extract: tar -xzf ${PACKAGE_DIR}.tar.gz"
    echo "3. cd ${PACKAGE_DIR}"
    echo "4. ./scripts/install.sh"
    echo "5. Edit backend/.env with API keys"
    echo "6. ./scripts/start.sh"
    echo "7. ./scripts/onboard_agents.sh"
else
    echo "❌ Compression failed"
    exit 1
fi
