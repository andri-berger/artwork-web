#!/usr/bin/env sh
# artwork-web installer: downloads the repo (~1.4 GB) and adds an `artwork-web` launcher
# usage: curl -fsSL https://raw.githubusercontent.com/andri-berger/artwork-web/main/install.sh | sh
set -eu

URL="https://github.com/andri-berger/artwork-web/archive/refs/heads/main.tar.gz"
DATA="${XDG_DATA_HOME:-$HOME/.local/share}"
DEST="$DATA/artwork-web"
BIN="$HOME/.local/bin"

say() { printf '%s\n' "$*"; }
die() { printf 'error: %s\n' "$*" >&2; exit 1; }
has() { command -v "$1" >/dev/null 2>&1; }

has curl || die "curl not found"
has tar || die "tar not found"
has python3 || die "python3 not found — install it with your package manager (macOS: xcode-select --install)"
python3 -c 'import sys; sys.exit(sys.version_info < (3, 7))' || die "python3 3.7+ required"

mkdir -p "$DATA" "$BIN"
TMP="$(mktemp -d "$DATA/artwork-web.XXXXXX")"
trap 'rm -rf "$TMP"' EXIT

say "downloading artwork-web (~1.4 GB, this takes a while)..."
curl -fL --progress-bar "$URL" | tar -xz -C "$TMP" --strip-components=1 || die "download failed"
[ -f "$TMP/readme.py" ] || die "download incomplete: readme.py missing"

rm -rf "$DEST"
mv "$TMP" "$DEST"
trap - EXIT

cat > "$BIN/artwork-web" <<EOF
#!/usr/bin/env sh
exec python3 "$DEST/readme.py" "\$@"
EOF
chmod +x "$BIN/artwork-web"

say "installed to $DEST"
say "if command not found, add to your shell config: export PATH=\"\$HOME/.local/bin:\$PATH\""
say "done — run: artwork-web --open   (then use http://localhost:8000, not 127.0.0.1)"
