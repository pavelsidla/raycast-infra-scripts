#!/bin/bash

# Required parameters:
# @raycast.schemaVersion 1
# @raycast.title Zone Lookup
# @raycast.mode fullOutput

# Optional parameters:
# @raycast.icon 🌐
# @raycast.packageName Infra
# @raycast.description Look up DNS zone, AWS profile and region for an environment. Supports partial names (e.g. "eu1" returns all eu1 zones).
# @raycast.argument1 { "type": "text", "placeholder": "zone-name or partial", "percentEncoded": false }

# ──────────────────────────────────────────────────────────────────────────────
# Locate python3 — tries Homebrew (Apple Silicon), Homebrew (Intel), then PATH
# ──────────────────────────────────────────────────────────────────────────────
if   [[ -x "/opt/homebrew/bin/python3" ]];  then PYTHON="/opt/homebrew/bin/python3"
elif [[ -x "/usr/local/bin/python3"   ]];   then PYTHON="/usr/local/bin/python3"
elif command -v python3 &>/dev/null;         then PYTHON="python3"
else
  echo "Error: python3 not found."
  echo "Install it via Homebrew:  brew install python"
  exit 1
fi

# ──────────────────────────────────────────────────────────────────────────────
# Locate zone-lookup.py relative to this script
# ──────────────────────────────────────────────────────────────────────────────
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
ZONE_LOOKUP_PY="${SCRIPT_DIR}/../zone-lookup.py"

if [[ ! -f "$ZONE_LOOKUP_PY" ]]; then
  echo "Error: zone-lookup.py not found at: $ZONE_LOOKUP_PY"
  echo "Make sure you cloned the full repository and haven't moved individual files."
  exit 1
fi

exec "$PYTHON" "$ZONE_LOOKUP_PY" "$1"
