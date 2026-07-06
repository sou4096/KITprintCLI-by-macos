#!/usr/bin/env bash
set -euo pipefail

if [[ $# -ne 2 ]]; then
  echo "Usage: $0 <input.pdf> <output.pdf>" >&2
  exit 1
fi

INPUT="$1"
OUTPUT="$2"

if [[ ! -f "$INPUT" ]]; then
  echo "Error: 入力ファイルが見つかりません: $INPUT" >&2
  exit 1
fi

if ! command -v gs >/dev/null 2>&1; then
  echo "Error: Ghostscript が見つかりません。" >&2
  echo "Install: brew install ghostscript" >&2
  exit 1
fi

gs -q \
  -dSAFER \
  -dBATCH \
  -dNOPAUSE \
  -sDEVICE=pdfwrite \
  -sColorConversionStrategy=Gray \
  -dProcessColorModel=/DeviceGray \
  -dCompatibilityLevel=1.4 \
  -sOutputFile="$OUTPUT" \
  "$INPUT"

echo "Created: $OUTPUT"
