#!/bin/bash
set -e

APP_DIR="$HOME/kitprint"
BIN_DIR="$HOME/bin"
CONFIG_DIR="$HOME/.config/kitprint"

echo "KIT Print CLI installer"

if [ ! -f "$APP_DIR/kitprint.py" ]; then
  echo "error: $APP_DIR/kitprint.py が見つかりません。"
  exit 1
fi

if ! command -v python3 >/dev/null 2>&1; then
  echo "error: python3 が見つかりません。"
  exit 1
fi

if ! command -v cupsfilter >/dev/null 2>&1; then
  echo "error: cupsfilter が見つかりません。"
  exit 1
fi

mkdir -p "$BIN_DIR"
mkdir -p "$CONFIG_DIR"

chmod +x "$APP_DIR/kitprint.py"
ln -sf "$APP_DIR/kitprint.py" "$BIN_DIR/kitprint"

if ! grep -q 'export PATH="$HOME/bin:$PATH"' "$HOME/.zprofile" 2>/dev/null; then
  echo 'export PATH="$HOME/bin:$PATH"' >> "$HOME/.zprofile"
fi

echo "installed: $BIN_DIR/kitprint"
echo "次のコマンドで反映してください:"
echo 'source ~/.zprofile'
echo ""
echo "初期設定:"
echo "kitprint --setup"
