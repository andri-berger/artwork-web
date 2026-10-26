#!/usr/bin/env python3
"""Serve artwork-web locally at http://localhost:PORT (Python standard library only).

The site uses root-absolute paths (/=/, /@/, /cdn/, ...), fetch, a Web Worker
and an iframe, so it needs an HTTP server at the site root; opening index.html
as a file does not work. Open it via "localhost", not 127.0.0.1: the page only
accepts iframe messages on that hostname.

Everything is served from this folder. /cd/<path> falls back to /cdn/<path>.

Optional: with OpenCV installed (opencv-python-headless), POST /opencv runs the
F02 photo effects on a PNG and returns the result as PNG; GET /opencv says
whether OpenCV is available. Without it the page simply skips the F02 effects.
If OpenCV isn't importable but ./.venv has it (install.sh creates that venv),
the server restarts itself with the venv's Python.
"""

import argparse
import functools
import http.server
import json
import os
import posixpath
import sys
import urllib.parse
import webbrowser

ROOT = os.path.dirname(os.path.abspath(__file__))
VENV = os.path.join(ROOT, ".venv")
MAX_UPLOAD = 512 * 1024 * 1024

try:
    import cv2
    import numpy as np
except ImportError:
    cv2 = None

# F02 type slider, in slider order (0 = off)
EFFECTS = ("Invert", "Edges", "Stylization", "Detail Enhance", "Pencil Sketch", "Cartoon")


def lerp(value, at0, at100):
    """Map a 0-100 slider value onto at0..at100."""
    return at0 + (at100 - at0) * min(max(value, 0), 100) / 100


def opencv_effect(data, fx, p1=0, p2=0, p3=0, fade=0):
    """Apply effect fx (1-6) to PNG bytes and return PNG bytes.

    Ported from artwork-tui (Backend/scripts.py) and extended with Pencil
    Sketch and Cartoon. Only the opaque bounding box is processed; alpha is
    kept as is. fade blends back to the original (0 = full effect, 100 = none).
    """
    image = cv2.imdecode(np.frombuffer(data, np.uint8), cv2.IMREAD_UNCHANGED)
    if image is None:
        raise ValueError("not an image")
    if image.ndim == 2:
        image = cv2.cvtColor(image, cv2.COLOR_GRAY2BGRA)
    elif image.shape[2] == 3:
        image = cv2.cvtColor(image, cv2.COLOR_BGR2BGRA)
    ys, xs = np.nonzero(image[:, :, 3])
    if ys.size == 0 or not 1 <= fx <= len(EFFECTS):
        return data
    box = (slice(ys.min(), ys.max() + 1), slice(xs.min(), xs.max() + 1))
    # a view: writing it back below changes image, alpha untouched
    rgb = image[:, :, :3][box]
    src = np.ascontiguousarray(rgb)

    if fx == 1:
        out = cv2.bitwise_not(src)
    elif fx == 2:
        # P1/P2 Canny thresholds, P3 line thickness 1-9 px
        out = cv2.Canny(src, lerp(p1, 10, 200), lerp(p2, 20, 400))
        size = round(lerp(p3, 1, 9))
        if size > 1:
            out = cv2.dilate(out, np.ones((size, size), np.uint8))
        out = cv2.cvtColor(out, cv2.COLOR_GRAY2BGR)
    elif fx == 3:
        out = cv2.stylization(src, sigma_s=lerp(p1, 100, 30), sigma_r=lerp(p2, 0.7, 0.2))
    elif fx == 4:
        out = cv2.detailEnhance(src, sigma_s=lerp(p1, 100, 5), sigma_r=lerp(p2, 0.5, 0.1))
    elif fx == 5:
        out, _ = cv2.pencilSketch(
            src, sigma_s=lerp(p1, 60, 5), sigma_r=lerp(p2, 0.07, 0.2), shade_factor=lerp(p3, 0.02, 0.1)
        )
        out = cv2.cvtColor(out, cv2.COLOR_GRAY2BGR)
    else:
        # P1 color smoothing, P2 line size, P3 line threshold (higher = fewer lines)
        color = cv2.edgePreservingFilter(src, flags=cv2.RECURS_FILTER, sigma_s=lerp(p1, 30, 200), sigma_r=0.4)
        gray = cv2.medianBlur(cv2.cvtColor(src, cv2.COLOR_BGR2GRAY), 5)
        block = 2 * round(lerp(p2, 3, 15)) + 1
        lines = cv2.adaptiveThreshold(
            gray, 255, cv2.ADAPTIVE_THRESH_MEAN_C, cv2.THRESH_BINARY, block, lerp(p3, 2, 15)
        )
        out = cv2.bitwise_and(color, color, mask=lines)

    if fade > 0:
        weight = lerp(fade, 0, 1)
        out = cv2.addWeighted(out, 1 - weight, src, weight, 0)
    rgb[...] = out
    ok, png = cv2.imencode(".png", image, [cv2.IMWRITE_PNG_COMPRESSION, 1])
    if not ok:
        raise ValueError("PNG encoding failed")
    return png.tobytes()


class Handler(http.server.SimpleHTTPRequestHandler):
    extensions_map = {
        **http.server.SimpleHTTPRequestHandler.extensions_map,
        ".avif": "image/avif",
        ".woff2": "font/woff2",
        ".json": "application/json",
        ".js": "text/javascript",
        ".mjs": "text/javascript",
        ".svg": "image/svg+xml",
    }

    def translate_path(self, path):
        local = super().translate_path(path)
        clean = posixpath.normpath(urllib.parse.unquote(path.split("?", 1)[0].split("#", 1)[0]))
        if not os.path.exists(local) and clean.startswith("/cd/"):
            alias = super().translate_path("/cdn/" + clean[len("/cd/"):])
            if os.path.exists(alias):
                return alias
        return local

    def end_headers(self):
        # Always revalidate, so local edits show up on reload.
        self.send_header("Cache-Control", "no-cache")
        super().end_headers()

    def log_message(self, fmt, *args):
        if not self.server.quiet:
            super().log_message(fmt, *args)

    def reply(self, code, body, content_type="application/json"):
        self.send_response(code)
        self.send_header("Content-Type", content_type)
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)

    def do_GET(self):
        if urllib.parse.urlsplit(self.path).path != "/opencv":
            return super().do_GET()
        status = {"opencv": cv2.__version__ if cv2 else None, "effects": EFFECTS}
        self.reply(200 if cv2 else 501, json.dumps(status).encode())

    def do_POST(self):
        url = urllib.parse.urlsplit(self.path)
        if url.path != "/opencv":
            return self.send_error(404)
        # Only the page itself may use it, not other sites open in the browser.
        origin = self.headers.get("Origin")
        if origin and urllib.parse.urlsplit(origin).hostname not in ("localhost", "127.0.0.1"):
            return self.send_error(403)
        if cv2 is None:
            return self.send_error(501, "OpenCV not installed")
        try:
            length = int(self.headers.get("Content-Length", 0))
            if not 0 < length <= MAX_UPLOAD:
                return self.send_error(413 if length else 400)
            data = self.rfile.read(length)
            query = urllib.parse.parse_qs(url.query)
            params = {k: float(query.get(k, ["0"])[0] or 0) for k in ("fx", "p1", "p2", "p3", "fade")}
            params["fx"] = int(params["fx"])
        except ValueError:
            return self.send_error(400)
        try:
            png = opencv_effect(data, **params)
        except Exception as error:
            self.log_error("opencv: %s", error)
            return self.send_error(500, str(error))
        self.reply(200, png, "image/png")


def main():
    parser = argparse.ArgumentParser(description="Serve artwork-web at http://localhost:PORT")
    parser.add_argument("-p", "--port", type=int, default=int(os.environ.get("PORT", 8000)))
    parser.add_argument("--open", action="store_true", help="open the page in the default browser")
    parser.add_argument("-q", "--quiet", action="store_true", help="don't log requests")
    args = parser.parse_args()

    venv_python = os.path.join(VENV, "bin", "python3")
    if cv2 is None and os.path.exists(venv_python) and os.path.realpath(sys.prefix) != os.path.realpath(VENV):
        os.execv(venv_python, [venv_python, os.path.abspath(__file__), *sys.argv[1:]])

    handler = functools.partial(Handler, directory=ROOT)
    for port in range(args.port, args.port + 20):
        try:
            server = http.server.ThreadingHTTPServer(("127.0.0.1", port), handler)
            break
        except OSError:
            continue
    else:
        sys.exit(f"error: no free port in {args.port}-{args.port + 19}")
    server.quiet = args.quiet

    url = f"http://localhost:{port}/"
    print(f"artwork-web: serving {ROOT}\nopen {url}  (use localhost, not 127.0.0.1) — Ctrl+C to stop")
    print(f"OpenCV {cv2.__version__}: F02 effects on" if cv2 else "OpenCV not found: F02 effects off (see readme.md)")
    if args.open:
        webbrowser.open(url)
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print()
    finally:
        server.server_close()


if __name__ == "__main__":
    main()
