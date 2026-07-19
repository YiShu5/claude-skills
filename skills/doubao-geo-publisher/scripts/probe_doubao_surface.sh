#!/usr/bin/env bash
set -euo pipefail

URL="https://www.doubao.com"
OUTPUT_DIR=""
WAIT_MS="4000"
CHANNEL=""
FULL_PAGE="false"

while [[ $# -gt 0 ]]; do
  case "$1" in
    --url)
      URL="$2"
      shift 2
      ;;
    --output-dir)
      OUTPUT_DIR="$2"
      shift 2
      ;;
    --wait-ms)
      WAIT_MS="$2"
      shift 2
      ;;
    --channel)
      CHANNEL="$2"
      shift 2
      ;;
    --full-page)
      FULL_PAGE="true"
      shift
      ;;
    *)
      echo "Unknown argument: $1" >&2
      exit 1
      ;;
  esac
done

if [[ -z "$OUTPUT_DIR" ]]; then
  echo "Missing required argument: --output-dir" >&2
  exit 1
fi

mkdir -p "$OUTPUT_DIR"
STAMP="$(date +%Y%m%d-%H%M%S)"
SHOT_PATH="$OUTPUT_DIR/doubao-surface-$STAMP.png"
NOTE_PATH="$OUTPUT_DIR/doubao-surface-$STAMP.txt"

CMD=(npx playwright screenshot --wait-for-timeout "$WAIT_MS")
if [[ -n "$CHANNEL" ]]; then
  CMD+=(--channel "$CHANNEL")
fi
if [[ "$FULL_PAGE" == "true" ]]; then
  CMD+=(--full-page)
fi
CMD+=("$URL" "$SHOT_PATH")

echo "Running: ${CMD[*]}"
"${CMD[@]}"

{
  echo "timestamp=$STAMP"
  echo "url=$URL"
  echo "screenshot=$SHOT_PATH"
  echo "note=Use the screenshot to determine whether the page is open, blocked, or login-gated."
} > "$NOTE_PATH"

echo "Saved screenshot: $SHOT_PATH"
echo "Saved note: $NOTE_PATH"
