#!/usr/bin/env bash
# self-improving-agent error detector
# Read-only script. Scans input for common error patterns and outputs reminders.
# Does not write to any file.

set -euo pipefail

# Error keywords to detect
ERROR_PATTERNS=(
  "error:"
  "Error:"
  "ERROR"
  "FAILED"
  "failed"
  "fatal:"
  "Fatal:"
  "FATAL"
  "command not found"
  "No such file or directory"
  "Permission denied"
  "Connection refused"
  "timeout"
  "Traceback"
  "panic:"
  "segfault"
  "ENOENT"
  "EACCES"
  "ECONNREFUSED"
  "exit code 1"
  "exit status 1"
  "ModuleNotFoundError"
  "ImportError"
  "SyntaxError"
  "TypeError"
  "ValueError"
)

INPUT="${1:-}"

if [ -z "$INPUT" ]; then
  echo "Usage: error-detector.sh <text-or-file>"
  echo "Scans for common error patterns and suggests logging."
  exit 0
fi

# If input is a file, read it; otherwise treat as string
if [ -f "$INPUT" ]; then
  CONTENT=$(cat "$INPUT")
else
  CONTENT="$INPUT"
fi

FOUND=0
for pattern in "${ERROR_PATTERNS[@]}"; do
  if echo "$CONTENT" | grep -q "$pattern" 2>/dev/null; then
    if [ "$FOUND" -eq 0 ]; then
      echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
      echo "  ⚠ Error pattern(s) detected"
      echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
      echo ""
    fi
    echo "  Found: \"$pattern\""
    FOUND=$((FOUND + 1))
  fi
done

if [ "$FOUND" -gt 0 ]; then
  cat <<'MSG'

Suggested action:
  → Record to .learnings/ERRORS.md with:
    - Command/tool that failed
    - Error message
    - Root cause (if known)
    - Resolution (if found)

⚠ Do NOT auto-promote to SOUL.md / MEMORY.md / AGENTS.md / TOOLS.md
  Errors stay in the cache layer unless manually promoted.
MSG
else
  echo "No error patterns detected."
fi
