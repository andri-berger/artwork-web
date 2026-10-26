#!/usr/bin/env sh
# artwork-web installer: downloads the repo (~1.4 GB), optionally OpenCV, and adds an `artwork-web` launcher
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

# Optional: OpenCV for the F02 effects, in a venv next to readme.py (which uses it
# by itself). Skip with ARTWORK_WEB_OPENCV=0; without it only F02 stays off.
if [ "${ARTWORK_WEB_OPENCV:-1}" != 0 ]; then
    say "installing OpenCV for the F02 effects (optional, about 230 MB on disk)..."
    VENV="$DEST/.venv"
    if python3 -m venv "$VENV" >/dev/null 2>&1 \
        && "$VENV/bin/python3" -m pip install -q --disable-pip-version-check opencv-python-headless; then
        say "OpenCV installed"
    elif has uv && uv venv -q --allow-existing "$VENV" \
        && uv pip install -q --python "$VENV/bin/python3" opencv-python-headless; then
        say "OpenCV installed (via uv)"
    else
        rm -rf "$VENV"
        say "note: OpenCV not installed (needs the python3 venv module, e.g. apt install python3-venv)."
        say "      Everything else works; rerun the installer to add it later."
    fi
fi

cat > "$BIN/artwork-web" <<EOF
#!/usr/bin/env sh
exec python3 "$DEST/readme.py" "\$@"
EOF
chmod +x "$BIN/artwork-web"

say "installed to $DEST"
say "if command not found, add to your shell config: export PATH=\"\$HOME/.local/bin:\$PATH\""
say "done — run: artwork-web --open   (then use http://localhost:8000, not 127.0.0.1)"
