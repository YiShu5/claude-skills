#!/usr/bin/env bash
# self-improving-agent activator
# Read-only reminder script. Does not modify any files.

set -euo pipefail

LEARNINGS_DIR="$(dirname "$0")/../.learnings"

cat <<'MSG'
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
  self-improving-agent · post-task check
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Task completed. Before moving on, consider:

  1. Was there a durable learning worth recording?
     → Log to .learnings/LEARNINGS.md

  2. Did any error occur that might recur?
     → Log to .learnings/ERRORS.md

  3. Was a capability gap exposed?
     → Log to .learnings/FEATURE_REQUESTS.md

⚠ IMPORTANT:
  - Default target is .learnings/ (cache layer)
  - Do NOT auto-promote to SOUL.md / MEMORY.md / AGENTS.md / TOOLS.md
  - Promotion requires: repeated + verified + user-approved

If nothing worth logging → skip. Silence > noise.
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
MSG

# Show current cache stats (read-only)
if [ -d "$LEARNINGS_DIR" ]; then
  echo ""
  echo "Cache stats:"
  for f in LEARNINGS.md ERRORS.md FEATURE_REQUESTS.md; do
    if [ -f "$LEARNINGS_DIR/$f" ]; then
      count=$(grep -c '^## \[' "$LEARNINGS_DIR/$f" 2>/dev/null || echo "0")
      printf "  %-24s %s entries\n" "$f" "$count"
    fi
  done
  echo ""
fi
