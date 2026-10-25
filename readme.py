#!/usr/bin/env python3
"""Serve artwork-web locally at http://localhost:PORT (Python standard library only).

The site uses root-absolute paths (/=/, /@/, /cdn/, ...), fetch, a Web Worker
and an iframe, so it needs an HTTP server at the site root; opening index.html
as a file does not work. Open it via "localhost", not 127.0.0.1: the page only
accepts iframe messages on that hostname.

Everything is served from this folder. /cd/<path> falls back to /cdn/<path>.
"""

import argparse
import functools
import http.server
import os
import posixpath
import sys
import urllib.parse
import webbrowser

ROOT = os.path.dirname(os.path.abspath(__file__))


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


def main():
    parser = argparse.ArgumentParser(description="Serve artwork-web at http://localhost:PORT")
    parser.add_argument("-p", "--port", type=int, default=int(os.environ.get("PORT", 8000)))
    parser.add_argument("--open", action="store_true", help="open the page in the default browser")
    parser.add_argument("-q", "--quiet", action="store_true", help="don't log requests")
    args = parser.parse_args()

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
