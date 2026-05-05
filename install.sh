#!/usr/bin/env bash
set -euo pipefail

# Install DonkeyType to system locations.
# Usage: sudo ./install.sh [PREFIX]
# Default PREFIX: /usr/local

PREFIX=${1:-/usr/local}
SRC_DIR="$(cd "$(dirname "$0")" && pwd)"
DEST="$PREFIX/lib/donkeytype"
BIN="$PREFIX/bin/donkeytype"

echo "Installing DonkeyType from $SRC_DIR to $DEST"

if [ "$EUID" -ne 0 ]; then
  echo "This installer requires root privileges. Re-run with sudo." >&2
  exit 1
fi

mkdir -p "$DEST"
# Copy files (exclude .git if present)
rsync -a --exclude='.git' --exclude='*.pyc' "$SRC_DIR/" "$DEST/"
chmod +x "$DEST/game.py"

# Create a small wrapper in $BIN that invokes the game with python3
cat > "$BIN" <<'WRAPPER'
#!/usr/bin/env bash
python3 "${PREFIX}/lib/donkeytype/game.py" "$@"
WRAPPER

chmod +x "$BIN"

echo "DonkeyType installed to $DEST"
echo "Command: $BIN"

echo "Done. Run 'donkeytype' to play."
