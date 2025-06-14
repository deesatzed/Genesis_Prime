#!/usr/bin/env bash
# -----------------------------------------------------------------
# clone_reorganize_v4.sh  –  Produce Genesis_Prime_V4 directory
# -----------------------------------------------------------------
# 1. Copies current repo to ../Genesis_Prime_V4 (or custom path)
# 2. Executes reorganize_gp_structure.sh inside the clone
#
# USAGE
#   chmod +x scripts/clone_reorganize_v4.sh
#   ./scripts/clone_reorganize_v4.sh [optional-absolute-dest]
# -----------------------------------------------------------------
set -euo pipefail

SRC_ROOT="$( cd "$( dirname "${BASH_SOURCE[0]}" )/.." && pwd )"
DEFAULT_DEST="/Users/o2satz/sentient-ai-suite/Genesis_Prime_V4"
DEST_ROOT="${1:-$DEFAULT_DEST}"

# Ensure DEST_ROOT is absolute
DEST_ROOT="$(python -c 'import os,sys; print(os.path.abspath(sys.argv[1]))' "$DEST_ROOT")"

if [[ -e "$DEST_ROOT" ]]; then
  echo "Destination $DEST_ROOT already exists – abort to prevent overwrite." >&2
  exit 1
fi

echo "Cloning repository to $DEST_ROOT …"
# Use rsync to preserve permissions; exclude git history to save space.
rsync -a --exclude='.git' --exclude='*.pyc' "$SRC_ROOT/" "$DEST_ROOT/"

echo "Clone complete. Now running reorganization inside new folder."
cd "$DEST_ROOT"

# Ensure reorganize script is executable
chmod +x scripts/reorganize_gp_structure.sh

# Ask user confirmation inside reorganize script (inherits prompts).
"$DEST_ROOT/scripts/reorganize_gp_structure.sh"

echo "\nGenesis_Prime_V4 prepared at $DEST_ROOT. Review and run tests before using."
