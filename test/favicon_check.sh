#!/usr/bin/env bash
set -euo pipefail

SITE_URL="${SITE_URL:-https://hunterma97.github.io}"
CACHE_BUST="${CACHE_BUST:-20260824-taiji4}"

fail() {
  echo "favicon_check: $*" >&2
  exit 1
}

check_url() {
  local path="$1"
  local min_bytes="${2:-100}"
  local tmp
  tmp="$(mktemp)"
  local code
  code="$(curl -fsSL -o "$tmp" -w '%{http_code}' "${SITE_URL}${path}")"
  [[ "$code" == "200" ]] || fail "${path} returned HTTP ${code}"
  local size
  size="$(wc -c <"$tmp" | tr -d ' ')"
  [[ "$size" -ge "$min_bytes" ]] || fail "${path} too small (${size} bytes)"
  rm -f "$tmp"
  echo "ok ${path} (${size} bytes)"
}

html="$(curl -fsSL "${SITE_URL}/")"
echo "$html" | grep -q 'data:image/svg+xml' || fail "homepage missing inline SVG favicon"
echo "$html" | grep -q "favicon-32.png?v=${CACHE_BUST}" || fail "homepage missing PNG favicon link"

check_url "/assets/img/favicon-32.png?v=${CACHE_BUST}" 200
check_url "/assets/img/favicon.ico?v=${CACHE_BUST}" 500
check_url "/assets/img/taiji-favicon.svg?v=${CACHE_BUST}" 200
check_url "/favicon.ico?v=${CACHE_BUST}" 500

ico_tmp="$(mktemp)"
curl -fsSL "${SITE_URL}/assets/img/favicon.ico?v=${CACHE_BUST}" -o "$ico_tmp"
python3 - "$ico_tmp" <<'PY'
import struct
import sys

data = open(sys.argv[1], "rb").read()
if len(data) < 6:
    raise SystemExit("ICO too small")
reserved, icotype, count = struct.unpack("<HHH", data[:6])
if reserved != 0 or icotype != 1:
    raise SystemExit("invalid ICO header")
if count < 2:
    raise SystemExit(f"expected multi-size ICO, got {count} entries")
print(f"ICO entries: {count}")
PY
rm -f "$ico_tmp"

echo "favicon_check: all checks passed"
