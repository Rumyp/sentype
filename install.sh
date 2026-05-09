#!/usr/bin/env bash
set -euo pipefail

# Install SenType to system locations.
# Usage: sudo ./install.sh [PREFIX]
# Default PREFIX: /usr/local

PREFIX=${1:-/usr/local}
SRC_DIR="$(cd "$(dirname "$0")" && pwd)"
DEST="$PREFIX/share/sentype"
BIN_DIR="$PREFIX/bin"
BIN="$BIN_DIR/sentype"

if [ "$EUID" -ne 0 ]; then
  echo "This installer requires root privileges. Re-run with sudo." >&2
  exit 1
fi

echo "Installing SenType from $SRC_DIR to $DEST"

mkdir -p "$DEST" "$BIN_DIR"
rsync -a --exclude='.git' --exclude='*.pyc' --exclude='__pycache__' "$SRC_DIR/" "$DEST/"
chmod +x "$DEST/game.py"

cat > "$BIN" <<WRAPPER
#!/usr/bin/env bash
exec python3 "$DEST/game.py" "\$@"
WRAPPER

chmod +x "$BIN"

echo "SenType installed to $DEST"
echo "Command: $BIN"
