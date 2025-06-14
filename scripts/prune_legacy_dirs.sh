#!/usr/bin/env bash
# ------------------------------------------------------------
# prune_legacy_dirs.sh  –  Removes legacy / duplicate folders
# ------------------------------------------------------------
# PURPOSE
#   Clean clutter from a cloned Genesis Prime workspace by
#   deleting directories known to be obsolete or superseded.
#   Run manually *after* verifying nothing inside is required.
#
#   The script is intentionally simple: edit LEGACY_DIRS below
#   if more folders must be purged in the future.
#
# USAGE
#   chmod +x scripts/prune_legacy_dirs.sh
#   ./scripts/prune_legacy_dirs.sh
# ------------------------------------------------------------
set -euo pipefail

ROOT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )/.." && pwd )"

# List folders deemed safe to remove (relative to repo root)
LEGACY_DIRS=(
  "Gen_Prime_V2-main"            # pre-V3 lineage
  "CLEANBUILD"                  # old build artifacts
  "Prior_QA_Parts"              # archived question-answer docs
  "option1_mono_agent_PriorVersion" # superseded backend variant
  "genesis_prime_production_backup" # prod backup copy (kept elsewhere)
)

printf "\nGenesis Prime legacy cleanup\n================================\n"
printf "The following directories will be **deleted**:\n\n"
for d in "${LEGACY_DIRS[@]}"; do
  printf "  • %s\n" "$d"
done

read -rp $'\nType "YES" to continue: ' CONFIRM
if [[ "$CONFIRM" != "YES" ]]; then
  echo "Aborted by user. No changes made."; exit 0
fi

for DIR in "${LEGACY_DIRS[@]}"; do
  TARGET="$ROOT_DIR/$DIR"
  if [[ -d "$TARGET" ]]; then
    echo "Removing $DIR …" && rm -rf "$TARGET"
  else
    echo "Skip $DIR (not found)"
  fi
done

echo "Cleanup complete."
