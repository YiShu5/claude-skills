#!/usr/bin/env bash
set -euo pipefail

URL="https://www.doubao.com"
PROFILE_DIR="/tmp/doubao-geo-profile"
BROWSER="chrome"

while [[ $# -gt 0 ]]; do
  case "$1" in
    --url)
      URL="$2"
      shift 2
      ;;
    --profile-dir)
      PROFILE_DIR="$2"
      shift 2
      ;;
    --browser)
      BROWSER="$2"
      shift 2
      ;;
    *)
      echo "Unknown argument: $1" >&2
      exit 1
      ;;
  esac
done

if ! command -v playwright-cli >/dev/null 2>&1; then
  echo "playwright-cli is not installed or not on PATH." >&2
  exit 1
fi

mkdir -p "$PROFILE_DIR"

cat <<EOF
Opening Doubao in headed mode.

Manual steps:
1. Complete login or account checks in the browser.
2. Do not automate CAPTCHA or security prompts.
3. After login, keep this profile directory for future research:
   $PROFILE_DIR

EOF

exec playwright-cli open "$URL" --headed --persistent --profile "$PROFILE_DIR" --browser "$BROWSER"
