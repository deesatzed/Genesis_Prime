#!/usr/bin/env bash
# ------------------------------------------------------------
# reorganize_gp_structure.sh – Restructure Genesis Prime repo
# ------------------------------------------------------------
# Moves backend + frontend into apps/, groups docs, updates
# env + compose paths. Execute **manually** from repo root.
# ------------------------------------------------------------
set -euo pipefail

ROOT="$( cd "$( dirname "${BASH_SOURCE[0]}" )/.." && pwd )"
cd "$ROOT"

BACKEND_SRC="Gen_Prime_V3c/apps/option1_mono_agent"
FRONTEND_SRC="apps/gp_b_core"
BACKEND_DST="apps/backend"
FRONTEND_DST="apps/frontend"

confirm() {
  read -rp "$1 [y/N]: " yn
  case $yn in
    [Yy]*) ;;
    *) echo "Abort."; exit 1;;
  esac
}

printf "\nPlanned actions:\n"
printf " 1. Move $BACKEND_SRC → $BACKEND_DST\n"
printf " 2. Move $FRONTEND_SRC → $FRONTEND_DST\n"
printf " 3. Create docs/ and group markdown files (non-code)\n"
printf " 4. Patch .env* and docker-compose.yml PYTHONPATH + volumes\n"
confirm "Proceed with restructure?"

# 1. Move backend
if [[ -d "$BACKEND_SRC" ]]; then
  mkdir -p "$(dirname "$BACKEND_DST")"
  mv "$BACKEND_SRC" "$BACKEND_DST"
  echo "✔ Backend moved"
else
  echo "⚠ Backend source not found ($BACKEND_SRC) – skipping"
fi

# 2. Move frontend
if [[ -d "$FRONTEND_SRC" ]]; then
  mkdir -p "$(dirname "$FRONTEND_DST")"
  mv "$FRONTEND_SRC" "$FRONTEND_DST"
  echo "✔ Frontend moved"
else
  echo "⚠ Frontend source not found ($FRONTEND_SRC) – skipping"
fi

# 3. Group markdown docs (keep README & QUICK_START at root)
mkdir -p docs/{architecture,plans,status}
shopt -s nullglob
for md in *.md; do
  case "$md" in
    README.md|QUICK_START_GUIDE.md) continue;;
  esac
  # heuristic: classify by filename keywords
  dest="docs/status"
  [[ $md == *Plan* || $md == *STRATEGY* ]] && dest="docs/plans"
  [[ $md == *architecture* || $md == *ARCHITECTURE* ]] && dest="docs/architecture"
  mv "$md" "$dest/" 2>/dev/null || true
  echo "→ moved $md to $dest/"
done
shopt -u nullglob

# 4. Patch env files
for envf in .env .env.docker; do
  if [[ -f $envf ]]; then
    sed -i.bak 's#Gen_Prime_V3c/apps/option1_mono_agent#apps/backend#g' "$envf"
    sed -i.bak 's#apps/gp_b_core#apps/frontend#g' "$envf"
    echo "Patched $envf"
  fi
done

# 4b. Patch docker-compose
if [[ -f docker-compose.yml ]]; then
  sed -i.bak 's#Gen_Prime_V3c/apps/option1_mono_agent#apps/backend#g' docker-compose.yml
  sed -i.bak 's#apps/gp_b_core#apps/frontend#g' docker-compose.yml
  echo "Patched docker-compose.yml"
fi

echo "\nReorganisation complete. Review git diff before committing."
